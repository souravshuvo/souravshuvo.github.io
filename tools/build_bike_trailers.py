# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

FFMPEG = r"C:\Users\shuvo\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_DIR = r"D:\souravshuvo.github.io\game_store_assets\Bike-Traffic-Racer"
DIR_RAW = os.path.join(OUTPUT_DIR, "raw_captures")
DIR_VID = os.path.join(OUTPUT_DIR, "videos")
TMP_FRAMES = os.path.join(DIR_VID, "tmp_frames")
os.makedirs(TMP_FRAMES, exist_ok=True)

# Generate 7 key video slides with dynamic hypercasual sticker text
slides = [
    ("raw_01_city_highway.png", "🏍️ TAKE THE HANDLEBARS! 🏍️", (255, 60, 40)),
    ("raw_02_traffic_weave.png", "⚡ DODGE TRAFFIC AT 180 KM/H! ⚡", (0, 210, 255)),
    ("raw_03_coastal_sunset.png", "🌅 TWO-WAY HIGHWAY RUSH! 🌅", (255, 170, 0)),
    ("raw_04_desert_canyon.png", "⏱️ BEAT THE MISSION CLOCK! ⏱️", (240, 80, 20)),
    ("raw_05_neon_midnight.png", "🌃 MIDNIGHT TOP SPEED! 🌃", (180, 50, 255)),
    ("raw_06_garage_tuning.png", "🔧 UPGRADE YOUR SUPERBIKE! 🔧", (0, 230, 120)),
    ("raw_08_victory.png", "🏆 3-STAR VICTORY! 🏆", (255, 215, 0))
]

try:
    font_lg = ImageFont.truetype("arialbd.ttf", 64)
    font_cta = ImageFont.truetype("arialbd.ttf", 52)
    font_sub = ImageFont.truetype("arial.ttf", 36)
except Exception:
    font_lg = ImageFont.load_default()
    font_cta = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# 1. LANDSCAPE SLIDES (1920x1080)
slide_files_land = []
for idx, (rf, text, col) in enumerate(slides):
    im_path = os.path.join(DIR_RAW, rf)
    with Image.open(im_path) as raw:
        im = raw.convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        
        # Sticker banner
        bw, bh = 1100, 110
        bx = (1920 - bw) // 2
        by = 60
        draw.rounded_rectangle([bx + 6, by + 6, bx + bw + 6, by + bh + 6], radius=28, fill=(0, 0, 0, 170))
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28, fill=(*col, 245), outline=(255, 255, 255, 240), width=4)
        draw.text((1920 // 2, by + bh // 2), text, font=font_lg, fill=(255, 255, 255, 255), anchor="mm")
        
        out_f = os.path.join(TMP_FRAMES, f"slide_l_{idx}.png")
        im.convert("RGB").save(out_f, "PNG")
        slide_files_land.append(out_f)

# Endcard Landscape
end_l = Image.new("RGBA", (1920, 1080), (12, 16, 26, 255))
icon_path = os.path.join(REPO_DIR, "play-store", "app-icon.png")
with Image.open(icon_path) as ic:
    ic_res = ic.resize((360, 360), Image.Resampling.LANCZOS)
    mask = Image.new("L", (360, 360), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 360], radius=72, fill=255)
    end_l.paste(ic_res, (280, (1080 - 360) // 2), mask)
    
draw_end = ImageDraw.Draw(end_l)
draw_end.rounded_rectangle([276, (1080 - 360) // 2 - 4, 280 + 360 + 4, (1080 - 360) // 2 + 360 + 4], radius=76, outline=(0, 229, 255, 220), width=5)
draw_end.text((700, 390), "BIKE: HIGHWAY TRAFFIC RACER", font=font_lg, fill=(255, 255, 255, 255))
draw_end.text((700, 480), "★ ★ ★ ★ ★   HIGH-SPEED 3D RACING HIT", font=font_sub, fill=(255, 215, 0, 255))
draw_end.text((700, 530), "Thread highway traffic • Feel the cockpit speed • Upgrade your ride", font=font_sub, fill=(180, 210, 240, 255))

# CTA button
draw_end.rounded_rectangle([700, 610, 1300, 710], radius=25, fill=(0, 210, 100, 245), outline=(255, 255, 255, 230), width=4)
draw_end.text((1000, 660), "DOWNLOAD NOW ON GOOGLE PLAY", font=font_cta, fill=(255, 255, 255, 255), anchor="mm")

end_l_file = os.path.join(TMP_FRAMES, "slide_l_end.png")
end_l.convert("RGB").save(end_l_file, "PNG")
slide_files_land.append(end_l_file)

# Build concat demuxer file for 15s video
concat_l = os.path.join(TMP_FRAMES, "concat_l.txt")
with open(concat_l, "w") as f:
    for sf in slide_files_land[:-1]:
        f.write(f"file '{sf.replace(chr(92), '/')}'\nduration 1.8\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\nduration 3.0\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")

# Audio tracks
bgm = os.path.join(REPO_DIR, "assets", "audio", "bgm", "bgm_loop.wav")
out_vid_l = os.path.join(DIR_VID, "bike_trailer_landscape_16x9.mp4")

cmd_l = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_l,
    "-stream_loop", "-1", "-i", bgm,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-b:v", "4.5M",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "14",
    "-vf", "scale=1920:1080",
    "-shortest",
    out_vid_l
]
subprocess.run(cmd_l, capture_output=True)
print("✓ Rendered Landscape Trailer:", out_vid_l)

# 2. PORTRAIT SLIDES (1080x1920)
slide_files_port = []
for idx in range(1, 9):
    ss_path = os.path.join(OUTPUT_DIR, "screenshots", f"screenshot_{idx:02d}.png")
    slide_files_port.append(ss_path)

concat_p = os.path.join(TMP_FRAMES, "concat_p.txt")
with open(concat_p, "w") as f:
    for sf in slide_files_port:
        f.write(f"file '{sf.replace(chr(92), '/')}'\nduration 1.75\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")

out_vid_p = os.path.join(DIR_VID, "bike_trailer_portrait_9x16.mp4")
cmd_p = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_p,
    "-stream_loop", "-1", "-i", bgm,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-b:v", "4.2M",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "14",
    "-vf", "scale=1080:1920",
    "-shortest",
    out_vid_p
]
subprocess.run(cmd_p, capture_output=True)
print("✓ Rendered Portrait Trailer:", out_vid_p)

# Cleanup temp frames
for f in os.listdir(TMP_FRAMES):
    try:
        os.remove(os.path.join(TMP_FRAMES, f))
    except Exception:
        pass
os.rmdir(TMP_FRAMES)
print("✓ Successfully completed all video trailers for Bike-Traffic-Racer!")