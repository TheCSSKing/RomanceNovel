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
- [ ] Minimal review site (name + series list) — FOR USER REVIEW FIRST
- [ ] User approves
- [ ] Generate cover images via OpenAI Images API (gpt-image-2)
- [ ] Full bookstore site (browse + "purchase")

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

Total: 12 series, 44 books.

## Log
- Init: empty repo, created notes + data model.
- Review round 1: renamed publisher to **Ravish House**; replaced series 5, 6, 8, 9, 10
  (zoning, dog grooming, falconry, typewriter repair, bowling) with values/lifestyle/
  common-theme/fetish themes per feedback.
