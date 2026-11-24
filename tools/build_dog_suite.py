# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FFMPEG = r"C:\Users\shuvo\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_DIR = os.path.join(WORKSPACE, "game_store_assets", "Dog-Escape-Run")

dir_icon = os.path.join(OUTPUT_DIR, "icon")
dir_feat = os.path.join(OUTPUT_DIR, "feature_graphic")
dir_ss = os.path.join(OUTPUT_DIR, "screenshots")
dir_raw = os.path.join(OUTPUT_DIR, "raw_captures")
dir_vid = os.path.join(OUTPUT_DIR, "videos")
tmp_frames = os.path.join(dir_vid, "tmp_frames")

for d in [dir_icon, dir_feat, dir_ss, dir_vid, tmp_frames]:
    os.makedirs(d, exist_ok=True)

# 1. ICON (512x512)
src_icon = os.path.join(REPO_DIR, "play-store", "icon-512.png")
with Image.open(src_icon) as im:
    im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon, "icon_512.png"), "PNG", quality=98)
print("✓ Saved 512x512 Icon")

# 2. FEATURE GRAPHIC (1024x500)
src_feat = os.path.join(REPO_DIR, "play-store", "feature-graphic-1024x500.png")
with Image.open(src_feat) as im:
    im.convert("RGB").resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat, "feature_graphic_1024x500.png"), "PNG", quality=98)
print("✓ Saved 1024x500 Feature Graphic")

# 3. 8 HYPERCASUAL ASO SCREENSHOT CARDS (1080x1920)
badges = [
    ("🐕 SNEAK PAST GUARDS! 🐕", "Timing & Patience Are Everything", (255, 120, 0)),
    ("⚡ DYNAMIC STEALTH DASH! ⚡", "Drag To Move & Dodge Vision Cones", (0, 190, 240)),
    ("🔘 STEP ON SECURITY SWITCHES! 🔘", "Open Locked Gates & Bypass Blockades", (150, 60, 255)),
    ("📦 PUSH CRATES FOR COVER! 📦", "Slide Heavy Boxes To Block Vision Lines", (210, 140, 20)),
    ("🚨 DODGE PULSING LASERS! 🚨", "Time Your Steps Past Red Laser Traps", (255, 50, 70)),
    ("🌿 BONUS HEDGE MAZE! 🌿", "Collect All 3 Stars In Secret Garden", (0, 190, 110)),
    ("🐶 UNLOCK PUPPIES & TRAILS! 🐶", "Classic Pup, Frenchie & Rainbow Trails", (255, 70, 160)),
    ("🏆 3-STAR LEVEL COMPLETE! 🏆", "Good Job! Earn Big Coin Rewards", (255, 215, 0))
]

raw_files = [
    "raw_01_sneak_past_guard.png",
    "raw_02_stealth_dash.png",
    "raw_03_switch_and_gate.png",
    "raw_04_box_push_puzzle.png",
    "raw_05_laser_barrier_bypass.png",
    "raw_06_bonus_hedge_maze.png",
    "raw_07_skin_wardrobe_shop.png",
    "raw_08_victory_good_job.png"
]

target_w, target_h = 1080, 1920

try:
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_sub = ImageFont.truetype("arialbd.ttf", 26)
    font_end_lg = ImageFont.truetype("arialbd.ttf", 60)
    font_end_cta = ImageFont.truetype("arialbd.ttf", 48)
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
        im = ImageEnhance.Color(im).enhance(1.18)
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
        draw.rounded_rectangle([sx, sy, sx + sub_w, sy + sub_h], radius=18, fill=(18, 22, 34, 230), outline=(*b_col, 210), width=2)
        draw.text((target_w // 2, sy + sub_h // 2), b_sub, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
        
        out_ss = os.path.join(dir_ss, f"screenshot_{i+1:02d}.png")
        im.convert("RGB").save(out_ss, "PNG", quality=96)
        print(f"✓ Generated Screenshot {i+1:02d}: {b_title}")

print("\nAll 8 Screenshots successfully created!")

# 4. BUILD VIDEO TRAILERS
# Portrait Video (1080x1920)
slide_files_port = []
for idx in range(1, 9):
    ss_path = os.path.join(dir_ss, f"screenshot_{idx:02d}.png")
    slide_files_port.append(ss_path)

# Endcard Portrait
end_p = Image.new("RGBA", (1080, 1920), (22, 30, 46, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((380, 380), Image.Resampling.LANCZOS)
    mask = Image.new("L", (380, 380), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 380, 380], radius=76, fill=255)
    end_p.paste(ic_res, ((1080 - 380) // 2, 450), mask)

draw_p = ImageDraw.Draw(end_p)
draw_p.rounded_rectangle([(1080 - 380) // 2 - 4, 446, (1080 - 380) // 2 + 380 + 4, 450 + 380 + 4], radius=80, outline=(255, 150, 0, 240), width=5)
draw_p.text((540, 920), "DOG ESCAPE", font=font_end_lg, fill=(255, 255, 255, 255), anchor="mm")
draw_p.text((540, 985), "SNEAK PAST THE GUARDS!", font=font_end_cta, fill=(255, 170, 0, 255), anchor="mm")
draw_p.text((540, 1050), "★ ★ ★ ★ ★   CHARMING STEALTH PUZZLE", font=font_end_sub, fill=(255, 215, 0, 255), anchor="mm")
draw_p.text((540, 1100), "Dodge Guards • Push Crates • Unlock Cute Pups!", font=font_end_sub, fill=(220, 230, 245, 255), anchor="mm")

# CTA Button
draw_p.rounded_rectangle([140, 1220, 940, 1340], radius=32, fill=(255, 120, 0, 245), outline=(255, 255, 255, 230), width=4)
draw_p.text((540, 1280), "DOWNLOAD FREE NOW!", font=font_end_cta, fill=(255, 255, 255, 255), anchor="mm")

end_p_path = os.path.join(tmp_frames, "end_p.png")
end_p.convert("RGB").save(end_p_path, "PNG")
slide_files_port.append(end_p_path)

concat_p = os.path.join(tmp_frames, "concat_p.txt")
with open(concat_p, "w") as f:
    for sf in slide_files_port[:-1]:
        f.write(f"file '{sf.replace(chr(92), '/')}'\nduration 1.6\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\nduration 2.8\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")

audio_bgm = os.path.join(REPO_DIR, "assets", "audio", "bgm.wav")
out_vid_p = os.path.join(dir_vid, "dog_escape_trailer_portrait_9x16.mp4")

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
        draw.rounded_rectangle([cx - 4, cy - 4, cx + card_w + 4, cy + card_h + 4], radius=28, outline=(255, 170, 0, 220), width=4)
        
        out_land = os.path.join(tmp_frames, f"land_{idx}.png")
        bg.convert("RGB").save(out_land, "PNG")
        slide_files_land.append(out_land)

# Endcard Landscape
end_l = Image.new("RGBA", (1920, 1080), (22, 30, 46, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((360, 360), Image.Resampling.LANCZOS)
    mask = Image.new("L", (360, 360), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 360], radius=72, fill=255)
    end_l.paste(ic_res, (280, (1080 - 360) // 2), mask)

draw_l = ImageDraw.Draw(end_l)
draw_l.rounded_rectangle([276, (1080 - 360) // 2 - 4, 280 + 360 + 4, (1080 - 360) // 2 + 360 + 4], radius=76, outline=(255, 170, 0, 230), width=5)
draw_l.text((700, 390), "DOG ESCAPE: SNEAK PAST GUARDS", font=font_end_lg, fill=(255, 255, 255, 255))
draw_l.text((700, 480), "★ ★ ★ ★ ★   CHARMING STEALTH ADVENTURE", font=font_end_sub, fill=(255, 215, 0, 255))
draw_l.text((700, 530), "Dodge Vision Cones • Push Crates • Unlock Cute Pups", font=font_end_sub, fill=(220, 230, 245, 255))

draw_l.rounded_rectangle([700, 610, 1300, 710], radius=25, fill=(255, 120, 0, 245), outline=(255, 255, 255, 230), width=4)
draw_l.text((1000, 660), "DOWNLOAD FREE NOW!", font=font_end_cta, fill=(255, 255, 255, 255), anchor="mm")

end_l_path = os.path.join(tmp_frames, "end_l.png")
end_l.convert("RGB").save(end_l_path, "PNG")
slide_files_land.append(end_l_path)

concat_l = os.path.join(tmp_frames, "concat_l.txt")
with open(concat_l, "w") as f:
    for sf in slide_files_land[:-1]:
        f.write(f"file '{sf.replace(chr(92), '/')}'\nduration 1.6\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\nduration 2.8\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")

out_vid_l = os.path.join(dir_vid, "dog_escape_trailer_landscape_16x9.mp4")
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
print("✓ Completed Dog Escape Asset Suite!")
