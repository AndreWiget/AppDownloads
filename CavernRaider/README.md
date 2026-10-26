# Cavern Raider – Bonus Missions

Bonus missions of the Android game **Cavern Raider**, hosted in the folder `CavernRaider/` of the
public repository `AndreWiget/AppDownloads`. The app downloads `catalog.json` and the level files from

```
https://raw.githubusercontent.com/AndreWiget/AppDownloads/main/CavernRaider/
```

## Publishing

The master copy lives in the app project under `level_repository/`. To publish changes, copy its
contents (`catalog.json`, `levels/`, this README) into `AppDownloads/CavernRaider/` and push to `main`.

New missions go live without an app update: add the level file and an entry in `catalog.json`.

## Format (`formatVersion: 1`)

`catalog.json` lists every level with `id`, `zone`, `missionNumberInZone`, `title`, `subtitle` and `file`
(always `levels/level_<id>.json`).

Each level file contains the mission data. The app validates everything and rejects a level if:

| Field | Rule |
| --- | --- |
| `id` | 100–9000, not a campaign id (1–9), not 9999 |
| `zone` | `MINES`, `MAGMA`, `FORTRESS`, `GLACIER` or `CRYSTAL` |
| `mapWidth` × `mapHeight` | 20–200 × 10–100 tiles |
| `baseLandingPadRow/Col` | inside the map (the pad is two tiles wide) |
| `prisoners` | 1–20, inside the map |
| `enemySpawns` | at most 30, type `TANK` or `ROBO_CHOPPER`, inside the world (tile size 100) |
| `targetTimeSeconds` | 10–1000 (third star) |
| `title`, `subtitle` | 1–80 characters |

Before publishing a new level, copy it into `level_repository/` of the app project and run
`gradlew :app:testDebugUnitTest`: `LevelJsonTest` checks every level for validity and that all
prisoners are reachable.
