# ClokeOS-Apps

Programme für [ClokeOS](https://github.com/cloke-tech/ClokeOS), als Grundlage eines App Stores. Aufgebaut wie eine Linux-Paketquelle:
Quellen und Index liegen im Repository, die Pakete als Release-Dateien.

| Pfad | Inhalt |
|---|---|
| `apps/` | die `.app`-Bundles im Aufbau von macOS (`Name.app/Contents/{Info.plist,MacOS,Resources}`), unter `System/…` (gehören zum Image) und `Applications/` (nachinstallierbar) |
| `packages/*.json` | Binärpakete, die keine einzelne App sind (z. B. `webkit` für Search, je Architektur mit SHA-256) |
| `index.json` | erzeugt, listet Programme und Pakete mit Download-URL und Prüfsumme |
| `tools/gen-index.py` | baut `dist/<kennung>-<version>.tgz` je Programm und `index.json` |
| `tools/cloke-app` | Installer für ClokeOS: `cloke-app list`, `cloke-app install org.dillo.dillo`, `cloke-app install webkit` |

Die Bundles stammen aus `cloakserver/bundles.py` im Hauptrepo (13 Programme). Binärdateien liegen nicht im Repo: Programme, die ein
Binärpaket brauchen, nennen es in `packages/` (Search empfiehlt `webkit`, sonst läuft es mit NetSurf).

Neues Programm: Bundle unter `apps/Applications/` ablegen, `tools/gen-index.py <version> <paket-url>` laufen lassen, `dist/*.tgz` als Release
`apps-<version>` hochladen, `index.json` committen. Stand: Gerüst. Nicht getestet: `cloke-app` in einer VM, Aktualisieren und Entfernen von
Paketen, Signaturen (nur SHA-256), eine Store-Oberfläche.

Lizenz der Bundles und Werkzeuge: wie das Hauptrepo (noch keine Lizenzdatei dort). WebKit: LGPL-2.1 / BSD, Quelle im Hauptrepo unter `clokeos-darwin/webkit/`.
