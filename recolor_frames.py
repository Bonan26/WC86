#!/usr/bin/env python3
"""Recolor ways frames to WC86 80s neon style (purple/magenta/gold)"""

from PIL import Image
import numpy as np
import colorsys
import os

def recolor_to_neon(input_path, output_path):
    """Shift hues to 80s neon palette: purple/magenta/gold"""
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img)

    # Separate channels
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Create output
    out = np.zeros_like(data)
    out[:,:,3] = a  # Keep alpha

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if a[y,x] == 0:
                continue

            ri, gi, bi = r[y,x]/255, g[y,x]/255, b[y,x]/255
            h, l, s = colorsys.rgb_to_hls(ri, gi, bi)

            # Detect color type and remap
            if s < 0.15:  # Grayscale/metal - shift to silver/chrome with purple tint
                # Add slight purple tint to grays
                new_h = 0.75  # Purple
                new_s = 0.15
                new_l = l
            elif 0.0 <= h <= 0.1 or h >= 0.9:  # Reds -> Magenta/Pink
                new_h = 0.85  # Magenta
                new_s = min(s * 1.3, 1.0)
                new_l = l
            elif 0.55 <= h <= 0.75:  # Blues/Purples -> Keep purple, boost
                new_h = 0.75  # Purple
                new_s = min(s * 1.2, 1.0)
                new_l = l
            elif 0.1 < h < 0.2:  # Orange/Brown -> Gold
                new_h = 0.12  # Gold
                new_s = min(s * 1.2, 1.0)
                new_l = min(l * 1.1, 1.0)
            elif 0.2 <= h < 0.45:  # Greens/Yellows -> Gold
                new_h = 0.12  # Gold
                new_s = min(s * 1.1, 1.0)
                new_l = l
            else:  # Other -> Purple
                new_h = 0.78
                new_s = s
                new_l = l

            nr, ng, nb = colorsys.hls_to_rgb(new_h, new_l, new_s)
            out[y,x,0] = int(nr * 255)
            out[y,x,1] = int(ng * 255)
            out[y,x,2] = int(nb * 255)

    result = Image.fromarray(out, 'RGBA')
    result.save(output_path)
    print(f"Saved: {output_path}")

def main():
    ways_sprites = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/ways/static/assets/sprites"
    wc86_sprites = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites"

    # Assets to adapt
    assets = [
        ("reelsFrame/reels_frame.png", "reelsFrame/reels_frame.png"),
        ("progressBar/progressBar.png", "progressBar/progressBar.png"),
    ]

    for src, dst in assets:
        src_path = os.path.join(ways_sprites, src)
        dst_path = os.path.join(wc86_sprites, dst)

        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            print(f"Recoloring: {src}")
            recolor_to_neon(src_path, dst_path)
        else:
            print(f"Not found: {src_path}")

if __name__ == "__main__":
    main()
