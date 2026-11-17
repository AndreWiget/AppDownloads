# Astro-SNR – Objektkatalog / Object catalogue

Der Objektkatalog der App Astro-SNR (NGC, IC, Messier) als CSV. Stand: Katalog in Astro-SNR seit November 2026.

The object catalogue of the Astro-SNR app (NGC, IC, Messier) as CSV.

## Dateien / Files

- `dso.csv`: ein Objekt pro Zeile (Koordinaten J2000 in Grad, Typ nach OpenNGC, Helligkeit, Grösse, Flächenhelligkeit) / one object per row
- `dso_name.csv`: Namen und Bezeichnungen je Sprache (`de`, `en`, `*` = sprachneutral) / names per language

## Quellen / Sources

- **OpenNGC** v20260501 von Mattia Verga, <https://github.com/mattiaverga/OpenNGC>, lizenziert unter [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Objektdaten und englische Namen.
- **Wikipedia**, Artikel «Messier-Katalog» der deutschen Wikipedia, Autorinnen und Autoren der Wikipedia, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Deutsche Namen der Messier-Objekte.

## Änderungen / Changes

- Auswahl der Spalten, die Astro-SNR braucht; Spaltennamen geändert.
- Flächenhelligkeit: meist das B-Band aus OpenNGC (Spalte `surface_brightness_band`). Fehlende Werte sind aus Helligkeit und Ellipsenfläche geschätzt (`surface_brightness_estimated = 1`).
- Farbindex B−V für die Umrechnung auf V ergänzt; wo er fehlt, ist er je Objekttyp angenommen (`b_minus_v_assumed = 1`).
- Deutsche Namen der Messier-Objekte aus Wikipedia ergänzt.

Selected columns, renamed; surface brightness mostly in B as in OpenNGC, estimated from magnitude and size where missing; colour index B−V added for the conversion to V (assumed per object type where missing, see the flag columns); German Messier names added from Wikipedia.

## Lizenz / Licence

Dieser abgeleitete Katalog steht ebenfalls unter **CC BY-SA 4.0**: <https://creativecommons.org/licenses/by-sa/4.0/>. Bitte OpenNGC, die Wikipedia-Autorinnen und -Autoren sowie Astro-SNR (Wiget Informatik GmbH) nennen.

This adapted catalogue is licensed under **CC BY-SA 4.0** as well. Please credit OpenNGC, the Wikipedia contributors and Astro-SNR (Wiget Informatik GmbH).

Die übrigen Daten der App (Kameras, Teleskope, Filter) sind nicht Teil dieses Katalogs. / The app's other data (cameras, telescopes, filters) is not part of this catalogue.
