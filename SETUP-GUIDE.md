# 🌌 Stardust Profile Kit — Setup Guide (for @strdst7)

Five files, five steps, ~10 minutes. Everything lives in the repo — no external card
services, nothing to rate-limit or break.

## What's in the kit

| File | What it is | Where it goes |
|---|---|---|
| `README.md` | The profile page | repo **root** |
| `stardust-banner.svg` | Animated Orion banner | repo **root** |
| `stellar-progress.svg` | Live stats star chart (pre-rendered with real data) | repo **root** |
| `constellation-loadout.svg` | Specializations + stack card | repo **root** |
| `stellar_stats.py` | The card generator (runs daily) | repo **root** |
| `stellar-stats.yml` | GitHub Actions workflow | `.github/workflows/` ⚠️ |

## Steps

**1 — Create the magic repo.**
New repository named exactly **`strdst7`** (same as the username), public.
GitHub will show a banner: *"You found a secret! strdst7/strdst7 is a special repository."*
Initialize it with a README (we'll replace it).

**2 — Upload the five root files.**
`Add file → Upload files` → drop in `README.md`, `stardust-banner.svg`,
`stellar-progress.svg`, `constellation-loadout.svg`, `stellar_stats.py` → commit to `main`.
The profile is already live at this point — the SVGs animate right on github.com/strdst7.

**3 — Allow the bot to commit.**
Repo → `Settings → Actions → General → Workflow permissions` →
select **Read and write permissions** → Save.

**4 — Add the workflow (⚠️ the one step people get wrong).**
The file must land in `.github/workflows/` — **with the leading dot**. Folders named
`github/workflows` (no dot) are silently ignored, and some upload paths strip the dot.
The foolproof way:

> Repo → **Actions** tab → *"set up a workflow yourself"* → GitHub pre-fills the
> correct `.github/workflows/main.yml` path → rename to `stellar-stats.yml` →
> paste in the contents of `stellar-stats.yml` → **Commit**.

**5 — First launch.**
`Actions` tab → **Update Stellar Progress** → `Run workflow`.
Green check in ~15 seconds, and the card commits itself with exact GraphQL stats.
After this it self-updates daily at **00:15 MYT** — a level-up appears within a day
of the contributions that earned it.

## How the progression works

- **XP** = contributions in the rolling last 365 days (all GitHub exposes cleanly)
- **Level** = ⌊√XP⌋ — so LV *N* costs *N²* XP, and the climb slows as you rise (intended RPG pacing)
- **Spectral class** follows real stellar classification, by level:

  | Class | Unlocks at | Title |
  |---|---|---|
  | M | LV 0 | Red Dwarf |
  | K | LV 8 | Orange Dwarf |
  | G | LV 14 | Main Sequence |
  | F | LV 20 | Yellow-White |
  | A | LV 26 | White Star |
  | **B** | **LV 32** | **Rigel Tier** ✦ *(β Orionis is B8Ia)* |
  | O | LV 40 | Hypergiant |

Current standing: **LV 32 · Class B · 1,045 XP** — Rigel tier, freshly reached.
Next milestone: Class **O** at LV 40 (1,600 XP).

## Easy customizations

- **Stack chips** on `constellation-loadout.svg` — each chip is a `<rect>` + `<text>` pair; swap labels/colors freely (palette: `#E9C46A` gold · `#C9932F` amber · `#F0D48A` pale gold · `#A6C8FF` reserved for Rigel).
- **Quote, mission text, table** — plain Markdown in `README.md`.
- **Class thresholds / colors** — the `CLASSES` list at the top of `stellar_stats.py`.
- **Sync time** — the `cron` line in the workflow (currently 16:15 UTC = 00:15 MYT).
