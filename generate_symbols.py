#!/usr/bin/env python3.12
"""
WC86 Symbol Generation with Gemini Imagen 4
Generates the 6 remaining static symbols in the same style as the wolves
"""

from google import genai
from google.genai import types
import os
import base64

# API Key
API_KEY = "AIzaSyDO6tt-Ft4zdkm8GZws8lp_bNw2l-zYM40"

# Output directory
OUTPUT_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/symbolsStatic"

# Style reference (matching the wolf cartoon style)
STYLE_PROMPT = """
Style: Cartoon illustration, bold black outlines, vibrant colors, 80s retro nightclub aesthetic.
Same style as a cartoon wolf character with exaggerated features.
High quality, detailed, transparent background (PNG with alpha).
Square format, centered composition, suitable for a slot game symbol.
"""

# Symbols to generate
SYMBOLS = {
    "cocktail": {
        "prompt": f"""A stylish martini cocktail glass with neon pink/blue liquid,
        olive on a stick, glowing neon effect, 80s disco nightclub style.
        {STYLE_PROMPT}"""
    },
    "vip_card": {
        "prompt": f"""A golden VIP membership card with holographic shine,
        "VIP" text embossed, luxury nightclub access card, metallic gold.
        {STYLE_PROMPT}"""
    },
    "disco_ball": {
        "prompt": f"""A shiny disco mirror ball reflecting colorful lights,
        sparkling reflections, 80s disco party, silver mirrors facets.
        {STYLE_PROMPT}"""
    },
    "dice": {
        "prompt": f"""A pair of casino dice glowing with neon light,
        showing lucky numbers, 80s neon style, vibrant pink/blue glow.
        {STYLE_PROMPT}"""
    },
    "moon_scatter": {
        "prompt": f"""A large full moon with a wolf silhouette howling,
        mystical purple/blue glow around it, "SCATTER" text below,
        nightclub meets mystical wolf theme.
        {STYLE_PROMPT}"""
    },
    "territory": {
        "prompt": f"""A golden territory marker or flag with wolf paw print symbol,
        glowing golden aura, represents wolf pack territory, tribal style.
        {STYLE_PROMPT}"""
    },
}


def generate_symbol(client, name, prompt):
    """Generate a single symbol using Imagen 4."""
    print(f"\nGenerating {name}...")
    print(f"  Prompt: {prompt[:80]}...")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="BLOCK_LOW_AND_ABOVE",
                person_generation="DONT_ALLOW",
            )
        )

        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            output_path = os.path.join(OUTPUT_DIR, f"{name}.png")

            with open(output_path, "wb") as f:
                f.write(image_data)

            print(f"  Saved: {output_path}")
            print(f"  Size: {len(image_data) / 1024:.1f} KB")
            return True
        else:
            print(f"  ERROR: No image generated")
            return False

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    print("=" * 50)
    print("WC86 Symbol Generation - Gemini Imagen 4")
    print("=" * 50)

    # Initialize client
    client = genai.Client(api_key=API_KEY)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate each symbol
    success_count = 0
    for name, config in SYMBOLS.items():
        if generate_symbol(client, name, config["prompt"]):
            success_count += 1

    print("\n" + "=" * 50)
    print(f"Generation complete! {success_count}/{len(SYMBOLS)} symbols created")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)

    # List all symbol files
    print("\nAll symbol files:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            path = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(path)
            print(f"  {f} ({size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
