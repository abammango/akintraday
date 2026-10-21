# ChatGPT vs Claude — Hyperframes edit

Short-form talking-head edit (1080x1920) built with [Hyperframes](https://npm.im/hyperframes).
Raw footage: `video_20261021_211339.mp4` (48.8s) → edit 28.8s.

## Transkrip (dengan keputusan edit)

| Source | Ucapan | Status |
| --- | --- | --- |
| 0.28–1.33 | Assalamualaikum guys, | dibuang — mula terus dengan hook |
| 1.33–3.1 | Korang masih guna ChatGPT ke? | **HOOK** + logo ChatGPT atas jari |
| 4.3–6.8 | Aku rasa lebih baik korang guna Claude. | ChatGPT → Claude |
| 7.2–9.3 | Yang lebih berbaloi yang aku rasa sekarang. | dibuang (ulang) |
| 10.2–11.4 | Sebab… sebab… | dibuang (gagap) |
| 11.7–19.3 | Dalam Claude korang boleh buat macam-macam. Dia tak semestinya teks. Dia boleh buat benda macam-macam kreatif. | chips + typing "abammango" atas jari |
| 13.4–13.9 | (jeda + suara anak) | dibuang |
| 19.3–21.2 | (jeda) | dibuang |
| 21.2–24.0 | OK, contoh macam sekarang, kalau tengok background aku biasa kan? | tag BACKGROUND: BIASA |
| 24.3–29.6 | Tapi kalau aku suruh Claude ubah background ni jadi blur | kad prompt Claude + background blur tepat pada "blur" |
| 30.6–36.5 | Dia akan blur. Ya? Ya. OK. | dibuang (ulang / janggal) |
| 36.6–43.9 | Lepas ni aku akan share macam mana nak gabungkan Claude dengan GitHub. | logo Claude + GitHub atas jari → NEXT VIDEO |
| 39.6–40.15 | (jeda + suara anak) | dibuang |
| 45.3–48.4 | Apa pun jangan lupa follow. 👍 | butang FOLLOW @abammango |

## Audio & warna

- **Suara** (`tools/clean_voice.py` → `assets/voice_clean.wav`): buang hum 48.7 Hz + harmonik, mask harmonik suara dewasa di tempat suara anak bertindih, noise reduction, EQ, kompresi, -16 LUFS. Video di-mute; bunyi datang dari track ini pada jam yang sama.
- **Muzik** (`tools/music.py` → `assets/music_bed.wav`): lo-fi/tech groove original (disintesis, tiada sampel/lesen). Tempo dikira supaya bar 7 jatuh tepat pada "blur": breakdown + riser semasa prompt ditaip, drop + crash pada blur. Auto-duck bawah suara (-12 dB semasa bercakap).
- **Grade**: "premium plus" (`grade/grades2.json`, calon E) — skin-soft base, kontras lebih, hijau dinding dinetralkan, wheels teal/warm, vignette. Dipakai pada semua klip video melalui `data-color-grading`.

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
ffmpeg -i assets/source.mp4 -vn -ac 2 -ar 48000 src48.wav
python3 tools/clean_voice.py src48.wav assets/voice_clean.wav
python3 gen.py
python3 tools/music.py timing.json assets/voice_clean.wav assets/music_bed.wav
```

Preview: `npx hyperframes render -q draft -o renders/preview.mp4` — final: `npx hyperframes render -q delivery`.
