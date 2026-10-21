import sys, subprocess, numpy as np, cv2
src=sys.argv[1]
for rng in sys.argv[2:]:
    a,b=map(float,rng.split(":"))
    t=a
    while t<=b+1e-6:
        raw=subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",src,"-frames:v","1","-vf","scale=540:960","-f","rawvideo","-pix_fmt","bgr24","-"],capture_output=True).stdout
        im=np.frombuffer(raw,np.uint8).reshape(960,540,3)
        ycc=cv2.cvtColor(im,cv2.COLOR_BGR2YCrCb)
        m=((ycc[:,:,1]>140)&(ycc[:,:,1]<180)&(ycc[:,:,2]>85)&(ycc[:,:,2]<130)).astype(np.uint8)
        m[:, 215:]=0; m[:120]=0; m[560:]=0
        m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
        n,lab,st,_=cv2.connectedComponentsWithStats(m)
        if n>1:
            i=1+np.argmax(st[1:,4]); ys,xs=np.where(lab==i); top=ys.min(); x=int(xs[ys<=top+6].mean())
            print(f"{t:.2f} tip=({x*2},{top*2}) area={st[i,4]}")
        else: print(f"{t:.2f} none")
        t+=0.1
