#!/usr/bin/env python3
"""Side-by-side RAW vs Claude edit (1080x1920), synced on the same moments.

Left: the untouched source at the same source ranges the edit uses (no grade,
no zoom, no overlays). Right: the rendered edit with its sound. Every cut
flashes a "dibuang" badge on the RAW panel with how much was removed.

usage: python3 gen_compare.py   (expects timing.json + assets/edit.mp4)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TM = json.load(open(os.path.join(HERE, "timing.json")))
SEGS, TOTAL = TM["segments"], TM["total"]
RAW_LEN = 48.833
HOLD = 1.6                     # end card after the edit finishes
DUR = round(TOTAL + HOLD, 3)

raw = []
for i, s in enumerate(SEGS):
    raw.append(f'        <video id="r{s["id"]}" class="pv" src="assets/source.mp4" data-start="{s["start"]}" '
               f'data-duration="{s["dur"]}" data-media-start="{s["a"]}" data-track-index="{i % 2}" muted playsinline></video>')

cuts = []  # (output time, seconds removed)
prev_end = 0.0
for s in SEGS:
    gap = s["a"] - prev_end
    if gap > 0.25:
        cuts.append((s["start"], round(gap, 1)))
    prev_end = s["b"]
removed = round(RAW_LEN - TOTAL, 1)

badges = "\n".join(f'          <div class="cut abs" id="cut{i}"><span>&#9986;</span> {g:.1f}s dibuang</div>'
                   for i, (_, g) in enumerate(cuts))

html = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Raw vs Claude edit</title>
    <script src="assets/js/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Montserrat"; font-weight: 800; src: url("assets/fonts/montserrat-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Montserrat"; font-weight: 900; src: url("assets/fonts/montserrat-latin-900-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 500; src: url("assets/fonts/poppins-latin-500-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-latin-600-normal.woff2") format("woff2"); }}
      html, body {{ margin: 0; background: #0c0c0e; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: radial-gradient(120% 70% at 50% 35%, #1d1a18 0%, #0c0c0e 70%); }}
      .abs {{ position: absolute; }}
      #title {{ left: 0; right: 0; top: 120px; text-align: center; font-family: Montserrat; font-weight: 900; font-size: 92px; color: #fff; letter-spacing: 1px; }}
      #title i {{ font-style: normal; color: #F08A5D; }}
      #sub {{ left: 0; right: 0; top: 232px; text-align: center; font-family: Poppins; font-weight: 500; font-size: 36px; color: #a9a39b; }}
      .panel {{ top: 330px; width: 516px; height: 917px; border-radius: 28px; overflow: hidden; background: #000; }}
      #pl {{ left: 16px; box-shadow: 0 0 0 3px #3a3a3e; }}
      #pr {{ left: 548px; box-shadow: 0 0 0 4px #F08A5D, 0 0 60px rgba(240,138,93,.35); }}
      .pv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .tag {{ top: 22px; left: 22px; font-family: Montserrat; font-weight: 900; font-size: 34px; padding: 10px 22px; border-radius: 14px; z-index: 5; }}
      #tl {{ background: rgba(0,0,0,.7); color: #fff; border: 2px solid rgba(255,255,255,.6); }}
      #tr {{ background: #F08A5D; color: #1a0f0a; }}
      .cut {{ left: 50%; top: 46%; font-family: Montserrat; font-weight: 900; font-size: 40px; color: #fff; background: #e5383b;
              padding: 16px 28px; border-radius: 16px; white-space: nowrap; z-index: 6; opacity: 0; box-shadow: 0 10px 30px rgba(0,0,0,.5); }}
      .time {{ top: 1268px; width: 516px; text-align: center; font-family: Montserrat; font-weight: 900; font-size: 54px; color: #fff; }}
      .time small {{ display: block; font-family: Poppins; font-weight: 500; font-size: 28px; color: #8f8a84; margin-top: 2px; }}
      #timl {{ left: 16px; }} #timr {{ left: 548px; color: #F08A5D; }}
      #list {{ left: 70px; right: 70px; top: 1440px; display: grid; grid-template-columns: 1fr 1fr; gap: 22px 30px; }}
      .it {{ font-family: Poppins; font-weight: 600; font-size: 31px; color: #ece6df; display: flex; align-items: center; gap: 14px; opacity: 0; }}
      .it b {{ width: 16px; height: 16px; border-radius: 50%; background: #F08A5D; flex: none; }}
      #endcard {{ inset: 0; background: rgba(12,12,14,.86); display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; z-index: 20; }}
      #endcard .big {{ font-family: Montserrat; font-weight: 900; font-size: 120px; color: #fff; }}
      #endcard .big i {{ font-style: normal; color: #F08A5D; }}
      #endcard .sm {{ font-family: Poppins; font-weight: 600; font-size: 40px; color: #cfc8bf; margin-top: 18px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cmp" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR}">
      <div id="title" class="abs">RAW <i>vs</i> EDIT</div>
      <div id="sub" class="abs">Diedit oleh Claude &middot; Hyperframes</div>

      <div id="pl" class="abs panel">
{chr(10).join(raw)}
        <div id="tl" class="abs tag">RAW</div>
{badges}
      </div>
      <div id="pr" class="abs panel">
        <video id="edit" class="pv" src="assets/edit.mp4" data-start="0" data-duration="{TOTAL}" data-media-start="0" data-track-index="2" playsinline data-has-audio="true"></video>
        <div id="tr" class="abs tag">CLAUDE EDIT</div>
      </div>

      <div id="timl" class="abs time">{RAW_LEN:.1f}s<small>video asal</small></div>
      <div id="timr" class="abs time">{TOTAL:.1f}s<small>lepas edit (-{removed:.1f}s)</small></div>

      <div id="list" class="abs">
        <div class="it"><b></b>Hook kuat di saat pertama</div>
        <div class="it"><b></b>Ulangan &amp; jeda dibuang</div>
        <div class="it"><b></b>Suara anak &amp; hum dibuang</div>
        <div class="it"><b></b>Muzik original + SFX</div>
        <div class="it"><b></b>Color grade premium</div>
        <div class="it"><b></b>Motion graphics &amp; caption</div>
        <div class="it"><b></b>Background blur AI</div>
        <div class="it"><b></b>Logo &amp; typing atas jari</div>
      </div>

      <div id="endcard" class="abs"><div class="big">{RAW_LEN:.0f}s &rarr; <i>{TOTAL:.0f}s</i></div><div class="sm">Diedit sepenuhnya oleh Claude</div></div>
    </div>
    <script>
      const CUTS = {json.dumps(cuts)};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#title", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 0);
      tl.fromTo("#sub", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.2);
      tl.fromTo(".it", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.12, ease: "power2.out" }}, 0.5);
      CUTS.forEach(([t], i) => {{
        const el = "#cut" + i;
        tl.set(el, {{ xPercent: -50, yPercent: -50 }}, 0);
        tl.fromTo(el, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "back.out(2.5)" }}, t);
        tl.to(el, {{ opacity: 0, duration: 0.2 }}, t + 0.75);
      }});
      tl.fromTo("#endcard", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {TOTAL});
      tl.fromTo("#endcard .big", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2)" }}, {TOTAL});
      window.__timelines["cmp"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(HERE, "index.html"), "w").write(html)
print("duration", DUR, "cuts", cuts)
