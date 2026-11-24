# 🚀 Antigravity ASO Pipeline Handoff Guide

## 📊 Current Status Overview
- **Completed Games**: 26 / 50 (Strictly 1-by-1, 100% genuine code & gameplay verified).
- **Storage Location**: `D:\souravshuvo.github.io\game_store_assets\<Game-Name>\`
- **Master Manifest**: [`PORTFOLIO_ASSETS_MANIFEST.md`](./PORTFOLIO_ASSETS_MANIFEST.md) & [`game_store_assets/README.md`](./game_store_assets/README.md)
- **Source Code Repository**: `https://github.com/souravshuvo/project-game.git`
- **Store Assets Repository**: `https://github.com/souravshuvo/souravshuvo.github.io.git`

---

## 🏆 Completed Games (1 – 26)
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

---

## 📋 Next Queue (Game 27 Onwards)
27. **Cozy-Fit** (Branch: `origin/Cozy-Fit` in `project-game.git`)
28. **Domino-Detour** (Branch: `origin/Domino-Detour`)
29. **Fold-&-Stamp** (Branch: `origin/Fold-&-Stamp`)
30. **Meadow-Claim** (Branch: `origin/Meadow-Claim`)
31. **Merge-Market** (Branch: `origin/Merge-Market`)
32. **Orbit-&-Ooze** (Branch: `origin/Orbit-&-Ooze`)
33. **Petal-Drop** (Branch: `origin/Petal-Drop`)
34. **Pine-&-Peak** (Branch: `origin/Pine-&-Peak`)
35. **Ribbon-Rail** (Branch: `origin/Ribbon-Rail`)
36. **Rust-&-Rotor** (Branch: `origin/Rust-&-Rotor`)
37. **Sand-&-Spire** (Branch: `origin/Sand-&-Spire`)
38. **Silk-&-Spool** (Branch: `origin/Silk-&-Spool`)
39. **Sip-&-Sort** (Branch: `origin/Sip-&-Sort`)
40. **Solar-Drift** (Branch: `origin/Solar-Drift`)
41. **Spark-&-Spindle** (Branch: `origin/Spark-&-Spindle`)
42. **Tangle-Tavern** (Branch: `origin/Tangle-Tavern`)
43. **Tile-Trek** (Branch: `origin/Tile-Trek`)
44. **Vine-&-Vase** (Branch: `origin/Vine-&-Vase`)
45. **Wax-&-Wick** (Branch: `origin/Wax-&-Wick`)
46. **Windmill-Way** (Branch: `origin/Windmill-Way`)
47. **Yarn-Yard** (Branch: `origin/Yarn-Yard`)
48. **Zen-Zodiac** (Branch: `origin/Zen-Zodiac`)
49. **Carrom-Board-Pro** (Branch: `origin/carrom`)
50. **Ludo-Classic-Star** (Branch: `origin/ludo`)

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

1. Ensure the workspace is set to `d:\souravshuvo.github.io` (or your local clone path).
2. Run `git pull origin main` to get the latest assets.
3. Paste the following prompt into the chat:

```text
আমি আমার Flutter গেম পোর্টফোলিওর ASO অ্যাসেট তৈরির কাজ কন্টিনিউ করতে চাই।
ইতিমধ্যে ১ থেকে ২৬ নম্বর গেম সম্পন্ন হয়েছে (PORTFOLIO_ASSETS_MANIFEST.md এবং ASO_PIPELINE_HANDOFF.md দেখো)।
এখন ২৭তম গেম Cozy-Fit (Branch: origin/Cozy-Fit from https://github.com/souravshuvo/project-game.git) থেকে শুরু করে স্ট্রিক্টলি ১টি ১টি করে গেম প্রসেস করা শুরু করো:
১. গেমটির ব্রাঞ্চ চেকআউট করে প্যাকেজ আইডি, সোর্স কোড ও অরিজিনাল অডিও/গ্রাফিক ভেরিফাই করা।
২. ৫১২×৫১২ আইকন ও ১০২৪×৫০০ ব্যানার সংরক্ষণ।
৩. ৮টি আল্ট্রা ৩ডি পপ-আউট স্ক্রিনশট (১০৮০×১৯২০) তৈরি (টুইন-টাওয়ার স্ট্যান্ডার্ড)।
৪. ২টি ফুল HD ভিডিও ট্রেইলার (পোর্ট্রেট ৯:১৬ ও ল্যান্ডস্কেপ ১৬:৯) অরিজিনাল সাউন্ড ও গুগল প্লে এন্ডকার্ড সহ রেন্ডার।
৫. D:\souravshuvo.github.io\game_store_assets\<Game-Name>\ এ সংরক্ষণ এবং PORTFOLIO_ASSETS_MANIFEST.md আপডেট করা।
```
