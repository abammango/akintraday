"""Original lo-fi / tech groove for the edit, synthesised from scratch (no samples).

Tempo is derived from the edit so that a downbeat lands exactly on the blur
moment (bar 7). Bar 6 is a breakdown with a riser while the Claude prompt is
typed; bar 7 drops back in with a crash and sub boom. The bed is ducked under
the voice using the cleaned voice track laid out on the edit timeline.

usage: python3 tools/music.py timing.json assets/voice_clean.wav assets/music_bed.wav
"""
import sys, json
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
from scipy.ndimage import maximum_filter1d

timing, voice_path, dst = sys.argv[1:4]
TM = json.load(open(timing))
SR = 48000
TOTAL = TM["total"]
BLUR = TM["T"]["blur"]
BAR = BLUR / 7.0          # bar 7 starts on the blur
BEAT = BAR / 4
N = int((TOTAL + 2.5) * SR)
rng = np.random.default_rng(7)

L = np.zeros(N); R = np.zeros(N)                  # drums / bass (dry)
EPL = np.zeros(N); EPR = np.zeros(N)              # electric piano bus
FX = np.zeros(N)                                  # riser / crash / sub (mono)
SNR = np.zeros(N)                                 # snare (sent to reverb)

def put(buf, t0, x, gain=1.0):
    i = int(t0 * SR)
    if i >= N: return
    x = x[: N - i]; buf[i:i + len(x)] += gain * x

def ts(d): return np.arange(int(d * SR)) / SR
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)

# ---------------------------------------------------------------- voices
def ep_note(m, dur, vel, det):
    f = mtof(m) * (1 + det); t = ts(dur + 1.6)
    env = np.exp(-t / 1.7) * (1 - np.exp(-t / 0.004))
    env *= np.where(t > dur, np.exp(-(t - dur) / 0.3), 1.0)
    x = (np.sin(2 * np.pi * f * t) + 0.38 * np.exp(-t / 0.8) * np.sin(4 * np.pi * f * t)
         + 0.12 * np.exp(-t / 0.35) * np.sin(6 * np.pi * f * t)
         + 0.05 * np.exp(-t / 0.05) * np.sin(2 * np.pi * 7.1 * f * t))
    return vel * env * x

def chord(t0, notes, dur, vel):
    for k, m in enumerate(notes):
        dt = k * 0.012                                    # slight strum
        put(EPL, t0 + dt, ep_note(m, dur, vel, +0.0011))
        put(EPR, t0 + dt, ep_note(m, dur, vel, -0.0011))

def bass(t0, m, dur, vel=0.33):
    f = mtof(m); t = ts(dur + 0.25)
    env = (1 - np.exp(-t / 0.006)) * np.exp(-t / 1.1) * np.where(t > dur, np.exp(-(t - dur) / 0.06), 1)
    x = np.tanh(1.6 * (np.sin(2 * np.pi * f * t) + 0.22 * np.sin(4 * np.pi * f * t)))
    put(L, t0, vel * env * x); put(R, t0, vel * env * x)

def kick(t0, vel=0.85):
    t = ts(0.45); f = 44 + 80 * np.exp(-t / 0.035)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.26)
    x[: int(0.003 * SR)] += rng.normal(0, 0.3, int(0.003 * SR))
    put(L, t0, vel * x); put(R, t0, vel * x)

_bp = signal.butter(2, [1400, 7500], "bandpass", fs=SR, output="sos")
_hp = signal.butter(2, 7000, "highpass", fs=SR, output="sos")
def snare(t0, vel=0.32):
    t = ts(0.35)
    x = signal.sosfilt(_bp, rng.normal(0, 1, len(t))) * np.exp(-t / 0.13) * 0.9
    x += np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5
    put(SNR, t0, vel * x)

def hat(t0, vel=0.10, open_=False):
    t = ts(0.4 if open_ else 0.08)
    x = signal.sosfilt(_hp, rng.normal(0, 1, len(t))) * np.exp(-t / (0.16 if open_ else 0.025))
    pan = 0.15 if int(t0 / BEAT * 2) % 2 else -0.15
    put(L, t0, vel * (1 - pan) * x); put(R, t0, vel * (1 + pan) * x)

def pluck(t0, m, vel=0.08):
    f = mtof(m); t = ts(0.9)
    x = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 0.28) * (1 - np.exp(-t / 0.003))
    put(EPL, t0, vel * x * 1.1); put(EPR, t0 + 0.011, vel * x * 0.9)

def crash(t0, vel=0.22):
    t = ts(3.0)
    x = signal.sosfilt(signal.butter(2, 3500, "highpass", fs=SR, output="sos"), rng.normal(0, 1, len(t)))
    put(FX, t0, vel * x * np.exp(-t / 1.1))

def sub_boom(t0, vel=0.5):
    t = ts(1.6); f = 32 + 40 * np.exp(-t / 0.25)
    put(FX, t0, vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7))

def riser(t0, t1, vel=0.16):
    t = ts(t1 - t0); p = t / t[-1]
    noise = rng.normal(0, 1, len(t)); out = np.zeros_like(noise); y = 0.0
    a = np.exp(-2 * np.pi * (300 + 7000 * p ** 2) / SR)  # one-pole sweep 300 Hz -> 7.3 kHz
    for i in range(len(noise)):
        y = a[i] * y + (1 - a[i]) * noise[i]; out[i] = y
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * p ** 2) / SR) * 0.25
    put(FX, t0, vel * (out * 2.2 + tone) * p ** 1.6)

# ---------------------------------------------------------------- song
PROG = [  # Fmaj9 | Em7 | Dm9 | Cmaj9
    ([53, 57, 60, 64, 67], 41),
    ([52, 55, 59, 62, 66], 40),
    ([50, 53, 57, 60, 64], 38),
    ([48, 52, 55, 59, 62], 36),
]
MELODY = [(0, 72), (1.5, 69), (2.5, 67), (3.25, 69)]  # beats within a bar, MIDI
n_bars = int(np.ceil(TOTAL / BAR)) + 1
SW = 0.09 * BEAT  # swing on off-beat 8ths

for b in range(n_bars):
    t0 = b * BAR
    if t0 > TOTAL - 0.05: break
    notes, root = PROG[b % 4]
    last = t0 + BAR > TOTAL - 0.4          # final (partial) bar: one ringing chord
    breakdown = b == 6
    chord(t0, notes, BAR * (0.62 if not last else 2.0), 0.085 if not last else 0.1)
    if not last and not breakdown:
        chord(t0 + 2.5 * BEAT + SW, notes[1:], BEAT * 1.2, 0.055)
    if breakdown:
        chord(t0 + 2 * BEAT, notes[1:], BEAT * 2, 0.05)
    bass(t0, root, BEAT * 1.3, 0.34 if not last else 0.3)
    if not last and not breakdown:
        bass(t0 + 2.5 * BEAT + SW, root + (7 if b % 2 else 0), BEAT * 0.9, 0.26)
    if last or breakdown:
        if breakdown:
            for k in range(8):                        # snare roll into the drop
                snare(t0 + 2 * BEAT + k * BEAT / 4, 0.06 + 0.035 * k)
            riser(t0, t0 + BAR)
        continue
    for beat in range(4):
        bt = t0 + beat * BEAT
        if beat in (0,) or (beat == 2 and b % 2 == 0): kick(bt)
        if beat == 2 and b % 2 == 1: kick(bt + 0.5 * BEAT + SW, 0.6)
        if beat in (1, 3): snare(bt)
        hat(bt, 0.085)
        hat(bt + BEAT / 2 + SW, 0.06, open_=(beat == 3 and b % 4 == 3))
    if b >= 7:                                       # melody lift after the drop
        for bb, m in MELODY:
            pluck(t0 + bb * BEAT + (SW if bb % 1 else 0), m + (0 if b % 2 == 0 else -2))

crash(BLUR); sub_boom(BLUR); kick(BLUR, 1.0)

# ---------------------------------------------------------------- buses
def reverb(x, decay=0.55, length=1.8, seed=0):
    r = np.random.default_rng(seed); t = ts(length)
    ir = r.normal(0, 1, len(t)) * np.exp(-t / decay)
    ir = signal.sosfilt(signal.butter(2, 5000, "lowpass", fs=SR, output="sos"), ir)
    ir /= np.sqrt((ir ** 2).sum())
    return signal.fftconvolve(x, ir)[: len(x)]

# EP: warm lowpass that closes during the breakdown bar and reopens on the drop
cut = np.full(N, 5200.0)
b6, b7 = int(6 * BAR * SR), int(7 * BAR * SR)
cut[b6:b7] = np.geomspace(5200, 650, b7 - b6)
def tv_lowpass(x):
    out = np.zeros_like(x); zi = None; hop = 512
    for i in range(0, len(x), hop):
        sos = signal.butter(2, cut[min(i, N - 1)], "lowpass", fs=SR, output="sos")
        if zi is None: zi = signal.sosfilt_zi(sos) * 0
        out[i:i + hop], zi = signal.sosfilt(sos, x[i:i + hop], zi=zi)
    return out
EPL, EPR = tv_lowpass(EPL), tv_lowpass(EPR)
EPL += 0.35 * reverb(EPL, seed=1); EPR += 0.35 * reverb(EPR, seed=2)

# sidechain pump from the kick grid
pump = np.ones(N); t = np.arange(N) / SR
for b in range(n_bars):
    if b == 6: continue
    for kt in (b * BAR, b * BAR + 2 * BEAT):
        if kt < TOTAL - 0.4:
            m = t >= kt
            pump[m] = np.minimum(pump[m], 1 - 0.32 * np.exp(-(t[m] - kt) / 0.14))

snl, snr_ = SNR + 0.25 * reverb(SNR, 0.4, 1.2, 3), SNR + 0.25 * reverb(SNR, 0.4, 1.2, 4)
fxl, fxr = FX + 0.3 * reverb(FX, 0.8, 2.0, 5), FX + 0.3 * reverb(FX, 0.8, 2.0, 6)
# vinyl texture
crackle = np.zeros(N); idx = rng.integers(0, N, int(9 * N / SR))
crackle[idx] = rng.normal(0, 0.25, len(idx))
crackle = signal.sosfilt(signal.butter(2, 2500, "highpass", fs=SR, output="sos"), crackle)
hiss = signal.sosfilt(signal.butter(2, [3000, 9000], "bandpass", fs=SR, output="sos"), rng.normal(0, 0.004, N))

mixL = (EPL * pump + L * np.where(t < 6 * BAR, 1, 1) + snl + fxl) + crackle * 0.5 + hiss
mixR = (EPR * pump + R + snr_ + fxr) + crackle * 0.5 + hiss
mix = np.stack([mixL, mixR], 1)
mix = np.tanh(1.2 * mix) / 1.2
mix = mix[: int(TOTAL * SR)]
meter = pyln.Meter(SR)
mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), -15.0)

# ---------------------------------------------------------------- duck under the voice
v, vsr = sf.read(voice_path)
v = v.mean(1) if v.ndim == 2 else v
assert vsr == SR
edit = np.zeros(len(mix))
for s in TM["segments"]:
    a, d, o = int(s["a"] * SR), int(s["dur"] * SR), int(s["start"] * SR)
    edit[o:o + d] += v[a:a + d][: len(edit) - o]
env = np.sqrt(signal.lfilter([1 - 0.9993], [1, -0.9993], edit ** 2) + 1e-10)
speaking = (20 * np.log10(env) > -38).astype(float)
speaking = maximum_filter1d(speaking, size=int(0.24 * SR), origin=-int(0.1 * SR))  # 120 ms lookahead
target = np.where(speaking > 0, -13.0, -6.0)
target[: int(0.6 * SR)] = -13.0                        # hook: first word must cut through
g = np.empty_like(target); cur = target[0]
att, rel = np.exp(-1 / (0.05 * SR)), np.exp(-1 / (0.4 * SR))
for i, x in enumerate(target):
    c = att if x < cur else rel
    cur = c * cur + (1 - c) * x; g[i] = cur
gain = 10 ** (g / 20)
fade = np.clip((TOTAL - t[: len(mix)]) / 0.8, 0, 1)              # fade the tail
gain *= np.minimum(1, t[: len(mix)] / 0.03) * fade
mix *= gain[:, None]
mix /= max(1.0, np.abs(mix).max() / 0.95)
sf.write(dst, mix.astype(np.float32), SR, subtype="PCM_24")
print(f"bpm {60 / BEAT:.1f}  bar {BAR:.3f}s  blur@bar7 {BLUR}s  len {len(mix) / SR:.2f}s")
