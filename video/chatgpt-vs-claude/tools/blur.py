import sys, subprocess, numpy as np, cv2
src, cut, dst, audio_src = sys.argv[1:5]
W,H=1080,1920
fa=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
fb=subprocess.Popen(["ffmpeg","-v","error","-c:v","libvpx-vp9","-i",cut,"-f","rawvideo","-pix_fmt","bgra","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-",
    "-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-g","15","-movflags","+faststart",dst],stdin=subprocess.PIPE)
n=0; k=np.ones((9,9),np.uint8)
while True:
    a=fa.stdout.read(W*H*3); b=fb.stdout.read(W*H*4)
    if len(a)<W*H*3 or len(b)<W*H*4: break
    f=np.frombuffer(a,np.uint8).reshape(H,W,3).astype(np.float32)
    m=np.frombuffer(b,np.uint8).reshape(H,W,4)[:,:,3].astype(np.float32)/255
    keep=1-cv2.dilate((m>0.15).astype(np.uint8),k,iterations=2).astype(np.float32)   # pure background pixels
    sw,sh=W//4,H//4
    fs=cv2.resize(f*keep[...,None],(sw,sh),interpolation=cv2.INTER_AREA); ks=cv2.resize(keep,(sw,sh),interpolation=cv2.INTER_AREA)
    sig=7.0
    num=cv2.GaussianBlur(fs,(0,0),sig); den=cv2.GaussianBlur(ks,(0,0),sig)[...,None]
    bg=num/np.maximum(den,1e-3)
    # fill any region with no background support using a much wider blur of the plain frame
    wide=cv2.GaussianBlur(cv2.resize(f,(sw,sh),interpolation=cv2.INTER_AREA),(0,0),sig*1.6)
    wgt=np.clip(den*4,0,1); bg=bg*wgt+wide*(1-wgt)
    bg=cv2.resize(bg,(W,H),interpolation=cv2.INTER_CUBIC)
    ms=cv2.GaussianBlur(m,(0,0),1.2)[...,None]
    o=np.clip(f*ms+bg*(1-ms),0,255).astype(np.uint8)
    enc.stdin.write(o.tobytes()); n+=1
enc.stdin.close(); enc.wait(); print("frames",n)
