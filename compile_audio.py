#!/usr/bin/env python3
"""Compile all audio files into a single sprite and generate sounds.json"""
import os
import subprocess
import json

RAW_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/audio/raw"
OUTPUT_DIR = "/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/audio"

# Define the order and mapping of sounds
# Format: (source_file, sprite_name, loop)
SOUND_MAP = [
    # BGM
    ("bgm/synth_loop.mp3", "bgm_main", True),
    ("bgm/synth_loop.mp3", "bgm_freespin", True),  # Reuse for now
    ("bgm/synth_loop.mp3", "bgm_alpha_domination", True),  # Reuse for now

    # Spins
    ("sfx_spins/wheel_spin.mp3", "sfx_spin_start", False),
    ("sfx_spins/reel_stop_1.mp3", "sfx_reel_stop_1", False),
    ("sfx_spins/reel_stop_2.mp3", "sfx_reel_stop_2", False),
    ("sfx_spins/reel_stop_1.mp3", "sfx_reel_stop_3", False),  # Reuse
    ("sfx_spins/reel_stop_2.mp3", "sfx_reel_stop_4", False),  # Reuse
    ("sfx_spins/reel_stop_1.mp3", "sfx_reel_stop_5", False),  # Reuse
    ("sfx_spins/reel_stop_2.mp3", "sfx_reel_stop_6", False),  # Reuse
    ("sfx_features/impact.mp3", "sfx_anticipation", False),

    # Scatter
    ("sfx_features/achievement.mp3", "sfx_scatter_stop_1", False),
    ("sfx_features/achievement.mp3", "sfx_scatter_stop_2", False),
    ("sfx_features/achievement.mp3", "sfx_scatter_stop_3", False),
    ("sfx_features/achievement.mp3", "sfx_scatter_stop_4", False),
    ("sfx_features/achievement.mp3", "sfx_scatter_stop_5", False),
    ("sfx_features/achievement.mp3", "sfx_scatter_stop_6", False),
    ("sfx_features/power_up.mp3", "sfx_scatter_win", False),

    # Wins
    ("sfx_wins/coin_win.mp3", "sfx_win_small", False),
    ("sfx_wins/slot_win.mp3", "sfx_win_medium", False),
    ("sfx_wins/bonus_collect.mp3", "sfx_win_large", False),
    ("sfx_wins/payout.mp3", "tumble_win_1", False),
    ("sfx_wins/payout.mp3", "tumble_win_2", False),
    ("sfx_wins/payout.mp3", "tumble_win_3", False),
    ("sfx_wins/payout.mp3", "tumble_win_4", False),
    ("sfx_wins/payout.mp3", "tumble_win_5", False),
    ("sfx_wins/win_siren.mp3", "sfx_bigwin_coinloop", True),
    ("sfx_features/level_up.mp3", "sfx_youwon_panel", False),

    # Features
    ("sfx_features/level_up.mp3", "sfx_multiplier_up", False),
    ("sfx_features/power_up.mp3", "sfx_multiplier_max", False),
    ("sfx_features/explosion.mp3", "sfx_pack_split", False),
    ("sfx_features/wolves_pack.mp3", "sfx_howl_chain_add", False),
    ("sfx_features/wolves_pack.mp3", "sfx_howl_chain_multi", False),
    ("sfx_features/impact.mp3", "sfx_territory_expand", False),
    ("sfx_features/power_up.mp3", "sfx_freespin_trigger", False),
    ("sfx_features/achievement.mp3", "sfx_freespin_intro", False),
    ("sfx_features/power_up.mp3", "sfx_freespin_retrigger", False),
    ("sfx_features/explosion.mp3", "sfx_alpha_domination_intro", False),
    ("sfx_features/wolf_howl_1.mp3", "sfx_wolf_howl_1", False),
    ("sfx_features/wolf_howl_2.mp3", "sfx_wolf_howl_2", False),
    ("sfx_features/explosion.mp3", "sfx_cascade_explosion", False),
    ("sfx_features/impact.mp3", "sfx_symbols_landing", False),

    # UI
    ("sfx_ui/btn_click.mp3", "sfx_btn_general", False),
    ("sfx_ui/btn_click.mp3", "sfx_btn_spin", False),
    ("sfx_ui/menu_open.mp3", "sfx_menu_open", False),
]

def get_duration_ms(filepath):
    """Get duration of audio file in milliseconds"""
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", filepath
    ], capture_output=True, text=True)
    try:
        return int(float(result.stdout.strip()) * 1000)
    except:
        return 1000  # Default 1 second if failed

def main():
    print("=== Compiling Audio Sprite ===\n")

    # Create list of files to concatenate
    concat_list = []
    sprite_data = {}
    current_position = 0

    for source_file, sprite_name, loop in SOUND_MAP:
        full_path = os.path.join(RAW_DIR, source_file)

        if not os.path.exists(full_path):
            print(f"⚠ Missing: {source_file}")
            continue

        duration = get_duration_ms(full_path)
        concat_list.append(full_path)

        # Store sprite info: [start, duration, loop?]
        if loop:
            sprite_data[sprite_name] = [current_position, duration, True]
        else:
            sprite_data[sprite_name] = [current_position, duration]

        print(f"✓ {sprite_name}: {current_position}ms, {duration}ms")
        current_position += duration

    # Create concat file for ffmpeg
    concat_file = "/tmp/concat_list.txt"
    with open(concat_file, "w") as f:
        for path in concat_list:
            f.write(f"file '{path}'\n")

    # Concatenate with ffmpeg
    output_mp3 = os.path.join(OUTPUT_DIR, "sounds.mp3")
    print(f"\n=== Concatenating {len(concat_list)} files ===")

    result = subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
        "-acodec", "libmp3lame", "-b:a", "192k", output_mp3
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ Created: sounds.mp3")
    else:
        print(f"✗ Error: {result.stderr}")
        return

    # Generate sounds.json
    sounds_json = {
        "src": ["sounds.mp3"],
        "sprite": sprite_data,
        "config": {
            "bgm_main": {"volume": 0.7},
            "bgm_freespin": {"volume": 0.8},
            "bgm_alpha_domination": {"volume": 0.9},
            "sfx_bigwin_coinloop": {"volume": 0.8},
            "sfx_wolf_howl_1": {"volume": 1.0},
            "sfx_wolf_howl_2": {"volume": 1.0}
        }
    }

    json_path = os.path.join(OUTPUT_DIR, "sounds.json")
    with open(json_path, "w") as f:
        json.dump(sounds_json, f, indent=2)

    print(f"✓ Created: sounds.json")
    print(f"\n=== Done! Total duration: {current_position}ms ({current_position/1000:.1f}s) ===")

if __name__ == "__main__":
    main()
