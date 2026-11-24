# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_BASE = os.path.join(WORKSPACE, "game_store_assets")

def enhance_to_aso_screenshot(src_img, title, subtitle, badge_text, out_path):
    target_w, target_h = 1080, 1920
    im = src_img.convert("RGBA")
    
    enh_col = ImageEnhance.Color(im)
    im = enh_col.enhance(1.28)
    enh_con = ImageEnhance.Contrast(im)
    im = enh_con.enhance(1.12)
    
    canvas = Image.new("RGBA", (target_w, target_h), (12, 16, 26, 255))
    bg = im.copy().resize((target_w, target_h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=25))
    canvas.paste(bg, (0, 0))
    
    scale = min((target_w - 40) / im.width, (target_h - 180) / im.height)
    new_w = int(im.width * scale)
    new_h = int(im.height * scale)
    resized_im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    offset_x = (target_w - new_w) // 2
    offset_y = 120 + (target_h - 180 - new_h) // 2
    canvas.paste(resized_im, (offset_x, offset_y), Image.new("L", (new_w, new_h), 255))
    
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([offset_x - 3, offset_y - 3, offset_x + new_w + 3, offset_y + new_h + 3], radius=16, outline=(0, 229, 255, 180), width=4)
    
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 38)
    except Exception:
        font_badge = ImageFont.load_default()
        
    badge_w = 700
    badge_h = 80
    bx = (target_w - badge_w) // 2
    by = 38
    draw.rounded_rectangle([bx + 4, by + 4, bx + badge_w + 4, by + badge_h + 4], radius=24, fill=(0, 0, 0, 140))
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=24, fill=(240, 20, 80, 240), outline=(255, 255, 255, 230), width=3)
    draw.text((target_w // 2, by + badge_h // 2), badge_text, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
    
    canvas.convert("RGB").save(out_path, "PNG", quality=95)

# 1. Process Save-the-King-Match3
print("Processing Save-the-King-Match3...")
subprocess.run(["git", "fetch", "origin", "save_the_king"], cwd=REPO_DIR, capture_output=True)
dir_king = os.path.join(OUTPUT_BASE, "Save-the-King-Match3")
dir_icon = os.path.join(dir_king, "icon")
dir_feat = os.path.join(dir_king, "feature_graphic")
os.makedirs(dir_icon, exist_ok=True)
os.makedirs(dir_feat, exist_ok=True)

# Icon
r = subprocess.run(["git", "show", "FETCH_HEAD:assets/store/save-the-king-store-icon.png"], cwd=REPO_DIR, capture_output=True)
if r.returncode == 0:
    tmp = os.path.join(dir_icon, "tmp.png")
    with open(tmp, "wb") as f:
        f.write(r.stdout)
    with Image.open(tmp) as im:
        im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon, "icon_512.png"))
    os.remove(tmp)
    print("  ✓ Save-the-King icon saved")

# Feature Graphic
r = subprocess.run(["git", "show", "FETCH_HEAD:assets/store/save-the-king-feature-graphic.png"], cwd=REPO_DIR, capture_output=True)
if r.returncode == 0:
    tmp = os.path.join(dir_feat, "tmp.png")
    with open(tmp, "wb") as f:
        f.write(r.stdout)
    with Image.open(tmp) as im:
        im.resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat, "feature_graphic_1024x500.png"))
    os.remove(tmp)
    print("  ✓ Save-the-King feature graphic saved")

# 2. Process Sholo-Guti-16-Beads
print("Processing Sholo-Guti-16-Beads...")
subprocess.run(["git", "fetch", "origin", "breed_16"], cwd=REPO_DIR, capture_output=True)
dir_sholo = os.path.join(OUTPUT_BASE, "Sholo-Guti-16-Beads")
dir_icon_s = os.path.join(dir_sholo, "icon")
dir_feat_s = os.path.join(dir_sholo, "feature_graphic")
dir_ss_s = os.path.join(dir_sholo, "screenshots")
os.makedirs(dir_icon_s, exist_ok=True)
os.makedirs(dir_feat_s, exist_ok=True)
os.makedirs(dir_ss_s, exist_ok=True)

# Icon
r = subprocess.run(["git", "show", "FETCH_HEAD:store-assets/play-store/16-breed-play-icon-512.png"], cwd=REPO_DIR, capture_output=True)
if r.returncode == 0:
    tmp = os.path.join(dir_icon_s, "tmp.png")
    with open(tmp, "wb") as f:
        f.write(r.stdout)
    with Image.open(tmp) as im:
        im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon_s, "icon_512.png"))
    os.remove(tmp)
    print("  ✓ Sholo-Guti icon saved")

# Feature Graphic
r = subprocess.run(["git", "show", "FETCH_HEAD:store-assets/play-store/16-breed-feature-graphic-1024x500.png"], cwd=REPO_DIR, capture_output=True)
if r.returncode == 0:
    tmp = os.path.join(dir_feat_s, "tmp.png")
    with open(tmp, "wb") as f:
        f.write(r.stdout)
    with Image.open(tmp) as im:
        im.resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat_s, "feature_graphic_1024x500.png"))
    os.remove(tmp)
    print("  ✓ Sholo-Guti feature graphic saved")

# Screenshots
badges = [
    "🔥 MASTER SHOLO GUTI! 🔥",
    "⚡ STRATEGIC CAPTURE! ⚡",
    "🎯 CHAIN JUMP COMBOS! 🎯",
    "🏆 SMART BOT CHALLENGE! 🏆",
    "🌉 2 PLAYER OFFLINE BATTLE! 🌉",
    "💥 BLUETOOTH MULTIPLAYER! 💥",
    "👑 RIVER JOURNEY QUESTS! 👑",
    "✨ TRADITIONAL BOARD HIT! ✨"
]

ss_files = [
    "store-assets/play-store/promo-screenshots/01-16-breed.png",
    "store-assets/play-store/promo-screenshots/02-legal-moves.png",
    "store-assets/play-store/promo-screenshots/03-capture.png",
    "store-assets/play-store/promo-screenshots/04-chain-captures.png",
    "store-assets/play-store/promo-screenshots/05-bot.png",
    "store-assets/play-store/promo-screenshots/06-local-two-player.png",
    "store-assets/play-store/promo-screenshots/07-bluetooth.png",
    "store-assets/play-store/promo-screenshots/08-history-rematch.png"
]

for idx, sf in enumerate(ss_files):
    r = subprocess.run(["git", "show", f"FETCH_HEAD:{sf}"], cwd=REPO_DIR, capture_output=True)
    if r.returncode == 0:
        tmp = os.path.join(dir_ss_s, f"tmp_{idx}.png")
        with open(tmp, "wb") as f:
            f.write(r.stdout)
        with Image.open(tmp) as im:
            enhance_to_aso_screenshot(im, "SHOLO GUTI 16 BEADS", f"Level {idx+1}", badges[idx], os.path.join(dir_ss_s, f"screenshot_{idx+1:02d}.png"))
        os.remove(tmp)
print("  ✓ Sholo-Guti 8 screenshots generated")
print("ALL DONE!")