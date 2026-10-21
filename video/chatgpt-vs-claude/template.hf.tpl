<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>ChatGPT vs Claude</title>
    <script src="assets/js/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Montserrat"; font-weight: 800; src: url("assets/fonts/montserrat-latin-800-normal.woff2") format("woff2"); }
      @font-face { font-family: "Montserrat"; font-weight: 900; src: url("assets/fonts/montserrat-latin-900-normal.woff2") format("woff2"); }
      @font-face { font-family: "Poppins"; font-weight: 500; src: url("assets/fonts/poppins-latin-500-normal.woff2") format("woff2"); }
      @font-face { font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-latin-600-normal.woff2") format("woff2"); }

      html, body { margin: 0; background: #000; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }

      /* footage */
      #stage { position: absolute; inset: 0; transform-origin: 540px 850px; }
      #base, #blurlayer { position: absolute; inset: 0; }
      #blurlayer { opacity: 0; }
      video.seg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }

      /* overlay layer */
      #ui { position: absolute; inset: 0; pointer-events: none; }
      .abs { position: absolute; left: 0; top: 0; opacity: 0; }
      .logo { width: 180px; height: 180px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .logo img { width: 62%; height: 62%; }
      .logo.gpt { box-shadow: 0 0 0 6px rgba(25,195,125,.55), 0 18px 50px rgba(0,0,0,.35); }
      .logo.claude { background: #fff6f1; box-shadow: 0 0 0 6px rgba(217,119,87,.6), 0 0 60px rgba(217,119,87,.55); }
      .logo.gh { box-shadow: 0 0 0 6px rgba(255,255,255,.6), 0 18px 50px rgba(0,0,0,.4); }
      .strike { position: absolute; left: -6%; top: 47%; width: 112%; height: 16px; background: #ff3b3b; border-radius: 8px; transform-origin: left center; box-shadow: 0 2px 10px rgba(0,0,0,.4); }
      #arrow { font-family: "Montserrat"; font-weight: 900; font-size: 110px; color: #fff; text-shadow: 0 6px 20px rgba(0,0,0,.5); }

      .chip { font-family: "Montserrat"; font-weight: 800; font-size: 40px; color: #111; background: #fff; padding: 14px 30px; border-radius: 999px; box-shadow: 0 10px 30px rgba(0,0,0,.3); white-space: nowrap; }
      .chip b { color: #D97757; }

      #typebox { isolation: isolate; width: 430px; height: 112px; border-radius: 30px; background: #fff; box-shadow: 0 16px 50px rgba(0,0,0,.35), 0 0 0 5px rgba(217,119,87,.55); display: flex; align-items: center; padding: 0 30px; box-sizing: border-box; }
      #typebox .txt { font-family: "Poppins"; font-weight: 600; font-size: 56px; color: #1a1a1a; letter-spacing: .5px; }
      #typebox .tail { position: absolute; left: 70px; bottom: -22px; width: 44px; height: 44px; background: #fff; transform: rotate(45deg); border-radius: 6px; }
      .caret { display: inline-block; width: 5px; height: 58px; background: #D97757; margin-left: 4px; vertical-align: -8px; }
      .ch { opacity: 0; }

      #bgtag { font-family: "Montserrat"; font-weight: 800; font-size: 40px; color: #fff; background: rgba(0,0,0,.72); padding: 16px 30px; border-radius: 18px; white-space: nowrap; border: 3px solid rgba(255,255,255,.85); }
      #bgtag i { font-style: normal; color: #FFD43B; }

      #card { width: 900px; border-radius: 34px; background: #faf9f5; box-shadow: 0 24px 70px rgba(0,0,0,.45); padding: 26px 30px 26px; box-sizing: border-box; }
      #card .hd { display: flex; align-items: center; gap: 14px; font-family: "Poppins"; font-weight: 600; font-size: 34px; color: #3d3929; }
      #card .hd img { width: 46px; height: 46px; }
      #card .row { margin-top: 18px; display: flex; align-items: center; gap: 18px; background: #fff; border: 2px solid #e6e1d6; border-radius: 22px; padding: 18px 18px 18px 26px; }
      #card .prompt { flex: 1; font-family: "Poppins"; font-weight: 500; font-size: 42px; color: #1f1e1d; white-space: nowrap; overflow: hidden; }
      #card .send { width: 74px; height: 74px; border-radius: 18px; background: #D97757; display: flex; align-items: center; justify-content: center; color: #fff; font-family: "Montserrat"; font-weight: 900; font-size: 44px; }
      #card .done { margin-top: 16px; font-family: "Poppins"; font-weight: 600; font-size: 34px; color: #2e7d32; opacity: 0; }

      #flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .spark { position: absolute; left: 0; top: 0; width: 64px; height: 64px; opacity: 0; }
      .spark svg { width: 100%; height: 100%; }

      #combo { display: flex; align-items: center; gap: 26px; }
      #combo .plus { font-family: "Montserrat"; font-weight: 900; font-size: 90px; color: #fff; text-shadow: 0 6px 20px rgba(0,0,0,.5); }
      #nextlbl { font-family: "Montserrat"; font-weight: 900; font-size: 46px; color: #111; background: #FFD43B; padding: 10px 26px; border-radius: 14px; white-space: nowrap; }

      #follow { display: flex; align-items: center; gap: 22px; background: #fff; border-radius: 999px; padding: 16px 18px 16px 18px; box-shadow: 0 20px 60px rgba(0,0,0,.45); }
      #follow .av { width: 92px; height: 92px; border-radius: 50%; background: linear-gradient(135deg,#a8432a,#c45f3d); color: #fff; font-family: "Montserrat"; font-weight: 900; font-size: 50px; display: flex; align-items: center; justify-content: center; }
      #follow .nm { font-family: "Poppins"; font-weight: 600; font-size: 44px; color: #111; padding-right: 6px; }
      #follow .btn { position: relative; font-family: "Montserrat"; font-weight: 900; font-size: 40px; color: #fff; background: #fe2c55; border-radius: 999px; padding: 22px 0; width: 330px; text-align: center; white-space: nowrap; }
      #follow .btn .b2 { position: absolute; inset: 0; border-radius: 999px; background: #e9e9ee; color: #333; display: flex; align-items: center; justify-content: center; opacity: 0; }

      /* captions */
      .cap { position: absolute; left: 60px; right: 60px; top: 1360px; height: 200px; display: flex; align-items: center; justify-content: center; opacity: 0; }
      .capin { font-family: "Montserrat"; font-weight: 900; font-size: 78px; line-height: 1.08; color: #fff; text-align: center; -webkit-text-stroke: 12px #000; paint-order: stroke fill; text-shadow: 0 8px 24px rgba(0,0,0,.55); }
      .capin .nw { white-space: nowrap; }
      .capin .gpt { color: #19C37D; }
      .capin .claude { color: #F08A5D; }
      .capin .hl { color: #FFD43B; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{{TOTAL}}">
      <div id="stage">
        <div id="base">
{{BASE_VIDEOS}}
        </div>
        <div id="blurlayer">
{{BLUR_VIDEOS}}
        </div>
      </div>

      <div id="ui">
        <div id="gpt" class="abs logo gpt"><img src="assets/logos/openai.svg" alt="" /><div class="strike" id="strike"></div></div>
        <div id="arrow" class="abs">&#8594;</div>
        <div id="claude" class="abs logo claude"><img src="assets/logos/claude-color.svg" alt="" /></div>

        <div class="abs chip" id="chip0"><b>&#9679;</b> WEBSITE</div>
        <div class="abs chip" id="chip1"><b>&#9679;</b> DESIGN</div>
        <div class="abs chip" id="chip2"><b>&#9679;</b> VIDEO</div>
        <div class="abs chip" id="chip3"><b>&#9679;</b> APP</div>

        <div id="typebox" class="abs"><div class="tail"></div><span class="txt" id="typetxt"></span><span class="caret" id="caret1"></span></div>

        <div id="bgtag" class="abs">BACKGROUND: <i>BIASA</i></div>

        <div id="card" class="abs">
          <div class="hd"><img src="assets/logos/claude-color.svg" alt="" />Claude</div>
          <div class="row"><div class="prompt"><span id="prompttxt"></span><span class="caret" id="caret2" style="height:46px;width:4px;vertical-align:-6px"></span></div><div class="send" id="send">&#8593;</div></div>
          <div class="done" id="done">&#10003; Siap! Background dah blur</div>
        </div>

        <div id="flash"></div>
        <div id="sparks"></div>

        <div id="claude2" class="abs logo claude"><img src="assets/logos/claude-color.svg" alt="" /></div>
        <div id="gh" class="abs logo gh"><img src="assets/logos/github.svg" alt="" /></div>
        <div id="plus" class="abs" style="font-family:Montserrat;font-weight:900;font-size:96px;color:#fff;text-shadow:0 6px 20px rgba(0,0,0,.5)">+</div>
        <div id="nextlbl" class="abs">NEXT VIDEO</div>

        <div id="follow" class="abs"><div class="av">A</div><div class="nm">@abammango</div><div class="btn" id="fbtn">FOLLOW<div class="b2" id="fbtn2">&#10003; FOLLOWING</div></div></div>
      </div>

      <div id="captions">
{{CAPTIONS}}
      </div>

{{SFX}}
    </div>

    <script>
      const T = {{T_JSON}};
      const ZOOMS = {{ZOOMS_JSON}};
      const ORIGIN = [540, 850];
      const tl = gsap.timeline({ paused: true });

      // screen position of a footage point while the stage is zoomed by z
      const scr = (x, y, z) => [ORIGIN[0] + (x - ORIGIN[0]) * z, ORIGIN[1] + (y - ORIGIN[1]) * z];
      const place = (sel, x, y, extra = {}) => tl.set(sel, Object.assign({ x, y, xPercent: -50, yPercent: -50 }, extra), 0);
      const pop = (sel, at, from = 0.2) => tl.fromTo(sel, { scale: from, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2.2)" }, at);
      const bob = (sel, at, until, amp = 10) => {
        const n = Math.max(1, Math.floor((until - at) / 0.9));
        tl.to(sel, { y: "-=" + amp, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, at);
      };
      const typeInto = (el, text, at, cps) => {
        const host = document.querySelector(el);
        [...text].forEach((c, i) => {
          const s = document.createElement("span");
          s.className = "ch";
          s.textContent = c === " " ? " " : c;
          host.appendChild(s);
          tl.set(s, { opacity: 1 }, at + i / cps);
        });
      };
      const blink = (sel, from, to) => {
        for (let t = from; t < to; t += 0.5) tl.set(sel, { opacity: 0 }, t + 0.25).set(sel, { opacity: 1 }, t + 0.5);
      };

      // ---------- camera: punch-in per cut (hides jump cuts)
      tl.fromTo("#stage", { scale: 1.32 }, { scale: ZOOMS[0][1], duration: 0.45, ease: "power3.out" }, 0);
      tl.fromTo("#flash", { opacity: 0.55 }, { opacity: 0, duration: 0.35, ease: "power2.out" }, 0);
      ZOOMS.slice(1).forEach(([t, z]) => tl.set("#stage", { scale: z }, t));

      // ---------- 1. ChatGPT logo floating on the finger
      {
        const z = ZOOMS[0][1];
        const [x, y] = scr(198, 660, z);
        place("#gpt", x, y);
        pop("#gpt", T.gpt_in);
        tl.to("#gpt", { y: y - 10, duration: 0.28, ease: "sine.out" }, T.gpt_in + 0.32);
        // at the cut it flies to the top: ChatGPT  ->  Claude
        tl.to("#gpt", { x: 300, y: 330, scale: 0.85, duration: 0.38, ease: "power3.inOut" }, T.seg_b);
        place("#arrow", 540, 330);
        place("#claude", 780, 330);
        tl.fromTo("#arrow", { opacity: 0, x: 500 }, { opacity: 1, x: 540, duration: 0.3, ease: "power2.out" }, T.claude_in - 0.25);
        pop("#claude", T.claude_in, 0.1);
        tl.fromTo("#strike", { scaleX: 0 }, { scaleX: 1, duration: 0.22, ease: "power2.out" }, T.claude_in + 0.05);
        tl.to("#gpt", { opacity: 0.55, duration: 0.2 }, T.claude_in + 0.05);
        tl.to("#claude", { scale: 1.15, duration: 0.15, yoyo: true, repeat: 1, ease: "power1.inOut" }, T.claude_in + 0.32);
        tl.to(["#gpt", "#arrow", "#claude"], { y: "-=60", opacity: 0, duration: 0.3, ease: "power2.in", stagger: 0.05 }, T.seg_c + 0.15);
      }

      // ---------- 2. "macam-macam" chips
      {
        const pos = [[250, 260], [820, 230], [230, 430], [860, 420]];
        pos.forEach(([x, y], i) => {
          place("#chip" + i, x, y, { rotation: i % 2 ? 4 : -4 });
          pop("#chip" + i, T.chips_in + i * 0.12);
        });
        tl.to(".chip", { scale: 0.6, opacity: 0, duration: 0.2, ease: "power2.in", stagger: 0.04 }, T.chips_out - 0.3);
      }

      // ---------- 3. typing "abammango" above the finger
      {
        place("#typebox", 255, 455);
        pop("#typebox", T.type_in, 0.3);
        typeInto("#typetxt", "abammango", T.type_in + 0.2, 10.5);
        blink("#caret1", T.type_in + 1.1, T.type_out);
        tl.to("#typebox", { y: 443, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3 }, T.type_in + 0.35);
        tl.to("#typebox", { scale: 0.5, opacity: 0, duration: 0.22, ease: "power2.in" }, T.type_out);
      }

      // ---------- 4. background tag
      {
        place("#bgtag", 540, 300);
        pop("#bgtag", T.bgtag_in, 0.4);
        tl.to("#bgtag", { opacity: 0, y: 270, duration: 0.2 }, T.seg_e);
      }

      // ---------- 5. Claude prompt card + MAGIC blur
      {
        place("#card", 540, 330);
        tl.fromTo("#card", { opacity: 0, y: 200 }, { opacity: 1, y: 330, duration: 0.4, ease: "power3.out" }, T.card_in);
        tl.set("#caret2", { opacity: 1 }, 0);
        const prompt = "Ubah background ni jadi blur";
        typeInto("#prompttxt", prompt, T.prompt_in, prompt.length / (T.prompt_end - T.prompt_in));
        tl.to("#send", { scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }, T.send);
        tl.set("#caret2", { opacity: 0 }, T.send);

        // the blur reveal
        tl.fromTo("#blurlayer", { opacity: 1, clipPath: "circle(0% at 50% 42%)" },
                  { opacity: 1, clipPath: "circle(120% at 50% 42%)", duration: 0.55, ease: "power2.out" }, T.blur);
        tl.fromTo("#flash", { opacity: 0 }, { opacity: 0.4, duration: 0.07, yoyo: true, repeat: 1, immediateRender: false }, T.blur);
        tl.to("#stage", { scale: 1.0, duration: 0.6, ease: "power2.out" }, T.blur);
        tl.to("#done", { opacity: 1, duration: 0.25 }, T.blur + 0.35);
        tl.to("#card", { opacity: 0, y: 260, duration: 0.3, ease: "power2.in" }, T.seg_g - 0.05);

        // sparkle burst (deterministic positions)
        const host = document.getElementById("sparks");
        const star = '<svg viewBox="0 0 24 24"><path fill="#fff" d="M12 0 L14.2 9.8 L24 12 L14.2 14.2 L12 24 L9.8 14.2 L0 12 L9.8 9.8 Z"/></svg>';
        const P = [[160,700],[930,640],[260,1020],[860,1080],[540,520],[110,1240],[980,1300],[700,1500],[380,1520],[600,760],[220,560],[880,880]];
        P.forEach(([x, y], i) => {
          const d = document.createElement("div");
          d.className = "spark"; d.innerHTML = star; host.appendChild(d);
          const s = 0.6 + ((i * 37) % 10) / 10;
          tl.set(d, { x, y, xPercent: -50, yPercent: -50 }, 0);
          tl.fromTo(d, { scale: 0, opacity: 0, rotation: 0 },
                    { scale: s, opacity: 1, rotation: 90, duration: 0.25, ease: "back.out(3)" }, T.blur + i * 0.035);
          tl.to(d, { scale: 0, opacity: 0, rotation: 180, duration: 0.3, ease: "power2.in" }, T.blur + 0.3 + i * 0.035);
        });
      }

      // ---------- 6. Claude + GitHub
      {
        place("#claude2", 790, 360);
        pop("#claude2", T.claude2_in, 0.1);
        bob("#claude2", T.claude2_in + 0.32, T.gh_out, 8);
        place("#gh", 245, 560);
        pop("#gh", T.gh_in, 0.1);
        place("#plus", 520, 450);
        tl.fromTo("#plus", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, T.gh_in + 0.25);
        // merge into a "next video" badge at the top
        tl.to("#gh", { x: 330, y: 330, scale: 0.85, duration: 0.45, ease: "power3.inOut" }, T.gh_out);
        tl.to("#claude2", { x: 750, y: 330, scale: 0.85, duration: 0.45, ease: "power3.inOut" }, T.gh_out);
        tl.to("#plus", { x: 540, y: 330, duration: 0.45, ease: "power3.inOut" }, T.gh_out);
        place("#nextlbl", 540, 500);
        pop("#nextlbl", T.gh_out + 0.35, 0.5);
        tl.to(["#gh", "#plus", "#claude2", "#nextlbl"], { opacity: 0, y: "-=50", duration: 0.3, stagger: 0.04, ease: "power2.in" }, T.follow_in - 0.35);
      }

      // ---------- 7. follow button
      {
        place("#follow", 540, 360);
        pop("#follow", T.follow_in, 0.4);
        tl.to("#fbtn", { scale: 0.86, duration: 0.09, yoyo: true, repeat: 1 }, T.follow_click);
        tl.set("#fbtn2", { opacity: 1 }, T.follow_click + 0.09);
        tl.to("#follow", { scale: 1.08, duration: 0.14, yoyo: true, repeat: 1, ease: "power1.inOut" }, T.follow_click + 0.1);
      }

      // ---------- captions (one on screen at a time)
      document.querySelectorAll(".cap").forEach((c) => {
        const a = +c.dataset.in, b = +c.dataset.out;
        tl.set(c, { opacity: 1 }, a);
        tl.fromTo(c.firstElementChild, { scale: 0.72, y: 20 }, { scale: 1, y: 0, duration: 0.18, ease: "back.out(2.5)" }, a);
        tl.set(c, { opacity: 0 }, b);
      });

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
