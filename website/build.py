"""Builds the public project website from Markdown pages and problems.yaml.

Usage:
  python3 website/build.py            build the site into _site/
  python3 website/build.py --status   print progress % and counts only

Needs: pip install pyyaml markdown
"""

import html
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_FILE = ROOT / "problems.yaml"
PAGES_DIR = ROOT / "website" / "pages"
ASSETS_DIR = ROOT / "website" / "assets"
OUT_DIR = ROOT / "_site"

AREAS = {"Hardware", "Firmware", "Portal", "Website", "Safety"}
STATUSES = ["Solved", "In progress", "Pending", "Parked"]
REQUIRED = ["id", "title", "area", "why", "status"]

# (file name in pages/, output file, menu label). The Problems page is generated.
NAV = [
    ("about.md", "index.html", "About"),
    (None, "problems.html", "Problems"),
    ("hardware.md", "hardware.html", "Hardware"),
    ("firmware.md", "firmware.html", "Firmware"),
    ("portal.md", "portal.html", "Portal"),
]

# Privacy guard: the site is public. Fail the build if something looks like an
# IMEI (15 digits) or a SIM ICCID (19-20 digits starting with 89).
PRIVATE_PATTERNS = {
    "IMEI-like number": re.compile(r"(?<!\d)\d{15}(?!\d)"),
    "SIM ICCID-like number": re.compile(r"(?<!\d)89\d{17,18}(?!\d)"),
}


def load_problems():
    data = yaml.safe_load(PROBLEMS_FILE.read_text(encoding="utf-8"))
    problems = data["problems"]
    seen = set()
    for p in problems:
        for field in REQUIRED:
            if not p.get(field):
                sys.exit(f"problems.yaml: {p.get('id', '?')} is missing '{field}'")
        if p["id"] in seen:
            sys.exit(f"problems.yaml: duplicate id {p['id']}")
        seen.add(p["id"])
        if p["area"] not in AREAS:
            sys.exit(f"problems.yaml: {p['id']} has unknown area '{p['area']}'")
        if p["status"] not in STATUSES:
            sys.exit(f"problems.yaml: {p['id']} has unknown status '{p['status']}'")
        if p["status"] == "Solved" and not p.get("date_solved"):
            sys.exit(f"problems.yaml: {p['id']} is Solved but has no date_solved")
    return problems


def progress(problems):
    counts = {s: sum(1 for p in problems if p["status"] == s) for s in STATUSES}
    active = len(problems) - counts["Parked"]
    percent = round(100 * counts["Solved"] / active) if active else 0
    return percent, counts, active


def check_private(text, where):
    for label, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            sys.exit(f"Privacy guard: {where} contains an {label}. Remove it before publishing.")


def render_md(text):
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    # Turn ```mermaid code blocks into diagrams Mermaid can draw.
    return re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: f'<pre class="mermaid">{m.group(1)}</pre>',
        body,
        flags=re.S,
    )


def header_html(percent, counts, active, current):
    active_attr = ' class="active"'
    links = "".join(
        f'<a href="{out}"{active_attr if out == current else ""}>{label}</a>'
        for _, out, label in NAV
    )
    return f"""<header>
  <div class="title">DIY Kids' Excursion Tracker <span>a learning project</span></div>
  <nav>{links}</nav>
  <div class="progress" aria-label="Progress {percent}%">
    <div class="bar"><div class="fill" style="width:{percent}%"></div></div>
    <div class="numbers"><strong>{percent}% solved</strong>
      &middot; {counts['Solved']} solved &middot; {counts['In progress']} in progress
      &middot; {counts['Pending']} pending <small>({counts['Parked']} parked, {active} counted)</small></div>
  </div>
</header>"""


def page_html(title, body, header):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | DIY Kids' Excursion Tracker</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{header}
<main>
{body}
</main>
<footer>Built automatically from <code>problems.yaml</code> on {date.today().isoformat()}.
No names, photos, locations or device numbers are ever published here.</footer>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({{ startOnLoad: true, theme: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "default" }});
</script>
</body>
</html>
"""


def problems_body(problems):
    rows = []
    for p in problems:
        e = {k: html.escape(str(p.get(k) or "")) for k in p}
        status_class = p["status"].lower().replace(" ", "-")
        rows.append(f"""<tr class="{status_class}">
  <td>{e['id']}</td>
  <td><strong>{e['title']}</strong> <span class="area-inline">&middot; {e['area']}</span>
    <div class="why">{e['why']}</div>
    {f'<div class="learned">Learned: {e["learned"]}</div>' if p.get('learned') else ''}
    {f'<div class="comments">{e["comments"]}</div>' if p.get('comments') else ''}</td>
  <td class="area">{e['area']}</td>
  <td><span class="badge {status_class}">{e['status']}</span>
    {f'<div class="date">{e["date_solved"]}</div>' if p.get('date_solved') else ''}</td>
</tr>""")
    return f"""<h1>Problems</h1>
<p>The whole project is a list of problems, solved one by one, easiest first.
Progress = solved problems divided by all problems that are not parked.
This page is generated from <code>problems.yaml</code>.</p>
<div class="table-wrap"><table class="problems">
<thead><tr><th>#</th><th>Problem</th><th class="area">Area</th><th>Status</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table></div>"""


def build():
    problems = load_problems()
    percent, counts, active = progress(problems)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir()
    shutil.copy(ASSETS_DIR / "style.css", OUT_DIR / "style.css")

    for source, out, label in NAV:
        if source:
            text = (PAGES_DIR / source).read_text(encoding="utf-8")
            check_private(text, f"website/pages/{source}")
            body = render_md(text)
        else:
            body = problems_body(problems)
            check_private(body, "problems.yaml")
        page = page_html(label, body, header_html(percent, counts, active, out))
        (OUT_DIR / out).write_text(page, encoding="utf-8")

    (OUT_DIR / ".nojekyll").touch()
    print(f"Built {len(NAV)} pages into {OUT_DIR.relative_to(ROOT)}/")
    print_status(percent, counts, active)


def print_status(percent, counts, active):
    print(
        f"Progress: {percent}% ({counts['Solved']} of {active} solved; "
        f"{counts['In progress']} in progress, {counts['Pending']} pending, "
        f"{counts['Parked']} parked)"
    )


if __name__ == "__main__":
    if "--status" in sys.argv:
        print_status(*progress(load_problems()))
    else:
        build()
