import sys, cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
lum = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
full = np.zeros(lum.shape, np.uint8)
# bounding boxes (x0,y0,x1,y1) of the old maps + a seed point inside each
for (x0,y0,x1,y1),(sx,sy) in [((470,445,645,556),(560,500)), ((1220,445,1395,560),(1310,505))]:
    sub = lum[y0:y1, x0:x1]
    bright = (sub > 55).astype(np.uint8)
    n, lab = cv2.connectedComponents(bright, connectivity=8)
    l = lab[sy-y0, sx-x0]
    assert l != 0, (sx, sy)
    comp = (lab == l).astype(np.uint8) * 255
    # fill holes (the dark grunge splotches inside the map)
    cnts,_ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filled = np.zeros_like(comp); cv2.drawContours(filled, cnts, -1, 255, -1)
    print('component px', int((filled>0).sum()), 'bbox', cv2.boundingRect(np.vstack(cnts)))
    full[y0:y1, x0:x1] = np.maximum(full[y0:y1, x0:x1], filled)
full = cv2.dilate(full, np.ones((5,5),np.uint8), iterations=1)
cv2.imwrite(out.replace('.png','_mask.png'), full)
res = cv2.inpaint(im, full, 6, cv2.INPAINT_TELEA)
# darken the inpainted area slightly so it reads as plain jersey black
m = cv2.GaussianBlur(full, (9,9), 0).astype(np.float32)/255.0
dark = (res.astype(np.float32)*0.55)
res = (res*(1-m[...,None]) + dark*m[...,None]).astype(np.uint8)
cv2.imwrite(out, res)
