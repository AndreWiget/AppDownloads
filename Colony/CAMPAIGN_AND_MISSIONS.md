# COLONY — Missions- & Kampagnen-Spezifikation (Entwicklerdokumentation)

Dieses Dokument bietet eine vollständige, entwicklerorientierte Referenz aller in **Colony** implementierten Kampagnen- und Missionsstrukturen. Es umfasst:
1. **Die 5 offiziellen Story-Kampagnen-Kapitel** (`STORY_CAMPAIGN`)
2. **Die 10 herunterladbaren Extra-Missionen** (`EXTRA_MISSION`) mit ihren jeweiligen 3 Sublevel-Phasen
3. **Missions-Engine-Architektur & Phasen-Progression** (`MissionSystem`, `MissionPhase`, `ObjectiveType`)
4. **JSON-Schemas & Verteilungs-Infrastruktur** (`AppDownloads`-Repository)

---

## 1. Architektur der Missions-Engine

### Phasen-Progression & Kontinuität (Zero-Reset Principle)
In klassischen RTS-Spielen führt das Erreichen von Teilzielen oft zu Karten-Resets oder Neustarts. In Colony arbeitet die Missions-Engine nach dem **Zero-Reset-Prinzip**:
- Eine Mission besteht aus einer geordneten Liste von **Phasen (`MissionPhase`)**.
- Wenn alle als `isPrimary = true` markierten Ziele einer Phase erfüllt sind, rückt der Phasen-Index (`currentPhaseIndex`) automatisch um 1 vor.
- **Zustandserhaltung**: Das gebaute unterirdische Wabennetzwerk (Kammern), die Koloniepopulation, die Brut in der Nursery, gesammelte Ressourcen und verlegte Pheromonspuren bleiben über Phasenwechsel hinweg **nahtlos und ohne Unterbrechung erhalten**.
- Der finale Missionssieg (`isVictory = true`) wird erst vergeben, wenn alle Primärziele der letzten Phase erfüllt sind. Die erreichten Blatt-Wertungen (`leavesEarned` 1–3) spiegeln die Gesamtzahl der absolvierten Primär- und Sekundärziele wider.

### Ziel-Typen (`ObjectiveType`)
Die Engine unterstützt folgende dynamische Zielauswertungen über `MissionSystem`:
* `COLLECT_RESOURCE`: Prüft Vorratsmengen im Lager (`targetResourceType`: `PLANT_MATERIAL`, `PROTEIN`, `WATER`, `RESIN_MINERAL`, `GENE_POINTS`).
* `EXPAND_POPULATION`: Bewertet die Gesamtzahl lebender Ameisen oder gezielt nach Kaste (`targetCaste`: `WORKER`, `SOLDIER`, `SCOUT`, etc.).
* `BUILD_CHAMBER`: Zählt fertig gebaute Wabenkammern (`targetChamberType`: `BROOD_ROOM`, `FOOD_STORE`, `WATER_RESERVOIR`, `FUNGUS_GARDEN`, `WASTE_ROOM`, `GUARD_ROOM`, `VENTILATION_SHAFT`).
* `DEFEAT_HAZARD`: Zählt das Besiegen von Feinden wie Springspinnen, Wespen oder Raubkäfern (`stats.totalThreatsDefeated`).
* `SURVIVE_DURATION`: Verlangt das Überleben einer Zeitspanne in Sekunden (`stats.timeElapsedSeconds`).

---

## 2. Offizielle Story-Kampagne (`STORY_CAMPAIGN`)

Die Hauptkampagne führt den Spieler schrittweise in die Spielmechaniken, Kasten und Herausforderungen des Gartens ein.

---

### Kapitel 1: Terrassenkante (`mission_01_terrace_edge`)
* **Region**: Terrassenbeet & Steinweg
* **Schwierigkeit**: Leicht (EASY)
* **Belohnung**: 30 🧬 Genpunkte
* **Hintergrund**: Gründung der ersten Kolonie an der sonnigen Terrassenkante. Das Beet bietet gute Nahrung, aber der offene Boden ist ungeschützt vor Regengüssen und Raubinsekten.

#### Phasen & Sublevel:
1. **Phase 1: Die Gründung (Die ersten Spuren)**
   - *Ziel 1 (Primär)*: Sammle 50 Pflanzenmaterial (`COLLECT_RESOURCE`, 50 🍃)
   - *Ziel 2 (Primär)*: Grabe 1 Brutkammer (`BUILD_CHAMBER`, 1x `BROOD_ROOM`)
2. **Phase 2: Wachstum & Vorrat (Vorbereitung auf den Regen)**
   - *Ziel 1 (Primär)*: Sammle 100 Pflanzenmaterial (`COLLECT_RESOURCE`, 100 🍃)
   - *Ziel 2 (Primär)*: Erweitere auf 3 Brutkammern (`BUILD_CHAMBER`, 3x `BROOD_ROOM`)
   - *Ziel 3 (Sekundär)*: Züchte Kolonie auf 12 Ameisen heran (`EXPAND_POPULATION`, 12)
3. **Phase 3: Garten-Gefahr (Schatten über der Terrasse)**
   - *Ziel 1 (Primär)*: Wehre die Raubspinne ab (`DEFEAT_HAZARD`, 1x Spinne)
   - *Ziel 2 (Sekundär)*: Vergrössere die Kolonie auf 15 Ameisen (`EXPAND_POPULATION`, 15)

---

### Kapitel 2: Apfelbaum-Hain (`mission_02_apple_tree`)
* **Region**: Rasen & Apfelbaum-Garten
* **Schwierigkeit**: Normal (MEDIUM)
* **Belohnung**: 45 🧬 Genpunkte
* **Hintergrund**: Am Boden liegendes Fallobst verströmt süssen Duft, zieht aber räuberische Käferlarven und Wespen an. Es müssen weite Pheromon-Highways etabliert werden.

#### Phasen & Sublevel:
1. **Phase 1: Süsse Spur (Die Apfelfunde)**
   - *Ziel 1 (Primär)*: Etabliere Pheromonspuren und ernte 150 Pflanzenmaterial/Zucker (`COLLECT_RESOURCE`, 150 🍃)
   - *Ziel 2 (Primär)*: Baue 2 Vorratskammern (`BUILD_CHAMBER`, 2x `FOOD_STORE`)
2. **Phase 2: Käfer-Begegnung (Chitin-Verstärkung)**
   - *Ziel 1 (Primär)*: Züchte 3 Soldaten-Ameisen (`EXPAND_POPULATION`, 3x `SOLDIER`)
   - *Ziel 2 (Primär)*: Erbeute 80 Protein von Bodeninsekten (`COLLECT_RESOURCE`, 80 🥩)
   - *Ziel 3 (Sekundär)*: Grabe 1 Wachkammer (`BUILD_CHAMBER`, 1x `GUARD_ROOM`)
3. **Phase 3: Grossernte (Vorratsfestung)**
   - *Ziel 1 (Primär)*: Bringe insgesamt 250 Pflanzenmaterial/Zucker ins Nest (`COLLECT_RESOURCE`, 250 🍃)
   - *Ziel 2 (Primär)*: Erweitere die Kolonie auf 20 Ameisen (`EXPAND_POPULATION`, 20)

---

### Kapitel 3: Kompost-Tiefen (`mission_03_compost_depths`)
* **Region**: Komposthaufen & Schattige Erde
* **Schwierigkeit**: Schwer (HARD)
* **Belohnung**: 60 🧬 Genpunkte
* **Hintergrund**: Gärungsprozesse im Kompost erzeugen enorme Wärme und locken Pilzsporen an. Die Kolonie muss lernen, eigene Pilzgärten anzulegen und mit Hitze umzugehen.

#### Phasen & Sublevel:
1. **Phase 1: Wärme-Pioniere (Eindringen in den Kompost)**
   - *Ziel 1 (Primär)*: Grabe 2 Pilzgärten (`BUILD_CHAMBER`, 2x `FUNGUS_GARDEN`)
   - *Ziel 2 (Primär)*: Sammle 180 feuchtes Pflanzenmaterial für das Myzel (`COLLECT_RESOURCE`, 180 🍃)
2. **Phase 2: Klimakontrolle (Temperatur & Belüftung)**
   - *Ziel 1 (Primär)*: Baue 2 Belüftungsschächte gegen Stauhitze (`BUILD_CHAMBER`, 2x `VENTILATION_SHAFT`)
   - *Ziel 2 (Primär)*: Baue 1 Abfallkammer zur Nestreinigung (`BUILD_CHAMBER`, 1x `WASTE_ROOM`)
   - *Ziel 3 (Sekundär)*: Erhalte 100 Protein aus Insektenlarven (`COLLECT_RESOURCE`, 100 🥩)
3. **Phase 3: Der lebende Superorganismus**
   - *Ziel 1 (Primär)*: Erhöhe die Kolonie auf 28 Ameisen (`EXPAND_POPULATION`, 28)
   - *Ziel 2 (Primär)*: Betreibe mindestens 3 aktive Brutkammern (`BUILD_CHAMBER`, 3x `BROOD_ROOM`)

---

### Kapitel 4: Tropen-Gewächshaus (`mission_04_greenhouse`)
* **Region**: Glashaus & Tropenbeete
* **Schwierigkeit**: Schwer (HARD)
* **Belohnung**: 75 🧬 Genpunkte
* **Hintergrund**: Das Gewächshaus bietet ganzjährige Feuchtigkeit und exotische Nektarpflanzen, birgt jedoch die Gefahr plötzlicher Hitzewellen und Raubwespen.

#### Phasen & Sublevel:
1. **Phase 1: Glashaus-Eroberung**
   - *Ziel 1 (Primär)*: Sammle 200 Wasser aus Kondensationstropfen (`COLLECT_RESOURCE`, 200 💧)
   - *Ziel 2 (Primär)*: Errichte 2 Wasserreservoirs (`BUILD_CHAMBER`, 2x `WATER_RESERVOIR`)
2. **Phase 2: Tropischer Schwarm**
   - *Ziel 1 (Primär)*: Baue 3 Pilzgärten zur Nahrungserzeugung (`BUILD_CHAMBER`, 3x `FUNGUS_GARDEN`)
   - *Ziel 2 (Primär)*: Züchte 5 Soldaten zur Abwehr fliegender Räuber (`EXPAND_POPULATION`, 5x `SOLDIER`)
   - *Ziel 3 (Sekundär)*: Besiege 1 Raubwespe (`DEFEAT_HAZARD`, 1)
3. **Phase 3: Das Treibhaus-Monopol**
   - *Ziel 1 (Primär)*: Erreiche eine Koloniepopulation von 35 Ameisen (`EXPAND_POPULATION`, 35)
   - *Ziel 2 (Primär)*: Sichere Vorräte von mindestens 350 Pflanzenstoffen (`COLLECT_RESOURCE`, 350 🍃)

---

### Kapitel 5: Teichbecken (`mission_05_pond_basin`)
* **Region**: Feuchtufer & Schilfgürtel
* **Schwierigkeit**: Experte (EXPERT)
* **Belohnung**: 90 🧬 Genpunkte
* **Hintergrund**: Das finale Kapitel der Story-Kampagne. Ständige Überschwemmungen und agile Raublibellen/Wespenschwärme verlangen absolute Meisterschaft über Pheromone und Nestarchitektur.

#### Phasen & Sublevel:
1. **Phase 1: Das feuchte Ufer (Deichbau)**
   - *Ziel 1 (Primär)*: Sammle 250 Wasser (`COLLECT_RESOURCE`, 250 💧)
   - *Ziel 2 (Primär)*: Errichte 3 Wasserreservoirs (`BUILD_CHAMBER`, 3x `WATER_RESERVOIR`)
   - *Ziel 3 (Primär)*: Baue 2 Wachkammern an den Nesteingängen (`BUILD_CHAMBER`, 2x `GUARD_ROOM`)
2. **Phase 2: Schlacht im Schilf**
   - *Ziel 1 (Primär)*: Trainiere 8 Soldaten (`EXPAND_POPULATION`, 8x `SOLDIER`)
   - *Ziel 2 (Primär)*: Besiege 2 Uferräuber (`DEFEAT_HAZARD`, 2)
   - *Ziel 3 (Sekundär)*: Sammle 150 Protein aus Wasserinsekten (`COLLECT_RESOURCE`, 150 🥩)
3. **Phase 3: Die Herrscherin des Teichs**
   - *Ziel 1 (Primär)*: Baue eine Superkolonie mit 40 Ameisen auf (`EXPAND_POPULATION`, 40)
   - *Ziel 2 (Primär)*: Sichere 5 Brutkammern gegen Überschwemmung (`BUILD_CHAMBER`, 5x `BROOD_ROOM`)
   - *Ziel 3 (Primär)*: Lagere 400 Einheiten Nahrung ein (`COLLECT_RESOURCE`, 400 🍃)

---

## 3. Die 10 herunterladbaren Extra-Missionen (`EXTRA_MISSION`)

Die Extra-Missionen sind modular über das Repository `AppDownloads` gehostet und bieten anspruchsvolle Spezialszenarien mit jeweils 3 vollwertigen Sublevel-Phasen.

---

### Extra-Mission 1: Gewitter-Krise (`extra_mission_01_rainstorm`)
* **Schwierigkeit**: Normal (MEDIUM) | **Belohnung**: 45 🧬 Genpunkte
* **Thematik**: Sturzfluten & Überflutung der Nesteingänge
* **Phasen**:
  1. *Phase 1: Sturmwarnung* — Not-Wasserreservoirs graben (1x `WATER_RESERVOIR`) und 150 Wasser vor dem Schlamm sichern.
  2. *Phase 2: Hochwasser-Evakuierung* — Brut in tiefere Waben verlegen (2x `BROOD_ROOM`), 200 Pflanzenteile bergen, 15 Ameisen am Leben halten.
  3. *Phase 3: Nach dem Wolkenbruch* — 100 Protein von ertrunkenen Insektenlarven bergen und die Kolonie auf 20 gesunde Arbeiterinnen aufstocken.

---

### Extra-Mission 2: Spinnennest-Infiltration (`extra_mission_02_spider_nest`)
* **Schwierigkeit**: Schwer (HARD) | **Belohnung**: 70 🧬 Genpunkte
* **Thematik**: Territoriale Konfrontation mit einer Springspinne
* **Phasen**:
  1. *Phase 1: Aufklärungs-Patrouille* — Vorsichtiges Beernten der Blattlaushecke (180 🍃) und Bau einer Wachkammer (`GUARD_ROOM`).
  2. *Phase 2: Kriegsmobilisierung* — Zucht von 4 Soldaten-Ameisen (`SOLDIER`) und Vergrösserung des Volkes auf 18 Ameisen.
  3. *Phase 3: Befreiung des Reviers* — Offensive Attacke auf die Springspinne (`DEFEAT_HAZARD`), Chitin bergen (120 🥩).

---

### Extra-Mission 3: Dürre & Grundwasser-Expedition (`extra_mission_03_drought`)
* **Schwierigkeit**: Experte (EXPERT) | **Belohnung**: 85 🧬 Genpunkte
* **Thematik**: Extreme Hitze (>32°C), rasche Pheromonverdunstung & Wassermangel
* **Phasen**:
  1. *Phase 1: Wassernotstand* — 2 Wasserreservoirs (`WATER_RESERVOIR`) und Belüftungsschächte (`VENTILATION_SHAFT`) zur Kühlung errichten.
  2. *Phase 2: Vorstoss ins Erdreich* — Tiefe Pilzgärten (`FUNGUS_GARDEN`) zur Feuchtigkeitsbindung anlegen und 220 Nahrung einlagern.
  3. *Phase 3: Oase unter der Erde* — 250 Wasser in Reservoirs sammeln und eine autarke Kolonie von 24 Ameisen etablieren.

---

### Extra-Mission 4: Luftangriff der Wespen (`extra_mission_04_wasp_attack`)
* **Schwierigkeit**: Schwer (HARD) | **Belohnung**: 75 🧬 Genpunkte
* **Thematik**: Schnelle Luftüberfälle durch agile Raubwespen
* **Phasen**:
  1. *Phase 1: Luftraum-Alarm* — Eingänge mit Wachkammern (`GUARD_ROOM`) befestigen und Vorräte unter Tage bringen (150 🍃).
  2. *Phase 2: Gegenwehr organisieren* — Gezielte Aufzucht von 5 schweren Soldatinnen (`SOLDIER`) zum Abfangen von Bodenlandungen.
  3. *Phase 3: Den Luftraum säubern* — Wespe im koordinierten Pheromon-Angriff eliminieren (`DEFEAT_HAZARD`) und 140 Protein einbringen.

---

### Extra-Mission 5: Pilzgarten-Expansion (`extra_mission_05_fungus_fever`)
* **Schwierigkeit**: Normal (MEDIUM) | **Belohnung**: 60 🧬 Genpunkte
* **Thematik**: Agrarische Symbiose & industrielle Myzelzucht
* **Phasen**:
  1. *Phase 1: Erste Sporen* — 2 Pilzgärten (`FUNGUS_GARDEN`) anlegen und 200 zerkleinerte Blätter zur Gärung heranschaffen.
  2. *Phase 2: Klima-Regulierung* — Belüftungsschächte und Abfallkammern (`WASTE_ROOM`) bauen, um Schimmelbefall zu verhindern.
  3. *Phase 3: Myzel-Grossbetrieb* — Ausbau auf 4 florierende Pilzgärten und Versorgung von 30 Ameisen.

---

### Extra-Mission 6: Die Zucker-Autobahn (`extra_mission_06_sugar_trail`)
* **Schwierigkeit**: Leicht (EASY) | **Belohnung**: 50 🧬 Genpunkte
* **Thematik**: Weitstrecken-Logistik quer über die Terrassenplatten
* **Phasen**:
  1. *Phase 1: Pfadfindung* — Erkundung des fernen Tisches, 2 Vorratskammern (`FOOD_STORE`) bauen und 100 Zucker sichern.
  2. *Phase 2: Karawanen-Logistik* — Pheromon-Schnellstrasse mit 15 Arbeiterinnen (`WORKER`) besetzen und 250 Zucker transportieren.
  3. *Phase 3: Das grosse Schlemmen* — Vorratsspeicher auf 400 Einheiten maximieren und Volk auf 25 Ameisen erweitern.

---

### Extra-Mission 7: Der Käfer-Friedhof (`extra_mission_07_beetle_graveyard`)
* **Schwierigkeit**: Schwer (HARD) | **Belohnung**: 80 🧬 Genpunkte
* **Thematik**: Protein-Reichtum im morschen Totholz unter Räuberdruck
* **Phasen**:
  1. *Phase 1: Sicherung des Totholzes* — Wachkammer errichten und Patrouillenspinne vertreiben (`DEFEAT_HAZARD`).
  2. *Phase 2: Chitin-Bergung* — 5 Soldatinnen zur Sicherung heranziehen und 180 Protein aus Käferpanzern bergen.
  3. *Phase 3: Kolossales Wachstum* — Massiver Kolonieausbau auf 32 Ameisen und 3 Brutkammern (`BROOD_ROOM`).

---

### Extra-Mission 8: Die Kaltfront (`extra_mission_08_cold_front`)
* **Schwierigkeit**: Experte (EXPERT) | **Belohnung**: 90 🧬 Genpunkte
* **Thematik**: Frostwetter (<10°C), Bewegungs-Verlangsamung & Kältestarre
* **Phasen**:
  1. *Phase 1: Kälte-Dämmung* — 160 Harz sammeln und 2 Belüftungsschächte zur Wärmezirkulation installieren.
  2. *Phase 2: Biowärme durch Gärung* — Gärende Pilzgärten (`FUNGUS_GARDEN`) als biologische Heizung nutzen, Brut schützen.
  3. *Phase 3: Überwinterung gemeistert* — Mindestens 26 Ameisen trotz Kälteeinbruch durchbringen und 300 Wintervorräte anlegen.

---

### Extra-Mission 9: Die Super-Metropole (`extra_mission_09_super_colony`)
* **Schwierigkeit**: Experte (EXPERT) | **Belohnung**: 100 🧬 Genpunkte
* **Thematik**: Monumentaler Nestbau & gigantische Schwarmintelligenz
* **Phasen**:
  1. *Phase 1: Infrastruktur-Fundament* — 3 Vorratskammern, 2 Wasserreservoirs und 1 Abfallkammer zur Hygiene errichten.
  2. *Phase 2: Bollwerk der Wehrhaften* — 2 Wachkammern und 6 Soldaten ausbilden, Gartenbedrohung abwehren.
  3. *Phase 3: Das Weltwunder der Insekten* — Megametropole auf 40 Ameisen und 500 Einheiten Vorräte ausbauen.

---

### Extra-Mission 10: Die Königinnen-Dynastie (`extra_mission_10_queen_dynasty`)
* **Schwierigkeit**: Experte (EXPERT) | **Belohnung**: 120 🧬 Genpunkte
* **Thematik**: Krönung des Schwarms & Vorbereitung auf den Schwarmflug
* **Phasen**:
  1. *Phase 1: Königliche Festung* — 2 Wachkammern, 2 Belüftungen und 3 Grosslager errichten.
  2. *Phase 2: Verteidigung der Krone* — 8 Elitesoldaten aufstellen und 2 Grossräuber (Wespe/Spinne) bezwingen.
  3. *Phase 3: Der goldene Schwarmflug* — Rekordvolk von 45 Ameisen, 5 Brutkammern und 600 Einheiten Nahrung für die nächste Generation bereitstellen.

---

## 4. JSON-Schema & Hosting-Infrastruktur

Alle Extra-Missionen werden als eigenständige `.json`-Dateien serialisiert und über das öffentliche GitHub-Repository ausgeliefert:
* **Catalog-Endpunkt**:  
  `https://raw.githubusercontent.com/AndreWiget/AppDownloads/main/Colony/levels/catalog.json`
* **Level-Dateien**:  
  `https://raw.githubusercontent.com/AndreWiget/AppDownloads/main/Colony/levels/extra_mission_XX_<name>.json`

### Level-Schema-Referenz
```json
{
  "id": "extra_mission_XX_name",
  "category": "EXTRA_MISSION",
  "number": 1,
  "title": "Missionsname",
  "subtitle": "Untertitel (3 Phasen)",
  "description": "Ausführliche Missionsbeschreibung",
  "author": "Ersteller / Studio",
  "version": 1,
  "difficulty": "EASY | MEDIUM | HARD | EXPERT",
  "initialResources": {
    "plantMaterial": 140.0,
    "protein": 70.0,
    "water": 160.0,
    "resinMineral": 90.0,
    "genePoints": 25.0
  },
  "customGardenNodes": [
    {
      "id": "node_id",
      "type": "PLANT_MATERIAL | WATER | PROTEIN | RESIN_MINERAL",
      "position": { "x": 50.0, "y": 50.0 },
      "remainingAmount": 200.0,
      "maxAmount": 200.0
    }
  ],
  "initialHazards": [
    {
      "id": "hazard_id",
      "type": "JUMPING_SPIDER | WASP | RAIN_PUDDLE | BEETLE_LARVA",
      "position": { "x": 60.0, "y": 60.0 },
      "hp": 150.0
    }
  ],
  "phases": [
    {
      "phaseNumber": 1,
      "title": "Phasentitel",
      "subtitle": "Phasenuntertitel",
      "description": "Aufgabenbeschreibung",
      "objectives": [
        {
          "id": "obj_id",
          "description": "Zieltext für den Spieler",
          "type": "COLLECT_RESOURCE | EXPAND_POPULATION | BUILD_CHAMBER | DEFEAT_HAZARD | SURVIVE_DURATION",
          "targetAmount": 100.0,
          "targetResourceType": "PLANT_MATERIAL",
          "targetChamberType": "BROOD_ROOM",
          "targetCaste": "WORKER",
          "isPrimary": true
        }
      ]
    }
  ],
  "rewardGenePoints": 50.0,
  "fileSizeKb": 16,
  "downloadUrl": "https://raw.githubusercontent.com/AndreWiget/AppDownloads/main/Colony/levels/extra_mission_XX_name.json"
}
```
