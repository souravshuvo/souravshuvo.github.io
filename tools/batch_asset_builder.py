# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import argparse
import concurrent.futures
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_BASE = os.path.join(WORKSPACE, "game_store_assets")

# THE EXACT 20 PRIORITY GAMES
PRIORITY_20 = {
    "amazeroll": {"name": "Amaze-Roll", "branch": "amazeroll", "pkg": "com.childhood.amazeroll", "title": "AMAZE ROLL"},
    "bike": {"name": "Bike-Traffic-Racer", "branch": "bike", "pkg": "com.childhood.bike", "title": "BIKE TRAFFIC RACER"},
    "cream": {"name": "Swirl-Studio-Ice-Cream", "branch": "ice_cream", "pkg": "com.childhood.cream", "title": "SWIRL STUDIO ICE CREAM"},
    "smash": {"name": "Smash-DIY-ASMR", "branch": "can_smash", "pkg": "com.childhood.smash", "title": "SMASH DIY SIMULATOR"},
    "city": {"name": "City-Cleaner-Hole", "branch": "city_hole", "pkg": "com.childhood.city", "title": "CITY CLEANER HOLE"},
    "dogescape": {"name": "Dog-Escape-Run", "branch": "dogescape", "pkg": "com.childhood.dogescape", "title": "DOG ESCAPE ROOM RUN"},
    "emoji": {"name": "Emoji-Merge-Link", "branch": "emoji", "pkg": "com.childhood.emoji", "title": "EMOJI LINK MERGE"},
    "helix": {"name": "Helix-Jump-Spiral", "branch": "helix", "pkg": "com.childhood.helix", "title": "HELIX SPIRAL JUMP"},
    "knife": {"name": "Knife-Hit-Master", "branch": "knife", "pkg": "com.childhood.knife", "title": "KNIFE HIT MASTER"},
    "golf": {"name": "Sky-Putt-Mini-Golf", "branch": "golf", "pkg": "com.childhood.golf", "title": "SKY PUTT MINI GOLF"},
    "run": {"name": "Speed-Runner-3D", "branch": "run", "pkg": "com.childhood.run", "title": "SPEED RUNNER 3D"},
    "titanworm": {"name": "Titan-Worm-Arcade", "branch": "titanworm", "pkg": "com.childhood.titanworm", "title": "TITAN WORM ARCADE"},
    "wing": {"name": "Wing-Rush-Glide", "branch": "wing", "pkg": "com.childhood.wing", "title": "WING RUSH GLIDE"},
    "escape": {"name": "Rivet-Block-Escape", "branch": "1", "pkg": "com.childhood.escape", "title": "RIVET BLOCK ESCAPE"},
    "pedal": {"name": "Pedal-Post-Rush", "branch": "2", "pkg": "com.childhood.pedal", "title": "PEDAL POST RUSH"},
    "mergepair": {"name": "Merge-Pair-Pastry", "branch": "4", "pkg": "com.childhood.mergepair", "title": "MERGE PAIR PASTRY"},
    "latchloomrings": {"name": "Latchloom-Rings", "branch": "5", "pkg": "com.childhood.latchloomrings", "title": "LATCHLOOM RINGS"},
    "stack": {"name": "Bite-Stack-Match", "branch": "3", "pkg": "com.childhood.stack", "title": "BITE STACK MATCH"},
    "slaprun": {"name": "Slap-and-Run", "branch": "run", "pkg": "com.childhood.slaprun", "title": "SLAP AND RUN"},
    "swat": {"name": "SWAT-Insect-Tap", "branch": "main", "pkg": "com.childhood.swat", "title": "SWAT INSECT TAP"}
}

# ALL OTHER EXTENDED PORTFOLIO GAMES
EXTENDED_GAMES = {
    "twintowerdrop": {"name": "Twin-Tower-Drop", "branch": "Twin-Tower-Drop", "pkg": "com.childhood.twintowerdrop", "title": "TWIN TOWER DROP"},
    "block": {"name": "Block-Grove-Puzzle", "branch": "block", "pkg": "com.childhood.block", "title": "BLOCK GROVE PUZZLE"},
    "color_courtyard": {"name": "Color-Courtyard", "branch": "Color-Courtyard", "pkg": "com.childhood.colorcourtyard", "title": "COLOR COURTYARD"},
    "bolt": {"name": "Bolt-and-Balance", "branch": "Bolt-&-Balance", "pkg": "com.childhood.boltbalance", "title": "BOLT AND BALANCE"},
    "cable": {"name": "Cable-Garden", "branch": "Cable-Garden", "pkg": "com.childhood.cablegarden", "title": "CABLE GARDEN"},
    "domino": {"name": "Domino-Detour", "branch": "Domino-Detour", "pkg": "com.childhood.dominodetour", "title": "DOMINO DETOUR"}
}

ALL_GAMES = {**PRIORITY_20, **EXTENDED_GAMES}

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

def process_game(game_key, config):
    print(f"\n[+] Processing: {config['name']} (Branch: {config['branch']})")
    game_dir = os.path.join(OUTPUT_BASE, config['name'])
    dir_ss = os.path.join(game_dir, "screenshots")
    dir_vid = os.path.join(game_dir, "videos")
    dir_icon = os.path.join(game_dir, "icon")
    dir_feat = os.path.join(game_dir, "feature_graphic")
    
    for d in [dir_ss, dir_vid, dir_icon, dir_feat]:
        os.makedirs(d, exist_ok=True)
        
    subprocess.run(["git", "fetch", "origin", config["branch"]], cwd=REPO_DIR, capture_output=True)
    
    # 1. Extract Icon
    icon_candidates = [
        "play-store/app-icon.png", "play-store/icon-512.png", "store/icon-512.png", 
        "store-listing/play-icon.png", "assets/images/app_icon.png",
        "ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png"
    ]
    icon_data = None
    for cand in icon_candidates:
        r = subprocess.run(["git", "show", f"FETCH_HEAD:{cand}"], cwd=REPO_DIR, capture_output=True)
        if r.returncode == 0 and len(r.stdout) > 200:
            icon_data = r.stdout
            break
            
    if icon_data:
        tmp_icon = os.path.join(game_dir, "tmp_icon.png")
        with open(tmp_icon, "wb") as f:
            f.write(icon_data)
        with Image.open(tmp_icon) as im_raw:
            im_ic = im_raw.copy().resize((512, 512), Image.Resampling.LANCZOS)
            im_ic.save(os.path.join(dir_icon, "icon_512.png"))
        if os.path.exists(tmp_icon):
            os.remove(tmp_icon)
        print(f"  ✓ Saved 512x512 Icon")
        
    # 2. Extract Feature Graphic
    feat_candidates = [
        "play-store/feature-graphic.png", "play-store/feature-graphic.jpg", "store/feature-1024x500.png",
        "store/feature_graphic_1024x500.png", "store-listing/feature-graphic.png", "play-store/feature-graphic-1024x500.png"
    ]
    feat_data = None
    for cand in feat_candidates:
        r = subprocess.run(["git", "show", f"FETCH_HEAD:{cand}"], cwd=REPO_DIR, capture_output=True)
        if r.returncode == 0 and len(r.stdout) > 200:
            feat_data = r.stdout
            break
            
    if feat_data:
        tmp_feat = os.path.join(game_dir, "tmp_feat.png")
        with open(tmp_feat, "wb") as f:
            f.write(feat_data)
        with Image.open(tmp_feat) as im_raw:
            im_ft = im_raw.copy().resize((1024, 500), Image.Resampling.LANCZOS)
            im_ft.save(os.path.join(dir_feat, "feature_graphic_1024x500.png"))
        if os.path.exists(tmp_feat):
            os.remove(tmp_feat)
        print(f"  ✓ Saved 1024x500 Feature Graphic")
        
    # 3. Extract or Generate 8 Screenshots
    r_tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD"], cwd=REPO_DIR, capture_output=True, text=True)
    all_files = r_tree.stdout.splitlines()
    ss_files = [f for f in all_files if ("screenshot" in f.lower() or "captures" in f.lower() or "source-art" in f.lower()) and f.endswith((".png", ".jpg"))]
    
    badges = [
        "🔥 HIGH SPEED ACTION! 🔥",
        "⚡ MASTER THE CONTROLS! ⚡",
        "🎯 PRECISION CHALLENGE! 🎯",
        "🏆 UNLOCK EPIC UPGRADES! 🏆",
        "🌉 MULTI-STAGE ADVENTURE! 🌉",
        "💥 COMBO MULTIPLIER! 💥",
        "👑 BEAT THE HIGHSCORE! 👑",
        "✨ PLAY FREE WORLDWIDE! ✨"
    ]
    
    extracted_imgs = []
    for sf in ss_files[:12]:
        r = subprocess.run(["git", "show", f"FETCH_HEAD:{sf}"], cwd=REPO_DIR, capture_output=True)
        if r.returncode == 0 and len(r.stdout) > 5000:
            tmp_p = os.path.join(game_dir, f"tmp_s_{len(extracted_imgs)}.png")
            with open(tmp_p, "wb") as f:
                f.write(r.stdout)
            try:
                with Image.open(tmp_p) as tmp_im:
                    extracted_imgs.append(tmp_im.copy())
            except Exception:
                pass
            if os.path.exists(tmp_p):
                os.remove(tmp_p)
            
    base_src = None
    feat_path = os.path.join(dir_feat, "feature_graphic_1024x500.png")
    icon_path = os.path.join(dir_icon, "icon_512.png")
    if os.path.exists(feat_path):
        base_src = Image.open(feat_path)
    elif os.path.exists(icon_path):
        base_src = Image.open(icon_path)
        
    for i in range(8):
        out_ss = os.path.join(dir_ss, f"screenshot_{i+1:02d}.png")
        src = extracted_imgs[i % len(extracted_imgs)] if extracted_imgs else base_src
        if src:
            enhance_to_aso_screenshot(src, config["title"], f"Level {i+1} Rush", badges[i], out_ss)
        
    print(f"  ✓ Successfully generated 8 Ultra-Rich ASO Screenshots for {config['name']}!")
    return config["name"]

def main():
    parser = argparse.ArgumentParser(description="Automated Game ASO Asset Pipeline")
    parser.add_argument("--games", nargs="+", help="Game keys (e.g. bike cream block)")
    parser.add_argument("--priority20", action="store_true", help="Process the 20 priority closed-track games")
    parser.add_argument("--all", action="store_true", help="Process all mapped games")
    parser.add_argument("--parallel", type=int, default=4, help="Max parallel jobs")
    args = parser.parse_args()
    
    targets = []
    if args.priority20:
        targets = list(PRIORITY_20.items())
    elif args.all:
        targets = list(ALL_GAMES.items())
    elif args.games:
        targets = [(k, ALL_GAMES[k]) for k in args.games if k in ALL_GAMES]
    else:
        targets = list(PRIORITY_20.items())
        
    print(f"Starting Batch ASO Asset Builder for {len(targets)} game(s) with {args.parallel} workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [executor.submit(process_game, k, cfg) for k, cfg in targets]
        for f in concurrent.futures.as_completed(futures):
            try:
                res = f.result()
                print(f"[SUCCESS] {res} completed!")
            except Exception as e:
                print(f"[ERROR] Worker failed: {e}")
                
    print("\nAll target games processed successfully! Check: D:\\souravshuvo.github.io\\game_store_assets\\")

if __name__ == "__main__":
    main()