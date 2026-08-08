#!/usr/bin/env python3
"""Generate parody romance cover art via OpenAI Images API (gpt-image-2).

Art-only covers (no baked-in text); title/author are overlaid by the site.
Usage:
  python3 scripts/gen_covers.py --test           # generate ONE image to verify
  python3 scripts/gen_covers.py                   # generate all missing covers
  python3 scripts/gen_covers.py --force           # regenerate everything
  python3 scripts/gen_covers.py --only <id>       # regenerate one series (or id-N)
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
SIZE = "1024x1536"     # portrait, book-cover aspect
QUALITY = "medium"

API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()

# Per-series art direction: mood/palette/imagery cues for the illustrator.
SERIES_ART = {
    "love-by-the-numbers": "a windswept couple embracing amid giant floating spreadsheets, actuarial charts and bell curves, calculators and pension ledgers; corporate teal and gold palette, dramatic office-window light",
    "fathoms-of-the-heart": "a passionate couple inside a cramped steel submarine control room, glowing sonar screens and pipes and valves, deep ocean-blue and red emergency lighting, portholes showing dark water",
    "rind-and-the-reckless": "a rugged couple in a rustic cheese cave surrounded by huge aging wheels of cheese on wooden shelves, warm golden dairy tones, dramatic candlelight, artisanal creamery",
    "below-zero-above-reason": "a couple bundled in heavy parkas embracing outside an Antarctic research station under swirling auroras, endless ice and snow, cold blue and green polar light, isolated Quonset huts",
    "leave-no-trace": "an earthy couple among lush compost gardens, mason jars, reusable everything, thriving green plants and solar panels, warm sustainable eco tones, sun-dappled homestead",
    "nothing-matters": "a melancholy couple embracing under a vast indifferent starry cosmic void, empty minimalist room, existential mood, muted grays and deep purples, single bare lightbulb, philosophical loneliness",
    "magma-rising": "a dramatic couple silhouetted against an erupting volcano with rivers of glowing orange lava, ash clouds, intense fiery red and black palette, heat shimmer",
    "bunker-down": "a rugged couple in an underground survival bunker stocked with canned goods and supplies, dim emergency lighting, blast door, gas masks and gear, tense post-apocalyptic amber tones",
    "between-the-flags": "a heroic lifeguard couple on duty by the water with a red rescue buoy and whistle, bright sunlit aquatic setting, red-and-yellow lifeguard palette, crashing water",
    "not-a-minute-late": "an elegant couple beneath enormous ornate clocks and train-station timetables, pocket watches and swinging pendulums, precise refined palette of brass and deep blue, dramatic clockwork",
    "sweetest-sting": "a couple in beekeeping veils amid golden honeycomb and swirling bees in a sunlit summer apiary, warm honey-gold and green palette, wildflowers and wooden hives",
    "cooking-the-books": "a sharp couple in a dim office surrounded by towering stacks of financial documents, ledgers and evidence folders, film-noir desk-lamp lighting, deep shadows and green banker's-lamp glow",
}

STYLE = ("Mass-market paperback ROMANCE NOVEL cover illustration, painterly and glossy, "
         "lush dramatic lighting, highly emotional and slightly over-the-top, "
         "attractive couple as the focal point, cinematic composition, portrait orientation. "
         "IMPORTANT: absolutely NO text, NO title, NO letters, NO words, NO numbers, "
         "NO logos, NO watermark, NO signature anywhere in the image — artwork only, "
         "leave calm uncluttered space near the top and bottom for a title to be added later.")


def build_prompt(series, book):
    art = SERIES_ART.get(series["id"], series["theme"])
    return (f"{STYLE}\n\nScene: {art}. "
            f"The emotional tone matches this book: \"{book['title']}\" — {book['description']} "
            f"Genre backdrop: {series['theme']}.")


def generate(prompt):
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "size": SIZE,
        "quality": QUALITY, "n": 1,
    }).encode()
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    return base64.b64decode(data["data"][0]["b64_json"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    if not API_KEY:
        sys.exit("ERROR: OPENAI_API_KEY not set in environment.")

    os.makedirs(OUT, exist_ok=True)
    with open(DATA) as f:
        catalog = json.load(f)

    jobs = []
    for s in catalog["series"]:
        for i, b in enumerate(s["books"], 1):
            fid = f"{s['id']}-{i}"
            jobs.append((fid, s, b))

    if args.test:
        jobs = jobs[:1]
    if args.only:
        jobs = [j for j in jobs if j[0] == args.only or j[1]["id"] == args.only]

    total = len(jobs)
    done = 0
    for fid, s, b in jobs:
        path = os.path.join(OUT, fid + ".png")
        if os.path.exists(path) and not args.force and not args.test:
            done += 1
            print(f"[skip] {fid} (exists)")
            continue
        prompt = build_prompt(s, b)
        for attempt in range(1, 5):
            try:
                print(f"[gen ] {fid}  ({s['title']} — {b['title']})  attempt {attempt}")
                png = generate(prompt)
                with open(path, "wb") as f:
                    f.write(png)
                done += 1
                print(f"[ok  ] {fid}  {len(png)//1024} KB  ({done}/{total})")
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:400]
                print(f"[err ] {fid} HTTP {e.code}: {msg}")
                if e.code in (400, 401, 403):
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
