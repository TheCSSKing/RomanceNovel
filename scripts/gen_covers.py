#!/usr/bin/env python3
"""Generate Ravish House covers: per-series art (OpenAI gpt-image-2) + typography.

Two layers (see docs/COVER_REQUIREMENTS.md):
  1. Artwork  - a per-series *style* is sent to the image model, which is told to
     render NO text and to leave calm space top and bottom.
  2. Typography - title, series line, author, tagline and publisher mark are
     composited with Pillow, so the words are always crisp and correctly spelled.

Usage:
  python3 scripts/gen_covers.py --only <series-id>     # regenerate one series
  python3 scripts/gen_covers.py --only <series-id-N>   # regenerate one book
  python3 scripts/gen_covers.py                        # all missing covers
  python3 scripts/gen_covers.py --force                # regenerate everything
  python3 scripts/gen_covers.py --only <id> --art-only # skip typography (debug)
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
OUT = os.path.join(ROOT, "covers")
RAW = os.path.join(OUT, ".raw")           # ungit'd source art, kept for review
FONTS = os.path.join(ROOT, "assets", "fonts")
API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-2"
SIZE = "1024x1536"
QUALITY = "medium"
W, H = 1024, 1536

API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()

# Shared art guardrails. Per-series `style` supplies the distinct look.
BASE = ("Portrait book-cover illustration, 2:3 aspect. Keep it tasteful and "
        "wholesome: PG, fully and modestly clothed, tender-not-explicit. "
        "Compose with calm, uncluttered space near the TOP and the BOTTOM of the "
        "frame for titling. IMPORTANT: absolutely NO text, letters, words, "
        "numbers, logos, watermarks or signatures anywhere — artwork only.")

# ── Per-series art direction + typography (mirrors docs/COVER_REQUIREMENTS.md) ──
# type keys: t=title, s=series eyebrow, g=taGline, a=author.  font/size/case.
def spec(**k):
    return k

SERIES = {
 "love-by-the-numbers": spec(
    style=("Clean modern CORPORATE MINIMALISM: contemporary flat-leaning digital "
           "illustration, crisp geometry, lots of negative space, subtle data-viz "
           "motifs (bell curves, grids, ledgers). Cool teal and warm gold on cream, "
           "restrained and sophisticated, a couple as a small elegant focal point."),
    art=("two actuaries sharing a quiet charged moment in a bright minimalist "
         "high-rise office of glass and pale wood, faint bell curves and grid lines"),
    title_font="Outfit-Bold", title_size=132, title_case="title",
    series_font="Jura-Light", series_track=10, series_case="upper",
    tag_font="WorkSans-Italic", tag_size=40,
    author_font="WorkSans-Regular", author_prefix="by ",
    text=(28,54,60), accent=(184,141,63), scrim=(246,241,230), light_bg=True),

 "fathoms-of-the-heart": spec(
    style=("Moody CINEMATIC REALISM inside a steel submarine: sonar glow, pipes, "
           "valves, portholes to dark water, red emergency lighting, deep navy and "
           "abyssal black, high contrast dramatic rim-light."),
    art="a couple in a cramped submarine control room lit by red alert light and sonar screens",
    title_font="BigShoulders-Bold", title_size=150, title_case="upper", title_track=2,
    series_font="Jura-Light", series_track=8, series_case="upper",
    tag_font="IBMPlexSerif-Italic", tag_size=38,
    author_font="Jura-Medium", author_prefix="", author_case="upper",
    text=(233,240,247), accent=(214,64,64), scrim=(3,14,28)),

 "rind-and-the-reckless": spec(
    style=("Warm rustic OIL PAINTING, old-master still-life warmth: candlelit "
           "cheese-aging cave, wooden shelves of golden wheels, textured painterly "
           "brushwork, amber and hay tones, cozy and artisanal."),
    art="a couple embracing among towering wheels of aging cheese by candlelight",
    title_font="YoungSerif-Regular", title_size=126, title_case="title",
    series_font="ArsenalSC-Regular", series_track=6, series_case="upper",
    tag_font="Lora-Italic", tag_size=38,
    author_font="Lora-Regular", author_prefix="by ",
    text=(247,238,214), accent=(214,158,74), scrim=(38,22,8)),

 "below-zero-above-reason": spec(
    style=("Icy, spare, TECHNICAL Nordic-poster minimalism: cold light, swirling "
           "aurora, endless snow with huge empty sky, a lonely Antarctic research "
           "station, glacial blue-teal and aurora green, restrained composition."),
    art="a bundled couple embracing outside Quonset huts under a vast aurora, endless ice",
    title_font="Jura-Medium", title_size=104, title_case="upper", title_track=10,
    series_font="Jura-Light", series_track=12, series_case="upper",
    tag_font="InstrumentSerif-Italic", tag_size=42,
    author_font="Jura-Light", author_prefix="", author_case="upper", author_track=6,
    text=(233,244,248), accent=(120,224,204), scrim=(11,30,48)),

 "leave-no-trace": spec(
    style=("Soft eco WATERCOLOR and botanical illustration: hand-made textures, "
           "sun-dappled homestead, mason jars, compost, thriving greenery, "
           "earthy greens and warm cream, cottagecore warmth."),
    art="a couple in a lush zero-waste garden with mason jars, compost and solar panels at golden hour",
    title_font="NationalPark-Bold", title_size=132, title_case="title",
    series_font="NationalPark-Regular", series_track=8, series_case="upper",
    tag_font="NothingYouCouldDo-Regular", tag_size=54,
    author_font="NationalPark-Regular", author_prefix="by ",
    text=(243,239,224), accent=(150,196,74), scrim=(26,46,20)),

 "nothing-matters": spec(
    style=("Stark existential MINIMALISM: a vast indifferent cosmic void, tiny "
           "figures, enormous empty space, muted grays and deep violet-black, a "
           "single bare bulb of warmth. Reads like a philosophy monograph."),
    art="a couple, small in the frame, embracing in an empty room open to a huge starry void",
    title_font="Italiana-Regular", title_size=120, title_case="title",
    series_font="Jura-Light", series_track=12, series_case="upper",
    tag_font="CrimsonPro-Italic", tag_size=40,
    author_font="Jura-Light", author_prefix="", author_case="upper", author_track=4,
    text=(224,222,230), accent=(150,132,178), scrim=(14,12,22)),

 "magma-rising": spec(
    style=("Explosive high-contrast DIGITAL PAINTING: fiery silhouettes against an "
           "erupting volcano, rivers of glowing lava, ash and heat-shimmer, molten "
           "orange and red on near-black, blockbuster-poster energy."),
    art="a couple silhouetted against an erupting volcano and rivers of lava",
    title_font="EricaOne-Regular", title_size=150, title_case="upper", title_track=1,
    series_font="BigShoulders-Regular", series_track=8, series_case="upper",
    tag_font="BigShoulders-Regular", tag_size=44,
    author_font="BigShoulders-Regular", author_prefix="", author_case="upper",
    text=(255,241,224), accent=(255,120,40), scrim=(20,6,4)),

 "bunker-down": spec(
    style=("Gritty SURVIVALIST realism: an underground bunker with blast door, "
           "shelves of canned goods, gas masks and gear, lantern light, worn "
           "utilitarian textures, desaturated amber and olive, tactical mood."),
    art="a couple embracing in a stocked survival bunker with a blast door and lantern light",
    title_font="Tektur-Medium", title_size=120, title_case="upper", title_track=1,
    series_font="RedHatMono-Regular", series_track=6, series_case="upper",
    tag_font="RedHatMono-Regular", tag_size=34,
    author_font="RedHatMono-Bold", author_prefix="", author_case="upper",
    text=(238,214,160), accent=(214,150,52), scrim=(20,18,10)),

 "between-the-flags": spec(
    style=("Bright RETRO-80s POP: super-saturated, sun-blasted, glossy 'Baywatch' "
           "nostalgia with airbrush/halftone energy, lifeguard red and yellow with "
           "pool-aqua, high saturation, water everywhere."),
    art="two lifeguards in red and yellow with a rescue buoy and whistle by bright water",
    title_font="EricaOne-Regular", title_size=140, title_case="upper",
    series_font="SmoochSans-Medium", series_track=8, series_case="upper",
    tag_font="SmoochSans-Medium", tag_size=48,
    author_font="SmoochSans-Medium", author_prefix="", author_case="upper",
    text=(255,255,255), accent=(240,52,52), scrim=(10,60,96)),

 "not-a-minute-late": spec(
    style=("Elegant ART-DECO vintage railway-poster: brass and deep navy, symmetry, "
           "sunburst geometry, monumental clocks, pocket watches and pendulums, "
           "1920s luxe, refined and precise."),
    art="an elegant couple beneath enormous ornate station clocks and pocket watches",
    title_font="PoiretOne-Regular", title_size=118, title_case="upper", title_track=6,
    series_font="Italiana-Regular", series_track=10, series_case="upper",
    tag_font="Italiana-Regular", tag_size=42,
    author_font="Italiana-Regular", author_prefix="", author_case="upper", author_track=4,
    text=(233,204,138), accent=(201,162,79), scrim=(12,22,44)),

 "sweetest-sting": spec(
    style=("Sun-drenched PASTORAL, warm and whimsical: a golden apiary with "
           "honeycomb, drifting bees, wildflowers and wooden hives, dappled summer "
           "light, painterly-soft, honey gold and meadow green and cream."),
    art="two beekeepers in veils sharing a tender moment among hives, honeycomb and drifting bees",
    title_font="Lora-Bold", title_size=128, title_case="title",
    series_font="ArsenalSC-Regular", series_track=6, series_case="upper",
    tag_font="NothingYouCouldDo-Regular", tag_size=56,
    author_font="Lora-Regular", author_prefix="by ",
    text=(252,244,222), accent=(240,190,64), scrim=(46,30,8)),

 "cooking-the-books": spec(
    style=("FILM NOIR: high-contrast chiaroscuro, deep shadow, venetian-blind light, "
           "a green banker's-lamp pool of light, towering case files and ledgers, "
           "1940s detective mood, near-monochrome charcoal with a single green accent."),
    art="a couple in a dim office of towering document stacks under a green banker's lamp",
    title_font="JetBrainsMono-Bold", title_size=104, title_case="upper", title_track=1,
    series_font="RedHatMono-Regular", series_track=6, series_case="upper",
    tag_font="RedHatMono-Regular", tag_size=32,
    author_font="RedHatMono-Bold", author_prefix="", author_case="upper",
    text=(232,232,224), accent=(120,210,120), scrim=(10,12,10)),
}


def build_prompt(sp, book):
    return (f"{sp['style']}\n\nScene: {sp['art']}. The emotional tone matches "
            f"\"{book['title']}\" — {book['description'][:280]}\n\n{BASE}")


def generate(prompt):
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": SIZE,
                       "quality": QUALITY, "n": 1}).encode()
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    return base64.b64decode(data["data"][0]["b64_json"])


# ─────────────────────────── typography layer ───────────────────────────
_font_cache = {}
def font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONTS, name + ".ttf"), size)
    return _font_cache[key]


def cased(text, case):
    if case == "upper": return text.upper()
    if case == "title": return text
    return text


def track_text(draw, xy, text, fnt, fill, tracking=0, anchor_mid=True, shadow=None):
    """Draw text with letter spacing; x in xy is the CENTER when anchor_mid."""
    x, y = xy
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    cx = x - total / 2 if anchor_mid else x
    for c, w in zip(text, widths):
        if shadow:
            draw.text((cx + shadow[0], y + shadow[1]), c, font=fnt, fill=shadow[2], anchor="lm")
        draw.text((cx, y), c, font=fnt, fill=fill, anchor="lm")
        cx += w + tracking
    return total


def wrap_to_width(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines


def fit_title(draw, text, name, max_size, max_w, track=0):
    """Shrink title font until it fits max_w in <=2 lines; return (font, lines)."""
    size = max_size
    while size > 40:
        fnt = font(name, size)
        lines = wrap_to_width(draw, text, fnt, max_w)
        if len(lines) <= 2 and all(
                sum(draw.textlength(c, font=fnt) for c in ln) + track * (len(ln) - 1) <= max_w
                for ln in lines):
            return fnt, lines
        size -= 4
    return font(name, size), wrap_to_width(draw, text, font(name, size), max_w)


def vgradient_scrim(base, top_a, bot_a, y0, y1, flip=False):
    """Vertical alpha ramp band of `base` color from y0..y1."""
    band = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, 0))
    px = band.load()
    span = max(y1 - y0 - 1, 1)
    for yy in range(y1 - y0):
        f = yy / span
        a = int(top_a + (bot_a - top_a) * (f if not flip else 1 - f))
        for xx in range(W):
            px[xx, yy] = (base[0], base[1], base[2], a)
    return band


def compose(art_bytes, sp, book):
    import io
    img = Image.open(io.BytesIO(art_bytes)).convert("RGBA")
    if img.size != (W, H):
        img = img.resize((W, H))

    # legibility scrims: darker (or lighter) toward top and bottom edges
    scrim = sp["scrim"]
    top = vgradient_scrim(scrim, 210, 0, 0, int(H * 0.20))
    bot = vgradient_scrim(scrim, 0, 235, int(H * 0.56), H)
    img.alpha_composite(top)
    img.alpha_composite(bot)

    d = ImageDraw.Draw(img)
    margin = 84
    max_w = W - 2 * margin
    text, accent = sp["text"], sp["accent"]
    shadow = (2, 3, (0, 0, 0, 150))

    # ── series eyebrow (top, small, LESS BOLD than title) ──
    s_size = 40
    sf = font(sp["series_font"], s_size)
    series_txt = cased(book["series"], sp["series_case"])
    track_text(d, (W / 2, int(H * 0.072)), series_txt, sf, text,
               tracking=sp.get("series_track", 6), shadow=shadow)
    # thin accent rule under the eyebrow
    rule_w = 120
    ry = int(H * 0.072) + 34
    d.line([(W/2 - rule_w/2, ry), (W/2 + rule_w/2, ry)], fill=accent, width=3)

    # ── bottom stack (measured, stacked upward so nothing overlaps) ──
    gap = 30
    # measure each block
    pub_f, pub_h = font("Jura-Light", 26), 26
    auth_f, auth_h = font(sp["author_font"], 40), 40
    tg = font(sp["tag_font"], sp["tag_size"])
    tag_lines = wrap_to_width(d, book["tagline"], tg, max_w)
    tag_lh = sp["tag_size"] + 6
    tag_h = len(tag_lines) * tag_lh
    tf, title_lines = fit_title(d, cased(book["title"], sp["title_case"]),
                                sp["title_font"], sp["title_size"], max_w,
                                track=sp.get("title_track", 0))
    title_lh = tf.size + 10
    title_h = len(title_lines) * title_lh

    # centers, stacked from the bottom up
    pub_cy   = H - 60
    auth_cy  = pub_cy - pub_h / 2 - gap * 0.7 - auth_h / 2
    tag_cy   = auth_cy - auth_h / 2 - gap - tag_h / 2
    title_cy = tag_cy - tag_h / 2 - gap - title_h / 2

    # publisher
    track_text(d, (W/2, pub_cy), "RAVISH HOUSE", pub_f, text, tracking=8, shadow=shadow)
    # author
    a_txt = cased(sp.get("author_prefix", "by ") + book["author"], sp.get("author_case", "as-is"))
    track_text(d, (W/2, auth_cy), a_txt, auth_f, text,
               tracking=sp.get("author_track", 0), shadow=shadow)
    # tagline (accent, may wrap)
    ty = tag_cy - tag_h / 2 + tag_lh / 2
    for ln in tag_lines:
        d.text((W/2 + shadow[0], ty + shadow[1]), ln, font=tg, fill=shadow[2], anchor="mm")
        d.text((W/2, ty), ln, font=tg, fill=accent, anchor="mm")
        ty += tag_lh
    # title (auto-fit, most prominent)
    yt = title_cy - title_h / 2 + title_lh / 2
    for ln in title_lines:
        track_text(d, (W/2, yt), ln, tf, text, tracking=sp.get("title_track", 0),
                   shadow=(3, 4, (0, 0, 0, 175)))
        yt += title_lh

    return img.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default=None)
    ap.add_argument("--art-only", action="store_true", help="skip typography (debug)")
    args = ap.parse_args()

    if not API_KEY:
        sys.exit("ERROR: OPENAI_API_KEY not set in environment.")
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(RAW, exist_ok=True)
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
        sp = SERIES[sid]
        prompt = build_prompt(sp, b)
        for attempt in range(1, 5):
            try:
                print(f"[gen ] {fid}  ({b['series']} — {b['title']})  attempt {attempt}")
                art = generate(prompt)
                with open(os.path.join(RAW, fid + ".png"), "wb") as f:
                    f.write(art)
                if args.art_only:
                    open(path, "wb").write(art)
                else:
                    compose(art, sp, b).save(path)
                done += 1
                print(f"[ok  ] {fid}  ({done}/{total})")
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
