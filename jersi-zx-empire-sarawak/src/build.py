"""Jana katalog 4 muka surat jersi Kawasaki ZX Empire Owner Sarawak.

Output: katalog.html (4 page 1080x1350) + assets/peta-sarawak.svg (artwork peta untuk cetakan).
Jalankan dari folder jersi-zx-empire-sarawak:  python3 src/build.py
"""
import base64
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, 'assets', *p)

NEON = '#8fe31c'
NEON_DK = '#5d9a0c'

# --------------------------------------------------------------------------
# Peta Sarawak
# --------------------------------------------------------------------------
LON0, LAT0, K = 109.45, 5.05, 160.0   # unjuran equirectangular -> viewBox 1008 x 680
MAP_W, MAP_H = 1008, 680
PAD = 40                               # ruang label di luar garisan pantai
VB = (-PAD, -PAD, MAP_W + 2 * PAD, MAP_H + 2 * PAD)


def proj(lon, lat):
    return (lon - LON0) * K, (LAT0 - lat) * K


def land_path():
    g = json.load(open(A('sarawak.geojson')))['geometry']
    parts = []
    for poly in g['coordinates']:
        pts = [proj(x, y) for x, y in poly[0]]
        parts.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z')
    return ''.join(parts)


# (nama, lon, lat, anchor, dx, dy, saiz, jenis)  jenis: town / park
PLACES = [
    ('KUCHING',      110.345, 1.553, 'end',    -14,  26, 24, 'town'),
    ('SANTUBONG',    110.330, 1.720, 'end',    -14,  -6, 24, 'town'),
    ('SAMARAHAN',    110.490, 1.460, 'start',   12, -12, 24, 'town'),
    ('SERIAN',       110.570, 1.170, 'start',   14,  10, 24, 'town'),
    ('BETONG',       111.530, 1.410, 'start',   14,   6, 24, 'town'),
    ('SRI AMAN',     111.460, 1.240, 'start',   14,  20, 24, 'town'),
    ('SARIKEI',      111.520, 2.130, 'end',    -14,   8, 24, 'town'),
    ('SIBU',         111.820, 2.300, 'start',   14,   4, 24, 'town'),
    ('MUKAH',        112.090, 2.900, 'end',    -14,  -2, 24, 'town'),
    ('KAPIT',        112.940, 2.020, 'start',   14,   8, 24, 'town'),
    ('BINTULU',      113.030, 3.170, 'end',    -14,  -6, 24, 'town'),
    ('BELAGA',       113.780, 2.700, 'start',   14,   8, 24, 'town'),
    ('NIAH',         113.780, 3.810, 'end',    -14,   2, 24, 'park'),
    ('MIRI',         113.990, 4.400, 'end',    -16,  -2, 24, 'town'),
    ('GUNUNG MULU',  114.920, 4.050, 'middle',   0,  36, 24, 'park'),
    ('LIMBANG',      115.000, 4.750, 'end',    -14, -10, 24, 'town'),
    ('LAWAS',        115.410, 4.850, 'start',   -6, -24, 24, 'town'),
]


def map_svg(uid, labels=True, embed_fonts=False, width=None, extra_style=''):
    """SVG peta Sarawak: isi kelabu grunge + outline hijau neon (ikut konsep asal di baju)."""
    d = land_path()
    w_attr = f' width="{width}"' if width else ''
    fonts = ''
    if embed_fonts:
        b64 = base64.b64encode(open(A('fonts', 'RussoOne-400.woff2'), 'rb').read()).decode()
        fonts = ("<style>@font-face{font-family:'Russo One';src:url(data:font/woff2;base64,"
                 + b64 + ") format('woff2');}</style>")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, VB))}"{w_attr} '
           f'class="map" style="{extra_style}" role="img" aria-label="Peta Sarawak dengan nama bahagian">',
           fonts,
           '<defs>',
           f'<clipPath id="{uid}-clip"><path d="{d}"/></clipPath>',
           # tompok gelap grunge
           f'<filter id="{uid}-splotch" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
           '<feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="3" seed="11" result="n"/>'
           '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.09  0 0 0 0 0.09  0 0 0 0 0.09  13 0 0 0 -7.4"/>'
           '</filter>',
           # tekstur halus (bintik) supaya nampak macam cetakan grunge
           f'<filter id="{uid}-grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
           '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="n"/>'
           '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -2.2 1.25"/>'
           '</filter>',
           f'<filter id="{uid}-glow" x="-10%" y="-10%" width="120%" height="120%">'
           '<feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
           '</filter>',
           f'<filter id="{uid}-shadow" x="-10%" y="-10%" width="120%" height="120%">'
           '<feGaussianBlur stdDeviation="14"/></filter>',
           f'<linearGradient id="{uid}-fill" x1="0" y1="0" x2="1" y2="1">'
           '<stop offset="0" stop-color="#a3a3a3"/><stop offset="0.55" stop-color="#8a8a8a"/><stop offset="1" stop-color="#6f6f6f"/>'
           '</linearGradient>',
           '</defs>',
           # bayang gelap di belakang supaya peta "terangkat" dari corak baju
           f'<path d="{d}" fill="#000" opacity="0.85" filter="url(#{uid}-shadow)" transform="translate(0 8)"/>',
           f'<path d="{d}" fill="url(#{uid}-fill)"/>',
           f'<g clip-path="url(#{uid}-clip)">'
           f'<rect x="0" y="0" width="{MAP_W}" height="{MAP_H}" filter="url(#{uid}-splotch)" opacity="0.9"/>'
           f'<rect x="0" y="0" width="{MAP_W}" height="{MAP_H}" filter="url(#{uid}-grain)" opacity="0.18"/>'
           '</g>',
           f'<path d="{d}" fill="none" stroke="{NEON}" stroke-width="7" stroke-linejoin="round" filter="url(#{uid}-glow)"/>',
           f'<path d="{d}" fill="none" stroke="#d8ff9a" stroke-width="1.6" stroke-linejoin="round" opacity="0.7"/>',
           ]
    if labels:
        out.append('<g font-family="\'Russo One\', \'Arial Black\', sans-serif" fill="#fff" '
                   'stroke="#070707" stroke-linejoin="round" paint-order="stroke">')
        for name, lon, lat, anchor, dx, dy, size, kind in PLACES:
            x, y = proj(lon, lat)
            if kind == 'park':
                out.append(f'<path d="M{x:.1f},{y - 10:.1f}L{x + 10:.1f},{y + 8:.1f}L{x - 10:.1f},{y + 8:.1f}Z" '
                           f'fill="{NEON}" stroke="#070707" stroke-width="3"/>')
            else:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{NEON}" stroke="#070707" stroke-width="3.5"/>')
            out.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" font-size="{size}" '
                       f'stroke-width="{size * 0.28:.1f}" letter-spacing="1">{name}</text>')
        out.append('</g>')
    out.append('</svg>')
    return ''.join(out)


# --------------------------------------------------------------------------
# Mockup: imej asal (peta lama dipadam) + peta vektor baharu
# --------------------------------------------------------------------------
IMG_W, IMG_H = 1536, 1024
IMG = 'assets/base@2x.jpg'
# kedudukan kawasan daratan peta baharu pada imej asal (px): x, y, lebar
SHIRT_MAPS = [(473, 446, 160), (1236, 452, 148)]
_scene_n = [0]


def scene(cx, cy, cw, ch, width, cls='', inner=''):
    s = width / cw
    _scene_n[0] += 1
    parts = [f'<div class="scene {cls}" style="width:{width:.1f}px;height:{ch * s:.1f}px">',
             f'<img src="{IMG}" alt="" style="left:{-cx * s:.1f}px;top:{-cy * s:.1f}px;width:{IMG_W * s:.1f}px">']
    for i, (mx, my, mw) in enumerate(SHIRT_MAPS):
        u = mw / MAP_W
        left, top = mx - PAD * u, my - PAD * u
        if left > cx + cw or left + VB[2] * u < cx or top > cy + ch or top + VB[3] * u < cy:
            continue
        parts.append(map_svg(f'm{_scene_n[0]}{i}', width=f'{VB[2] * u * s:.1f}',
                             extra_style=f'position:absolute;left:{(left - cx) * s:.1f}px;top:{(top - cy) * s:.1f}px'))
    parts.append(inner)
    parts.append('</div>')
    return ''.join(parts)


def markers(cx, cy, cw, width, pts):
    s = width / cw
    return ''.join(f'<span class="mk" style="left:{(x - cx) * s:.1f}px;top:{(y - cy) * s:.1f}px">{n}</span>'
                   for n, x, y in pts)


# --------------------------------------------------------------------------
# Data saiz / spesifikasi
# --------------------------------------------------------------------------
SIZES = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']
CHEST = [18, 19, 20, 21, 22, 23, 24, 25, 26]
LENGTH = [26, 27, 28, 29, 30, 31, 32, 33, 33]
SLEEVE_LONG = [22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26]


def fmt(v):
    return f'{v:g}'


def size_table(long=False):
    rows = [('Lebar dada', CHEST), ('Panjang badan', LENGTH)]
    if long:
        rows.append(('Panjang lengan', SLEEVE_LONG))
    head = ''.join(f'<th>{s}</th>' for s in SIZES)
    body = ''.join('<tr><td class="rl">' + n + '</td>' + ''.join(f'<td>{fmt(v)}</td>' for v in vals) + '</tr>'
                   for n, vals in rows)
    return f'<table class="sz"><thead><tr><th class="rl">Inci</th>{head}</tr></thead><tbody>{body}</tbody></table>'


def spec_table(items):
    return '<table class="spec">' + ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in items) + '</table>'


def feature_list(items):
    return '<ol class="feat">' + ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in items) + '</ol>'


def header(no, title, sub):
    return (f'<header class="hd"><div class="kick">KAWASAKI • ZX • EMPIRE OWNER • SARAWAK</div>'
            f'<div class="pg">{no:02d}<i>/04</i></div>'
            f'<h1 class="brush">{title}</h1><div class="sub">{sub}</div></header>')


FOOT = '<footer class="ft">• KAWASAKI • ZX • EMPIRE • OWNER • SARAWAK • <span>RIDE TOGETHER · STAY TOGETHER</span></footer>'

# --------------------------------------------------------------------------
# Page 1 & 2
# --------------------------------------------------------------------------
SHORT_CROP = (12, 292, 765, 508)
LONG_CROP = (768, 292, 762, 508)
SCENE_W = 700


def page_short():
    cx, cy, cw, ch = SHORT_CROP
    mk = markers(cx, cy, cw, SCENE_W, [
        (1, 238, 318), (2, 128, 400), (3, 52, 520), (4, 492, 462), (5, 452, 612), (6, 555, 772)])
    feats = [
        ('Kolar bulat rib', 'Rib hijau neon, kemas & selesa.'),
        ('Logo depan penuh', 'Emblem ZX Empire Owner + bendera Sarawak & Malaysia.'),
        ('Lengan pendek', 'Jalur neon di hujung lengan + corak calar.'),
        ('Peta Sarawak baharu', 'Cutout peta Sarawak + nama daerah.'),
        ('Skyline Kuching', 'Jambatan Darul Hana + ZX25R | 4R | 6R | 10R.'),
        ('Logo ZX', 'Logo ZX di bawah depan & belakang.'),
    ]
    spec = spec_table([
        ('Fabrik', '100% Polyester (microfiber) – ringan & cepat kering'),
        ('Cetakan', 'Full sublimation – warna tak pudar, tak merekah'),
        ('Kolar', 'Round neck, rib hijau neon'),
        ('Lengan', 'Pendek (set-in), jalur neon di hujung'),
        ('Potongan', 'Regular fit – unisex'),
        ('Ciri', 'Breathable, serap peluh, sesuai harian & ride'),
        ('Warna', 'Hitam • Hijau Neon Kawasaki • Kelabu'),
    ])
    return f'''
<section class="page">
  {header(1, 'SHORT SLEEVE', 'JERSI LENGAN PENDEK — INFO DETAIL')}
  <div class="row r1">
    <div class="frame fade-tr">{scene(cx, cy, cw, ch, SCENE_W, inner=mk)}
      <div class="tag l">DEPAN</div><div class="tag r">BELAKANG</div></div>
    <aside class="side"><h3>SOROTAN REKAAN</h3>{feature_list(feats)}</aside>
  </div>
  <div class="row r2">
    <div class="panel mapbox">
      <h3>PETA SARAWAK <em>VERSI BAHARU</em></h3>
      <p class="note">Cutout peta Sarawak sahaja • konsep &amp; warna asal dikekalkan • 17 nama bahagian / daerah</p>
      {map_svg('p1big', width='440')}
    </div>
    <div class="panel"><h3>SPESIFIKASI</h3>{spec}</div>
  </div>
  <div class="panel szp"><h3>CARTA SAIZ <em>LENGAN PENDEK</em></h3>{size_table()}
    <p class="note">Ukuran dalam inci (lebar dada × panjang badan, diukur rata). Toleransi ±1 inci.</p></div>
  {FOOT}
</section>'''


def page_long():
    cx, cy, cw, ch = LONG_CROP
    mk = markers(cx, cy, cw, SCENE_W, [
        (1, 990, 318), (2, 878, 400), (3, 812, 560), (4, 1252, 466), (5, 1212, 612), (6, 792, 768)])
    feats = [
        ('Kolar bulat rib', 'Rib hijau neon, kemas & selesa.'),
        ('Logo depan penuh', 'Emblem ZX Empire Owner + bendera Sarawak & Malaysia.'),
        ('Lengan panjang', 'Corak calar & jalur neon sepanjang lengan.'),
        ('Peta Sarawak baharu', 'Cutout peta Sarawak + nama daerah.'),
        ('Skyline & model ZX', 'Jambatan Darul Hana + ZX25R | 4R | 6R | 10R.'),
        ('Cuff rib neon', 'Cuff hijau neon – kemas bila ride.'),
    ]
    spec = spec_table([
        ('Fabrik', '100% Polyester (microfiber) – ringan & cepat kering'),
        ('Cetakan', 'Full sublimation – warna tak pudar, tak merekah'),
        ('Kolar', 'Round neck, rib hijau neon'),
        ('Lengan', 'Panjang (set-in) + cuff rib hijau neon'),
        ('Potongan', 'Regular fit – unisex'),
        ('Ciri', 'Lindung lengan dari panas matahari masa ride jauh'),
        ('Warna', 'Hitam • Hijau Neon Kawasaki • Kelabu'),
    ])
    back = scene(1212, 368, 200, 270, 200, cls='zoom')
    cuff = scene(735, 670, 130, 130, 200, cls='zoom')
    return f'''
<section class="page">
  {header(2, 'LONG SLEEVE', 'JERSI LENGAN PANJANG — INFO DETAIL')}
  <div class="row r1">
    <div class="frame fade-tl">{scene(cx, cy, cw, ch, SCENE_W, inner=mk)}
      <div class="tag l">DEPAN</div><div class="tag r">BELAKANG</div></div>
    <aside class="side"><h3>SOROTAN REKAAN</h3>{feature_list(feats)}</aside>
  </div>
  <div class="row r2">
    <div class="panel zoomp">
      <h3>DETAIL <em>CLOSE-UP</em></h3>
      <div class="zooms">
        <figure>{back}<figcaption>Belakang: peta Sarawak baharu + skyline</figcaption></figure>
        <figure>{cuff}<figcaption>Cuff rib hijau neon</figcaption></figure>
      </div>
    </div>
    <div class="panel"><h3>SPESIFIKASI</h3>{spec}</div>
  </div>
  <div class="panel szp"><h3>CARTA SAIZ <em>LENGAN PANJANG</em></h3>{size_table(long=True)}
    <p class="note">Ukuran dalam inci. Panjang lengan diukur dari jahitan bahu hingga hujung cuff. Toleransi ±1 inci.</p></div>
  {FOOT}
</section>'''


# --------------------------------------------------------------------------
# Page 3: pola potong
# --------------------------------------------------------------------------
SC = 3.7      # px per cm
SA = 1.0      # elaun jahit (cm)


def body_path(back=False):
    """Badan penuh (depan/belakang), unit cm, saiz M. Titik (0,0) = tengah leher di aras bahu."""
    drop = 2.5 if back else 9.0
    ctrl = 2.6 if back else 8.6
    half = [(8.5, 0)]
    # kanan: bahu -> lubang lengan -> sisi -> labuh
    p = (f'M0,{drop} Q7.2,{ctrl} 8.5,0 L23,4.6 C21.6,13 22.4,22.6 25.6,24 '
         f'L26.2,71 Q13,71.8 0,71.8 Q-13,71.8 -26.2,71 L-25.6,24 C-22.4,22.6 -21.6,13 -23,4.6 '
         f'L-8.5,0 Q-7.2,{ctrl} 0,{drop}Z')
    return p, (-26.2, 0, 26.2, 71.8)


def sleeve_path(long=False):
    if long:
        p = 'M-20,13 C-12,12 -8,0 0,0 C8,0 12,12 20,13 L11,52.5 L-11,52.5Z'
        return p, (-20, 0, 20, 52.5)
    p = 'M-20,13 C-12,12 -8,0 0,0 C8,0 12,12 20,13 L17.5,21.5 L-17.5,21.5Z'
    return p, (-20, 0, 20, 21.5)


_piece_n = [0]


def piece(path, bbox, label, qty, art='', grain=True, dims=None, color=None):
    """Satu kepingan pola: isi rekaan (preview sublimasi) + garisan potong + garisan jahit."""
    _piece_n[0] += 1
    pid = f'pc{_piece_n[0]}'
    x0, y0, x1, y1 = bbox
    m = SA + 6  # ruang untuk garisan dimensi
    vb = (x0 - m, y0 - SA - 1, (x1 - x0) + 2 * m, (y1 - y0) + 2 * SA + 9)
    w, h = vb[2] * SC, vb[3] * SC
    fill = color or f'url(#jersey)'
    parts = [f'<svg class="piece" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" width="{w:.0f}" height="{h:.0f}">',
             f'<defs><clipPath id="{pid}c"><path d="{path}"/></clipPath></defs>',
             # elaun jahit (garisan potong luar) – teknik stroke berganda
             f'<path d="{path}" fill="none" stroke="#e9ffd0" stroke-width="{2 * SA + 0.5}" stroke-linejoin="miter"/>',
             f'<path d="{path}" fill="none" stroke="#151717" stroke-width="{2 * SA - 0.25}" stroke-linejoin="miter"/>',
             f'<g clip-path="url(#{pid}c)"><rect x="{x0 - 2}" y="{y0 - 2}" width="{x1 - x0 + 4}" height="{y1 - y0 + 4}" fill="{fill}"/>{art}</g>',
             f'<path d="{path}" fill="none" stroke="{NEON}" stroke-width="0.35" stroke-dasharray="1.2 0.8"/>']
    if grain:
        gx = (x0 + x1) / 2 if not dims or 'gx' not in dims else dims['gx']
        gy0, gy1 = y0 + (y1 - y0) * 0.30, y0 + (y1 - y0) * 0.86
        parts.append(f'<g stroke="#fff" stroke-width="0.35" fill="#fff" opacity="0.9">'
                     f'<line x1="{gx}" y1="{gy0 + 1.6}" x2="{gx}" y2="{gy1 - 1.6}"/>'
                     f'<path d="M{gx},{gy0} l-1,1.8 h2Z M{gx},{gy1} l-1,-1.8 h2Z" stroke="none"/></g>')
    if dims:
        if 'w' in dims:
            yy = y1 + SA + 2.6
            parts.append(dim_h(x0, x1, yy, dims['w']))
        if 'h' in dims:
            xx = x1 + SA + 2.6
            parts.append(dim_v(y0, y1, xx, dims['h']))
    parts.append('</svg>')
    return (f'<div class="pc">{"".join(parts)}<div class="pl"><b>{label}</b>'
            f'<span>POTONG ×{qty}</span></div></div>')


def dim_h(x0, x1, y, txt):
    return (f'<g stroke="#9aa09a" stroke-width="0.22" fill="#cfd4cf"><line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>'
            f'<line x1="{x0}" y1="{y - 1}" x2="{x0}" y2="{y + 1}"/><line x1="{x1}" y1="{y - 1}" x2="{x1}" y2="{y + 1}"/>'
            f'<text x="{(x0 + x1) / 2}" y="{y + 3.2}" text-anchor="middle" stroke="none" font-size="2.6" '
            f'font-family="Barlow Condensed" font-weight="700">{txt}</text></g>')


def dim_v(y0, y1, x, txt):
    cy = (y0 + y1) / 2
    return (f'<g stroke="#9aa09a" stroke-width="0.22" fill="#cfd4cf"><line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>'
            f'<line x1="{x - 1}" y1="{y0}" x2="{x + 1}" y2="{y0}"/><line x1="{x - 1}" y1="{y1}" x2="{x + 1}" y2="{y1}"/>'
            f'<text x="{x + 1.4}" y="{cy}" stroke="none" font-size="2.6" font-family="Barlow Condensed" font-weight="700" '
            f'transform="rotate(90 {x + 1.4} {cy})" text-anchor="middle">{txt}</text></g>')


def body_art(back):
    """Rekaan dalam kepingan badan (imej dipotong dari mockup + peta vektor)."""
    if not back:
        # emblem utama (bahagian atas tengah imej asal)
        k = 31 / 320  # emblem asal ~320px diameter, pusat (765,173) -> 31 cm di dada
        return (chevrons() + slashes()
                + f'<image href="{IMG}" x="{-765 * k:.2f}" y="{27 - 173 * k:.2f}" width="{IMG_W * k:.2f}" '
                  f'height="{IMG_H * k:.2f}" clip-path="url(#emblemClip)" preserveAspectRatio="none"/>')
    # belakang: teks "THE SPIRIT OF SCREAMING" + peta + skyline
    u = 34 / MAP_W
    mp = map_svg('pat', width=None).replace('<svg ', f'<svg x="{-17 - PAD * u:.2f}" y="{24 - PAD * u:.2f}" '
                                                   f'width="{VB[2] * u:.2f}" height="{VB[3] * u:.2f}" ', 1)
    return (chevrons() + slashes()
            + '<image href="assets/back-title.png" x="-17" y="10" width="34" height="13"/>'
            + mp
            + '<image href="assets/back-skyline.png" x="-17" y="46.5" width="34" height="19"/>')


def chevrons():
    g = []
    for i, yy in enumerate([50, 56, 62, 68]):
        op = 0.55 - i * 0.08
        g.append(f'<path d="M-30,{yy - 14} L0,{yy} L30,{yy - 14} L30,{yy - 10} L0,{yy + 4} L-30,{yy - 10}Z" '
                 f'fill="#5b5f5d" opacity="{op:.2f}"/>')
    return ''.join(g)


def slashes():
    return (f'<g fill="{NEON}"><path d="M-26,30 l2,0 l9,26 l-1.2,0Z"/><path d="M26,30 l-2,0 l-9,26 l1.2,0Z"/>'
            f'<path d="M-26,48 l1.4,0 l6,18 l-0.8,0Z"/><path d="M26,48 l-1.4,0 l-6,18 l0.8,0Z"/></g>')


def sleeve_art(long):
    hem = 52.5 if long else 21.5
    s = (f'<g fill="{NEON}"><path d="M-14,{hem * 0.45} l1.4,0 l5,{hem * 0.4} l-0.8,0Z"/>'
         f'<path d="M14,{hem * 0.45} l-1.4,0 l-5,{hem * 0.4} l0.8,0Z"/></g>'
         f'<path d="M-20,{hem * 0.35} L0,{hem * 0.6} L20,{hem * 0.35} L20,{hem * 0.35 + 3} L0,{hem * 0.6 + 3} L-20,{hem * 0.35 + 3}Z" '
         f'fill="#5b5f5d" opacity="0.5"/>')
    if not long:
        s += f'<rect x="-22" y="{hem - 2.2}" width="44" height="1.2" fill="{NEON}"/>'
    return s


def rib(wcm, hcm, label, qty, note):
    p = f'M{-wcm / 2},0 L{wcm / 2},0 L{wcm / 2},{hcm} L{-wcm / 2},{hcm}Z'
    fold = (f'<line x1="{-wcm / 2}" y1="{hcm / 2}" x2="{wcm / 2}" y2="{hcm / 2}" stroke="#0c2a00" '
            f'stroke-width="0.3" stroke-dasharray="2 1"/>')
    return piece(p, (-wcm / 2, 0, wcm / 2, hcm), f'{label}<small>{note}</small>', qty, art=fold, grain=False,
                 dims={'w': f'{wcm:g} cm'}, color=NEON)


def page_pattern():
    fp, fb = body_path(False)
    bp, bb = body_path(True)
    sp, sb = sleeve_path(False)
    lp, lb = sleeve_path(True)

    def set_(long):
        sl, slb = (lp, lb) if long else (sp, sb)
        cuffs = rib(21, 12, 'CUFF RIB', 2, '<br>lipat 2 → 6 cm') if long else ''
        return f'''
      <div class="pset">
        {piece(fp, fb, 'BADAN DEPAN', 1, art=body_art(False), dims={'w': '52.4 cm', 'h': '71.8 cm'})}
        {piece(bp, bb, 'BADAN BELAKANG', 1, art=body_art(True), dims={'w': '52.4 cm', 'h': '71.8 cm'})}
        {piece(sl, slb, 'LENGAN ' + ('PANJANG' if long else 'PENDEK'), 2, art=sleeve_art(long),
               dims={'w': '40 cm', 'h': f'{slb[3]:g} cm'})}
        <div class="ribs">{rib(46, 6, 'KOLAR RIB', 1, '<br>lipat 2 → 3 cm')}{cuffs}</div>
      </div>'''

    return f'''
<section class="page pat">
  {header(3, 'POLA POTONG', 'CUTTING PATTERN — LENGAN PENDEK &amp; LENGAN PANJANG')}
  <svg width="0" height="0" style="position:absolute">
    <defs>
      <pattern id="hex" width="6" height="10.4" patternUnits="userSpaceOnUse">
        <path d="M3,0 L6,1.73 L6,5.2 L3,6.93 L0,5.2 L0,1.73Z M3,6.93 L3,10.4" fill="none" stroke="#2a2d2c" stroke-width="0.3"/>
      </pattern>
      <linearGradient id="jg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141615"/><stop offset="1" stop-color="#0a0b0b"/></linearGradient>
      <pattern id="jersey" width="200" height="200" patternUnits="userSpaceOnUse" x="-100" y="0">
        <rect width="200" height="200" fill="url(#jg)"/><rect width="200" height="200" fill="url(#hex)"/>
      </pattern>
      <clipPath id="emblemClip"><circle cx="0" cy="27" r="15.5"/></clipPath>
    </defs>
  </svg>
  <div class="panel pband"><h3><span class="num">A</span> LENGAN PENDEK <em>SHORT SLEEVE · SAIZ M</em></h3>{set_(False)}</div>
  <div class="panel pband"><h3><span class="num">B</span> LENGAN PANJANG <em>LONG SLEEVE · SAIZ M</em></h3>{set_(True)}</div>
  <div class="legend">
    <span><i class="lg cut"></i>Garisan potong</span>
    <span><i class="lg sew"></i>Garisan jahit (elaun 1 cm)</span>
    <span><i class="lg grain">↕</i>Arah ira kain</span>
    <span><i class="lg fold"></i>Garisan lipat (rib)</span>
  </div>
  <div class="psum">
    <div><b>A · LENGAN PENDEK</b><span>5 kepingan</span><small>Badan depan ×1 • Badan belakang ×1 • Lengan ×2 • Kolar rib ×1</small></div>
    <div><b>B · LENGAN PANJANG</b><span>7 kepingan</span><small>Badan depan ×1 • Badan belakang ×1 • Lengan ×2 • Kolar rib ×1 • Cuff rib ×2</small></div>
  </div>
  <p class="pnote">Unit: cm • Ukuran pola asas saiz M (rujukan) — saiz lain digred ikut carta saiz. Cetak sublimasi pada
  fabrik polyester dahulu, kemudian potong &amp; jahit. Pastikan corak bersambung di bahu, sisi &amp; lengan.
  Sahkan ukuran akhir dengan kilang / supplier sebelum potong pukal.</p>
  {FOOT}
</section>'''


# --------------------------------------------------------------------------
# Page 4: overall + end card
# --------------------------------------------------------------------------
def page_overall():
    return f'''
<section class="page">
  {header(4, 'OVERALL DESIGN', 'LENGAN PENDEK &amp; LENGAN PANJANG — PETA SARAWAK BAHARU')}
  <div class="frame full">{scene(0, 0, IMG_W, IMG_H, 1000)}</div>
  <div class="endcard">
    <div class="ec-top">
      <div class="ec-q brush">BERMINAT NAK BELI?</div>
      <div class="ec-sub">Tempah jersi <b>Kawasaki ZX Empire Owner Sarawak</b> sekarang!</div>
    </div>
    <div class="steps">
      <div><span>1</span><b>PILIH JENIS</b>Lengan pendek / lengan panjang</div>
      <div><span>2</span><b>PILIH SAIZ</b>XS hingga 5XL (rujuk carta saiz)</div>
      <div><span>3</span><b>PM / WHATSAPP</b>Hantar nama, saiz &amp; kuantiti</div>
    </div>
    <div class="contact">
      <div class="slogan brush">RIDE TOGETHER<br><em>STAY TOGETHER</em></div>
    </div>
  </div>
  {FOOT}
</section>'''


CSS = open(os.path.join(ROOT, 'src', 'style.css')).read()


def build():
    html = f'''<!doctype html>
<html lang="ms"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jersi ZX Empire Sarawak</title>
<link rel="stylesheet" href="assets/fonts.css">
<style>{CSS}</style></head>
<body>
{page_short()}
{page_long()}
{page_pattern()}
{page_overall()}
<section class="export" id="overall-export">{scene(0, 0, IMG_W, IMG_H, IMG_W)}</section>
<section class="export" id="map-export">{map_svg('mx', width='2016')}</section>
</body></html>'''
    open(os.path.join(ROOT, 'katalog.html'), 'w').write(html)
    standalone = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                  + map_svg('peta', embed_fonts=True, width='2176'))
    open(A('peta-sarawak.svg'), 'w').write(standalone)
    print('ok: katalog.html, assets/peta-sarawak.svg')


if __name__ == '__main__':
    build()
