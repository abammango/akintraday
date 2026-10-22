"""Sediakan aset dari mockup asal: padam peta lama, upscale 2x, potong teks & skyline belakang.

Guna: python3 src/prepare.py   (perlu opencv-python-headless, pillow, numpy)
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, 'assets', *p)

subprocess.run([sys.executable, os.path.join(ROOT, 'src', 'erase.py'), A('asal-mockup.webp'), A('base.png')], check=True)
im = Image.open(A('base.png'))
im2 = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
im2.convert('RGB').save(A('base@2x.jpg'), quality=93)
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
