#!/usr/bin/env python3.12
"""
WC86 - Generate UI sprites with Gemini Imagen 4
Usage: python3.12 generate_ui_sprite.py <sprite_name>
"""

from google import genai
from google.genai import types
import os
import sys

# API Key
API_KEY = "AIzaSyDO6tt-Ft4zdkm8GZws8lp_bNw2l-zYM40"

# Base output directory
BASE_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites"

# Style for UI elements
STYLE_UI = """80s retro nightclub style, neon colors (pink, cyan, purple),
dark background with glowing elements, sleek and stylish, suitable for a slot game UI.
High quality, detailed."""

STYLE_FRAME = """Metallic frame with neon glow accents, 80s retro style,
dark metal with cyan/pink neon trim, suitable for a slot machine reel frame.
Plain black background for easy removal."""

# UI Sprites config: name -> (subfolder, prompt, aspect_ratio)
SPRITES = {
    # Reel Frames - ONLY the border/frame, empty inside
    "frame_6x5": ("reelsFrame", f"A simple rectangular decorative border frame ONLY, no content inside, empty transparent center, metallic gold ornate edge with subtle glow, like a picture frame. Solid bright green background (#00FF00) for removal.", "4:3"),

    "frame_7x6": ("reelsFrame", f"A simple rectangular decorative border frame ONLY, no content inside, empty transparent center, metallic gold ornate edge with subtle glow, like a picture frame. Solid bright green background (#00FF00) for removal.", "4:3"),

    "frame_8x7": ("reelsFrame", f"A simple rectangular decorative border frame ONLY, no content inside, empty transparent center, metallic gold ornate edge with subtle glow, like a picture frame. Solid bright green background (#00FF00) for removal.", "4:3"),

    "frame_8x8": ("reelsFrame", f"A simple square decorative border frame ONLY, no content inside, empty transparent center, metallic gold ornate edge with subtle glow, like a picture frame. Solid bright green background (#00FF00) for removal.", "1:1"),

    # Free Spins
    "fs_background": ("freeSpins", f"A dark nightclub background with purple and blue lighting, disco lights, moon visible, mystical wolf theme atmosphere, {STYLE_UI}", "16:9"),

    "fs_frame": ("freeSpins", f"A decorative frame for free spins display, golden wolves on sides, neon purple glow, 80s style ornate border, transparent center, black background, {STYLE_UI}", "16:9"),

    "fs_counter_bg": ("freeSpins", f"A small counter background panel for displaying spin count, dark metal with neon cyan glow border, compact rounded rectangle, black background, {STYLE_UI}", "16:9"),

    # Progress Bar
    "progress_bar_bg": ("progressBar", f"A horizontal progress bar background, empty dark metal trough with neon edge, sleek 80s style, black background, {STYLE_UI}", "16:9"),

    "progress_bar_fill": ("progressBar", f"A horizontal progress bar fill segment, glowing golden/amber gradient, neon style, meant to fill a progress bar, black background, {STYLE_UI}", "16:9"),

    "territory_icon": ("progressBar", f"A small golden wolf paw icon for territory progress, glowing gold, cartoon style with black outlines, green background for removal, {STYLE_UI}", "1:1"),

    # UI Assets
    "logo": ("uiAssets", f"Logo text 'W86' in bold vintage distressed font style, dark red/maroon color, rough worn texture like old stamp or letterpress, simple and iconic, no glow no neon. IMPORTANT: solid bright green background (#00FF00) for easy removal.", "1:1"),

    "buy_bonus_btn": ("uiAssets", f"A 'BUY BONUS' button, golden shiny metallic, bold vintage style text, casino slot machine button look. IMPORTANT: solid bright green background (#00FF00) for easy removal.", "16:9"),
}


def generate(sprite_name):
    if sprite_name not in SPRITES:
        print(f"Unknown sprite: {sprite_name}")
        print(f"Available: {', '.join(SPRITES.keys())}")
        return

    subfolder, prompt, aspect_ratio = SPRITES[sprite_name]
    output_dir = os.path.join(BASE_DIR, subfolder)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating {sprite_name}...")
    print(f"Folder: {subfolder}/")
    print(f"Aspect: {aspect_ratio}")
    print(f"Prompt: {prompt[:80]}...")

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=aspect_ratio,
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        )
    )

    if response.generated_images:
        image_data = response.generated_images[0].image.image_bytes
        output_path = os.path.join(output_dir, f"{sprite_name}.png")

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"Saved: {output_path}")
        print(f"Size: {len(image_data) / 1024:.1f} KB")
    else:
        print("ERROR: No image generated")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3.12 generate_ui_sprite.py <sprite_name>")
        print(f"\nAvailable sprites:")
        for name, (folder, _, _) in SPRITES.items():
            print(f"  {name} ({folder}/)")
    else:
        generate(sys.argv[1])
