# Project: DIY asset tracker (a learning project)

## Who I am and why
I'm Irfan, an adult with no background in electronics or software. I want to learn by solving a real problem: a small tracker that tells me where my things are. The detailed real-world use case is kept in Claude's private project memory, not in this public repo; read it there. This is a hobby. It will never be a commercial product, so always choose what teaches me most and is simplest. Ignore scale, cost optimisation and certification.

## How to talk to me
- Be brief. Short answers, short steps, no walls of text.
- Use plain language. The first time you use a technical term, explain it in one simple sentence, with an everyday analogy if it helps.
- One step at a time. Tell me exactly what to do (click, type, plug in), then wait for me to confirm before moving on.
- Before you write code or propose hardware, say in 1 to 2 sentences what we are doing and why.
- When there are options, show at most 3, recommend one, and give the reason in one line.
- If I'm heading toward something unsafe or a dead end, tell me directly.
- When we finish a problem, give me a "What you learned" summary of 2 to 3 bullets.

## The method: build by solving problems
Treat the whole project as a list of problems that we solve one by one. Each solved problem means I learned something new.
- Keep one source of truth: a problems file (for example problems.yaml). Each entry has: id, title, area (Hardware / Firmware / Portal / Website / Safety), why it matters (one line), status (Pending / In progress / Solved / Parked), what I learned, comments, and date solved.
- Progress % = solved problems divided by all problems that are not parked. Always calculate it automatically, never by hand.
- Problems can be split or added as we discover them. That is normal, not a failure.
- At the start of every session, read the problems file, tell me the current %, and suggest the next problem. At the end of every session, update the problems file and the website.

## What the tracker should do (my current thinking; challenge it where needed)
- It lives in a zipped pocket of a bag. Small and slim: roughly a credit-card footprint, ideally about 1 cm thick.
- "Live mode": location every 30 to 60 seconds for a few hours, then recharged overnight.
- A "location ladder", cheapest option first: a motion sensor wakes the device, then a WiFi scan (works indoors, in stations and museums), then GPS outdoors, then cell towers as a rough fallback.
- Data is sent over cellular LTE-M/NB-IoT using an IoT SIM (for example 1NCE).
- Apple Find My or Google Find Hub only as a later, optional backup, because official access is restricted.
- A "tether": a trusted person carries a small Bluetooth beacon. If the tracker stops hearing it for about 2 minutes, the tracker switches to alarm mode (frequent location fixes plus a push alert to my phone).
- A geofence alert around the planned destination.
- Candidate learning hardware: Nordic Thingy:91 X (cellular, GPS, WiFi scanning and Bluetooth in one box). I have not bought anything yet. Propose and justify every purchase before I buy.

## Non-negotiable safety and privacy rules
- Physical safety: no coin-cell batteries, no loose small parts, a rigid enclosure closed with screws, and never worn around the neck.
- Only a certified LiPo battery with a protection circuit.
- No microphone or "listen-in" feature.
- The tracking portal must be private, behind a login.
- The website is public, so it must never show personal names, photos, live or past locations, IMEI, SIM numbers, API keys or passwords.
- Keep all secrets out of the git repository.

## The public project website
A simple static website that documents my journey. Suggest the simplest tooling, for example Markdown pages hosted for free on GitHub Pages. Pages:
1. About: what I'm building and why.
2. Problems: the list with status and comments, generated automatically from the problems file. The site header shows a progress bar with % completed and counts (solved / in progress / pending).
3. Hardware: components considered and chosen, and why; the BOM (part, purpose, price, link); a block diagram.
4. Firmware: what the device software does, the architecture chosen and why, and a diagram.
5. Portal: how I see the location on my phone, the architecture chosen and why, and a diagram.
Each technical page ends with a short "Decisions" log: the decision, the options considered, and why it was chosen (2 to 3 lines each). Draw all diagrams in Mermaid so they are stored as text.

## Your first task
1. Save these instructions as CLAUDE.md in the project folder so you follow them every session.
2. Propose a simple folder structure (hardware, firmware, portal, website, plus the problems file).
3. Draft the first problem list: 15 to 25 problems, ordered from easiest to hardest, starting with free ones such as "understand the block diagram".
4. Build the first version of the website with a working progress bar.
5. Stop, show me the current % (it will be low, and that's fine), and suggest Problem #1.

---

## Repo notes for Claude (added during setup)
- `problems.yaml` (repo root) is the single source of truth for the problem list.
- Current progress: run `python3 website/build.py --status`. It prints the % and counts. Never compute % by hand.
- `python3 website/build.py` builds the site into `_site/` (needs `pip install pyyaml markdown`). It also fails if it spots something that looks like an IMEI or SIM number.
- Website page text lives in `website/pages/*.md`. The Problems page and the progress bar are generated; don't edit them by hand.
- GitHub Actions (`.github/workflows/pages.yml`) rebuilds and publishes the site to GitHub Pages on every push to `main`.
- Code and notes per area: `hardware/`, `firmware/`, `portal/`. Secrets go in local `.env` files, which are git-ignored.
- Public story (decided 2026-10-01): the website, README and problem list describe a key finder. This repo is public: never write personal details about the real use case into any file here, including this one.
