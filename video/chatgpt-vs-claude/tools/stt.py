import sys, json, wave, numpy as np, sherpa_onnx as so
S=sys.argv[1]; M=S+"/models/sherpa-onnx-whisper-large-v3/large-v3-"
w=wave.open(S+"/src/audio.wav"); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
cfg=so.VadModelConfig(); cfg.silero_vad.model=S+"/models/vad.onnx"; cfg.silero_vad.min_silence_duration=0.25; cfg.silero_vad.min_speech_duration=0.2; cfg.silero_vad.threshold=0.45; cfg.sample_rate=sr
vad=so.VoiceActivityDetector(cfg,buffer_size_in_seconds=120)
segs=[]
ws=cfg.silero_vad.window_size
for i in range(0,len(a),ws):
    vad.accept_waveform(a[i:i+ws])
    while not vad.empty():
        segs.append((vad.front.start/sr, len(vad.front.samples)/sr)); vad.pop()
vad.flush()
while not vad.empty(): segs.append((vad.front.start/sr, len(vad.front.samples)/sr)); vad.pop()
rec=so.OfflineRecognizer.from_whisper(encoder=M+"encoder.int8.onnx",decoder=M+"decoder.int8.onnx",tokens=M+"tokens.txt",language="ms",num_threads=4,enable_token_timestamps=True,tail_paddings=500)
out=[]
for st,du in segs:
    pad=0.15; s0=max(0,st-pad); e0=min(len(a)/sr,st+du+pad)
    x=a[int(s0*sr):int(e0*sr)]
    s=rec.create_stream(); s.accept_waveform(sr,x); rec.decode_stream(s); r=s.result
    toks=[{"t":t,"s":round(s0+ts,2)} for t,ts in zip(r.tokens, r.timestamps)] if r.timestamps else []
    out.append({"start":round(st,2),"end":round(st+du,2),"text":r.text,"tokens":toks})
    print(f"[{st:6.2f}-{st+du:6.2f}] {r.text}",flush=True)
json.dump(out,open(S+"/src/transcript.json","w"),ensure_ascii=False,indent=1)
