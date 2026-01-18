#!/usr/bin/env python3
"""Create animation JSON for missing effects"""
import json
import os

EFFECTS_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/spines/effects"

EFFECTS = {
    "howlChain": {
        "name": "howlChain",
        "description": "Lines connecting wild symbols",
        "animations": {
            "chain_2": {
                "type": "chain_connect",
                "duration": 500,
                "loop": False,
                "keyframes": [
                    {"time": 0, "opacity": 0, "line_width": 0},
                    {"time": 0.3, "opacity": 1, "line_width": 5, "glow": 10},
                    {"time": 1.0, "opacity": 1, "line_width": 3, "glow": 5}
                ],
                "effect": "additive_multiplier"
            },
            "chain_3plus": {
                "type": "chain_connect",
                "duration": 700,
                "loop": False,
                "keyframes": [
                    {"time": 0, "opacity": 0, "line_width": 0},
                    {"time": 0.2, "opacity": 1, "line_width": 8, "glow": 20},
                    {"time": 0.5, "opacity": 1, "line_width": 6, "glow": 15, "flash": True},
                    {"time": 1.0, "opacity": 1, "line_width": 4, "glow": 10}
                ],
                "effect": "multiplicative_multiplier"
            },
            "connection": {
                "type": "particle_line",
                "duration": 300,
                "loop": True,
                "keyframes": [
                    {"time": 0, "particle_count": 5, "speed": 100},
                    {"time": 1.0, "particle_count": 5, "speed": 100}
                ],
                "color": "#FFD700"
            }
        }
    },
    "packSplit": {
        "name": "packSplit",
        "description": "Alpha wolf duplication effect",
        "animations": {
            "split": {
                "type": "split_effect",
                "duration": 800,
                "loop": False,
                "keyframes": [
                    {"time": 0, "scale": 1.0, "flash": False},
                    {"time": 0.2, "scale": 1.3, "flash": True, "shake": 5},
                    {"time": 0.4, "scale": 1.0, "split_start": True},
                    {"time": 0.7, "spread": 80, "opacity": 1},
                    {"time": 1.0, "spread": 100, "opacity": 1}
                ]
            },
            "duplicate": {
                "type": "clone_appear",
                "duration": 400,
                "loop": False,
                "keyframes": [
                    {"time": 0, "scale": 0, "opacity": 0},
                    {"time": 0.3, "scale": 1.2, "opacity": 0.8},
                    {"time": 0.6, "scale": 0.95, "opacity": 1},
                    {"time": 1.0, "scale": 1.0, "opacity": 1}
                ]
            }
        }
    },
    "territoryExpand": {
        "name": "territoryExpand",
        "description": "Grid expansion effect",
        "animations": {
            "expand_7x6": {
                "type": "grid_expand",
                "duration": 1000,
                "loop": False,
                "from_grid": "6x5",
                "to_grid": "7x6",
                "keyframes": [
                    {"time": 0, "scale": 1.0, "glow": 0},
                    {"time": 0.3, "scale": 1.05, "glow": 15, "shake": 3},
                    {"time": 0.6, "expand_progress": 0.5, "glow": 20},
                    {"time": 1.0, "expand_progress": 1.0, "scale": 1.0, "glow": 0}
                ]
            },
            "expand_8x7": {
                "type": "grid_expand",
                "duration": 1000,
                "loop": False,
                "from_grid": "7x6",
                "to_grid": "8x7",
                "keyframes": [
                    {"time": 0, "scale": 1.0, "glow": 0},
                    {"time": 0.3, "scale": 1.05, "glow": 15, "shake": 3},
                    {"time": 0.6, "expand_progress": 0.5, "glow": 20},
                    {"time": 1.0, "expand_progress": 1.0, "scale": 1.0, "glow": 0}
                ]
            },
            "expand_8x8": {
                "type": "grid_expand",
                "duration": 1200,
                "loop": False,
                "from_grid": "8x7",
                "to_grid": "8x8",
                "keyframes": [
                    {"time": 0, "scale": 1.0, "glow": 0},
                    {"time": 0.2, "scale": 1.08, "glow": 20, "shake": 5},
                    {"time": 0.5, "expand_progress": 0.5, "glow": 30, "flash": True},
                    {"time": 0.8, "expand_progress": 0.8, "glow": 20},
                    {"time": 1.0, "expand_progress": 1.0, "scale": 1.0, "glow": 0}
                ]
            }
        }
    },
    "alphaDomination": {
        "name": "alphaDomination",
        "description": "Super bonus mode animations",
        "animations": {
            "intro": {
                "type": "dramatic_intro",
                "duration": 2000,
                "loop": False,
                "keyframes": [
                    {"time": 0, "opacity": 0, "scale": 2.0, "blur": 20},
                    {"time": 0.2, "opacity": 0.5, "scale": 1.5, "blur": 10, "flash": True},
                    {"time": 0.4, "opacity": 1, "scale": 1.2, "blur": 5, "shake": 10},
                    {"time": 0.6, "scale": 1.0, "blur": 0},
                    {"time": 0.8, "fire_intensity": 0.5},
                    {"time": 1.0, "fire_intensity": 1.0, "glow": 15}
                ],
                "background": "bg_alpha_domination"
            },
            "idle": {
                "type": "fire_ambient",
                "duration": 3000,
                "loop": True,
                "keyframes": [
                    {"time": 0, "fire_intensity": 0.8, "glow": 10},
                    {"time": 0.5, "fire_intensity": 1.0, "glow": 15},
                    {"time": 1.0, "fire_intensity": 0.8, "glow": 10}
                ]
            },
            "outro": {
                "type": "fade_out",
                "duration": 1500,
                "loop": False,
                "keyframes": [
                    {"time": 0, "opacity": 1, "fire_intensity": 1.0},
                    {"time": 0.5, "opacity": 0.7, "fire_intensity": 0.5, "blur": 5},
                    {"time": 1.0, "opacity": 0, "fire_intensity": 0, "blur": 15}
                ]
            }
        }
    }
}

def main():
    for effect_name, effect_data in EFFECTS.items():
        effect_dir = os.path.join(EFFECTS_DIR, effect_name)
        os.makedirs(effect_dir, exist_ok=True)

        json_path = os.path.join(effect_dir, f"{effect_name}.json")
        with open(json_path, "w") as f:
            json.dump(effect_data, f, indent=2)

        print(f"Created: {effect_name}.json")

    print(f"\nDone! Created {len(EFFECTS)} effect animation files.")

if __name__ == "__main__":
    main()
