#!/usr/bin/env python3
"""Extract the Series 1 Teaser Bank inventory from the staging drafts.

Reads ~/workspace/drafts/linkedin-drip-dayN-YYYY-MM-DD.md (N=1..14) plus the
Art Director's visuals brief for titles, and writes data/series1.json.
Copy is taken verbatim from each draft's "## Post copy" section.
"""
import json
import re
from pathlib import Path

DRAFTS = Path.home() / "workspace" / "drafts"
VISUALS_DIR = Path.home() / "workspace" / "art-director-buddy" / "teaser-bank-visuals"
OUT = Path.home() / "workspace" / "projects" / "teaser-bank" / "data" / "series1.json"

TITLES = {
    1: "The 40-year arc",
    2: "The Knowledge Navigator",
    3: "Rae Assist, 1993",
    4: "The fall",
    5: "Penny's return",
    6: "Why now",
    7: "What it is — a staff",
    8: "The trojan horse",
    9: "Forgotten subscriptions",
    10: "Double-charged",
    11: "The eyeglasses story",
    12: "One picture",
    13: "The staff grows",
    14: "The tip jar",
}

posts = []
for day in range(1, 15):
    matches = sorted(DRAFTS.glob(f"linkedin-drip-day{day}-*.md"))
    assert matches, f"no draft for day {day}"
    text = matches[0].read_text()
    date = re.search(r"day\d+-(\d{4}-\d{2}-\d{2})\.md", matches[0].name).group(1)

    # Post copy: between the "## Post copy" heading and the next "## " heading.
    m = re.search(r"## Post copy[^\n]*\n(.*?)\n## ", text, re.S)
    copy = m.group(1).strip() if m else ""

    # Live LinkedIn URL, if the draft recorded one.
    urls = re.findall(r"https://www\.linkedin\.com/feed/update/urn:li:activity:\d+/?", text)
    url = urls[-1] if urls else None

    # Visual section text (first ~6 lines after the heading).
    vm = re.search(r"## Visuals?\n(.*?)(?:\n## |\Z)", text, re.S)
    visual_note = " ".join(vm.group(1).strip().split())[:400] if vm else ""

    posted = bool(url) or "POSTED" in text.split("\n")[3] if len(text.split("\n")) > 3 else bool(url)

    posts.append({
        "series": 1,
        "day": day,
        "date": date,
        "title": TITLES[day],
        "copy": copy,
        "linkedin_url": url,
        "visual_default": f"post-{day:02d}.jpg",
        "visual_note": visual_note,
        "posted": posted,
        "draft_file": matches[0].name,
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(posts, indent=2, ensure_ascii=False))
for p in posts:
    print(f"Day {p['day']:2d} {p['date']}  url={'yes' if p['linkedin_url'] else 'NO '}  "
          f"copy={len(p['copy'])} chars  posted={p['posted']}  {p['title']}")
print(f"\nwrote {OUT}")
