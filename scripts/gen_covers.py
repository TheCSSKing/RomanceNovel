#!/usr/bin/env python3
"""Generate Ravish House covers with OpenAI Images (gpt-image-2).

All cover text (title, series line, author, tagline, publisher) is rendered by
the image generator itself — no post-hoc font overlays. Each series feeds a
distinct ART aesthetic AND a distinct LETTERING style into the prompt, so the
covers no longer look alike. See docs/COVER_REQUIREMENTS.md.

Usage:
  python3 scripts/gen_covers.py --only <series-id>     # regenerate one series
  python3 scripts/gen_covers.py --only <series-id-N>   # regenerate one book
  python3 scripts/gen_covers.py                        # all missing covers
  python3 scripts/gen_covers.py --force                # regenerate everything
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
OUT = os.path.join(ROOT, "covers")
API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-2"
SIZE = "1024x1536"      # portrait, book-cover aspect
QUALITY = "high"

API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()


def spec(**k):
    return k

# Per series: `art` = a DISTINCT set/staging + visual style (medium/palette/mood),
#             `letter` = how the cover lettering should look (typography style).
# Every set stages the over-the-top clinch differently (see build_prompt).
SERIES = {
 "love-by-the-numbers": spec(
    art=("Set: a power-couple clinch sprawled across a vast glass boardroom table at "
         "night, papers and glowing bell-curve charts scattering, city lights "
         "beyond. The shirtless hero's tie hangs loose; the heroine pulls him down "
         "by it, her blouse slipping off a shoulder. Sleek modern corporate-"
         "minimalist illustration, cool teal and warm gold, flat-leaning digital."),
    letter=("crisp modern GEOMETRIC SANS-SERIF lettering, corporate and precise, "
            "teal and gold")),

 "fathoms-of-the-heart": spec(
    art=("Set: a fevered embrace pinned against the steel submarine bulkhead as red "
         "alert lights spin and sonar screens glow; the hero shirtless and sweat-"
         "sheened, the heroine's uniform half-unbuttoned, pipes and valves crowding "
         "in. Moody cinematic realism, deep navy and abyssal black, red rim-light."),
    letter=("bold INDUSTRIAL CONDENSED uppercase lettering, cold white with red "
            "emergency-light accents, cinematic")),

 "rind-and-the-reckless": spec(
    art=("Set: a couple tangled together against a rack of giant golden cheese "
         "wheels in a candlelit aging cave, the shirtless hero lifting the heroine "
         "off her feet, her rustic dress slipping off one shoulder. Warm rustic oil "
         "painting, old-master warmth, textured brushwork, amber and hay tones."),
    letter=("warm rustic hand-crafted SERIF lettering, artisanal, gold on dark amber")),

 "below-zero-above-reason": spec(
    art=("Set: a steamy clinch inside a cramped research-station bunk, parkas thrown "
         "off and bare skin against the cold, frost on the window with the aurora "
         "blazing green beyond. Icy technical Nordic-poster style, glacial blue-teal "
         "and aurora green."),
    letter=("thin, WIDELY LETTER-SPACED geometric sans-serif, cold and precise, "
            "ice-white with aurora-teal accents")),

 "leave-no-trace": spec(
    art=("Set: a sun-warmed couple entwined in the dirt of a lush zero-waste garden "
         "among mason jars, compost and wildflowers, the shirtless hero and the "
         "heroine in a loose linen slip off the shoulder, smudged and laughing. Soft "
         "eco watercolor / botanical illustration, earthy greens and warm cream."),
    letter=("friendly rounded lettering with a HANDWRITTEN SCRIPT tagline, earthy "
            "and organic, forest green on cream")),

 "nothing-matters": spec(
    art=("Set: two half-undressed bodies clinging together, small in the frame, on "
         "the edge of an immense indifferent starry cosmic void, a single bare bulb "
         "overhead, endless empty dark. Stark existential minimalism, muted grays "
         "and deep violet-black."),
    letter=("austere elegant HIGH-CONTRAST SERIF lettering with generous empty "
            "space, muted pale gray")),

 "magma-rising": spec(
    art=("Set: a molten clinch on the very rim of an erupting volcano — the shirtless "
         "hero and the heroine in a windswept gown crushed together, backs arching, "
         "as rivers of lava erupt behind them and embers and ash swirl, firelight "
         "and sweat on bare skin. Explosive high-contrast digital painting, molten "
         "orange and red on near-black, blockbuster drama."),
    letter=("MASSIVE BOLD CONDENSED all-caps poster lettering, molten orange and "
            "white, high drama")),

 "bunker-down": spec(
    art=("Set: a couple tangled together atop stacked crates of supplies in a bunker, "
         "the hero shirtless with dog tags, the heroine's tank top strap sliding "
         "down, blast door and lantern light behind. Gritty survivalist realism, "
         "desaturated amber and olive."),
    letter=("STENCILED military-utility lettering, weathered, amber on olive")),

 "between-the-flags": spec(
    art=("Set: two lifeguards locked in a dripping-wet clinch on the sand, red "
         "swimsuit and bare glistening torso, the rescue buoy dropped, a wave "
         "crashing behind them. Super-saturated retro-1980s 'Baywatch' pop, sun-"
         "blasted, airbrush and halftone, red, yellow and pool-aqua."),
    letter=("bold rounded RETRO-80s lettering, super-saturated, white with a red "
            "keyline")),

 "not-a-minute-late": spec(
    art=("Set: an opulent clinch beneath a monumental station clock, the hero's "
         "dress shirt undone and the heroine's beaded gown slipping, pocket watches "
         "and pendulums swinging around them. Elegant Art-Deco railway-poster, brass "
         "gold on deep navy, sunburst geometry, 1920s luxe."),
    letter=("elegant ART-DECO capitals, geometric and symmetrical, brass gold on "
            "deep navy, 1920s")),

 "sweetest-sting": spec(
    art=("Set: a golden-hour clinch in the apiary, beekeeping suits peeled to the "
         "waist with bare shoulders and honey-slick skin, veils cast aside, hives "
         "and honeycomb around them and bees drifting through warm light. Sun-"
         "drenched pastoral, painterly-soft, honey gold, meadow green and cream."),
    letter=("warm SERIF title with a WHIMSICAL HANDWRITTEN SCRIPT tagline, honey "
            "gold and cream")),

 "cooking-the-books": spec(
    art=("Set: a couple entangled across a desk buried in scattered case files under "
         "a green banker's lamp, the hero's shirt open and the heroine's blouse "
         "loosened, venetian-blind stripes of light falling over bare skin. Film "
         "noir, high-contrast chiaroscuro, near-monochrome charcoal, green accent."),
    letter=("TYPEWRITER MONOSPACE lettering like a case file, off-white with a "
            "green accent, noir")),
}


def build_prompt(sp, book):
    return (
        f"A gloriously OVER-THE-TOP MASS-MARKET ROMANCE NOVEL COVER in the classic "
        f"bodice-ripper tradition, portrait 2:3. A passionate couple ENTANGLED in a "
        f"dramatic clinch — bodies pressed together, all over each other — with LOTS "
        f"of bare skin: a shirtless, muscular hero and the heroine in a flowing off-"
        f"the-shoulder gown, bare shoulders, arms and backs, sensual and swooning.\n\n"
        f"Artwork: {sp['art']} The mood matches this book: \"{book['title']}\" — "
        f"{book['description'][:200]}\n\n"
        f"Render the following COVER TEXT as part of the image, integrated into the "
        f"design with clean professional typography and a clear hierarchy. Spell "
        f"every word EXACTLY as written — do not add, drop, reorder or misspell any "
        f"word:\n"
        f"  • BOOK TITLE (the largest, most prominent text): \"{book['title']}\"\n"
        f"  • SERIES NAME (noticeably smaller and LESS BOLD than the title, a subtle "
        f"eyebrow line): \"{book['series']}\"\n"
        f"  • TAGLINE (a short italic hook near the title): \"{book['tagline']}\"\n"
        f"  • AUTHOR byline (small): \"{book['author']}\"\n"
        f"  • PUBLISHER (small, at the very bottom): \"RAVISH HOUSE\"\n\n"
        f"Typography style: {sp['letter']}. Place the series eyebrow near the top and "
        f"the title, tagline, author and publisher toward the bottom; keep the text "
        f"legible and clear of the couple's faces. Correct spelling is essential; no "
        f"extra or gibberish text. Keep it in the mainstream romance-genre register: "
        f"steamy and sensual but NOT explicit — no nudity, no exposed genitals, no "
        f"sex acts; a passionate embrace only."
    )


def generate(prompt):
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": SIZE,
                       "quality": QUALITY, "n": 1}).encode()
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    return base64.b64decode(data["data"][0]["b64_json"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    if not API_KEY:
        sys.exit("ERROR: OPENAI_API_KEY not set in environment.")
    os.makedirs(OUT, exist_ok=True)
    catalog = json.load(open(DATA))

    jobs = []
    for s in catalog["series"]:
        for i, b in enumerate(s["books"], 1):
            fid = f"{s['id']}-{i}"
            b = dict(b, series=s["title"], author=s["author"])
            jobs.append((fid, s["id"], b))
    if args.only:
        jobs = [j for j in jobs if j[0] == args.only or j[1] == args.only]
    if not jobs:
        sys.exit(f"No jobs matched --only {args.only!r}")

    total, done = len(jobs), 0
    for fid, sid, b in jobs:
        path = os.path.join(OUT, fid + ".png")
        if os.path.exists(path) and not args.force:
            done += 1; print(f"[skip] {fid} (exists)"); continue
        prompt = build_prompt(SERIES[sid], b)
        for attempt in range(1, 5):
            try:
                print(f"[gen ] {fid}  ({b['series']} — {b['title']})  attempt {attempt}")
                png = generate(prompt)
                with open(path, "wb") as f:
                    f.write(png)
                done += 1
                print(f"[ok  ] {fid}  {len(png)//1024} KB  ({done}/{total})")
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:400]
                print(f"[err ] {fid} HTTP {e.code}: {msg}")
                if e.code in (401, 403):
                    sys.exit(1)
                time.sleep(2 ** attempt)
            except Exception as e:
                print(f"[err ] {fid} {e}")
                time.sleep(2 ** attempt)
        else:
            print(f"[FAIL] {fid} after retries")
    print(f"\nDone: {done}/{total}")


if __name__ == "__main__":
    main()
