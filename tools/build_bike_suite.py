# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FFMPEG = r"C:\Users\shuvo\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_DIR = os.path.join(WORKSPACE, "game_store_assets", "Bike-Traffic-Racer")

dir_icon = os.path.join(OUTPUT_DIR, "icon")
dir_feat = os.path.join(OUTPUT_DIR, "feature_graphic")
dir_ss = os.path.join(OUTPUT_DIR, "screenshots")
dir_raw = os.path.join(OUTPUT_DIR, "raw_captures")
dir_vid = os.path.join(OUTPUT_DIR, "videos")

for d in [dir_icon, dir_feat, dir_ss, dir_vid]:
    os.makedirs(d, exist_ok=True)

# 1. ICON
src_icon = os.path.join(REPO_DIR, "play-store", "app-icon.png")
with Image.open(src_icon) as im:
    im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon, "icon_512.png"), "PNG", quality=98)
print("✓ Saved 512x512 Icon")

# 2. FEATURE GRAPHIC
src_feat = os.path.join(REPO_DIR, "play-store", "feature-graphic.jpg")
with Image.open(src_feat) as im:
    im.convert("RGB").resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat, "feature_graphic_1024x500.png"), "PNG", quality=98)
print("✓ Saved 1024x500 Feature Graphic")

# 3. 8 HYPERCASUAL SCREENSHOT CARDS (1080x1920)
badges = [
    ("🏍️ FIRST-PERSON 3D COCKPIT! 🏍️", "Feel The Real Speed In Cockpit View", (255, 60, 40)),
    ("⚡ HIGHWAY TRAFFIC WEAVE! ⚡", "Close Passes & Near-Miss Combos", (0, 210, 255)),
    ("🌅 COASTAL SUNSET OVERTAKE! 🌅", "Two-Way Oncoming Traffic Challenge", (255, 170, 0)),
    ("🏜️ CANYON TRUCK CHASE! 🏜️", "Thread The Gaps Between Heavy Trucks", (240, 80, 20)),
    ("🌃 NEON MIDNIGHT SPRINT! 🌃", "Night Racing With Glowing Headlights", (180, 50, 255)),
    ("🔧 SUPERBIKE GARAGE TUNING! 🔧", "Upgrade Power, Handling & Braking", (0, 230, 120)),
    ("🗺️ 5 CAMPAIGN ENVIRONMENTS! 🗺️", "City, Coast, Desert & Highway Maps", (0, 180, 255)),
    ("🏆 MISSION COMPLETED 3-STARS! 🏆", "Earn Cash, Gold & Unlock Superbikes", (255, 215, 0))
]

raw_files = [
    "raw_01_city_highway.png",
    "raw_02_traffic_weave.png",
    "raw_03_coastal_sunset.png",
    "raw_04_desert_canyon.png",
    "raw_05_neon_midnight.png",
    "raw_06_garage_tuning.png",
    "raw_07_mission_map.png",
    "raw_08_victory.png"
]

target_w, target_h = 1080, 1920

try:
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_sub = ImageFont.truetype("arialbd.ttf", 26)
except Exception:
    font_badge = ImageFont.load_default()
    font_sub = ImageFont.load_default()

for i, (rf, (b_title, b_sub, b_col)) in enumerate(zip(raw_files, badges)):
    p_raw = os.path.join(dir_raw, rf)
    with Image.open(p_raw) as raw_im:
        im = raw_im.convert("RGBA")
        
        # Color boost
        im = ImageEnhance.Color(im).enhance(1.22)
        im = ImageEnhance.Contrast(im).enhance(1.10)
        
        # Background
        canvas = Image.new("RGBA", (target_w, target_h), (10, 14, 22, 255))
        bg = im.copy().resize((target_w, target_h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=30))
        # Dark vignette overlay
        dark = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 100))
        bg = Image.alpha_composite(bg, dark)
        canvas.paste(bg, (0, 0))
        
        # Center frame (16:9 scaled to fit width 1020)
        fw = 1020
        fh = int(fw * 1080 / 1920)
        im_frame = im.resize((fw, fh), Image.Resampling.LANCZOS)
        
        # Rounded frame mask
        mask = Image.new("L", (fw, fh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw, fh], radius=24, fill=255)
        
        fx = (target_w - fw) // 2
        fy = (target_h - fh) // 2 + 30
        
        # Outer glow / shadow
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle([fx - 6, fy - 6, fx + fw + 6, fy + fh + 6], radius=28, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([fx - 4, fy - 4, fx + fw + 4, fy + fh + 4], radius=26, outline=(0, 229, 255, 220), width=4)
        draw.rounded_rectangle([fx - 1, fy - 1, fx + fw + 1, fy + fh + 1], radius=24, outline=(255, 255, 255, 200), width=2)
        
        canvas.paste(im_frame, (fx, fy), mask)
        
        # Top Badge Pill
        badge_w, badge_h = 820, 84
        bx = (target_w - badge_w) // 2
        by = 80
        draw.rounded_rectangle([bx + 4, by + 4, bx + badge_w + 4, by + badge_h + 4], radius=24, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=24, fill=(*b_col, 240), outline=(255, 255, 255, 230), width=3)
        draw.text((target_w // 2, by + badge_h // 2), b_title, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
        # Bottom Subtitle Ribbon
        sub_w, sub_h = 760, 60
        sx = (target_w - sub_w) // 2
        sy = fy + fh + 60
        draw.rounded_rectangle([sx + 3, sy + 3, sx + sub_w + 3, sy + sub_h + 3], radius=18, fill=(0, 0, 0, 140))
        draw.rounded_rectangle([sx, sy, sx + sub_w, sy + sub_h], radius=18, fill=(16, 24, 38, 220), outline=(0, 229, 255, 180), width=2)
        draw.text((target_w // 2, sy + sub_h // 2), b_sub, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
        
        out_ss = os.path.join(dir_ss, f"screenshot_{i+1:02d}.png")
        canvas.convert("RGB").save(out_ss, "PNG", quality=96)
        print(f"✓ Generated Screenshot {i+1:02d}: {b_title}")

print("\nAll 8 Screenshots successfully created!")