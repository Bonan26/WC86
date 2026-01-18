#!/bin/bash
# Download free sounds from Mixkit and other sources

BASE="/Users/ariebonan/Desktop/WC86/web-sdk/apps/wc86/static/assets/audio/raw"
MIXKIT="https://assets.mixkit.co/active_storage/sfx"

cd "$BASE"

echo "=== Downloading Wolf Sounds ==="
curl -sL -o sfx_features/wolf_howl_1.mp3 "$MIXKIT/2532/2532-preview.mp3" && echo "✓ wolf_howl_1"
curl -sL -o sfx_features/wolf_howl_2.mp3 "$MIXKIT/2533/2533-preview.mp3" && echo "✓ wolf_howl_2"
curl -sL -o sfx_features/wolves_pack.mp3 "$MIXKIT/2534/2534-preview.mp3" && echo "✓ wolves_pack"

echo ""
echo "=== Downloading Slot/Casino Sounds ==="
curl -sL -o sfx_wins/slot_win.mp3 "$MIXKIT/2018/2018-preview.mp3" && echo "✓ slot_win"
curl -sL -o sfx_wins/coin_win.mp3 "$MIXKIT/2003/2003-preview.mp3" && echo "✓ coin_win"
curl -sL -o sfx_wins/bonus_collect.mp3 "$MIXKIT/2019/2019-preview.mp3" && echo "✓ bonus_collect"
curl -sL -o sfx_wins/payout.mp3 "$MIXKIT/2020/2020-preview.mp3" && echo "✓ payout"
curl -sL -o sfx_wins/win_siren.mp3 "$MIXKIT/2021/2021-preview.mp3" && echo "✓ win_siren"
curl -sL -o sfx_spins/wheel_spin.mp3 "$MIXKIT/2017/2017-preview.mp3" && echo "✓ wheel_spin"

echo ""
echo "=== Downloading UI Sounds ==="
curl -sL -o sfx_ui/btn_click.mp3 "$MIXKIT/2568/2568-preview.mp3" && echo "✓ btn_click"
curl -sL -o sfx_ui/btn_hover.mp3 "$MIXKIT/2571/2571-preview.mp3" && echo "✓ btn_hover"
curl -sL -o sfx_ui/menu_open.mp3 "$MIXKIT/2574/2574-preview.mp3" && echo "✓ menu_open"

echo ""
echo "=== Downloading Impact/Explosion Sounds ==="
curl -sL -o sfx_features/explosion.mp3 "$MIXKIT/1662/1662-preview.mp3" && echo "✓ explosion"
curl -sL -o sfx_features/impact.mp3 "$MIXKIT/2803/2803-preview.mp3" && echo "✓ impact"

echo ""
echo "=== Downloading Reel Stop Sounds ==="
curl -sL -o sfx_spins/reel_stop_1.mp3 "$MIXKIT/2073/2073-preview.mp3" && echo "✓ reel_stop_1"
curl -sL -o sfx_spins/reel_stop_2.mp3 "$MIXKIT/2074/2074-preview.mp3" && echo "✓ reel_stop_2"

echo ""
echo "=== Downloading Multiplier/Level Up ==="
curl -sL -o sfx_features/level_up.mp3 "$MIXKIT/1978/1978-preview.mp3" && echo "✓ level_up"
curl -sL -o sfx_features/power_up.mp3 "$MIXKIT/1979/1979-preview.mp3" && echo "✓ power_up"
curl -sL -o sfx_features/achievement.mp3 "$MIXKIT/1980/1980-preview.mp3" && echo "✓ achievement"

echo ""
echo "=== Downloading BGM (searching for synth/retro) ==="
curl -sL -o bgm/synth_loop.mp3 "$MIXKIT/649/649-preview.mp3" && echo "✓ synth_loop"

echo ""
echo "Done! Downloaded sounds:"
find "$BASE" -name "*.mp3" | wc -l
