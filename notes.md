# Ravish House — Build Notes

Parody romance publishing house. Static site served from `index.html`.

## Concept
- **Publisher:** Ravish House (renamed from "Swoon & Sons" per review — punchier)
- **Tagline:** Love, in the unlikeliest places.
- Each **series** has one ultra-specific theme, a single author, and N books.
- Each **book** has a title, short description, price, and (eventually) a generated cover.

## Plan / Progress
- [x] Scaffold repo on branch `claude/parody-romance-bookstore-43uvbo`
- [x] Author series + book data (`data.json`)
- [x] Minimal review site (name + series list) — FOR USER REVIEW FIRST
- [x] User approves
- [x] Generate cover images via OpenAI Images API (gpt-image-2)
- [x] Full bookstore site (browse + "purchase")

## Series (12)
1. **Actuarial romance** — "Love by the Numbers" — Prudence Everdeath (4)
2. **Submarine romance** — "Fathoms of the Heart" — Marina Deeps (3)
3. **Competitive cheese-making romance** — "The Rind & the Reckless" — Colby Jack Sterling (5)
4. **Antarctic research-station romance** — "Below Zero, Above Reason" — Dr. Ptarmigan Frost (3)
5. **Aggressively zero-waste romance** — "Leave No Trace" — Fern Compostella (3)
6. **Nihilist romance** — "Nothing Matters" — Søren Blank (4)
7. **Volcanology romance** — "Magma Rising" — Ignatia Cinders (4)
8. **Doomsday-prepper romance** — "Bunker Down" — Dakota Ridge (4)
9. **Lifeguard (per body of water) romance** — "Between the Flags" — Sandy Shores (4)
10. **Punctuality-fetish romance** — "Not a Minute Late" — Dot Sharpe (3)
11. **Beekeeping romance** — "The Sweetest Sting" — Melissa Comb (3)
12. **Forensic accounting romance** — "Cooking the Books" — Miles Ledger (3)

Total: 12 series, 43 books.

## Log
- Init: empty repo, created notes + data model.
- Review round 1: renamed publisher to **Ravish House**; replaced series 5, 6, 8, 9, 10
  (zoning, dog grooming, falconry, typewriter repair, bowling) with values/lifestyle/
  common-theme/fetish themes per feedback.
- Built full bookstore: `scripts/build_site.py` generates `index.html` from `data.json`
  (catalog inlined so it works from file:// too). Features: series grid, series pages
  with author bios, book modals, add-to-cart drawer w/ localStorage, fake checkout.
  Covers: real PNGs from `covers/<id>-<n>.png` when present, else themed CSS placeholder.

## Cover image generation — DONE
- `scripts/gen_covers.py` (gpt-image-2, size 1024x1536, quality=medium, art-only
  prompts w/ per-series art direction; title/author overlaid by the site).
- Egress to `api.openai.com` is now permitted; ran the generator with the
  `OPENAI_API_KEY` environment variable and generated all **43 covers** into
  `covers/<id>-<n>.png`. Each was reviewed individually before being committed.
- Prompt hardening: added a tasteful/PG guard to the base style (one book tripped
  the API's output-moderation filter with the original prompt), and made the
  generator retry on HTTP 400 instead of aborting the whole run (only 401/403 stop it).
- The site auto-uses the real PNGs; the themed CSS placeholder remains as a fallback.
