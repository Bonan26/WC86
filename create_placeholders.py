#!/usr/bin/env python3
"""Create placeholder images"""
from PIL import Image, ImageDraw, ImageFont

def create_placeholder(text, output_path, size=(300, 300)):
    img = Image.new('RGBA', size, (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Draw text centered
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    # Purple/magenta color for placeholder
    draw.text((x, y), text, fill=(200, 50, 200, 255), font=font)

    # Add border
    draw.rectangle([(10, 10), (size[0]-10, size[1]-10)], outline=(200, 50, 200, 255), width=3)

    img.save(output_path)
    print(f"Created: {output_path}")

base = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites"

# uiAssets placeholders
create_placeholder("VL", f"{base}/uiAssets/volatility_lone.png")
create_placeholder("VP", f"{base}/uiAssets/volatility_pack.png")
create_placeholder("VA", f"{base}/uiAssets/volatility_alpha.png")

# pressToContinueText placeholders
create_placeholder("PRESS TO\nCONTINUE", f"{base}/pressToContinueText/press_continue_en.png", (400, 150))
create_placeholder("APPUYEZ POUR\nCONTINUER", f"{base}/pressToContinueText/press_continue_fr.png", (400, 150))

print("Done!")
