# Ravish House — Cover Art Requirements

This document is the single source of truth for what every book cover in the
Ravish House catalog must contain and how each series must look. It exists
because the first-pass covers were **art-only** (no title, author, series, or
tagline) and every series shared one identical painterly-couple aesthetic.

Covers are generated in a **single pass** with OpenAI Images (`gpt-image-2`,
portrait `1024×1536`, high quality). The prompt feeds the model both:

1. **Art direction** — a *per-series* aesthetic (medium, palette, mood), and
2. **Lettering direction** — a *per-series* typography style, plus the exact
   text to render (title, series line, author, tagline, publisher).

The image generator renders the artwork **and** all cover text together, so the
type is integrated into the design. The prompt states each string in quotes and
insists on exact spelling; every generated cover is reviewed for spelling and
legibility before it is committed.

---

## 1. Universal requirements (every cover)

Every finished cover MUST carry, with this visual hierarchy:

| Element | Rule |
| --- | --- |
| **Title** | The book's title. The **most prominent** text on the cover. Per-series display font. |
| **Series name** | The series title, rendered **smaller and less bold than the title** — a light, letter-spaced eyebrow. It labels the series without competing with the book title. |
| **Author** | The pen name, as a byline (e.g. `PRUDENCE EVERDEATH` or `by Prudence Everdeath`). Clearly subordinate to the title. |
| **Tagline** | One short hook line (≈4–10 words), set apart from the title (small italic or accent weight). See per-book tables in §3. |
| **Publisher** | `RAVISH HOUSE` as a small mark at the foot of the cover. |

Layout & legibility rules:

- **Format:** portrait, 2:3 aspect (`1024×1536`), matching the site's `.cover`.
- **Safe zones:** the artwork keeps calm, uncluttered space near the **top**
  (for the series eyebrow) and the **bottom** (for title / tagline / author),
  and keeps text clear of the couple's faces.
- **Legibility & spelling:** all text must be sharp, correctly spelled, and
  readable against the art. No stray, duplicate, or gibberish text anywhere.
- **Order top→bottom:** series eyebrow (top) · … artwork … · title, tagline,
  author, publisher (toward the bottom).

**Art tone (all covers) — over-the-top clinch.** These are gloriously melodramatic
bodice-ripper covers. Every cover shows a passionate couple **entangled in a
dramatic "clinch"** — bodies pressed together, all over each other — with **lots
of bare skin**: a shirtless, muscular hero and the heroine in a flowing
off-the-shoulder gown; bare shoulders, arms, and backs. Sensual, swooning, and
theatrical. Keep it in the **mainstream romance-genre register: steamy but not
explicit** — no nudity, no exposed genitals, no sex acts; a passionate embrace
only. (This taste line replaces the earlier "tender / fully clothed" rule.)

---

## 2. Per-series art direction

The central complaint was "they all look the same." Each series therefore gets
a **distinct medium, palette, mood, typographic identity, AND set** — a
different *scene and staging*, not just a different text layout on the same
"couple standing in a landscape" template. Vary the **clinch staging** too:
pinned against a bulkhead, lifted off the floor, tangled across a desk, dripping
on the sand — no two series should repeat the same pose or set. The couple is
always the focus (see the over-the-top clinch rule above); the *set* and *style*
are what make each series read as a different imprint.

### 1. Love by the Numbers — *Actuarial* — Prudence Everdeath
- **Aesthetic:** Clean modern corporate minimalism. Contemporary flat-leaning
  digital illustration, crisp geometry, generous negative space, subtle
  data-viz motifs (bell curves, grids, ledgers). Sophisticated fintech-brand
  romance.
- **Palette:** Cool teal + warm gold on cream; restrained.
- **Type:** Geometric sans. Title **Outfit Bold**; series eyebrow **Jura**
  (light, wide-tracked, uppercase); tagline **Work Sans Italic**; author Work Sans.
- **Text/accent:** deep teal ink, gold accent.

### 2. Fathoms of the Heart — *Submarine* — Marina Deeps
- **Aesthetic:** Moody cinematic realism inside a steel submarine — sonar glow,
  pipes, portholes, red emergency light. High contrast, dramatic rim-light.
- **Palette:** Deep navy + abyssal black with red-alert accents.
- **Type:** Industrial condensed. Title **Big Shoulders Bold** (uppercase);
  series **Jura**; tagline **IBM Plex Serif Italic**.
- **Text/accent:** cold white, red accent.

### 3. The Rind & the Reckless — *Competitive cheese-making* — Colby Jack Sterling
- **Aesthetic:** Warm rustic oil-painting; old-master still-life warmth,
  candlelit aging cave, textured wheels of cheese. Cozy, artisanal.
- **Palette:** Golden dairy tones, amber, hay.
- **Type:** Warm serif. Title **Young Serif**; series **Arsenal SC**; tagline
  **Lora Italic**.
- **Text/accent:** cream, deep amber accent.

### 4. Below Zero, Above Reason — *Antarctic research station* — Dr. Ptarmigan Frost
- **Aesthetic:** Icy, spare, technical. Cold light, aurora, endless snow with
  lots of empty sky; a lonely station. Minimal Nordic-poster restraint.
- **Palette:** Glacial blue/teal + aurora green; ice-white.
- **Type:** Thin geometric sans, wide tracking. Title **Jura** (uppercase,
  spaced); series **Jura Light**; tagline **Instrument Serif Italic**.
- **Text/accent:** ice white, aurora-teal accent.

### 5. Leave No Trace — *Aggressively zero-waste* — Fern Compostella
- **Aesthetic:** Soft eco watercolor / botanical illustration; hand-made
  textures, sun-dappled homestead, mason jars, compost, thriving greens.
  Cottagecore/Kinfolk warmth.
- **Palette:** Earthy greens + warm cream, sustainable naturals.
- **Type:** Outdoorsy + hand. Title **National Park Bold**; series National
  Park; tagline **Nothing You Could Do** (handwritten script).
- **Text/accent:** deep forest green on cream.

### 6. Nothing Matters — *Nihilist* — Søren Blank
- **Aesthetic:** Stark existential minimalism. A vast indifferent cosmic void,
  tiny figures, enormous empty space. Reads like a philosophy monograph.
- **Palette:** Muted grays, deep violet-black, a single bare bulb of warmth.
- **Type:** Austere high-contrast. Title **Italiana**; series **Jura Light**;
  tagline **Crimson Pro Italic**.
- **Text/accent:** pale gray, faint violet accent.

### 7. Magma Rising — *Volcanology* — Ignatia Cinders
- **Aesthetic:** Explosive high-contrast digital painting; fiery silhouettes
  against eruption, lava rivers, ash, heat-shimmer. Blockbuster-poster energy.
- **Palette:** Molten orange/red on near-black.
- **Type:** Massive bold display, all caps. Title **Erica One**; series **Big
  Shoulders**; tagline **Big Shoulders** (small).
- **Text/accent:** molten white/orange.

### 8. Bunker Down — *Doomsday-prepper* — Dakota Ridge
- **Aesthetic:** Gritty survivalist realism; bunker, blast door, canned goods,
  gas masks, lantern light. Worn, utilitarian, tactical.
- **Palette:** Desaturated amber/olive, crate-stencil browns.
- **Type:** Military/techy stencil. Title **Tektur** (uppercase); series
  **Red Hat Mono**; tagline Red Hat Mono.
- **Text/accent:** amber on olive-black.

### 9. Between the Flags — *Lifeguard* — Sandy Shores
- **Aesthetic:** Bright retro-80s pop; super-saturated, sun-blasted, glossy
  "Baywatch" nostalgia, airbrush/halftone energy, water everywhere.
- **Palette:** Lifeguard red + yellow + pool aqua, high saturation.
- **Type:** Bold rounded retro. Title **Erica One**; series **Smooch Sans**;
  tagline Smooch Sans.
- **Text/accent:** white with red keyline.

### 10. Not a Minute Late — *Punctuality* — Dot Sharpe
- **Aesthetic:** Elegant Art-Deco / vintage railway-poster; brass + deep navy,
  symmetry, sunburst geometry, monumental clocks and pocket watches. 1920s luxe.
- **Palette:** Brass gold on deep navy.
- **Type:** Deco geometric. Title **Poiret One** (wide caps); series **Italiana**;
  tagline **Italiana**.
- **Text/accent:** brass gold on navy.

### 11. The Sweetest Sting — *Beekeeping* — Melissa Comb
- **Aesthetic:** Sun-drenched pastoral, warm and whimsical; golden apiary,
  honeycomb, drifting bees, wildflowers, dappled summer light. Painterly-soft.
- **Palette:** Honey gold + meadow green + cream.
- **Type:** Whimsical script + warm serif. Title **Lora Bold**; series
  **Arsenal SC**; tagline **Nothing You Could Do** (script accent).
- **Text/accent:** cream/honey with deep-amber shadow.

### 12. Cooking the Books — *Forensic accounting* — Miles Ledger
- **Aesthetic:** Film noir. High-contrast chiaroscuro, deep shadow, venetian-
  blind light, a green banker's-lamp pool, towering case files. 1940s detective.
- **Palette:** Near-monochrome charcoal with a single green-lamp accent.
- **Type:** Typewriter mono (case-file feel). Title **JetBrains Mono Bold**;
  series **Red Hat Mono**; tagline Red Hat Mono Italic.
- **Text/accent:** off-white + banker's-lamp green.

---

## 3. Per-book titles & taglines

Taglines are the short hook set apart from the title on each cover. (These are
also stored on each book in `data.json` as `tagline`.)

### Love by the Numbers
| # | Title | Tagline |
|---|---|---|
| 1 | Present Value | Some risks are worth a whole life. |
| 2 | Confidence Interval | She was the outlier that broke his model. |
| 3 | The Deductible | Some things you can't insure against. |
| 4 | Terminal Dividend | A love thirty years in the making. |

### Fathoms of the Heart
| # | Title | Tagline |
|---|---|---|
| 1 | Silent Running | Two hundred meters down, no one can hear you sigh. |
| 2 | Crush Depth | The deeper they dive, the harder he falls. |
| 3 | Periscope Up | She surfaced for the one thing she couldn't leave below. |

### The Rind & the Reckless
| # | Title | Tagline |
|---|---|---|
| 1 | The Washed Rind | Love, like a good cheese, cannot be rushed. |
| 2 | Aged to Perfection | Eighteen months in the cave changes a man. |
| 3 | Say Cheese | Two rivals. One very small aging room. |
| 4 | Reserve | The blend everyone at the co-op saw coming. |
| 5 | The Whey Home | Snowed in, with only a wheel of Stilton and each other. |

### Below Zero, Above Reason
| # | Title | Tagline |
|---|---|---|
| 1 | The Long Night | When the sun sets for the winter, something ignites. |
| 2 | Core Sample | Two miles of ancient ice. One buried secret. |
| 3 | Windchill | The plane has landed. The choice has not. |

### Leave No Trace
| # | Title | Tagline |
|---|---|---|
| 1 | Reduce | A love she could not recycle away. |
| 2 | Reuse | Some hearts are too good to throw out. |
| 3 | Recycle | The greenest thing is never giving up. |

### Nothing Matters
| # | Title | Tagline |
|---|---|---|
| 1 | The Void Between Us | The abyss stared back — with her eyes. |
| 2 | Nothing to Lose | If nothing matters, she may as well kiss him. |
| 3 | Amor Fati | She never expected fate to have such good forearms. |
| 4 | The Heat Death of the Heart | Entropy comes for all things. But not tonight. |

### Magma Rising
| # | Title | Tagline |
|---|---|---|
| 1 | Pyroclastic | A confession you cannot outrun. |
| 2 | The Lava Tube | Trapped underground, with only their chemistry. |
| 3 | Dormant No More | He'd been quiet for years. Then she recalibrated everything. |
| 4 | Effusive | When the mountain settles, love overflows. |

### Bunker Down
| # | Title | Tagline |
|---|---|---|
| 1 | Bug-Out Bag | She had a plan for every catastrophe but him. |
| 2 | Canned Goods | Fifteen years of shelf life. One very short fuse. |
| 3 | Fallout | The sirens were a drill. The feelings were not. |
| 4 | The All-Clear | The scariest scenario of all: a future together. |

### Between the Flags
| # | Title | Tagline |
|---|---|---|
| 1 | The Deep End | He dove straight past every rule she had. |
| 2 | Still Waters | Beneath a calm surface, a current pulls. |
| 3 | Riptide | The strongest pull isn't the tide. |
| 4 | The Wave Pool | Two real hearts, thrown together every ninety seconds. |

### Not a Minute Late
| # | Title | Tagline |
|---|---|---|
| 1 | On the Dot | He arrived four minutes early. She nearly swooned. |
| 2 | Synchronized | Two watches. One heartbeat. |
| 3 | Right on Time | The best moment to say "I love you" is precisely now. |

### The Sweetest Sting
| # | Title | Tagline |
|---|---|---|
| 1 | Smoke & Honey | The bees knew before she did. |
| 2 | The Swarm | Ten thousand bees. Two rival hearts. |
| 3 | Requeened | A heart long thought colony-collapsed finds its queen. |

### Cooking the Books
| # | Title | Tagline |
|---|---|---|
| 1 | Material Misstatement | She flagged the discrepancy. He signed the audit. |
| 2 | Off the Books | A missing four million. Two people who can't stop crossing lines. |
| 3 | The Reconciliation | Two hearts, balanced to the penny. |

---

## 4. Production notes

- Art direction + lettering direction live in `scripts/gen_covers.py` (`SERIES`
  table); taglines live in `data.json`. This doc is the human-readable contract.
- The **image generator renders all text** — no font overlays. The font names in
  the per-series "Type" notes above are *style references* for the lettering
  look requested in the prompt, not bundled assets.
- Regenerate one series at a time: `python3 scripts/gen_covers.py --only <id>`
  (`--force` to overwrite existing). Add `-N` to target a single book.
- Every regenerated cover is reviewed individually — spelling and legibility
  included — before it is committed.
