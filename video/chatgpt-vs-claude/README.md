# ChatGPT vs Claude — Hyperframes edit

Short-form talking-head edit (1080x1920) built with [Hyperframes](https://npm.im/hyperframes).
Raw footage: `video_20261021_211339.mp4` (48.8s) → edit 29.9s.

## Transkrip (dengan keputusan edit)

| Source | Ucapan | Status |
| --- | --- | --- |
| 0.28–1.2 | Assalamualaikum guys, | dibuang — mula terus dengan hook |
| 1.2–3.1 | Korang masih guna ChatGPT ke? | **HOOK** + logo ChatGPT atas jari |
| 4.3–6.8 | Aku rasa lebih baik korang guna Claude. | ChatGPT → Claude |
| 7.2–9.3 | Yang lebih berbaloi yang aku rasa sekarang. | dibuang (ulang) |
| 10.2–11.4 | Sebab… sebab… | dibuang (gagap) |
| 11.7–19.3 | Dalam Claude korang boleh buat macam-macam. Dia tak semestinya teks. Dia boleh buat benda macam-macam kreatif. | chips + typing "abammango" atas jari |
| 19.3–21.2 | (jeda) | dibuang |
| 21.2–24.0 | OK, contoh macam sekarang, kalau tengok background aku biasa kan? | tag BACKGROUND: BIASA |
| 24.3–29.6 | Tapi kalau aku suruh Claude ubah background ni jadi blur | kad prompt Claude + background blur tepat pada "blur" |
| 30.6–36.5 | Dia akan blur. Ya? Ya. OK. | dibuang (ulang / janggal) |
| 36.6–43.9 | Lepas ni aku akan share macam mana nak gabungkan Claude dengan GitHub. | logo Claude + GitHub atas jari → NEXT VIDEO |
| 45.3–48.4 | Apa pun jangan lupa follow. 👍 | butang FOLLOW @abammango |

## Struktur

- `gen.py` — semua keputusan edit (cut, zoom, caption, SFX) dalam jadual masa *source*. Jalankan `python3 gen.py` untuk jana `index.html`.
- `template.hf.tpl` — layout, gaya dan GSAP timeline untuk motion graphics.
- `assets/` — fonts (Montserrat/Poppins), logo (LobeHub icons), SFX (Hyperframes bundled library, lihat `assets/sfx/CREDITS.md`), GSAP.
- `tools/` — skrip transcribe (Whisper large-v3 via sherpa-onnx), finger tracking dan compositor background blur.

Fail video besar tidak di-commit (`assets/source.mp4`, `assets/blurred26.mp4`, `renders/`). Untuk jana semula:

```bash
ffmpeg -i video_20261021_211339.mp4 -c:v libx264 -crf 16 -pix_fmt yuv420p -r 30 -g 15 -c:a aac -b:a 192k assets/source.mp4
ffmpeg -ss 26.0 -i assets/source.mp4 -c:v libx264 -crf 14 -pix_fmt yuv420p -r 30 -an sub26.mp4
npx hyperframes remove-background sub26.mp4 -o cutout26.webm --quality best
python3 tools/blur.py sub26.mp4 cutout26.webm assets/blurred26.mp4 -
```

Preview: `npx hyperframes render -q draft -o renders/preview.mp4` — final: `npx hyperframes render -q delivery`.
