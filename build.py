#!/usr/bin/env python3
"""Build the Teaser Bank package site from data/series1.json + data/series2.json.

Design: the campaign's established hand (Art Director, teaser-pages-direction):
ink #14161b / amber #e8a33d, Playfair Display headlines with italic amber tails,
Libre Franklin body, film grain, light scheme #f6f1e7. Every page carries the
visitor beacon (data-site="teaser-bank"). Series 1 pages reproduce the posts as
published (verbatim copy, the image that ran, live LinkedIn link where recorded);
Series 2 pages present the slate, labeled as such.
"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ASSETS_SRC_S1 = Path.home() / "workspace" / "art-director-buddy" / "teaser-bank-visuals"
DAY14_DIR = Path.home() / "workspace" / "linkedin-day14-review"
BEACON = '<script async src="https://visitor-counter.dave-5d7.workers.dev/beacon.js" data-site="teaser-bank"></script>'

CSS = """
:root{
  --bg:#14161b; --bg-deep:#0e0f12; --ink:#ece7da; --ink-soft:#b9b3a4; --ink-faint:#7d7768;
  --accent:#e8a33d; --hairline:rgba(236,231,218,.16); --hairline-soft:rgba(236,231,218,.08);
}
@media (prefers-color-scheme: light){
  :root{ --bg:#f6f1e7; --bg-deep:#efe8d8; --ink:#1c1a16; --ink-soft:#55503f; --ink-faint:#8a8471;
    --accent:#9a6d1d; --hairline:rgba(28,26,22,.18); --hairline-soft:rgba(28,26,22,.09); }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Libre Franklin",system-ui,sans-serif;font-weight:300;line-height:1.7;
  font-size:clamp(1rem,2.3vw,1.13rem)}
body::after{content:"";position:fixed;inset:0;pointer-events:none;opacity:.05;z-index:50;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E")}
@media (prefers-color-scheme: light){ body::after{opacity:.035} }
.wrap{max-width:880px;margin:0 auto;padding:0 22px}
.masthead{display:flex;justify-content:space-between;align-items:baseline;gap:16px;
  padding:18px 0 14px;border-bottom:1px solid var(--hairline);
  font-family:"Libre Franklin",sans-serif;font-weight:600;font-size:11px;
  letter-spacing:.3em;text-transform:uppercase}
.masthead .r{letter-spacing:.26em;color:var(--ink-faint);text-align:right}
.masthead .r b{color:var(--accent);font-weight:600}
.masthead a{color:inherit;text-decoration:none}
h1,h2{font-family:"Playfair Display",Georgia,serif;font-weight:500;line-height:1.08}
h1{font-size:clamp(2.6rem,8vw,4.6rem);letter-spacing:-.01em;margin:.35em 0 .3em}
h2{font-size:clamp(1.9rem,5.4vw,3.1rem);line-height:1.12;margin:1.4em 0 .4em}
h1 em,h2 em{font-style:italic;color:var(--accent)}
.kicker{font-family:"Libre Franklin",sans-serif;font-weight:600;font-size:11px;
  letter-spacing:.26em;text-transform:uppercase;color:var(--ink-faint);margin-top:34px}
.kicker b{color:var(--accent);font-weight:600}
p{color:var(--ink-soft);max-width:62ch}
p strong,li strong{color:var(--ink);font-weight:500}
.lede{font-size:clamp(1.08rem,2.6vw,1.28rem);color:var(--ink-soft)}
.rule{width:56px;height:2px;background:var(--accent);margin:34px 0 0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin:26px 0 8px}
.card{display:block;text-decoration:none;border:1px solid var(--hairline);color:var(--ink);
  background:transparent;transition:border-color .25s}
.card:hover{border-color:var(--accent)}
.card img{width:100%;aspect-ratio:1200/627;object-fit:cover;display:block}
.card .pad{padding:14px 16px 16px}
.card .n{font-family:"Libre Franklin",sans-serif;font-weight:600;font-size:11px;
  letter-spacing:.26em;text-transform:uppercase;color:var(--accent)}
.card .t{font-family:"Playfair Display",Georgia,serif;font-size:1.28rem;line-height:1.2;margin:6px 0 4px}
.card .d{font-size:.86rem;color:var(--ink-faint)}
.card.type .pad{padding-top:18px}
.card .beat{font-size:.92rem;color:var(--ink-soft);margin-top:6px;line-height:1.55}
figure{margin:26px 0}
figure img{width:100%;display:block;cursor:zoom-in;border:1px solid var(--hairline-soft)}
figcaption{font-size:.82rem;color:var(--ink-faint);margin-top:8px}
.copy p{color:var(--ink-soft)}
.btn{display:inline-block;margin:10px 10px 0 0;padding:11px 20px;border:1px solid var(--accent);
  color:var(--accent);text-decoration:none;font-family:"Libre Franklin",sans-serif;
  font-weight:600;font-size:.82rem;letter-spacing:.14em;text-transform:uppercase}
.btn:hover{background:var(--accent);color:var(--bg)}
.note{border-left:2px solid var(--accent);padding:4px 0 4px 16px;margin:26px 0;color:var(--ink-soft);font-size:.95rem}
.pn{display:flex;justify-content:space-between;gap:14px;margin:44px 0 6px;
  border-top:1px solid var(--hairline);padding-top:18px;font-size:.92rem}
.pn a{color:var(--accent);text-decoration:none}
.pn .off{color:var(--ink-faint)}
.colophon{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  border-top:1px solid var(--hairline);margin-top:40px;padding:16px 0 34px;
  font-size:.85rem;color:var(--ink-faint)}
.vision{font-family:"Playfair Display",Georgia,serif;font-style:italic;
  font-size:clamp(1.3rem,3.6vw,1.8rem);color:var(--ink);margin:44px 0 0}
#lightbox{position:fixed;inset:0;background:rgba(8,9,11,.94);display:none;z-index:100;
  align-items:center;justify-content:center;flex-direction:column}
#lightbox.open{display:flex}
#lightbox img{max-width:94vw;max-height:84vh;object-fit:contain}
#lightbox .bar{display:flex;gap:22px;align-items:center;margin-top:14px;color:#ece7da;
  font-family:"Libre Franklin",sans-serif;font-size:.85rem;letter-spacing:.12em}
#lightbox button{background:none;border:1px solid rgba(236,231,218,.4);color:#ece7da;
  font-size:1rem;padding:6px 14px;cursor:pointer}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;1,500'
         '&family=Libre+Franklin:wght@300;500;600&display=swap" rel="stylesheet">')

LIGHTBOX = """
<div id="lightbox" role="dialog" aria-label="Photo viewer">
  <img id="lb-img" alt="">
  <div class="bar"><button id="lb-prev" aria-label="Previous photo">&#8249;</button>
  <span id="lb-count"></span><button id="lb-next" aria-label="Next photo">&#8250;</button>
  <button id="lb-close" aria-label="Close">&#10005;</button></div>
</div>
<script>
(function(){
  var imgs=[].slice.call(document.querySelectorAll('figure img'));
  if(!imgs.length) return;
  var lb=document.getElementById('lightbox'), im=document.getElementById('lb-img'),
      ct=document.getElementById('lb-count'), cur=0;
  function show(i){ cur=(i+imgs.length)%imgs.length; im.src=imgs[cur].src;
    ct.textContent=(cur+1)+' / '+imgs.length;
    document.getElementById('lb-prev').style.display=imgs.length>1?'':'none';
    document.getElementById('lb-next').style.display=imgs.length>1?'':'none'; }
  imgs.forEach(function(el,i){ el.addEventListener('click',function(){ show(i); lb.classList.add('open'); }); });
  document.getElementById('lb-close').addEventListener('click',function(){ lb.classList.remove('open'); });
  document.getElementById('lb-prev').addEventListener('click',function(){ show(cur-1); });
  document.getElementById('lb-next').addEventListener('click',function(){ show(cur+1); });
  lb.addEventListener('click',function(e){ if(e.target===lb) lb.classList.remove('open'); });
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('open')) return;
    if(e.key==='Escape') lb.classList.remove('open');
    if(e.key==='ArrowLeft') show(cur-1);
    if(e.key==='ArrowRight') show(cur+1); });
})();
</script>
"""


def esc(s):
    return html.escape(s, quote=True)


def paras(copy):
    return "\n".join(f"<p>{esc(p.strip())}</p>" for p in copy.split("\n\n") if p.strip())


def fmt_date(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%a %b %-d, %Y")


def page(title, kicker, body, prefix=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — The Teaser Bank</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="masthead"><a href="{prefix}index.html">The Buddy System</a><span class="r">The Teaser Bank · <b>LinkedIn 2026</b></span></header>
<p class="kicker">{kicker}</p>
{body}
<p class="vision">The vision took 40 years. We&rsquo;re building it now.</p>
<footer class="colophon"><span>The Buddy System · The Teaser Bank</span><span>Stop managing software. Start directing staff.</span></footer>
</div>
{LIGHTBOX}
{BEACON}
</body>
</html>
"""


def main():
    s1 = json.loads((DATA / "series1.json").read_text())
    s2 = json.loads((DATA / "series2.json").read_text())
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)

    # Copy Series 1 visuals; Day 14 ran with Dave's own screenshots instead of post-14.jpg.
    for p in s1:
        if p["day"] == 14:
            shutil.copy(DAY14_DIR / "day14-hero-games.jpg", assets / "day14-hero.jpg")
            shutil.copy(DAY14_DIR / "day14-alt-maxheadroom.jpg", assets / "day14-alt.jpg")
            p["images"] = [("assets/day14-hero.jpg", "Money Buddy at home — Dave's own screenshot, wearing the Pac-Man background he set himself. The finale's hero image."),
                            ("assets/day14-alt.jpg", "The same Money Buddy home screen in its Max Headroom look — the customization point, second angle.")]
        else:
            src = ASSETS_SRC_S1 / p["visual_default"]
            shutil.copy(src, assets / p["visual_default"])
            p["images"] = [(f"assets/{p['visual_default']}", f"The image that ran with Day {p['day']} on LinkedIn.")]

    # ---- Series 1 pages
    s1dir = ROOT / "series-1"
    s1dir.mkdir(exist_ok=True)
    for i, p in enumerate(s1):
        figs = "\n".join(
            f'<figure><img src="../{src}" alt="{esc(caption)}"><figcaption>{esc(caption)}</figcaption></figure>'
            for src, caption in p["images"])
        link = (f'<a class="btn" href="{p["linkedin_url"]}">Read it on LinkedIn</a>'
                if p["linkedin_url"] else "")
        prev = (f'<a href="day-{s1[i-1]["day"]:02d}.html">&larr; Day {s1[i-1]["day"]} — {esc(s1[i-1]["title"])}</a>'
                if i > 0 else '<span class="off">Day 1 — the start</span>')
        nxt = (f'<a href="day-{s1[i+1]["day"]:02d}.html">Day {s1[i+1]["day"]} — {esc(s1[i+1]["title"])} &rarr;</a>'
               if i < len(s1) - 1 else '<a href="../series-2/post-01.html">Into Series 2 &rarr;</a>')
        body = f"""<h1>{esc(p['title'])}</h1>
<p class="lede">Series 1 · Day {p['day']} of 14 · Posted {fmt_date(p['date'])} on LinkedIn.</p>
{figs}
<div class="copy">{paras(p['copy'])}</div>
{link}
<nav class="pn">{prev}{nxt}</nav>"""
        (s1dir / f"day-{p['day']:02d}.html").write_text(
            page(p["title"], f"Series 1 · <b>Day {p['day']} of 14</b>", body, prefix="../"))

    # ---- Series 2 pages
    s2dir = ROOT / "series-2"
    s2dir.mkdir(exist_ok=True)
    for i, p in enumerate(s2):
        prev = (f'<a href="post-{s2[i-1]["day"]:02d}.html">&larr; Post {s2[i-1]["day"]} — {esc(s2[i-1]["title"])}</a>'
                if i > 0 else '<a href="../series-1/day-14.html">&larr; Series 1 finale</a>')
        nxt = (f'<a href="post-{s2[i+1]["day"]:02d}.html">Post {s2[i+1]["day"]} — {esc(s2[i+1]["title"])} &rarr;</a>'
               if i < len(s2) - 1 else '<span class="off">The finale — the slate ends here</span>')
        body = f"""<h1>{esc(p['title'])}</h1>
<p class="lede">Series 2 · Post {p['day']} of 14 · {esc(p['date_label'])}.</p>
<div class="note"><strong>The beat:</strong> {esc(p['beat'])}</div>
<div class="copy">{paras(p['copy'])}</div>
<div class="note"><strong>Production note:</strong> {esc(p['screenshot_plan'])}</div>
<p>This page presents the draft from the Series 2 slate, presented to Dave on Nov 2, 2026. Per the campaign rule, nothing posts until he green-lights the series.</p>
<nav class="pn">{prev}{nxt}</nav>"""
        (s2dir / f"post-{p['day']:02d}.html").write_text(
            page(p["title"], f"Series 2 · <b>Post {p['day']} of 14 — the slate</b>", body, prefix="../"))

    # ---- Index
    cards1 = "\n".join(
        f'<a class="card" href="series-1/day-{p["day"]:02d}.html">'
        f'<img src="{p["images"][0][0]}" alt="">'
        f'<span class="pad" style="display:block"><span class="n">Day {p["day"]}</span>'
        f'<span class="t" style="display:block">{esc(p["title"])}</span>'
        f'<span class="d">{fmt_date(p["date"])}</span></span></a>' for p in s1)
    cards2 = "\n".join(
        f'<a class="card type" href="series-2/post-{p["day"]:02d}.html">'
        f'<span class="pad"><span class="n">Post {p["day"]}</span>'
        f'<span class="t" style="display:block">{esc(p["title"])}</span>'
        f'<span class="d">{esc(p["date_label"])}</span>'
        f'<span class="beat" style="display:block">{esc(p["beat"])}</span></span></a>' for p in s2)
    body = f"""<h1>Fourteen posts, twice —<br><em>the whole campaign, kept.</em></h1>
<p class="lede">In the fall of 2026, Dave Dell'Aquila told the 40-year story of an idea on LinkedIn — one post a day, in two series. Feeds scroll away. This package keeps the campaign: every post as it ran, and the second series as it stands.</p>
<div class="rule"></div>
<h2>Series 1 — <em>one app.</em></h2>
<p>Oct 20 – Nov 2, 2026. The origin arc — a 1987 concept video, a 1993 Mac program called Rae Assist, its first user coming back — and then the present day: Money Buddy, the first buddy out the door, and a tip jar for a business model. All fourteen posts are live on LinkedIn; each page here carries the copy exactly as published, the image that ran with it, and the link to the post itself.</p>
<div class="cards">{cards1}</div>
<h2>Series 2 — <em>the whole staff.</em></h2>
<p>Series 1 was one app. Series 2 is the platform: the staff model, the dashboard, the briefings and the standup, two newspapers, an hourly chime, a joke vault — Money Buddy reframed as one desk among many. The slate was presented on Nov 2, 2026 with a proposed run of Nov 3–16; per the campaign rule, nothing posts until Dave green-lights the series. These pages present the slate as written — beat, draft copy, and the screenshot each post calls for.</p>
<div class="cards">{cards2}</div>"""
    (ROOT / "index.html").write_text(page("The Teaser Bank", "The Buddy System · <b>A LinkedIn campaign, collected</b>", body))

    print(f"built: index + {len(s1)} series-1 pages + {len(s2)} series-2 pages")


if __name__ == "__main__":
    main()
