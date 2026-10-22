# Jersi Kawasaki ZX Empire Owner Sarawak — Katalog 4 Page

Peta Sarawak di belakang baju diganti dengan **cutout peta Sarawak sebenar** (outline Natural Earth) dan
**17 nama bahagian / daerah**. Konsep dan warna asal dikekalkan: isi kelabu grunge dengan outline hijau neon.

## Output (`output/`)
| Fail | Isi |
|---|---|
| `page-01-lengan-pendek.png` | Info detail lengan pendek: mockup, sorotan rekaan, peta baharu, spesifikasi, carta saiz |
| `page-02-lengan-panjang.png` | Info detail lengan panjang: mockup, close-up belakang & cuff, spesifikasi, carta saiz |
| `page-03-pola-potong.png` | Pola potong (saiz M, cm) untuk lengan pendek & lengan panjang |
| `page-04-overall-berminat.png` | Gambar overall + end card **BERMINAT NAK BELI?** |
| `katalog-jersi-zx-empire-sarawak.pdf` | Semua 4 page dalam satu PDF |
| `overall-baju-peta-baharu.png` | Mockup overall (3072×2048) dengan peta baharu |
| `peta-sarawak-artwork.png` | Artwork peta sahaja, latar lutsinar (untuk designer / cetakan) |

`assets/peta-sarawak.svg` ialah versi vektor peta (font tertanam) untuk cetakan sublimasi.

## Edit & jana semula
- No. WhatsApp / nama admin: ubah `CONTACT` dalam `src/build.py`.
- Nama daerah & kedudukan label: senarai `PLACES` dalam `src/build.py`.
- Carta saiz: `CHEST`, `LENGTH`, `SLEEVE_LONG` dalam `src/build.py`.

```sh
python3 src/prepare.py                      # sekali sahaja: padam peta lama dari mockup asal
python3 src/build.py                        # jana katalog.html + assets/peta-sarawak.svg
NODE_PATH=$(npm root -g) node src/render.js # render PNG + PDF ke output/
```

Carta saiz dan ukuran pola ialah ukuran rujukan biasa jersi sublimasi. Sahkan dengan supplier sebelum potong.
