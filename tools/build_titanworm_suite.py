# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FFMPEG = r"C:\Users\shuvo\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_DIR = os.path.join(WORKSPACE, "game_store_assets", "Titan-Worm-Arcade")

dir_icon = os.path.join(OUTPUT_DIR, "icon")
dir_feat = os.path.join(OUTPUT_DIR, "feature_graphic")
dir_ss = os.path.join(OUTPUT_DIR, "screenshots")
dir_raw = os.path.join(OUTPUT_DIR, "raw_captures")
dir_vid = os.path.join(OUTPUT_DIR, "videos")
tmp_frames = os.path.join(dir_vid, "tmp_frames")

for d in [dir_icon, dir_feat, dir_ss, dir_vid, tmp_frames]:
    os.makedirs(d, exist_ok=True)

# 1. ICON (512x512)
src_icon = os.path.join(REPO_DIR, "store-listing", "icon.png")
with Image.open(src_icon) as im:
    im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon, "icon_512.png"), "PNG", quality=98)
print("Saved 512x512 Icon")

# 2. FEATURE GRAPHIC (1024x500)
src_feat = os.path.join(REPO_DIR, "store-listing", "feature-graphic.png")
with Image.open(src_feat) as im:
    im.convert("RGB").resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat, "feature_graphic_1024x500.png"), "PNG", quality=98)
print("Saved 1024x500 Feature Graphic")

# 3. 8 HYPERCASUAL ASO SCREENSHOT CARDS (1080x1920)
badges = [
    ("COLOSSAL TITAN MONSTER!", "Awaken The Ancient Underground Sand Predator", (220, 50, 30)),
    ("BREACH THE DESERT SURFACE!", "Leap High Into The Air & Crush Enemy Convoys", (245, 130, 20)),
    ("SMASH ATTACK HELICOPTERS!", "Devour Gunships & Fighter Aircraft Mid-Air", (210, 30, 80)),
    ("UNLEASH FIERY RUSH POWER!", "Ignite Explosive Fireballs & Obliterate Armor", (255, 70, 0)),
    ("DEEP SUBTERRANEAN BURROW!", "Tunnel Deep Below Enemy Radar & Defenses", (40, 160, 220)),
    ("CRUSHING MISSION VICTORY!", "Level Base Bases, Earn Millions & Collect Stars", (255, 195, 30)),
    ("UPGRADE CARAPACE & FANGS!", "Boost Armor, Rush Speed, Fireballs & Spikes", (140, 40, 220)),
    ("100 CAMPAIGN WAR ZONES!", "Conquer Vast Desert Sectors, Military Outposts", (35, 180, 80))
]

raw_files = [
    "raw_01_home_monster.png",
    "raw_02_desert_breach.png",
    "raw_03_helicopter_strike.png",
    "raw_04_rush_fireball.png",
    "raw_05_underground_burrow.png",
    "raw_06_mission_victory.png",
    "raw_07_worm_upgrades.png",
    "raw_08_campaign_map.png"
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
        canvas = Image.new("RGBA", (target_w, target_h), (12, 10, 8, 255))
        bg = im.copy().resize((target_w, target_h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=30))
        dark = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 110))
        bg = Image.alpha_composite(bg, dark)
        canvas.paste(bg, (0, 0))
        
        # Center frame (16:9 scaled to fit width 1020)
        fw = 1020
        fh = int(fw * 1080 / 1920)
        im_frame = im.resize((fw, fh), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (fw, fh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw, fh], radius=24, fill=255)
        
        fx = (target_w - fw) // 2
        fy = (target_h - fh) // 2 + 30
        
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle([fx - 6, fy - 6, fx + fw + 6, fy + fh + 6], radius=28, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([fx - 4, fy - 4, fx + fw + 4, fy + fh + 4], radius=26, outline=(255, 140, 20, 220), width=4)
        draw.rounded_rectangle([fx - 1, fy - 1, fx + fw + 1, fy + fh + 1], radius=24, outline=(255, 255, 255, 200), width=2)
        
        canvas.paste(im_frame, (fx, fy), mask)
        
        # Top Badge Pill
        badge_w, badge_h = 840, 84
        bx = (target_w - badge_w) // 2
        by = 80
        draw.rounded_rectangle([bx + 4, by + 4, bx + badge_w + 4, by + badge_h + 4], radius=24, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=24, fill=(*b_col, 245), outline=(255, 255, 255, 230), width=3)
        draw.text((target_w // 2, by + badge_h // 2), b_title, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
        # Bottom Subtitle Ribbon
        sub_w, sub_h = 780, 60
        sx = (target_w - sub_w) // 2
        sy = fy + fh + 60
        draw.rounded_rectangle([sx + 3, sy + 3, sx + sub_w + 3, sy + sub_h + 3], radius=18, fill=(0, 0, 0, 140))
        draw.rounded_rectangle([sx, sy, sx + sub_w, sy + sub_h], radius=18, fill=(24, 18, 12, 230), outline=(255, 140, 20, 180), width=2)
        draw.text((target_w // 2, sy + sub_h // 2), b_sub, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
        
        out_ss = os.path.join(dir_ss, f"screenshot_{i+1:02d}.png")
        canvas.convert("RGB").save(out_ss, "PNG", quality=96)
        print(f"Generated Screenshot {i+1:02d}: {b_title}")

# 4. FULL HD VIDEO TRAILERS (Landscape & Portrait)
try:
    font_lg = ImageFont.truetype("arialbd.ttf", 64)
    font_cta = ImageFont.truetype("arialbd.ttf", 52)
    font_title = ImageFont.truetype("arialbd.ttf", 68)
    font_sub_v = ImageFont.truetype("arial.ttf", 36)
except Exception:
    font_lg = ImageFont.load_default()
    font_cta = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_sub_v = ImageFont.load_default()

trailer_slides = [
    ("raw_01_home_monster.png", "TITAN WORM: CARNAGE!", (220, 50, 30)),
    ("raw_02_desert_breach.png", "BREACH FROM THE DEPTHS!", (245, 130, 20)),
    ("raw_03_helicopter_strike.png", "SMASH AIR MILITARY GUNSHIPS!", (210, 30, 80)),
    ("raw_04_rush_fireball.png", "SUPER RUSH & FIREBALL CANNON!", (255, 70, 0)),
    ("raw_05_underground_burrow.png", "BURROW UNDERGROUND SECRETS!", (40, 160, 220)),
    ("raw_07_worm_upgrades.png", "EVOLVE YOUR ANCIENT BEAST!", (140, 40, 220)),
    ("raw_06_mission_victory.png", "MASSIVE CARNAGE VICTORY!", (255, 195, 30))
]

# Build Landscape Slides (1920x1080)
slide_files_land = []
for idx, (rf, text, col) in enumerate(trailer_slides):
    im_path = os.path.join(dir_raw, rf)
    with Image.open(im_path) as raw:
        im = raw.convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        
        bw, bh = 1140, 110
        bx = (1920 - bw) // 2
        by = 60
        draw.rounded_rectangle([bx + 6, by + 6, bx + bw + 6, by + bh + 6], radius=28, fill=(0, 0, 0, 170))
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28, fill=(*col, 245), outline=(255, 255, 255, 240), width=4)
        draw.text((1920 // 2, by + bh // 2), text, font=font_lg, fill=(255, 255, 255, 255), anchor="mm")
        
        out_f = os.path.join(tmp_frames, f"slide_l_{idx}.png")
        im.convert("RGB").save(out_f, "PNG")
        slide_files_land.append(out_f)

# Landscape Endcard
end_l = Image.new("RGBA", (1920, 1080), (14, 12, 10, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((360, 360), Image.Resampling.LANCZOS)
    mask = Image.new("L", (360, 360), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 360], radius=72, fill=255)
    end_l.paste(ic_res, (220, 360), mask)

draw_el = ImageDraw.Draw(end_l)
draw_el.rounded_rectangle([216, 356, 584, 724], radius=74, outline=(255, 140, 20, 240), width=4)
draw_el.text((640, 420), "TITAN WORM ARCADE", font=font_title, fill=(255, 255, 255, 255))
draw_el.text((640, 500), "Hunt, Breach & Annihilate Enemy Fortresses!", font=font_sub_v, fill=(255, 180, 50, 255))

draw_el.rounded_rectangle([640, 580, 1140, 680], radius=24, fill=(255, 120, 0, 255), outline=(255, 255, 255, 220), width=3)
draw_el.text((890, 630), "INSTALL NOW FREE", font=font_cta, fill=(255, 255, 255, 255), anchor="mm")

end_l_file = os.path.join(tmp_frames, "slide_l_end.png")
end_l.convert("RGB").save(end_l_file, "PNG")
slide_files_land.append(end_l_file)

# Build Portrait Slides (1080x1920)
slide_files_port = []
for idx in range(len(trailer_slides)):
    ss_path = os.path.join(dir_ss, f"screenshot_{idx+1:02d}.png")
    out_f = os.path.join(tmp_frames, f"slide_p_{idx}.png")
    with Image.open(ss_path) as im:
        im.resize((1080, 1920), Image.Resampling.LANCZOS).save(out_f, "PNG")
        slide_files_port.append(out_f)

# Portrait Endcard
end_p = Image.new("RGBA", (1080, 1920), (14, 12, 10, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((420, 420), Image.Resampling.LANCZOS)
    mask = Image.new("L", (420, 420), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 420, 420], radius=84, fill=255)
    end_p.paste(ic_res, (330, 480), mask)

draw_ep = ImageDraw.Draw(end_p)
draw_ep.rounded_rectangle([324, 474, 756, 906], radius=86, outline=(255, 140, 20, 240), width=4)
draw_ep.text((540, 1000), "TITAN WORM ARCADE", font=font_title, fill=(255, 255, 255, 255), anchor="mm")
draw_ep.text((540, 1080), "Unleash The Ancient Sand Beast", font=font_sub_v, fill=(255, 180, 50, 255), anchor="mm")

draw_ep.rounded_rectangle([240, 1200, 840, 1320], radius=28, fill=(255, 120, 0, 255), outline=(255, 255, 255, 220), width=3)
draw_ep.text((540, 1260), "INSTALL NOW FREE", font=font_cta, fill=(255, 255, 255, 255), anchor="mm")

draw_ep.text((540, 1390), "Google Play Store  *  Free Download", font=font_sub_v, fill=(180, 180, 180, 255), anchor="mm")

end_p_file = os.path.join(tmp_frames, "slide_p_end.png")
end_p.convert("RGB").save(end_p_file, "PNG")
slide_files_port.append(end_p_file)

# Write concat files
concat_l = os.path.join(tmp_frames, "concat_l.txt")
with open(concat_l, "w") as f:
    for s in slide_files_land[:-1]:
        f.write(f"file '{s.replace(chr(92), '/')}'\n")
        f.write("duration 2.2\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")
    f.write("duration 3.5\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")

concat_p = os.path.join(tmp_frames, "concat_p.txt")
with open(concat_p, "w") as f:
    for s in slide_files_port[:-1]:
        f.write(f"file '{s.replace(chr(92), '/')}'\n")
        f.write("duration 2.2\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")
    f.write("duration 3.5\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")

audio_file = os.path.join(REPO_DIR, "assets", "audio", "bgm", "bgm_loop.wav")
out_mp4_land = os.path.join(dir_vid, "titanworm_trailer_landscape_16x9.mp4")
out_mp4_port = os.path.join(dir_vid, "titanworm_trailer_portrait_9x16.mp4")

total_dur = 2.2 * 7 + 3.5

# Render Landscape Trailer
cmd_l = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_l,
    "-stream_loop", "-1", "-i", audio_file,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-t", str(total_dur),
    out_mp4_land
]
subprocess.run(cmd_l, check=True)
print("Saved Landscape Trailer:", out_mp4_land)

# Render Portrait Trailer
cmd_p = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_p,
    "-stream_loop", "-1", "-i", audio_file,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-t", str(total_dur),
    out_mp4_port
]
subprocess.run(cmd_p, check=True)
print("Saved Portrait Trailer:", out_mp4_port)
print("ALL TITAN WORM ASSETS SUCCESSFULLY COMPLETED!")
