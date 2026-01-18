#!/usr/bin/env python3
"""Recolor to TRUE 80s neon - vivid magenta, cyan, gold"""

from PIL import Image, ImageEnhance
import numpy as np
import colorsys

def recolor_neon_80s(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img, dtype=np.float32)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    out = np.zeros_like(data)
    out[:,:,3] = a

    # Process all pixels at once with numpy
    mask = a > 0

    # Calculate luminance
    lum = 0.299 * r + 0.587 * g + 0.114 * b

    # Detect if pixel is more red/warm or blue/cool
    warm = (r > b) & mask
    cool = (b >= r) & mask
    gray = (np.abs(r - g) < 30) & (np.abs(g - b) < 30) & mask

    # NEON MAGENTA for warm tones (was brown/red)
    out[:,:,0] = np.where(warm & ~gray, np.clip(lum * 1.1 + 80, 0, 255), out[:,:,0])
    out[:,:,1] = np.where(warm & ~gray, np.clip(lum * 0.3, 0, 255), out[:,:,1])
    out[:,:,2] = np.where(warm & ~gray, np.clip(lum * 0.9 + 60, 0, 255), out[:,:,2])

    # NEON CYAN/PURPLE for cool tones (was blue/gray frame)
    out[:,:,0] = np.where(cool & ~gray, np.clip(lum * 0.6 + 40, 0, 255), out[:,:,0])
    out[:,:,1] = np.where(cool & ~gray, np.clip(lum * 0.5 + 20, 0, 255), out[:,:,1])
    out[:,:,2] = np.where(cool & ~gray, np.clip(lum * 1.0 + 80, 0, 255), out[:,:,2])

    # SILVER/CHROME for grays with slight purple tint
    out[:,:,0] = np.where(gray, np.clip(lum * 0.9 + 30, 0, 255), out[:,:,0])
    out[:,:,1] = np.where(gray, np.clip(lum * 0.85 + 20, 0, 255), out[:,:,1])
    out[:,:,2] = np.where(gray, np.clip(lum * 1.0 + 50, 0, 255), out[:,:,2])

    result = Image.fromarray(out.astype(np.uint8), 'RGBA')

    # Boost saturation
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.4)

    result.save(output_path)
    print(f"Saved: {output_path}")

# Recolor both
recolor_neon_80s(
    "/Users/ariebonan/Desktop/WC86/web-sdk/apps/ways/static/assets/sprites/reelsFrame/reels_frame.png",
    "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/reelsFrame/reels_frame.png"
)

recolor_neon_80s(
    "/Users/ariebonan/Desktop/WC86/web-sdk/apps/ways/static/assets/sprites/progressBar/progressBar.png",
    "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/progressBar/progressBar.png"
)
