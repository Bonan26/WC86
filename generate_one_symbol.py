#!/usr/bin/env python3.12
"""
WC86 - Generate one symbol at a time with Gemini Imagen 4
Usage: python3.12 generate_one_symbol.py <symbol_name>
"""

from google import genai
from google.genai import types
import os
import sys

# API Key
API_KEY = "AIzaSyDO6tt-Ft4zdkm8GZws8lp_bNw2l-zYM40"

# Output directory
OUTPUT_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/symbolsStatic"

# Style reference - matching the cartoon wolves
STYLE = """Hand-drawn cartoon style with thick bold black outlines, cel-shaded coloring,
exaggerated proportions, vibrant saturated colors, similar to classic cartoon characters.
The object should look like it belongs in a cartoon wolf universe.
IMPORTANT: Plain solid bright green background (#00FF00 lime green) for easy removal.
Square format, centered, large object filling most of the frame."""

# Symbol prompts
PROMPTS = {
    "cocktail": f"A cartoon martini cocktail glass with pink liquid, olive on stick, the glass has personality with curved shapes, thick black outlines around everything. {STYLE}",

    "vip_card": f"A cartoon golden VIP card, shiny metallic gold, 'VIP' text in bold, sparkles around it, thick black outlines, looks expensive and cartoony. {STYLE}",

    "disco_ball": f"A cartoon disco ball, silver mirror facets, colorful light reflections, happy party vibe, thick black outlines, fun and bouncy looking. {STYLE}",

    "dice": f"Two cartoon casino dice, one red one white, showing dots only (no numbers, just dots like real dice), thick black outlines, slightly tilted, fun gambling vibe. {STYLE}",

    "moon_scatter": f"A cartoon full moon with a howling wolf silhouette inside it, purple mystical glow, thick black outlines, magical nighttime vibe. {STYLE}",

    "territory": f"A cartoon golden paw print emblem, like a wolf territory marker, shiny gold with thick black outlines, tribal badge style. {STYLE}",
}


def generate(symbol_name):
    if symbol_name not in PROMPTS:
        print(f"Unknown symbol: {symbol_name}")
        print(f"Available: {', '.join(PROMPTS.keys())}")
        return

    print(f"Generating {symbol_name}...")
    print(f"Prompt: {PROMPTS[symbol_name][:100]}...")

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=PROMPTS[symbol_name],
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        )
    )

    if response.generated_images:
        image_data = response.generated_images[0].image.image_bytes
        output_path = os.path.join(OUTPUT_DIR, f"{symbol_name}.png")

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"Saved: {output_path}")
        print(f"Size: {len(image_data) / 1024:.1f} KB")
    else:
        print("ERROR: No image generated")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3.12 generate_one_symbol.py <symbol_name>")
        print(f"Available symbols: {', '.join(PROMPTS.keys())}")
    else:
        generate(sys.argv[1])
