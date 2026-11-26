"""Prueft die Katalog-Updates von Astro-SNR unter AstroSNR/catalog-db/schema-<S>/ (laeuft in GitHub Actions).

Je Schemaversion: genau ein Paket catalog-<N>.db.gz, das zum Manifest passt (Dateiname, Groesse gepackt und
entpackt, SHA-256), eine gueltige ECDSA-Signatur (P-256, SHA-256) mit dem oeffentlichen Schluessel der App,
Schemaversion (PRAGMA user_version) und data_version in der Datenbank wie im Manifest, und dataVersion nicht
kleiner als im vorherigen Commit (Geraete uebernehmen nur hoehere Staende).

Erzeugt werden Paket und Manifest mit tools/publish_catalog.py im Repository Astro_SNR; die App prueft dasselbe
(CatalogUpdater, CatalogPackage). Der Schluessel steht hier fest, damit ein Paket mit fremdem Schluessel auffaellt;
wird er in der App gewechselt, auch hier aendern.

Aufruf: python .github/scripts/verify_astro_snr_catalog.py [--before <commit>]
"""
import argparse
import base64
import glob
import gzip
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DB = os.path.join(ROOT, 'AstroSNR', 'catalog-db')
# CatalogUpdater.PUBLIC_KEY in Astro_SNR (X.509 SubjectPublicKeyInfo, DER, Base64)
PUBLIC_KEY = ('MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEDw8POsOWTMuw5yqR8K9QCITpvWDQmRyJ/NBB/J0GR1XIr+4FFrSOpCE7jh/xGZKcSzOGu6rEQD3OmlYrvwZKlQ==')
FIELDS = {'schema': int, 'dataVersion': int, 'file': str, 'size': int, 'dbSize': int, 'sha256': str, 'signature': str}
FILE_NAME = re.compile(r'^catalog-\d+\.db\.gz$')
MAX_DB_BYTES = 100 * 1024 * 1024


def verify_signature(db_path, signature, tmp):
    pem = os.path.join(tmp, 'public.pem')
    with open(pem, 'w', encoding='ascii') as f:
        f.write('-----BEGIN PUBLIC KEY-----\n' + '\n'.join(textwrap.wrap(PUBLIC_KEY, 64)) + '\n-----END PUBLIC KEY-----\n')
    sig = os.path.join(tmp, 'signature.der')
    with open(sig, 'wb') as f:
        f.write(signature)
    r = subprocess.run(['openssl', 'dgst', '-sha256', '-verify', pem, '-signature', sig, db_path],
                       capture_output=True, text=True)
    return r.returncode == 0


def previous_version(manifest_rel, before):
    """dataVersion des Manifests im Commit [before]; None, wenn es dort fehlt oder [before] unbekannt ist."""
    if not before or set(before) == {'0'}:
        return None
    r = subprocess.run(['git', 'show', f'{before}:{manifest_rel}'], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return int(json.loads(r.stdout)['dataVersion'])
    except (ValueError, KeyError):
        return None


def check_schema_dir(folder, before):
    errors = []
    name = os.path.basename(folder)
    manifest_path = os.path.join(folder, 'manifest.json')
    try:
        with open(manifest_path, encoding='utf-8') as f:
            m = json.load(f)
    except (OSError, ValueError) as e:
        return [f'{name}: manifest.json nicht lesbar: {e}']
    for key, typ in FIELDS.items():
        if not isinstance(m.get(key), typ):
            errors.append(f'{name}: Feld {key} fehlt oder hat den falschen Typ')
    if errors:
        return errors
    if name != f'schema-{m["schema"]}':
        errors.append(f'{name}: Manifest nennt Schema {m["schema"]}')
    if not FILE_NAME.match(m['file']) or m['file'] != f'catalog-{m["dataVersion"]}.db.gz':
        errors.append(f'{name}: Dateiname {m["file"]} passt nicht zu dataVersion {m["dataVersion"]}')
    if not 0 < m['dbSize'] <= MAX_DB_BYTES:
        errors.append(f'{name}: dbSize {m["dbSize"]} ausserhalb 1..{MAX_DB_BYTES}')
    packages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(folder, '*.gz')))
    if packages != [m['file']]:
        errors.append(f'{name}: erwartet genau {m["file"]}, gefunden {packages}')
    package = os.path.join(folder, m['file'])
    if not os.path.exists(package):
        return errors + [f'{name}: {m["file"]} fehlt']
    if os.path.getsize(package) != m['size']:
        errors.append(f'{name}: {m["file"]} hat {os.path.getsize(package)} Bytes, Manifest {m["size"]}')
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, 'catalog.db')
        try:
            with gzip.open(package, 'rb') as src, open(db, 'wb') as dst:
                total = 0
                while chunk := src.read(1 << 16):
                    total += len(chunk)
                    if total > m['dbSize']:
                        raise ValueError('groesser als dbSize')
                    dst.write(chunk)
        except (OSError, ValueError, EOFError) as e:
            return errors + [f'{name}: {m["file"]} nicht entpackbar: {e}']
        if total != m['dbSize']:
            errors.append(f'{name}: entpackt {total} Bytes, Manifest {m["dbSize"]}')
        with open(db, 'rb') as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        if m['sha256'] and digest != m['sha256']:
            errors.append(f'{name}: SHA-256 {digest} passt nicht zum Manifest')
        try:
            signature = base64.b64decode(m['signature'], validate=True)
        except ValueError:
            signature = None
            errors.append(f'{name}: Signatur ist kein Base64')
        if signature is not None and not verify_signature(db, signature, tmp):
            errors.append(f'{name}: Signatur ungueltig (falscher Schluessel oder veraenderte Datei)')
        try:
            con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
            try:
                user_version = con.execute('PRAGMA user_version').fetchone()[0]
                row = con.execute("SELECT value FROM catalog_meta WHERE key = 'data_version'").fetchone()
                integrity = con.execute('PRAGMA quick_check').fetchone()[0]
            finally:
                con.close()
        except sqlite3.Error as e:
            return errors + [f'{name}: keine gueltige Datenbank: {e}']
        if user_version != m['schema']:
            errors.append(f'{name}: PRAGMA user_version {user_version}, Manifest schema {m["schema"]}')
        if row is None or str(row[0]) != str(m['dataVersion']):
            errors.append(f'{name}: data_version {row and row[0]} in der Datenbank, Manifest {m["dataVersion"]}')
        if integrity != 'ok':
            errors.append(f'{name}: quick_check meldet {integrity}')
    rel = os.path.relpath(manifest_path, ROOT).replace(os.sep, '/')
    prev = previous_version(rel, before)
    if prev is not None and m['dataVersion'] < prev:
        errors.append(f'{name}: dataVersion {m["dataVersion"]} kleiner als vorher ({prev}); Geraete uebernehmen das nicht')
    if not errors:
        print(f'{name}: dataVersion {m["dataVersion"]}, {m["file"]} ({m["size"]} Bytes, entpackt {m["dbSize"]}) in Ordnung'
              + (f', vorher {prev}' if prev is not None else ''))
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--before', default=os.environ.get('BEFORE', ''))
    a = p.parse_args()
    folders = sorted(glob.glob(os.path.join(CATALOG_DB, 'schema-*')))
    if not folders:
        sys.exit('Keine Ordner schema-* unter AstroSNR/catalog-db')
    errors = [e for folder in folders for e in check_schema_dir(folder, a.before)]
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
