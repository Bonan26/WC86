#!/usr/bin/env python3
"""Create simple animation JSON for symbols"""
import json
import os

SYMBOLS_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/spines/symbols"
STATIC_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/sprites/symbolsStatic"

# Animation templates
BASE_ANIMS = {
    "idle": {
        "type": "breathe",
        "duration": 2000,
        "loop": True,
        "keyframes": [
            {"time": 0, "scale": 1.0, "opacity": 1.0},
            {"time": 0.5, "scale": 1.03, "opacity": 1.0},
            {"time": 1.0, "scale": 1.0, "opacity": 1.0}
        ]
    },
    "land": {
        "type": "bounce",
        "duration": 400,
        "loop": False,
        "keyframes": [
            {"time": 0, "scale": 1.2, "y": -20},
            {"time": 0.3, "scale": 0.95, "y": 5},
            {"time": 0.6, "scale": 1.02, "y": -2},
            {"time": 1.0, "scale": 1.0, "y": 0}
        ]
    },
    "win": {
        "type": "pulse_glow",
        "duration": 800,
        "loop": True,
        "keyframes": [
            {"time": 0, "scale": 1.0, "brightness": 1.0, "glow": 0},
            {"time": 0.25, "scale": 1.1, "brightness": 1.3, "glow": 10},
            {"time": 0.5, "scale": 1.0, "brightness": 1.0, "glow": 5},
            {"time": 0.75, "scale": 1.1, "brightness": 1.3, "glow": 10},
            {"time": 1.0, "scale": 1.0, "brightness": 1.0, "glow": 0}
        ]
    },
    "explosion": {
        "type": "explode",
        "duration": 500,
        "loop": False,
        "keyframes": [
            {"time": 0, "scale": 1.0, "opacity": 1.0, "rotation": 0},
            {"time": 0.3, "scale": 1.3, "opacity": 0.8, "rotation": 15},
            {"time": 0.6, "scale": 0.8, "opacity": 0.4, "rotation": -10},
            {"time": 1.0, "scale": 0, "opacity": 0, "rotation": 0}
        ]
    }
}

# Special animations for specific symbols
SPECIAL_ANIMS = {
    "alpha_wolf": {
        "split": {
            "type": "duplicate",
            "duration": 600,
            "loop": False,
            "keyframes": [
                {"time": 0, "scale": 1.0, "copies": 1},
                {"time": 0.3, "scale": 1.2, "copies": 1, "flash": True},
                {"time": 0.5, "scale": 1.0, "copies": 2, "spread": 50},
                {"time": 1.0, "scale": 1.0, "copies": 2, "spread": 100}
            ]
        }
    },
    "howling_wild": {
        "howl": {
            "type": "howl",
            "duration": 1000,
            "loop": False,
            "keyframes": [
                {"time": 0, "scale": 1.0, "y": 0},
                {"time": 0.2, "scale": 1.1, "y": -10},
                {"time": 0.5, "scale": 1.15, "y": -15, "glow": 20},
                {"time": 0.8, "scale": 1.1, "y": -10, "glow": 10},
                {"time": 1.0, "scale": 1.0, "y": 0, "glow": 0}
            ]
        }
    },
    "territory": {
        "glow": {
            "type": "territory_glow",
            "duration": 1500,
            "loop": True,
            "keyframes": [
                {"time": 0, "glow": 0, "glow_color": "#FFD700"},
                {"time": 0.5, "glow": 15, "glow_color": "#FFD700"},
                {"time": 1.0, "glow": 0, "glow_color": "#FFD700"}
            ]
        }
    }
}

SYMBOLS = [
    "boss_wolf", "hustler", "tech_bro", "diamond_hands",
    "cocktail", "vip_card", "disco_ball", "dice",
    "alpha_wolf", "howling_wild", "moon_scatter", "territory"
]

def create_symbol_json(symbol_name):
    """Create animation JSON for a symbol"""

    # Start with base animations
    anims = dict(BASE_ANIMS)

    # Add special animations if any
    if symbol_name in SPECIAL_ANIMS:
        anims.update(SPECIAL_ANIMS[symbol_name])

    data = {
        "name": symbol_name,
        "image": f"../../sprites/symbolsStatic/{symbol_name}.png",
        "size": {"width": 200, "height": 200},
        "anchor": {"x": 0.5, "y": 0.5},
        "animations": anims
    }

    return data

def main():
    for symbol in SYMBOLS:
        symbol_dir = os.path.join(SYMBOLS_DIR, symbol)
        os.makedirs(symbol_dir, exist_ok=True)

        # Create JSON
        data = create_symbol_json(symbol)
        json_path = os.path.join(symbol_dir, f"{symbol}.json")

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Created: {symbol}.json")

    print(f"\nDone! Created {len(SYMBOLS)} symbol animation files.")

if __name__ == "__main__":
    main()
