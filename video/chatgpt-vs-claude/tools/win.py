import sys, wave, numpy as np, sherpa_onnx as so
S=sys.argv[1]; M=S+"/models/sherpa-onnx-whisper-large-v3/large-v3-"
w=wave.open(S+"/src/audio.wav"); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
rec=so.OfflineRecognizer.from_whisper(encoder=M+"encoder.int8.onnx",decoder=M+"decoder.int8.onnx",tokens=M+"tokens.txt",language="ms",num_threads=4,tail_paddings=500)
for arg in sys.argv[2:]:
    s0,e0=map(float,arg.split(":"))
    st=rec.create_stream(); st.accept_waveform(sr,a[int(s0*sr):int(e0*sr)]); rec.decode_stream(st)
    print(f"{s0:6.2f}-{e0:6.2f}: {st.result.text}",flush=True)
