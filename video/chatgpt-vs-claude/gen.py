#!/usr/bin/env python3
"""Generate index.html for the "ChatGPT vs Claude" talking-head edit.

All edit decisions live in the tables below (source-time based). Re-run this
script after changing them:  python3 gen.py
"""
import json, os

FPS = 30
def fr(t):  # snap to frame grid
    return round(round(t * FPS) / FPS, 4)

# ---------------------------------------------------------------- cuts
# (id, src_in, src_out, zoom)  -- source seconds in assets/source.mp4
SEGMENTS = [
    ("A", 1.333, 3.100, 1.14),   # Korang masih guna ChatGPT ke?          (hook; "Assalamualaikum guys" dibuang)
    ("B", 4.250, 6.867, 1.06),   # Aku rasa lebih baik korang guna Claude.
    # 7.19-9.29 "Yang lebih berbaloi yang aku rasa sekarang" dibuang (ulang)
    # 10.2-11.4 "sebab sebab" (gagap) dibuang
    ("C1", 11.667, 13.420, 1.00), # Dalam Claude korang boleh
    # 13.42-13.90 jeda + suara anak dibuang
    ("C2", 13.900, 19.333, 1.07), # buat macam-macam ... tak semestinya teks ... kreatif.
    # 19.3-21.2 jeda dibuang
    ("D", 21.233, 23.967, 1.10), # Contoh macam sekarang, kalau tengok background aku biasa kan?
    ("E", 24.267, 25.933, 1.00), # Tapi kalau aku suruh Claude
    ("F", 26.633, 29.567, 1.08), # ubah background ni jadi blur  (+ hold untuk magic)
    # 30.6-36.5 "Dia akan blur. Ya? Ya. OK" dibuang (ulang / janggal)
    ("G1", 36.567, 39.620, 1.06), # Lepas ni aku akan share macam mana
    # 39.62-40.15 jeda + suara anak dibuang
    ("G2", 40.150, 43.867, 1.00), # nak gabungkan Claude dengan GitHub
    ("H", 45.300, 48.400, 1.10), # Apa pun jangan lupa follow  (+ thumbs up)
]
GRADE = json.dumps({"preset": "skin-soft", "intensity": 0.6, "adjust": {"exposure": 0.03, "contrast": 0.16, "highlights": -0.24, "shadows": 0.05, "blacks": -0.1, "temperature": 0.07, "tint": 0.06, "saturation": -0.05, "vibrance": 0.08}, "wheels": {"shadows": {"hue": 200, "amount": 0.14, "level": -0.01}, "highlights": {"hue": 36, "amount": 0.1, "level": 0}}, "secondaries": [{"key": {"hue": {"center": 110, "range": 45, "softness": 25}, "saturation": {"min": 0.03, "max": 1, "softness": 0.05}, "luma": {"min": 0.05, "max": 0.98, "softness": 0.08}}, "correction": {"saturation": -0.45, "hueShift": 40}}, {"key": {"hue": {"center": 22, "range": 18, "softness": 12}, "saturation": {"min": 0.12, "max": 0.8, "softness": 0.08}, "luma": {"min": 0.15, "max": 0.9, "softness": 0.1}}, "correction": {"saturation": 0.06, "luma": 0.03}}], "curves": {"master": [[0, 0.02], [0.25, 0.21], [0.75, 0.8], [1, 0.98]]}, "details": {"vignette": 0.2}}, separators=(",", ":"))  # "premium plus" grade (grade/grades2.json)
BLUR_SRC = 28.32          # source time of the word "blur"
BLUR_FILE_OFFSET = 26.0   # assets/blurred26.mp4 starts at this source time

# build source->output map
segs, tf = [], 0  # integer frame bookkeeping keeps clips edge-to-edge
for sid, a, b, z in SEGMENTS:
    af, bf = round(a * FPS), round(b * FPS)
    segs.append(dict(id=sid, a=round(af / FPS, 4), b=round(bf / FPS, 4), z=z,
                     start=round(tf / FPS, 4), dur=int((bf - af) / FPS * 10000) / 10000))
    tf += bf - af
TOTAL = round(tf / FPS, 4)

def out(src):
    for s in segs:
        if s["a"] - 1e-6 <= src <= s["b"] + 1e-6:
            return round(s["start"] + src - s["a"], 3)
    raise ValueError(f"source time {src} is in a cut-out region")

BLUR_T = out(BLUR_SRC)

# ---------------------------------------------------------------- captions
# (src_start, src_end, text, highlight-class or None)
CAPTIONS = [
    (1.36, 1.85, "KORANG MASIH", None),
    (1.85, 3.08, "GUNA *CHATGPT* KE?", "gpt"),
    (4.30, 5.50, "AKU RASA LEBIH BAIK", None),
    (5.50, 6.22, "KORANG GUNA", None),
    (6.22, 6.86, "*CLAUDE*", "claude"),
    (11.70, 12.50, "DALAM *CLAUDE*", "claude"),
    (12.50, 13.42, "KORANG BOLEH", None),
    (13.90, 14.98, "BUAT MACAM-MACAM", None),
    (15.02, 15.95, "DIA TAK SEMESTINYA", None),
    (15.95, 16.55, "*TEKS*", "hl"),
    (16.57, 17.40, "DIA BOLEH BUAT", None),
    (17.40, 18.50, "BENDA MACAM-MACAM", None),
    (18.50, 19.33, "*KREATIF*", "hl"),
    (21.25, 22.50, "CONTOH MACAM SEKARANG", None),
    (22.50, 23.25, "KALAU TENGOK *BACKGROUND*", "hl"),
    (23.25, 23.96, "AKU BIASA KAN?", None),
    (24.28, 25.44, "TAPI KALAU AKU SURUH", None),
    (25.44, 25.93, "*CLAUDE*", "claude"),
    (26.65, 28.10, "UBAH BACKGROUND NI", None),
    (28.10, 29.50, "JADI *BLUR*", "hl"),
    (36.58, 37.60, "LEPAS NI", None),
    (37.90, 38.90, "AKU AKAN SHARE", None),
    (38.90, 39.62, "MACAM MANA", None),
    (40.15, 41.00, "NAK GABUNGKAN", None),
    (41.00, 41.70, "*CLAUDE*", "claude"),
    (41.70, 42.85, "DENGAN", None),
    (42.85, 43.86, "*GITHUB*", "hl"),
    (45.32, 45.98, "APA PUN", None),
    (45.98, 47.20, "JANGAN LUPA *FOLLOW*", "hl"),
]

# ---------------------------------------------------------------- sfx
# (name, file, src_time, volume)
SFX = [
    ("whoosh-open", "whoosh.mp3", None, 0.22),           # t=0 hook entry
    ("pop-gpt", "pop.mp3", 2.50, 0.55),                  # ChatGPT logo on finger
    ("whoosh-vs", "whoosh-short.mp3", 4.27, 0.40),       # logo flies to the top
    ("ping-claude", "ping.mp3", 6.22, 0.40),             # Claude logo lands
    ("pop-chips", "pop.mp3", 13.95, 0.35),               # "macam-macam" chips
    ("typing", "typing.mp3", 15.98, 0.55),               # abammango typing
    ("sparkle-kreatif", "sparkle.mp3", 18.50, 0.35),
    ("pop-bgtag", "pop.mp3", 22.60, 0.40),               # BACKGROUND: BIASA tag
    ("whoosh-card", "whoosh-short.mp3", 25.42, 0.40),    # Claude prompt card in
    ("keys-prompt", "typing.mp3", 26.70, 0.14),          # prompt typing
    ("click-send", "click.mp3", 28.12, 0.40),            # send
    ("whoosh-blur", "whoosh.mp3", 28.30, 0.2),          # MAGIC
    ("sparkle-blur", "sparkle.mp3", 28.70, 0.30),
    ("impact-blur", "impact-bass-1.mp3", 28.72, 0.22),
    ("ping-claude2", "pop.mp3", 41.00, 0.40),
    ("pop-github", "pop.mp3", 42.85, 0.55),
    ("chime-combo", "chime.mp3", 43.25, 0.25),
    ("pop-follow", "pop.mp3", 46.65, 0.45),
    ("click-follow", "click.mp3", 47.45, 0.65),
]

SEG = {s["id"]: s for s in segs}
T = {  # named moments in OUTPUT time
    "gpt_in": out(2.47), "seg_b": SEG["B"]["start"], "claude_in": out(6.22), "seg_c": SEG["C1"]["start"],
    "chips_in": out(13.95), "chips_out": out(15.70), "type_in": out(15.92), "type_out": out(19.0),
    "seg_d": SEG["D"]["start"], "bgtag_in": out(22.60), "seg_e": SEG["E"]["start"],
    "card_in": out(25.42), "prompt_in": out(26.70), "prompt_end": out(28.10), "send": out(28.18),
    "blur": BLUR_T, "seg_f_end": SEG["F"]["start"] + SEG["F"]["dur"], "seg_g": SEG["G1"]["start"],
    "claude2_in": out(41.00), "gh_in": out(42.85), "gh_out": out(43.80), "seg_h": SEG["H"]["start"],
    "follow_in": out(46.65), "follow_click": out(47.45), "end": TOTAL,
}

MUSIC = (f'  <audio id="music" src="assets/music_bed.wav" data-start="0" data-duration="{TOTAL}" '
         f'data-track-index="15" data-volume="1"></audio>')
json.dump({"total": TOTAL, "fps": FPS, "segments": segs, "T": T},
          open(os.path.join(os.path.dirname(__file__), "timing.json"), "w"), indent=1)

# ---------------------------------------------------------------- html
def video_tags():
    base, blur, voice = [], [], []
    for i, s in enumerate(segs):
        # picture from source.mp4 (muted); sound from the cleaned voice track on the same clock
        base.append(
            f'      <video id="v{s["id"]}" class="seg" src="assets/source.mp4" data-start="{s["start"]}" '
            f'data-duration="{s["dur"]}" data-media-start="{s["a"]}" data-track-index="{i % 2}" '
            f'muted playsinline data-color-grading=\'{GRADE}\'></video>')
        voice.append(
            f'  <audio id="a{s["id"]}" src="assets/voice_clean.wav" data-start="{s["start"]}" '
            f'data-duration="{s["dur"]}" data-media-start="{s["a"]}" data-track-index="{10 + i % 2}" '
            f'data-fade-in="0.015" data-fade-out="0.03"></audio>')
        if s["b"] > BLUR_SRC - 1.0:  # segments that need the blurred plate
            blur.append(
                f'      <video id="b{s["id"]}" class="seg" src="assets/blurred26.mp4" data-start="{s["start"]}" '
                f'data-duration="{s["dur"]}" data-media-start="{fr(s["a"] - BLUR_FILE_OFFSET)}" '
                f'data-track-index="{2 + i % 2}" muted playsinline data-color-grading=\'{GRADE}\'></video>')
    return "\n".join(base), "\n".join(blur), "\n".join(voice)

def cap_html(text, cls):
    parts = text.split("*")
    h = ""
    for i, p in enumerate(parts):
        if not p:
            continue
        # never break inside a hyphenated word (MACAM-MACAM)
        p = " ".join(f'<span class="nw">{w}</span>' if "-" in w else w for w in p.split(" "))
        h += f'<span class="{cls}">{p}</span>' if i % 2 else p
    return h

def cap_size(text):
    n = len(text.replace("*", ""))
    return "" if n < 15 else ' style="font-size:66px"' if n < 20 else ' style="font-size:62px"'

def caption_tags():
    tags = []
    for i, (a, b, text, cls) in enumerate(CAPTIONS):
        tags.append(f'    <div class="cap" id="cap{i}" data-in="{out(a)}" data-out="{out(b)}"><div class="capin"{cap_size(text)}>{cap_html(text, cls)}</div></div>')
    return "\n".join(tags)

def sfx_tags():
    tags = []
    for i, (name, f, src, vol) in enumerate(SFX):
        st = 0.0 if src is None else out(src)
        dur = {"whoosh.mp3": .57, "whoosh-short.mp3": .57, "pop.mp3": .72, "typing.mp3": 1.5, "sparkle.mp3": 1.8,
               "impact-bass-1.mp3": 2.12, "click.mp3": .37, "ping.mp3": 1.32, "chime.mp3": 2.5}[f]
        dur = min(dur, TOTAL - st)
        tags.append(f'  <audio id="sfx-{name}" src="assets/sfx/{f}" data-start="{st}" data-duration="{round(dur,3)}" data-track-index="{20 + i}" data-volume="{vol}"></audio>')
    return "\n".join(tags)

base_v, blur_v, voice_a = video_tags()
zooms = [(s["start"], s["z"]) for s in segs]
caps = [(out(a), out(b)) for a, b, *_ in CAPTIONS]

html = open(os.path.join(os.path.dirname(__file__), "template.hf.tpl")).read()
html = (html.replace("{{TOTAL}}", str(TOTAL))
            .replace("{{BASE_VIDEOS}}", base_v)
            .replace("{{BLUR_VIDEOS}}", blur_v)
            .replace("{{CAPTIONS}}", caption_tags())
            .replace("{{SFX}}", voice_a + "\n" + MUSIC + "\n" + sfx_tags())
            .replace("{{T_JSON}}", json.dumps(T))
            .replace("{{ZOOMS_JSON}}", json.dumps(zooms)))
open(os.path.join(os.path.dirname(__file__), "index.html"), "w").write(html)

print(f"total {TOTAL}s")
for s in segs:
    print(f'  {s["id"]}: src {s["a"]:.3f}-{s["b"]:.3f} -> out {s["start"]:.3f}+{s["dur"]:.3f}')
print(json.dumps(T, indent=1))
