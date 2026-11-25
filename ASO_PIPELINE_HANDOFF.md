# 🚀 Antigravity ASO Pipeline Handoff Guide

## 📊 Current Status Overview
- **Completed Games**: 44 / 58 (44 completed with genuine Flutter code verification, native UI/gameplay captures, and Full HD synced trailers; 14 verified game branches remaining in queue).
- **Storage Location**: `D:\souravshuvo.github.io\game_store_assets\<Game-Name>\`
- **Portable ASO Scripts**: [`aso_scripts/`](./aso_scripts/) (`run_phone_aso.py`, `aso_screenshot_engine.py`, `aso_trailer_engine.py`)
- **Master Manifest**: [`PORTFOLIO_ASSETS_MANIFEST.md`](./PORTFOLIO_ASSETS_MANIFEST.md) & [`game_store_assets/README.md`](./game_store_assets/README.md)
- **Source Code Repository**: `https://github.com/souravshuvo/project-game.git`
- **Store Assets Repository**: `https://github.com/souravshuvo/souravshuvo.github.io.git`

---

## 🏆 Completed Games (1 – 44)
1. `Twin-Tower-Drop` (`com.childhood.twintowerdrop`)
2. `Amaze-Roll` (`com.childhood.amazeroll`)
3. `Bike-Traffic-Racer` (`com.childhood.bike`)
4. `Swirl-Studio-Ice-Cream` (`com.childhood.cream`)
5. `Smash-DIY-ASMR` (`com.childhood.smash`)
6. `City-Cleaner-Hole` (`com.childhood.city`)
7. `Dog-Escape-Run` (`com.childhood.dogescape`)
8. `Sholo-Guti-16-Beads` (`com.childhood.sixteenbreed`)
9. `Save-the-King-Match3` (`com.childhood.savetheking`)
10. `Emoji-Merge-Link` (`com.childhood.emoji`)
11. `Helix-Jump-Spiral` (`com.childhood.helix`)
12. `Knife-Hit-Master` (`com.childhood.knife`)
13. `Sky-Putt-Mini-Golf` (`com.childhood.golf`)
14. `Speed-Runner-3D` (`com.childhood.run`)
15. `Titan-Worm-Arcade` (`com.childhood.titanworm`)
16. `Wing-Rush-Glide` (`com.childhood.wing`)
17. `Rivet-Block-Escape` (`com.childhood.escape`)
18. `Pedal-Post-Rush` (`com.childhood.pedal`)
19. `Slap-and-Run` (`com.childhood.slaprun`)
20. `Merge-Pair-Pastry` (`com.childhood.mergepair`)
21. `Latchloom-Rings` (`com.childhood.latchloomrings`)
22. `Block-Grove-Puzzle` (`com.childhood.block`)
23. `Bolt-&-Balance` (`com.childhood.boltbalance`)
24. `Cable-Garden` (`com.childhood.cablegarden`)
25. `Carve-the-Shape` (`com.childhood.carvetheshape`)
26. `Color-Courtyard` (`com.childhood.colorcourtyard`)
27. `Cozy-Fit` (`com.childhood.cozyfit`)
28. `Domino-Detour` (`com.childhood.dominodetour`)
29. `Fold-&-Stamp` (`com.childhood.foldstamp` — folder `Fold-and-Stamp`)
30. `Meadow-Claim` (`com.childhood.meadowclaim`)
31. `Night-Market-Minute` (`com.childhood.nightmarketminute` — replaced non-existent `Merge-Market` placeholder)
32. `Object-Finder` (`com.childhood.objectfinder`)
33. `Pocket-Habitat` (`com.childhood.pockethabitat`)
34. `Pocket-Pinball-Expedition` (`com.childhood.pocketpinballexpedition`)
35. `Sum-Foundry` (`com.childhood.sumfoundry`)
36. `Switchyard-Minute` (`com.childhood.switchyardminute`)
37. `Word-Trail-Expedition` (`com.childhood.wordtrailexpedition`)
38. `Arrow-Flow` (`com.childhood.arrowflow`, Branch: `arrow_flow`)
39. `Can-Smash` (`com.childhood.smash`, Branch: `can_smash` — distinct from #5 `Smash-DIY-ASMR`)
40. `Canopy-Rush` (`com.childhood.canopyrush`, Branch: `canopy_rush`)
41. `Card-Haven` (`com.childhood.cardhaven`, Branch: `card-haven`)
42. `City-Hole` (`com.childhood.city`, Branch: `city_hole` — distinct from #6 `City-Cleaner-Hole`)
43. `Color-Sort` (`com.childhood.weatherlabsort`, Branch: `color_sort`)
44. `Dew-Bubble-Garden` (`com.childhood.dewbubble`, Branch: `dew_bubble`)

---

## 📋 Next Queue (Games 45–58 — All 14 Remaining Verified `project-game.git` Branches)
45. **food_order** (`origin/food_order` — Bite Stack: Food Match / Stack, `com.childhood.stack`)
46. **gate_squad** (`origin/gate_squad` — Gate Squad: Runner Shooter, `com.childhood.gatesquad`)
47. **brain-wink** (`origin/brain-wink` — Brain Wink: Notebook Puzzles, `com.childhood.brainwink`)
48. **bridal** (`origin/bridal` — Skyline Relay, `com.childhood.skylinerelay`)
49. **dot-and-box** (`origin/dot-and-box` — Dots and Boxes: 2 Player Game, `com.childhood.dotsandboxes`)
50. **kettle_match** (`origin/kettle_match` — Kettle Match: Triple Tile, `com.childhood.kettlematch`)
51. **kids_land** (`origin/kids_land` — Kids Land: ABC & 123 Learning, `com.childhood.kidsland`)
52. **killer** (`origin/killer` — SWAT: Insect Tap Challenge, `com.childhood.swat`)
53. **mini_games** (`origin/mini_games` — Mini Games: Pocket Arcade, `com.childhood.minigames`)
54. **pen_cricket** (`origin/pen_cricket` — Pen Cricket: Spin & Chase, `com.childhood.pencricket`)
55. **police_thief** (`origin/police_thief` — Chor Police: Hidden Roles, `com.childhood.policethief`)
56. **space_shooter** (`origin/space_shooter` — Space Shooter: Galaxy Patrol, `com.childhood.spaceshooter`)
57. **sudoku** (`origin/sudoku` — Sudoku Lantern: Number Puzzles, `com.childhood.sudoku`)
58. **tic_tac_toe** (`origin/tic_tac_toe` — Tic Tac Toe: Two Player XO, `com.childhood.tictactoe`)

> *(Excludes `main` archive branch and `codex/*` WIP branches; prior speculative placeholder names not present in the repo remain excluded.)*

---

## 🎯 Twin-Tower / Amaze-Roll Standard Specification

For each game, create the following 5 assets under `D:\souravshuvo.github.io\game_store_assets\<Game-Name>\`:

1. **Official Icon (512×512)**:
   - Path: `icon/icon_512.png`
   - Verified 512×512 PNG, RGBA with crisp rounded design.

2. **Feature Graphic (1024×500)**:
   - Path: `feature_graphic/feature_graphic_1024x500.png`
   - Verified 1024×500 PNG, RGB.

3. **8 Ultra 3D Pop-Out Screenshots (1080×1920)**:
   - Path: `screenshots/screenshot_01.png` to `08.png`
   - 3-stop game theme gradient background + 24 sunburst radial rays + soft particle sparkles.
   - Floating titanium smartphone mockup with camera punch hole, rounded borders, and multi-layered Gaussian drop shadow.
   - 5-point drawn golden star badge with category pill (`★ 4.9 · CATEGORY`).
   - Extruded 3D typography headers with dual-layer depth.
   - 3D Pop-out character / game sprite bursting past bezel boundaries.
   - Dual 3D floating pill action stickers.

4. **2 Full HD Video Trailers (Gyan FFmpeg)**:
   - **Portrait 9:16 (1080×1920)**: `videos/<game>_trailer_portrait_9x16.mp4`
   - **Landscape 16:9 (1920×1080)**: `videos/<game>_trailer_landscape_16x9.mp4`
   - Authentic gameplay action with live phone capture or high-fidelity simulation.
   - Synchronized authentic game OST (looping BGM) and SFX for taps, moves, clears, and victory.
   - 4 timed pop action callouts.
   - 3.5s animated Google Play CTA endcard with app icon, 5 gold stars, title, and button.

5. **Raw Captures**:
   - Path: `raw_captures/`
   - Store all high-res native in-game screenshots and UI frames.

---

## 💬 How to Continue on Any PC (New Conversation Prompt)

When opening a new conversation in Antigravity (at home or elsewhere):

1. Ensure the workspace is set to your local clone of `souravshuvo.github.io` (e.g. `d:\souravshuvo.github.io` or any drive/path on your PC).
2. Run `git pull origin main` to get the latest assets and portable [`aso_scripts/`](./aso_scripts/) (`run_phone_aso.py`, `aso_screenshot_engine.py`, `aso_trailer_engine.py`).
3. Ensure `flutter`, `adb`, `python` (+ `pillow`), and `ffmpeg`/`ffprobe` are installed, connect your Android phone via USB Debugging, and paste the prompt into a new chat:

```text
আমি আমার Flutter গেম পোর্টফোলিওর ASO অ্যাসেট তৈরির কাজ কন্টিনিউ করতে চাই।
ইতিমধ্যে ১ থেকে ৪৪ নম্বর গেম সম্পন্ন হয়েছে (PORTFOLIO_ASSETS_MANIFEST.md এবং ASO_PIPELINE_HANDOFF.md দেখো)।
এখন ৪৫তম গেম food_order (Branch: origin/food_order from https://github.com/souravshuvo/project-game.git) থেকে শুরু করে স্ট্রিক্টলি ১টি ১টি করে গেম প্রসেস করা শুরু করো:
১. গেমটির ব্রাঞ্চ চেকআউট করে প্যাকেজ আইডি, সোর্স কোড ও অরিজিনাল অডিও/গ্রাফিক ভেরিফাই করা।
২. ৫১২×৫১২ আইকন ও ১০২৪×৫০০ ব্যানার সংরক্ষণ।
৩. ৮টি আল্ট্রা ৩ডি পপ-আউট স্ক্রিনশট (১০৮০×১৯২০) তৈরি (টুইন-টাওয়ার স্ট্যান্ডার্ড)।
৪. ২টি ফুল HD ভিডিও ট্রেইলার (পোর্ট্রেট ৯:১৬ ও ল্যান্ডস্কেপ ১৬:৯) অরিজিনাল সাউন্ড ও গুগল প্লে এন্ডকার্ড সহ রেন্ডার।
৫. D:\souravshuvo.github.io\game_store_assets\<Game-Name>\ এ সংরক্ষণ এবং PORTFOLIO_ASSETS_MANIFEST.md আপডেট করা।
```
