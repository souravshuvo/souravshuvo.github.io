# Portable ASO Pipeline Scripts

These scripts power the Twin-Tower 3D ASO screenshots, live physical-device capture, and synced Full HD trailers across any PC without hardcoded drive letters or user-specific scratch folders.

## Included Scripts
- `run_phone_aso.py`: Runs `integration_test/_phone_aso_test.dart` on the connected Android phone (`--device auto` auto-detects `adb devices`, keeping Motorola Edge 50 `ZD222PJ69H` preferred if connected), pulls lossless `ASO_SNAP:<name>` PNGs into `--raw-dir`, and records high-bitrate MP4 gameplay between `ASO_REC_START` and `ASO_REC_STOP`. Auto-locates `flutter` and `adb`.
- `aso_screenshot_engine.py`: Renders 8 × `1080×1920` Twin-Tower / Landscape Titanium bezel 3D pop-out cards into `game_store_assets/<Game>/screenshots/` (and optionally mirrors to `--mirror-dir`). Auto-detects repository root (`REPO_ROOT`) and Flutter Material Roboto / Windows fallback fonts.
- `aso_trailer_engine.py`: Mixes looping game BGM (`-stream_loop -1`) with millisecond-delayed in-game SFX (`ffprobe`-clean 44.1 kHz stereo AAC) and renders `17.50s` Full HD `1080×1920` (9:16 portrait) and `1920×1080` (16:9 landscape) H.264 trailers with PiP inset, 4 timed callouts, and an animated Google Play CTA endcard into `game_store_assets/<Game>/videos/`.

## Prerequisites on Any Machine
- Flutter SDK (`flutter` on `PATH` or `FLUTTER_ROOT` env var)
- Android SDK `platform-tools` (`adb` on `PATH` or `ANDROID_HOME` / default SDK path)
- Python 3 + `Pillow` (`pip install pillow`)
- `ffmpeg` and `ffprobe` on `PATH`
