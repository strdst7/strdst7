#!/usr/bin/env python3
"""
STELLAR PROGRESS LOG — generator
Renders an animated SVG star-chart stats card from GitHub contribution data.

Progression system
------------------
  level  = floor(sqrt(total contributions, rolling 365 days))
  XP to next level = (level+1)^2 - level^2  (RPG pacing: each level costs more)

  Spectral class (real stellar classification, M -> O) is derived from level.
  Class B begins at LV 32 -- the class of Beta Orionis (Rigel, B8Ia),
  a blue supergiant ~850 light-years away in Orion.

Data modes
----------
  1. GraphQL (exact, includes today)  -- used when GITHUB_TOKEN is set (Actions)
  2. Public contribution graph scrape -- zero-auth fallback, works anywhere

Usage
-----
  GH_USERNAME=strdst7 python3 stellar_stats.py
  (optionally with GITHUB_TOKEN in env for exact GraphQL data)

Output: stellar-progress.svg (written next to this script)
"""

import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from string import Template

USERNAME = os.environ.get("GH_USERNAME", "strdst7")
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stellar-progress.svg")

# Malaysia time for the "synced" stamp
MYT = timezone(timedelta(hours=8))

# ---------------------------------------------------------------- palette --
VOID = "#0A0908"      # deep space  (matches aimirah.com theme color)
PANEL = "#0F0D0A"
EDGE = "#2A2117"
RIGEL = "#A6C8FF"     # blue-white supergiant
CYAN = "#E9C46A"    # gold accent
DUST = "#C9932F"    # deep amber      # violet stardust
FAINT = "#8A8272"
STARLIGHT = "#F5EDD8"

# spectral classes: (min_level, letter, title, color)
CLASSES = [
    (0,  "M", "RED DWARF",      "#FF9E80"),
    (8,  "K", "ORANGE DWARF",   "#FFC46B"),
    (14, "G", "MAIN SEQUENCE",  "#FFE9A8"),
    (20, "F", "YELLOW-WHITE",   "#FFF6D6"),
    (26, "A", "WHITE STAR",     "#EAF2FF"),
    (32, "B", "RIGEL TIER",     "#A6C8FF"),
    (40, "O", "HYPERGIANT",     "#9BB5FF"),
]


# ------------------------------------------------------------- data layer --
def _http(url, headers=None, payload=None):
    req = urllib.request.Request(url, headers=headers or {})
    if payload is not None:
        req.data = json.dumps(payload).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def fetch_days_graphql():
    """Exact daily counts (includes today) via the GraphQL API."""
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }"""
    body = _http(
        "https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {TOKEN}",
                 "User-Agent": "stellar-progress-card"},
        payload={"query": query, "variables": {"login": USERNAME}},
    )
    cal = json.loads(body)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"])
            for w in cal["weeks"] for d in w["contributionDays"]]
    return sorted(days), "GRAPHQL API"


def fetch_days_public():
    """Zero-auth fallback: parse the public contribution graph HTML."""
    html = _http(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (stellar-progress-card)"},
    )
    tds = re.findall(r'<td[^>]*data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="([^"]+)"', html)
    if not tds:  # attribute order can flip
        pairs = re.findall(r'<td[^>]*id="([^"]+)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"', html)
        tds = [(d, i) for i, d in pairs]
    tips = dict(re.findall(
        r'<tool-tip[^>]*for="([^"]+)"[^>]*>\s*(No|\d+) contribution', html))
    days = [(d, 0 if tips.get(i, "No") == "No" else int(tips[i])) for d, i in tds]
    if not days:
        raise RuntimeError("could not parse public contribution graph")
    return sorted(days), "PUBLIC CONTRIB GRAPH"


def gather():
    if TOKEN:
        try:
            return fetch_days_graphql()
        except Exception as e:  # fall back rather than fail the workflow
            print(f"[warn] GraphQL failed ({e}); falling back to public graph",
                  file=sys.stderr)
    return fetch_days_public()


# ------------------------------------------------------------- game logic --
def spectral(level):
    cur = CLASSES[0]
    nxt = None
    for c in CLASSES:
        if level >= c[0]:
            cur = c
        elif nxt is None:
            nxt = c
    return cur, nxt


def compute(days):
    total = sum(c for _, c in days)
    level = math.isqrt(total)
    floor_xp, ceil_xp = level * level, (level + 1) ** 2
    into, need = total - floor_xp, ceil_xp - floor_xp

    best_date, best = max(days, key=lambda x: x[1])
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    vals = [c for _, c in days]
    i = len(vals) - 1
    if vals and vals[i] == 0:
        i -= 1  # an empty "today" doesn't break the streak yet
    current = 0
    while i >= 0 and vals[i] > 0:
        current += 1
        i -= 1

    cls, nxt = spectral(level)
    return {
        "total": total, "level": level, "into": into, "need": need,
        "next_at": ceil_xp, "best": best, "best_date": best_date,
        "longest": longest, "current": current, "cls": cls, "nxt": nxt,
    }


# ---------------------------------------------------------------- render --
SVG = Template(r"""<svg width="840" height="252" viewBox="0 0 840 252"
     xmlns="http://www.w3.org/2000/svg" font-family="'Courier New',Courier,monospace">
  <title>Stellar Progress Log for $username</title>
  <defs>
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="$dust"/>
      <stop offset="0.55" stop-color="$clscolor"/>
      <stop offset="1" stop-color="$cyan"/>
    </linearGradient>
    <radialGradient id="corona" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="$clscolor" stop-opacity="0.85"/>
      <stop offset="1" stop-color="$clscolor" stop-opacity="0"/>
    </radialGradient>
    <style>
      .lbl  { fill:$faint; font-size:10.5px; letter-spacing:1px; }
      .val  { fill:$starlight; font-size:21px; font-weight:bold; }
      .sub  { fill:$faint; font-size:10px; }
      .pulse { animation: pulse 2.6s ease-in-out infinite; }
      .tw1 { animation: tw 3.1s ease-in-out infinite; }
      .tw2 { animation: tw 4.3s ease-in-out infinite 0.9s; }
      .tw3 { animation: tw 5.2s ease-in-out infinite 1.7s; }
      @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:.55; } }
      @keyframes tw    { 0%,100% { opacity:.9; } 50% { opacity:.25; } }
    </style>
  </defs>

  <!-- panel -->
  <rect width="840" height="252" rx="14" fill="$void"/>
  <rect x="1.5" y="1.5" width="837" height="249" rx="13"
        fill="$panel" stroke="$edge" stroke-width="1.5"/>

  <!-- ambient stardust (starts visible; twinkle is enhancement only) -->
  <g fill="$starlight">
    <circle class="tw1" cx="330" cy="30"  r="1.4"/>
    <circle class="tw2" cx="512" cy="52"  r="1.1"/>
    <circle class="tw3" cx="782" cy="34"  r="1.5"/>
    <circle class="tw2" cx="694" cy="118" r="1.0"/>
    <circle class="tw1" cx="806" cy="206" r="1.2"/>
    <circle class="tw3" cx="418" cy="226" r="1.0"/>
    <path class="tw2" d="M566 200 l2.4 5 5 2.4 -5 2.4 -2.4 5 -2.4 -5 -5 -2.4 5 -2.4z" fill="$dust"/>
  </g>

  <!-- header -->
  <text x="26" y="34" fill="$dust" font-size="13" letter-spacing="3">// STELLAR PROGRESS LOG</text>
  <circle cx="736" cy="30" r="3.5" fill="$cyan" class="pulse"/>
  <text x="746" y="34" font-size="11" letter-spacing="1.5" fill="$cyan">$sync_state</text>
  <line x1="26" y1="46" x2="814" y2="46" stroke="$edge" stroke-width="1"/>

  <!-- class star + level block -->
  <circle cx="72" cy="98" r="34" fill="url(#corona)" class="pulse"/>
  <circle cx="72" cy="98" r="15" fill="$clscolor"/>
  <circle cx="72" cy="98" r="15" fill="none" stroke="$starlight" stroke-opacity="0.6" stroke-width="1"/>
  <text x="72" y="103" text-anchor="middle" font-size="14" font-weight="bold" fill="$void">$clsletter</text>

  <text x="122" y="88" class="lbl">SPECTRAL CLASS $clsletter &#183; $clstitle</text>
  <text x="122" y="114" fill="$starlight" font-size="28" font-weight="bold" letter-spacing="1">LV $level</text>
  <text x="236" y="114" class="sub">$total_fmt XP &#183; rolling 365d</text>

  <!-- fusion bar -->
  <text x="122" y="140" class="lbl">FUSION PROGRESS &#8594; LV $next_level</text>
  <rect x="122" y="148" width="420" height="12" rx="6" fill="$void" stroke="$edge"/>
  <rect x="122" y="148" height="12" rx="6" fill="url(#bar)" width="$bar_w">
    <animate attributeName="width" from="0" to="$bar_w" dur="1.2s" fill="freeze"/>
  </rect>
  <text x="542" y="140" text-anchor="end" class="sub">$into / $need &#183; next at $next_at</text>

  <!-- spectral ladder -->
  <text x="122" y="186" class="lbl">SPECTRAL LADDER</text>
  $ladder
  <text x="122" y="222" class="sub">$ladder_note</text>

  <!-- right stat column -->
  <line x1="600" y1="62" x2="600" y2="230" stroke="$edge" stroke-width="1"/>
  <g>
    <text x="614" y="84"  class="lbl">CURRENT ORBIT</text>
    <text x="614" y="106" class="val">$current d</text>
    <text x="614" y="119" class="sub">day streak</text>

    <text x="614" y="146" class="lbl">LONGEST BURN</text>
    <text x="614" y="168" class="val">$longest d</text>
    <text x="614" y="181" class="sub">best in 365d</text>

    <text x="722" y="84"  class="lbl">SUPERNOVA</text>
    <text x="722" y="106" class="val">$best</text>
    <text x="722" y="119" class="sub">on $best_date</text>

    <text x="722" y="146" class="lbl">NEXT CLASS</text>
    <text x="722" y="168" class="val">$nxt_letter</text>
    <text x="722" y="181" class="sub">$nxt_note</text>
  </g>

  <!-- footer -->
  <line x1="26" y1="232" x2="814" y2="232" stroke="$edge" stroke-width="1"/>
  <text x="26" y="245" class="sub">SYNCED $stamp &#183; SOURCE: $source</text>
  <text x="814" y="245" text-anchor="end" class="sub" fill="$rigel">&#946; ORI &#183; RIGEL &#183; B8Ia &#183; 850 LY</text>
</svg>
""")


def ladder_svg(level):
    """M K G F A B O row; current class framed and glowing."""
    x, y, out = 122, 196, []
    for min_lv, letter, _, color in CLASSES:
        active = spectral(level)[0][1] == letter
        if active:
            out.append(f'<rect x="{x-9}" y="{y-13}" width="28" height="21" rx="5" '
                       f'fill="{color}" fill-opacity="0.18" stroke="{color}"/>')
        fill = color if active else FAINT
        weight = ' font-weight="bold"' if active else ""
        out.append(f'<text x="{x+4}" y="{y}" text-anchor="middle" font-size="13"'
                   f'{weight} fill="{fill}">{letter}</text>')
        x += 40
    return "\n  ".join(out)


def render(s):
    cls, nxt = s["cls"], s["nxt"]
    bar_w = round(420 * s["into"] / s["need"], 1) if s["need"] else 420
    if nxt:
        nxt_letter = nxt[1]
        nxt_note = f"LV {nxt[0]} &#183; {nxt[0]**2} XP"
        if cls[1] == "B":
            ladder_note = f"CLASS B REACHED &#8212; RIGEL TIER &#183; class {nxt[1]} at LV {nxt[0]}"
        else:
            ladder_note = f"climbing toward class B (Rigel, B8Ia) at LV 32"
    else:
        nxt_letter, nxt_note = "&#8734;", "beyond the chart"
        ladder_note = "CLASS O &#8212; the chart ends here. Keep shining."

    now = datetime.now(MYT)
    return SVG.substitute(
        username=USERNAME,
        void=VOID, panel=PANEL, edge=EDGE, rigel=RIGEL, cyan=CYAN,
        dust=DUST, faint=FAINT, starlight=STARLIGHT,
        clscolor=cls[3], clsletter=cls[1], clstitle=cls[2],
        level=s["level"], next_level=s["level"] + 1,
        total_fmt=f'{s["total"]:,}',
        into=s["into"], need=s["need"], next_at=f'{s["next_at"]:,}',
        bar_w=bar_w,
        ladder=ladder_svg(s["level"]), ladder_note=ladder_note,
        current=s["current"], longest=s["longest"],
        best=s["best"], best_date=__import__("datetime").datetime.strptime(s["best_date"], "%Y-%m-%d").strftime("%d %b").upper(),
        nxt_letter=nxt_letter, nxt_note=nxt_note,
        sync_state="TRACKING",
        stamp=now.strftime("%d %b %Y").upper(),
        source=s["source"],
    )


def main():
    days, source = gather()
    stats = compute(days)
    stats["source"] = source
    svg = render(stats)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"[ok] {OUT}")
    print(f"     LV {stats['level']} &middot; class {stats['cls'][1]} ({stats['cls'][2]})"
          f" &middot; {stats['total']:,} XP &middot; source: {source}")


if __name__ == "__main__":
    main()
