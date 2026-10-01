# DIY Asset Tracker

A hobby learning project: building a small GPS/LTE-M tracker to find my keys, learning electronics and connectivity along the way.

Project website: https://irfanali1.github.io/AssetTracker/

## Folders

| Folder | What goes there |
|---|---|
| `problems.yaml` | The list of problems to solve, with status. The single source of truth for progress. |
| `hardware/` | Parts list notes, wiring, enclosure files. |
| `firmware/` | The software that runs on the tracker. |
| `portal/` | The private app/website where the location shows up on a phone. |
| `website/` | The public project website (pages in Markdown, plus the build script). |

See the progress any time with `python3 website/build.py --status`.

No secrets in this repo: device numbers, SIM numbers, keys and passwords stay in local `.env` files, which git ignores.
