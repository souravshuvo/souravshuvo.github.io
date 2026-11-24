# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FFMPEG = r"C:\Users\shuvo\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_DIR = os.path.join(WORKSPACE, "game_store_assets", "Helix-Jump-Spiral")

dir_icon = os.path.join(OUTPUT_DIR, "icon")
dir_feat = os.path.join(OUTPUT_DIR, "feature_graphic")
dir_ss = os.path.join(OUTPUT_DIR, "screenshots")
dir_raw = os.path.join(OUTPUT_DIR, "raw_captures")
dir_vid = os.path.join(OUTPUT_DIR, "videos")
tmp_frames = os.path.join(dir_vid, "tmp_frames")

for d in [dir_icon, dir_feat, dir_ss, dir_vid, tmp_frames]:
    os.makedirs(d, exist_ok=True)

# 1. ICON (512x512)
src_icon = os.path.join(REPO_DIR, "play-store", "app-icon.png")
with Image.open(src_icon) as im:
    im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon, "icon_512.png"), "PNG", quality=98)
print("✓ Saved 512x512 Icon")

# 2. FEATURE GRAPHIC (1024x500)
src_feat = os.path.join(REPO_DIR, "play-store", "feature-graphic.png")
with Image.open(src_feat) as im:
    im.convert("RGB").resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat, "feature_graphic_1024x500.png"), "PNG", quality=98)
print("✓ Saved 1024x500 Feature Graphic")

# 3. 8 HYPERCASUAL ASO SCREENSHOT CARDS (1080x1920)
badges = [
    ("3D HELIX TOWER DROP!", "Spin The Tower & Master Fluid Bouncing Drops", (28, 215, 235)),
    ("BUTTER-SMOOTH BOUNCE!", "Realistic 3D Physics & Tactile Ball Controls", (35, 170, 240)),
    ("MEGA FEVER SMASH!", "Multi-Platform Drops Shatter Slabs With Fireball Power", (250, 75, 95)),
    ("TOWER CONQUERED!", "Reach The Checkered Base To Claim Epic Rewards", (70, 210, 95)),
    ("12+ EPIC BALL SKINS!", "Unlock Ninja Shurikens, Ice Cubes & Cyber Orbs", (245, 180, 15)),
    ("LEAGUE PROMOTION!", "Climb Global Leaderboard Ranks & Win Tournaments", (150, 45, 185)),
    ("SECOND CHANCE REVIVE!", "Activate Mega Fever Boost & Continue Your Streak", (240, 55, 120)),
    ("DODGE RED HAZARDS!", "Outsmart Deadly Splats Across 100+ Endless Towers", (230, 40, 50))
]

raw_files = [
    "raw_01_helix_menu.png",
    "raw_02_bouncing_descent.png",
    "raw_03_gap_drop_smash.png",
    "raw_04_victory_clear.png",
    "raw_05_skin_shop.png",
    "raw_06_league_climb.png",
    "raw_07_revive_countdown.png",
    "raw_08_expert_tower.png"
]

target_w, target_h = 1080, 1920

try:
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_sub = ImageFont.truetype("arialbd.ttf", 26)
    font_end_lg = ImageFont.truetype("arialbd.ttf", 58)
    font_end_cta = ImageFont.truetype("arialbd.ttf", 46)
    font_end_sub = ImageFont.truetype("arial.ttf", 32)
except Exception:
    font_badge = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_end_lg = ImageFont.load_default()
    font_end_cta = ImageFont.load_default()
    font_end_sub = ImageFont.load_default()

for i, (rf, (b_title, b_sub, b_col)) in enumerate(zip(raw_files, badges)):
    p_raw = os.path.join(dir_raw, rf)
    with Image.open(p_raw) as raw_im:
        im = raw_im.convert("RGBA")
        
        # Color & Contrast polish
        im = ImageEnhance.Color(im).enhance(1.15)
        im = ImageEnhance.Contrast(im).enhance(1.08)
        
        draw = ImageDraw.Draw(im)
        
        # Top Badge Pill
        badge_w, badge_h = 820, 84
        bx = (target_w - badge_w) // 2
        by = 56
        draw.rounded_rectangle([bx + 4, by + 4, bx + badge_w + 4, by + badge_h + 4], radius=24, fill=(0, 0, 0, 150))
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=24, fill=(*b_col, 245), outline=(255, 255, 255, 235), width=3)
        draw.text((target_w // 2, by + badge_h // 2), b_title, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
        # Bottom Subtitle Ribbon
        sub_w, sub_h = 760, 56
        sx = (target_w - sub_w) // 2
        sy = target_h - 110
        draw.rounded_rectangle([sx + 3, sy + 3, sx + sub_w + 3, sy + sub_h + 3], radius=18, fill=(0, 0, 0, 140))
        draw.rounded_rectangle([sx, sy, sx + sub_w, sy + sub_h], radius=18, fill=(16, 22, 38, 230), outline=(*b_col, 210), width=2)
        draw.text((target_w // 2, sy + sub_h // 2), b_sub, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
        
        out_ss = os.path.join(dir_ss, f"screenshot_{i+1:02d}.png")
        im.convert("RGB").save(out_ss, "PNG", quality=95)
print(f"✓ Generated 8 Polished Screenshots in {dir_ss}")

# 4. VIDEOS & TRAILERS
# Portrait Video (1080x1920)
slide_files_port = []
for i in range(1, 9):
    slide_files_port.append(os.path.join(dir_ss, f"screenshot_{i:02d}.png"))

# Endcard Portrait
end_p = Image.new("RGBA", (1080, 1920), (12, 18, 36, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((380, 380), Image.Resampling.LANCZOS)
    mask = Image.new("L", (380, 380), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 380, 380], radius=84, fill=255)
    end_p.paste(ic_res, ((1080 - 380) // 2, 440), mask)

draw_p = ImageDraw.Draw(end_p)
# Icon border
draw_p.rounded_rectangle([(1080 - 380) // 2 - 4, 436, (1080 - 380) // 2 + 380 + 4, 440 + 380 + 4], radius=88, outline=(28, 233, 245, 235), width=5)

# Text & CTA
draw_p.text((540, 890), "HELIX DROP: SPIRAL JUMP", font=font_end_lg, fill=(255, 255, 255, 255), anchor="mm")
draw_p.text((540, 970), "★ ★ ★ ★ ★   ARCADE BOUNCE & SMASH 3D", font=font_end_sub, fill=(255, 215, 0, 255), anchor="mm")
draw_p.text((540, 1030), "Spin Tower • Fever Drops • 12+ Skins • Endless Levels", font=font_end_sub, fill=(220, 235, 250, 255), anchor="mm")

# CTA Button
draw_p.rounded_rectangle([140, 1220, 940, 1340], radius=32, fill=(28, 215, 235, 245), outline=(255, 255, 255, 230), width=4)
draw_p.text((540, 1280), "DOWNLOAD FREE NOW!", font=font_end_cta, fill=(12, 24, 48, 255), anchor="mm")

end_p_path = os.path.join(tmp_frames, "end_p.png")
end_p.convert("RGB").save(end_p_path, "PNG")
slide_files_port.append(end_p_path)

concat_p = os.path.join(tmp_frames, "concat_p.txt")
with open(concat_p, "w") as f:
    for sf in slide_files_port[:-1]:
        f.write(f"file '{sf.replace(chr(92), '/')}'\nduration 1.6\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\nduration 2.8\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")

audio_bgm = os.path.join(REPO_DIR, "assets", "audio", "bgm", "bgm_loop.wav")
out_vid_p = os.path.join(dir_vid, "helix_trailer_portrait_9x16.mp4")

cmd_p = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_p,
    "-stream_loop", "-1", "-i", audio_bgm,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-b:v", "4.2M",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "14",
    "-vf", "scale=1080:1920",
    "-shortest",
    out_vid_p
]
subprocess.run(cmd_p, capture_output=True)
print("✓ Rendered Portrait Trailer:", out_vid_p)

# Landscape Video (1920x1080)
slide_files_land = []
for idx, sf in enumerate(slide_files_port[:-1]):
    with Image.open(sf) as sim:
        bg = sim.resize((1920, 1080), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=30))
        dark = Image.new("RGBA", (1920, 1080), (0, 0, 0, 90))
        bg = Image.alpha_composite(bg.convert("RGBA"), dark)
        
        # Center card
        card_h = 1000
        card_w = int(card_h * 1080 / 1920)
        card_res = sim.resize((card_w, card_h), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (card_w, card_h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w, card_h], radius=24, fill=255)
        
        cx = (1920 - card_w) // 2
        cy = (1080 - card_h) // 2
        bg.paste(card_res, (cx, cy), mask)
        draw = ImageDraw.Draw(bg)
        draw.rounded_rectangle([cx - 4, cy - 4, cx + card_w + 4, cy + card_h + 4], radius=28, outline=(28, 233, 245, 220), width=4)
        
        out_land = os.path.join(tmp_frames, f"land_{idx}.png")
        bg.convert("RGB").save(out_land, "PNG")
        slide_files_land.append(out_land)

# Endcard Landscape
end_l = Image.new("RGBA", (1920, 1080), (12, 18, 36, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((360, 360), Image.Resampling.LANCZOS)
    mask = Image.new("L", (360, 360), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 360], radius=76, fill=255)
    end_l.paste(ic_res, (280, (1080 - 360) // 2), mask)

draw_l = ImageDraw.Draw(end_l)
draw_l.rounded_rectangle([276, (1080 - 360) // 2 - 4, 280 + 360 + 4, (1080 - 360) // 2 + 360 + 4], radius=80, outline=(28, 233, 245, 230), width=5)
draw_l.text((700, 390), "HELIX DROP: SPIRAL JUMP", font=font_end_lg, fill=(255, 255, 255, 255))
draw_l.text((700, 480), "★ ★ ★ ★ ★   ARCADE BOUNCE & SMASH 3D", font=font_end_sub, fill=(255, 215, 0, 255))
draw_l.text((700, 530), "Spin Tower • Fever Drops • 12+ Skins • Endless Levels", font=font_end_sub, fill=(220, 235, 250, 255))

draw_l.rounded_rectangle([700, 610, 1300, 710], radius=25, fill=(28, 215, 235, 245), outline=(255, 255, 255, 230), width=4)
draw_l.text((1000, 660), "DOWNLOAD FREE NOW!", font=font_end_cta, fill=(12, 24, 48, 255), anchor="mm")

end_l_path = os.path.join(tmp_frames, "end_l.png")
end_l.convert("RGB").save(end_l_path, "PNG")
slide_files_land.append(end_l_path)

concat_l = os.path.join(tmp_frames, "concat_l.txt")
with open(concat_l, "w") as f:
    for sf in slide_files_land[:-1]:
        f.write(f"file '{sf.replace(chr(92), '/')}'\nduration 1.6\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\nduration 2.8\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")

out_vid_l = os.path.join(dir_vid, "helix_trailer_landscape_16x9.mp4")
cmd_l = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_l,
    "-stream_loop", "-1", "-i", audio_bgm,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-b:v", "4.5M",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "14",
    "-vf", "scale=1920:1080",
    "-shortest",
    out_vid_l
]
subprocess.run(cmd_l, capture_output=True)
print("✓ Rendered Landscape Trailer:", out_vid_l)

# Cleanup
for f in os.listdir(tmp_frames):
    try:
        os.remove(os.path.join(tmp_frames, f))
    except Exception:
        pass
try:
    os.rmdir(tmp_frames)
except Exception:
    pass
print("✓ Completed Helix Jump Spiral Asset Suite!")
