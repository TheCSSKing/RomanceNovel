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

# Per series: `art` = scene + visual aesthetic (medium/palette/mood),
#             `letter` = how the cover lettering should look (typography style).
SERIES = {
 "love-by-the-numbers": spec(
    art=("Clean modern corporate-minimalist illustration: a couple sharing a quiet "
         "charged moment in a bright minimalist glass high-rise office, faint bell "
         "curves, grids and ledgers, lots of negative space. Cool teal and warm "
         "gold on cream, sophisticated and restrained, flat-leaning digital style."),
    letter=("crisp modern GEOMETRIC SANS-SERIF lettering, corporate and precise, "
            "teal and gold")),

 "fathoms-of-the-heart": spec(
    art=("Moody cinematic realism inside a steel submarine: a couple by glowing "
         "sonar screens, pipes and valves, a porthole to dark water, red emergency "
         "lighting, deep navy and abyssal black, high contrast dramatic rim-light."),
    letter=("bold INDUSTRIAL CONDENSED uppercase lettering, cold white with red "
            "emergency-light accents, cinematic")),

 "rind-and-the-reckless": spec(
    art=("Warm rustic oil painting with old-master still-life warmth: a couple in a "
         "candlelit cheese-aging cave, wooden shelves of golden wheels, textured "
         "painterly brushwork, amber and hay tones, cozy and artisanal."),
    letter=("warm rustic hand-crafted SERIF lettering, artisanal, gold on dark amber")),

 "below-zero-above-reason": spec(
    art=("Icy, spare, technical Nordic-poster minimalism: a bundled couple outside "
         "Quonset huts under a vast swirling aurora, endless snow and huge empty "
         "sky, glacial blue-teal and aurora green, cold restrained light."),
    letter=("thin, WIDELY LETTER-SPACED geometric sans-serif, cold and precise, "
            "ice-white with aurora-teal accents")),

 "leave-no-trace": spec(
    art=("Soft eco watercolor and botanical illustration: a couple in a lush "
         "zero-waste garden with mason jars, compost and solar panels at golden "
         "hour, hand-made textures, earthy greens and warm cream, cottagecore."),
    letter=("friendly rounded lettering with a HANDWRITTEN SCRIPT tagline, earthy "
            "and organic, forest green on cream")),

 "nothing-matters": spec(
    art=("Stark existential minimalism: a couple small in the frame embracing in an "
         "almost-empty room open to an enormous indifferent starry cosmic void, a "
         "single bare bulb, muted grays and deep violet-black, vast empty space."),
    letter=("austere elegant HIGH-CONTRAST SERIF lettering with generous empty "
            "space, muted pale gray")),

 "magma-rising": spec(
    art=("Explosive high-contrast digital painting: a couple silhouetted against an "
         "erupting volcano with rivers of glowing lava, ash and heat-shimmer, "
         "molten orange and red on near-black, blockbuster-poster drama."),
    letter=("MASSIVE BOLD CONDENSED all-caps poster lettering, molten orange and "
            "white, high drama")),

 "bunker-down": spec(
    art=("Gritty survivalist realism: a couple in a stocked underground bunker with "
         "a blast door, shelves of canned goods, gas masks and gear, lantern light, "
         "worn utilitarian textures, desaturated amber and olive, tactical mood."),
    letter=("STENCILED military-utility lettering, weathered, amber on olive")),

 "between-the-flags": spec(
    art=("Bright retro-1980s pop illustration: two lifeguards in red and yellow with "
         "a rescue buoy and whistle by dazzling water, super-saturated sun-blasted "
         "glossy 'Baywatch' nostalgia, airbrush and halftone energy, red, yellow "
         "and pool-aqua."),
    letter=("bold rounded RETRO-80s lettering, super-saturated, white with a red "
            "keyline")),

 "not-a-minute-late": spec(
    art=("Elegant Art-Deco vintage railway-poster: an elegant couple beneath "
         "monumental ornate station clocks, pocket watches and pendulums, brass and "
         "deep navy, symmetry and sunburst geometry, 1920s luxe, refined."),
    letter=("elegant ART-DECO capitals, geometric and symmetrical, brass gold on "
            "deep navy, 1920s")),

 "sweetest-sting": spec(
    art=("Sun-drenched pastoral, warm and whimsical: two beekeepers in veils sharing "
         "a tender moment among wooden hives, golden honeycomb, drifting bees and "
         "wildflowers, dappled summer light, painterly-soft, honey gold, meadow "
         "green and cream."),
    letter=("warm SERIF title with a WHIMSICAL HANDWRITTEN SCRIPT tagline, honey "
            "gold and cream")),

 "cooking-the-books": spec(
    art=("Film noir: a couple in a dim office of towering document stacks and "
         "ledgers under a green banker's lamp, high-contrast chiaroscuro, deep "
         "shadow, venetian-blind light, 1940s detective mood, near-monochrome "
         "charcoal with a single green-lamp accent."),
    letter=("TYPEWRITER MONOSPACE lettering like a case file, off-white with a "
            "green accent, noir")),
}


def build_prompt(sp, book):
    return (
        f"A finished, professional MASS-MARKET ROMANCE NOVEL COVER, portrait 2:3.\n\n"
        f"Artwork: {sp['art']} The emotional tone matches this book: "
        f"\"{book['title']}\" — {book['description'][:220]}\n\n"
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
        f"clear of the couple's faces and fully legible. Correct spelling is "
        f"essential. Tasteful and wholesome: PG, fully and modestly clothed, "
        f"tender-not-explicit. No extra or gibberish text anywhere on the cover."
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
