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
# logo lama: (pusat x, pusat y, jejari x, jejari y) kawasan dipadam, diameter logo baharu (px imej asal),
# dan sama ada logo dicetak pada baju (ikut lengkung badan + cahaya kain) atau logo paparan biasa
LOGOS = [((766, 172, 160, 172), 345, False),   # logo besar atas
         ((240, 493, 118, 108), 214, True),    # depan lengan pendek
         ((990, 495, 112, 108), 206, True)]    # depan lengan panjang

bgr = cv2.imread(A('base.png'))
mask = np.zeros(bgr.shape[:2], np.uint8)
for (cx, cy, rx, ry), _, _ in LOGOS:
    cv2.ellipse(mask, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
bgr = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
# kawasan yang diinpaint jadi kelabu licin; gelapkan supaya serasi dengan fabrik hitam
m = cv2.GaussianBlur(mask, (0, 0), 6).astype(np.float32)[..., None] / 255.0
bgr = (bgr * (1 - m) + bgr * 0.35 * m).astype(np.uint8)
im = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
im2 = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
im2 = im2.convert('RGBA')

logo = Image.open(A('logo-baru.webp')).convert('RGBA')
logo = logo.crop(logo.getchannel('A').point(lambda a: 255 if a > 40 else 0).getbbox())


def on_shirt(lg, x, y):
    """Lilit logo pada badan (silinder) + darab dengan cahaya/lipatan kain dari mockup."""
    a = np.asarray(lg).astype(np.float32)
    h, w = a.shape[:2]
    half = w / 2
    rc = half * 1.55                      # jejari "badan" (lebih besar dari logo)
    xs = np.arange(w) - half + 0.5
    u = rc * np.arcsin(np.clip(xs / rc, -1, 1))
    u = u / u.max() * half                # kekalkan lebar asal di tengah, mampat di tepi
    mapx = np.tile((u + half - 0.5).astype(np.float32), (h, 1))
    mapy = np.tile(np.arange(h, dtype=np.float32)[:, None], (1, w))
    a = cv2.remap(a, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    # cahaya kain: luminans mockup dikaburkan, dinormalkan ke purata
    region = np.asarray(im2.crop((x, y, x + w, y + h)).convert('L')).astype(np.float32)
    shade = cv2.GaussianBlur(region, (0, 0), w * 0.06)
    shade = np.clip(shade / max(shade.mean(), 1) , 0.72, 1.12)
    shade = 0.72 + 0.28 * shade           # lembutkan kesan
    fall = 0.88 + 0.12 * np.cos(np.arcsin(np.clip(xs / rc, -1, 1)) * 1.6)  # gelap sikit di tepi badan
    a[..., :3] *= (shade * fall[None, :])[..., None]
    # tepi hitam paling luar diserap ke fabrik hitam supaya tak nampak macam sticker
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    lum = a[..., :3].max(axis=2)
    edge = np.clip((r - 0.90) / 0.08, 0, 1) * np.clip((60 - lum) / 40, 0, 1)
    a[..., 3] *= 1 - edge
    a[..., 3] *= 0.97                     # dakwat sublimasi, bukan sticker
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


for (cx, cy, _, _), d, shirt in LOGOS:
    w = d * 2
    h = round(w * logo.height / logo.width)
    lg = logo.resize((w, h), Image.LANCZOS)
    x, y = cx * 2 - w // 2, cy * 2 - h // 2
    if shirt:
        im2.alpha_composite(on_shirt(lg, x, y), (x, y))
        continue
    # logo paparan: bayang lembut atas latar
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
