#!/usr/bin/env python3
"""
WC86 Wolf Assembly Script
Assembles wolf characters from layered PNG parts
"""

from PIL import Image
import os

# Paths
PARTS_DIR = "/Users/ariebonan/Desktop/WC86/Wolf_parts_final"
OUTPUT_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/symbolsStatic"

# Wolf configurations (layers from bottom to top)
WOLVES = {
    "boss_wolf": {
        "fur_mouth": "Fur_Mouth/Grey_Smiling.png",
        "shirt": "Shirt/suit.png",
        "eyes": "Eyes/suspicious_grey.png",
        "glasses": "Glasses/monocle.png",
        "neckless": "neckless/neckring.png",
    },
    "hustler": {
        "fur_mouth": "Fur_Mouth/Red_Mocking.png",
        "vest": "Vest/perfecto.png",
        "eyes": "Eyes/high_red.png",
        "ears": "ears_accessories/eargold.png",
    },
    "tech_bro": {
        "fur_mouth": "Fur_Mouth/Blue_Boring.png",
        "shirt": "Shirt/turtleneck.png",
        "eyes": "Eyes/chill_blue.png",
        "glasses": "Glasses/hipster.png",
    },
    "diamond_hands": {
        "fur_mouth": "Fur_Mouth/GradientPurple_Smiling.png",
        "vest": "Vest/pimp.png",
        "eyes": "Eyes/high_snake.png",
        "glasses": "Glasses/kw.png",
    },
}

# Layer order (bottom to top)
LAYER_ORDER = ["fur_mouth", "shirt", "vest", "neckless", "tatoo", "eyes", "glasses", "hat", "ears", "mouth_acc"]


def assemble_wolf(name, layers):
    """Assemble a wolf from multiple PNG layers."""
    print(f"\nAssembling {name}...")

    # Start with a transparent base
    base = None

    for layer_name in LAYER_ORDER:
        if layer_name not in layers:
            continue

        layer_path = os.path.join(PARTS_DIR, layers[layer_name])

        if not os.path.exists(layer_path):
            print(f"  WARNING: {layer_path} not found, skipping")
            continue

        print(f"  Adding layer: {layers[layer_name]}")
        layer = Image.open(layer_path).convert("RGBA")

        if base is None:
            base = layer
        else:
            # Resize layer to match base if needed
            if layer.size != base.size:
                layer = layer.resize(base.size, Image.Resampling.LANCZOS)
            # Composite layer on top
            base = Image.alpha_composite(base, layer)

    if base is None:
        print(f"  ERROR: No layers found for {name}")
        return

    # Save with transparent background
    output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    base.save(output_path, "PNG")
    print(f"  Saved: {output_path}")
    print(f"  Size: {base.size}")


def main():
    print("=" * 50)
    print("WC86 Wolf Assembly")
    print("=" * 50)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Assemble each wolf
    for name, layers in WOLVES.items():
        assemble_wolf(name, layers)

    print("\n" + "=" * 50)
    print("Assembly complete!")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 50)

    # List output files
    print("\nGenerated files:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            path = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(path)
            print(f"  {f} ({size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
