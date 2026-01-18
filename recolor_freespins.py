#!/usr/bin/env python3
"""Recolor freeSpins to WC86 80s neon style"""

from PIL import Image
import numpy as np
import colorsys

def recolor_to_neon(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    out = np.zeros_like(data)
    out[:,:,3] = a

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if a[y,x] == 0:
                continue
            ri, gi, bi = r[y,x]/255, g[y,x]/255, b[y,x]/255
            h, l, s = colorsys.rgb_to_hls(ri, gi, bi)

            if s < 0.15:
                new_h, new_s, new_l = 0.75, 0.15, l
            elif 0.0 <= h <= 0.1 or h >= 0.9:
                new_h, new_s, new_l = 0.85, min(s*1.3,1), l
            elif 0.55 <= h <= 0.75:
                new_h, new_s, new_l = 0.75, min(s*1.2,1), l
            elif 0.1 < h < 0.2:
                new_h, new_s, new_l = 0.12, min(s*1.2,1), min(l*1.1,1)
            elif 0.2 <= h < 0.45:
                new_h, new_s, new_l = 0.12, min(s*1.1,1), l
            else:
                new_h, new_s, new_l = 0.78, s, l

            nr, ng, nb = colorsys.hls_to_rgb(new_h, new_l, new_s)
            out[y,x,0], out[y,x,1], out[y,x,2] = int(nr*255), int(ng*255), int(nb*255)

    Image.fromarray(out, 'RGBA').save(output_path)
    print(f"Saved: {output_path}")

recolor_to_neon(
    "/Users/ariebonan/Desktop/WC86/web-sdk/apps/ways/static/assets/sprites/freeSpins/freeSpins.png",
    "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/freeSpins/freeSpins.png"
)
