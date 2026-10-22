"""Sediakan aset dari mockup asal: padam peta & logo lama, upscale 2x, letak logo baharu,
potong teks & skyline belakang.

Guna: python3 src/prepare.py   (perlu opencv-python-headless, pillow, numpy)
"""
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, 'assets', *p)

subprocess.run([sys.executable, os.path.join(ROOT, 'src', 'erase.py'), A('asal-mockup.webp'), A('base.png')], check=True)
# logo lama: (pusat x, pusat y, jejari x, jejari y) kawasan dipadam + diameter logo baharu (px imej asal)
LOGOS = [((766, 172, 160, 172), 345),   # logo besar atas
         ((240, 493, 118, 108), 236),   # depan lengan pendek
         ((990, 495, 112, 108), 226)]   # depan lengan panjang

bgr = cv2.imread(A('base.png'))
mask = np.zeros(bgr.shape[:2], np.uint8)
for (cx, cy, rx, ry), _ in LOGOS:
    cv2.ellipse(mask, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
bgr = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
im = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
im2 = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
im2 = im2.convert('RGBA')

logo = Image.open(A('logo-baru.webp')).convert('RGBA')
logo = logo.crop(logo.getchannel('A').point(lambda a: 255 if a > 40 else 0).getbbox())
for (cx, cy, _, _), d in LOGOS:
    w = d * 2
    h = round(w * logo.height / logo.width)
    lg = logo.resize((w, h), Image.LANCZOS)
    x, y = cx * 2 - w // 2, cy * 2 - h // 2
    # bayang lembut supaya logo duduk atas latar / fabrik
    sh = Image.new('RGBA', lg.size, (0, 0, 0, 0))
    sh.putalpha(lg.getchannel('A').point(lambda a: int(a * 0.7)))
    sh = sh.filter(ImageFilter.GaussianBlur(w * 0.02))
    im2.alpha_composite(sh, (x, y + round(w * 0.012)))
    im2.alpha_composite(lg, (x, y))
im2 = im2.convert('RGB')
im2.save(A('base@2x.jpg'), quality=93)
os.remove(A('base.png'))
os.remove(A('base_mask.png'))


def cut(box, out):
    """Potong kawasan imej, latar gelap dijadikan lutsinar."""
    c = np.asarray(im2.convert('RGB').crop(tuple(v * 2 for v in box))).astype(np.float32)
    a = np.clip((c.max(axis=2) - 30) * 4.0, 0, 255)
    Image.fromarray(np.dstack([c, a]).astype(np.uint8), 'RGBA').save(out)


cut((452, 365, 668, 450), A('back-title.png'))
cut((452, 522, 668, 642), A('back-skyline.png'))
print('ok: assets/base@2x.jpg, back-title.png, back-skyline.png')
