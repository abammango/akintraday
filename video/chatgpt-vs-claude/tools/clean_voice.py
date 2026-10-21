"""Clean the voice track of the raw recording (full source timeline, 48 kHz).

1. remove hum (48.7 Hz fundamental + harmonics)
2. suppress the child's voice in given windows with an adult-harmonic mask
3. stationary spectral noise reduction (room/fan noise)
4. EQ + gentle compression, loudness-normalise

usage: python3 clean_voice.py in.wav out.wav
"""
import sys
import numpy as np, soundfile as sf, librosa, noisereduce as nr, pyloudnorm as pyln
from scipy import signal
from scipy.ndimage import minimum_filter1d

src, dst = sys.argv[1:3]
y, sr = sf.read(src)
y = y.mean(1) if y.ndim == 2 else y

# 1. hum ---------------------------------------------------------------
sos = signal.butter(4, 70, "highpass", fs=sr, output="sos")
y = signal.sosfiltfilt(sos, y)
for k in range(2, 7):  # 97, 146, 195, 243, 292 Hz
    b, a = signal.iirnotch(48.7 * k, Q=40 if k == 3 else 25, fs=sr)
    y = signal.filtfilt(b, a, y)

# 2. child voice: keep only the adult's harmonics inside these windows -
CHILD = [(12.95, 14.15), (39.50, 40.22)]
N, HOP = 2048, 256
S = librosa.stft(y, n_fft=N, hop_length=HOP)
freqs = librosa.fft_frequencies(sr=sr, n_fft=N)
times = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=HOP)
mask = np.ones(S.shape, np.float32)
for a, b in CHILD:
    i0, i1 = np.searchsorted(times, a - 0.1), np.searchsorted(times, b + 0.1)
    seg = librosa.istft(S[:, i0:i1], hop_length=HOP)
    f0, vf, _ = librosa.pyin(seg, fmin=80, fmax=240, sr=sr, frame_length=N, hop_length=HOP)
    for j in range(min(len(f0), i1 - i0)):
        t = times[i0 + j]
        w = np.clip(min(t - a, b - t) / 0.08, 0, 1)  # 80 ms fade at window edges
        if w <= 0:
            continue
        if vf[j] and not np.isnan(f0[j]):
            h = freqs / f0[j]
            near = np.abs(h - np.round(h)) * f0[j] < np.maximum(0.16 * f0[j], 18)
            m = np.where(near | (freqs < 250), 1.0, 0.08)   # floor = -22 dB between harmonics
        else:
            m = np.where((freqs > 300) & (freqs < 2500), 0.12, 1.0)  # adult unvoiced: duck the child's band
        mask[:, i0 + j] = 1 - w * (1 - m)
mask = signal.convolve2d(mask, np.ones((3, 3)) / 9, mode="same", boundary="symm")  # soften
y = librosa.istft(S * mask, hop_length=HOP, length=len(y))

# 3. noise reduction (profile: quiet room tone, no speech) -------------
noise = np.concatenate([y[int(32.3 * sr):int(33.7 * sr)], y[int(29.4 * sr):int(30.5 * sr)]])
y = nr.reduce_noise(y=y, sr=sr, y_noise=noise, stationary=True, prop_decrease=0.85, n_fft=2048)

# 4. EQ + compression + loudness ---------------------------------------
def peq(x, f, gain_db, q):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f / sr; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)
y = peq(y, 320, -2.5, 1.0)    # less boxy
y = peq(y, 3800, 2.5, 0.9)    # presence
y = peq(y, 120, 1.5, 0.8)     # a bit of warmth

env = np.sqrt(signal.lfilter([0.002], [1, -0.998], y ** 2) + 1e-12)  # ~10 ms RMS
lvl = 20 * np.log10(env)
thr, ratio = -24.0, 3.0
gain_db = np.where(lvl > thr, (thr - lvl) * (1 - 1 / ratio), 0.0)
gain_db = signal.lfilter([0.01], [1, -0.99], gain_db)  # smooth
y = y * 10 ** (gain_db / 20)

meter = pyln.Meter(sr)
y = pyln.normalize.loudness(y, meter.integrated_loudness(y), -16.0)
# peak limiter: 5 ms lookahead, instant attack, 80 ms release
look = int(0.005 * sr)
need = np.minimum(1.0, 0.89 / np.maximum(np.abs(y), 1e-9))
need = minimum_filter1d(need, size=2 * look + 1)  # gain is already down when the peak arrives
rel = np.exp(-1 / (0.08 * sr)); g = np.empty_like(need); cur = 1.0
for i, v in enumerate(need):
    cur = v if v < cur else rel * cur + (1 - rel) * v
    g[i] = cur
y = y * g
sf.write(dst, np.stack([y, y], 1).astype(np.float32), sr, subtype="PCM_24")
print("done", dst, "LUFS", round(meter.integrated_loudness(y), 1))
