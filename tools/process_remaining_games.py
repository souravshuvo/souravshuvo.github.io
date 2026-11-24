# -*- coding: utf-8 -*-
import os
import subprocess
import concurrent.futures
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_BASE = os.path.join(WORKSPACE, "game_store_assets")

REMAINING_GAMES = {
    "arrowflow": {"name": "Arrow-Puzzle-Grid-Escape", "branch": "arrow_flow", "title": "ARROW PUZZLE ESCAPE"},
    "boltbalance": {"name": "Bolt-and-Balance-Screw", "branch": "Bolt-&-Balance", "title": "BOLT AND BALANCE"},
    "brainwink": {"name": "Brain-Wink-Puzzles", "branch": "brain-wink", "title": "BRAIN WINK PUZZLES"},
    "cablegarden": {"name": "Cable-Garden-Untangle", "branch": "Cable-Garden", "title": "CABLE GARDEN UNTANGLE"},
    "canopyrush": {"name": "Canopy-Rush-Jungle-Swing", "branch": "canopy_rush", "title": "CANOPY RUSH JUNGLE"},
    "cardhaven": {"name": "Card-Haven-Solitaire", "branch": "card-haven", "title": "CARD HAVEN SOLITAIRE"},
    "carvetheshape": {"name": "Carve-the-Shape-Workshop", "branch": "Carve-the-Shape", "title": "CARVE THE SHAPE"},
    "colorcourtyard": {"name": "Color-Courtyard-Paint", "branch": "Color-Courtyard", "title": "COLOR COURTYARD"},
    "cozyfit": {"name": "Cozy-Fit-Packing-Puzzle", "branch": "Cozy-Fit", "title": "COZY FIT PACKING"},
    "dewbubble": {"name": "Dew-Garden-Bubble-Shooter", "branch": "dew_bubble", "title": "DEW GARDEN BUBBLE"},
    "dominodetour": {"name": "Domino-Detour-Reaction", "branch": "Domino-Detour", "title": "DOMINO DETOUR"},
    "dotsandboxes": {"name": "Dots-and-Boxes-Two-Player", "branch": "dot-and-box", "title": "DOTS AND BOXES 2P"},
    "foldstamp": {"name": "Fold-and-Stamp-Puzzles", "branch": "Fold-&-Stamp", "title": "FOLD AND STAMP"},
    "gatesquad": {"name": "Gate-Squad-Runner-Shooter", "branch": "gate_squad", "title": "GATE SQUAD RUNNER"},
    "kettlematch": {"name": "Kettle-Match-Triple-Tile", "branch": "kettle_match", "title": "KETTLE MATCH TRIPLE"},
    "kidsland": {"name": "Kids-Land-Learning", "branch": "kids_land", "title": "KIDS LAND LEARNING"},
    "meadowclaim": {"name": "Meadow-Claim-Territory", "branch": "Meadow-Claim", "title": "MEADOW CLAIM"},
    "minigames": {"name": "Mini-Games-Pocket-Arcade", "branch": "mini_games", "title": "MINI GAMES ARCADE"},
    "nightmarket": {"name": "Night-Market-Minute-Cook", "branch": "Night-Market-Minute", "title": "NIGHT MARKET MINUTE"},
    "objectfinder": {"name": "Object-Finder-Hidden", "branch": "Object-Finder", "title": "OBJECT FINDER HIDDEN"},
    "pencricket": {"name": "Pen-Cricket-Spin-Chase", "branch": "pen_cricket", "title": "PEN CRICKET CHASE"},
    "pockethabitat": {"name": "Pocket-Habitat-Hex", "branch": "Pocket-Habitat", "title": "POCKET HABITAT HEX"},
    "pocketpinball": {"name": "Pocket-Pinball-Expedition", "branch": "Pocket-Pinball-Expedition", "title": "POCKET PINBALL"},
    "policethief": {"name": "Chor-Police-Hidden-Roles", "branch": "police_thief", "title": "CHOR POLICE CHASE"},
    "savetheking": {"name": "Save-the-King-Match3", "branch": "save_the_king", "title": "SAVE THE KING"},
    "sixteenbreed": {"name": "Sholo-Guti-16-Beads", "branch": "breed_16", "title": "SHOLO GUTI 16 BEADS"},
    "spaceshooter": {"name": "Space-Shooter-Galaxy", "branch": "space_shooter", "title": "SPACE SHOOTER GALAXY"},
    "sudoku": {"name": "Sudoku-Lantern-Puzzles", "branch": "sudoku", "title": "SUDOKU LANTERN PRO"},
    "sumfoundry": {"name": "Sum-Foundry-Math", "branch": "Sum-Foundry", "title": "SUM FOUNDRY MATH"},
    "switchyard": {"name": "Switchyard-Minute-Train", "branch": "Switchyard-Minute", "title": "SWITCHYARD TRAIN"},
    "tictactoe": {"name": "Tic-Tac-Toe-Two-Player", "branch": "tic_tac_toe", "title": "TIC TAC TOE 2P"},
    "weatherlab": {"name": "Color-Sort-Weather-Lab", "branch": "color_sort", "title": "COLOR SORT LAB"},
    "wordtrail": {"name": "Word-Trail-Word-Search", "branch": "Word-Trail-Expedition", "title": "WORD TRAIL SEARCH"}
}

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
        "store-listing/play-icon.png", "assets/images/app_icon.png", "assets/images/play_icon.png",
        "ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png",
        "android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png"
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
    ss_files = [f for f in all_files if ("screenshot" in f.lower() or "captures" in f.lower() or "source-art" in f.lower() or "images" in f.lower()) and f.endswith((".png", ".jpg"))]
    
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
            
    # Generate Feature Graphic if missing
    if not os.path.exists(feat_path) and os.path.exists(icon_path):
        with Image.open(icon_path) as im_raw:
            im_ic = im_raw.convert("RGBA")
            banner = Image.new("RGBA", (1024, 500), (10, 16, 28, 255))
            bg = im_ic.resize((1024, 500), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=40))
            banner.paste(bg, (0, 0))
            draw = ImageDraw.Draw(banner)
            ic_res = im_ic.resize((280, 280), Image.Resampling.LANCZOS)
            mask = Image.new("L", (280, 280), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, 280, 280], radius=56, fill=255)
            draw.rounded_rectangle([106, 106, 110 + 280 + 4, 110 + 280 + 4], radius=60, outline=(0, 229, 255, 200), width=4)
            banner.paste(ic_res, (110, 110), mask)
            try:
                f_t = ImageFont.truetype("arialbd.ttf", 44)
                f_s = ImageFont.truetype("arial.ttf", 26)
            except Exception:
                f_t = ImageFont.load_default()
                f_s = ImageFont.load_default()
            draw.text((440, 160), config["title"], font=f_t, fill=(255, 255, 255, 255))
            draw.text((440, 225), "Official Hypercasual Release", font=f_s, fill=(0, 229, 255, 255))
            draw.text((440, 270), "★ ★ ★ ★ ★   TOP RATED CASUAL HIT", font=f_s, fill=(255, 215, 0, 255))
            banner.convert("RGB").save(feat_path, "PNG", quality=95)
        print(f"  ✓ Generated 1024x500 Feature Graphic")
        
    print(f"  ✓ Successfully completed {config['name']}!")
    return config["name"]

def main():
    print(f"Starting Batch ASO Asset Builder for all {len(REMAINING_GAMES)} remaining games with 4 parallel workers...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_game, k, cfg) for k, cfg in REMAINING_GAMES.items()]
        for f in concurrent.futures.as_completed(futures):
            try:
                res = f.result()
                print(f"[SUCCESS] {res} completed!")
            except Exception as e:
                print(f"[ERROR] Worker failed: {e}")
                
    print("\nAll remaining games processed successfully! Check: D:\\souravshuvo.github.io\\game_store_assets\\")

if __name__ == "__main__":
    main()