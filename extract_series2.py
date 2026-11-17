#!/usr/bin/env python3
"""Extract the Series 2 slate from the slate doc's plain text (/tmp/series2-slate.txt).

Each post block: "Post N — <Wday> <Mon> <D> — <Title>", then Beat:, Screenshot(s):,
Copy: lines until the next Post heading or "Production notes".
Writes data/series2.json with status "slate" (nothing posts without Dave's green light).
"""
import json
import re
from pathlib import Path

SRC = Path("/tmp/series2-slate.txt")
OUT = Path.home() / "workspace" / "projects" / "teaser-bank" / "data" / "series2.json"

text = SRC.read_text()
# Split on post headings.
parts = re.split(r"\nPost (\d+) — \w+ Nov (\d+) — ([^\n]+)\n", text)
# parts: [prelude, n, day, title, body, n, day, title, body, ...]
posts = []
for i in range(1, len(parts), 4):
    n, day, title, body = int(parts[i]), int(parts[i + 1]), parts[i + 2].strip(), parts[i + 3]
    beat = re.search(r"Beat: (.*?)\nScreenshot", body, re.S).group(1).strip()
    shot = re.search(r"Screenshot\(s\): (.*?)\nCopy:", body, re.S).group(1).strip()
    copy = re.search(r"Copy:\n(.*?)(?:\nProduction notes|\Z)", body, re.S).group(1).strip()
    posts.append({
        "series": 2,
        "day": n,
        "date": f"2026-11-{day:02d}",
        "date_label": f"Proposed — Tue Nov {day}, 2026" if False else f"Proposed for Nov {day}, 2026",
        "title": title,
        "beat": " ".join(beat.split()),
        "screenshot_plan": " ".join(shot.split()),
        "copy": copy,
        "linkedin_url": None,
        "posted": False,
        "status": "slate",
    })

assert len(posts) == 14, f"expected 14 posts, got {len(posts)}"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(posts, indent=2, ensure_ascii=False))
for p in posts:
    print(f"Post {p['day']:2d} {p['date']}  copy={len(p['copy'])} chars  {p['title']}")
print(f"\nwrote {OUT}")
