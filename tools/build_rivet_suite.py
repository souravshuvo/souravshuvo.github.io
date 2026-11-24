# -*- coding: utf-8 -*-
import os
import subprocess
import wave
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FFMPEG = r"C:\Users\shuvo\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
WORKSPACE = r"D:\souravshuvo.github.io"
REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"
OUTPUT_DIR = os.path.join(WORKSPACE, "game_store_assets", "Rivet-Block-Escape")

dir_icon = os.path.join(OUTPUT_DIR, "icon")
dir_feat = os.path.join(OUTPUT_DIR, "feature_graphic")
dir_ss = os.path.join(OUTPUT_DIR, "screenshots")
dir_raw = os.path.join(OUTPUT_DIR, "raw_captures")
dir_vid = os.path.join(OUTPUT_DIR, "videos")
tmp_frames = os.path.join(dir_vid, "tmp_frames")

for d in [dir_icon, dir_feat, dir_ss, dir_vid, tmp_frames]:
    os.makedirs(d, exist_ok=True)

# 1. ICON (512x512)
src_icon = os.path.join(REPO_DIR, "handoff", "store", "play-icon.png")
with Image.open(src_icon) as im:
    im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(dir_icon, "icon_512.png"), "PNG", quality=98)
print("Saved 512x512 Icon")

# 2. FEATURE GRAPHIC (1024x500)
src_feat = os.path.join(REPO_DIR, "handoff", "store", "feature-graphic.png")
with Image.open(src_feat) as im:
    im.convert("RGB").resize((1024, 500), Image.Resampling.LANCZOS).save(os.path.join(dir_feat, "feature_graphic_1024x500.png"), "PNG", quality=98)
print("Saved 1024x500 Feature Graphic")

# 3. 8 HYPERCASUAL ASO SCREENSHOT CARDS (1080x1920)
badges = [
    ("SLIDE STURDY RIVET BLOCKS!", "Push Colored Blocks Through Matching Workshop Gates", (244, 106, 84)),
    ("UNLOCK RESTRICTED CORRIDORS!", "Move Blocking Pieces To Clear The Exit Lane", (41, 188, 165)),
    ("TRACE LEGAL ROUTE HINTS!", "Follow Dotted Pathfinding Directly To Your Gate", (255, 191, 66)),
    ("100 TIMED WORKSHOP PUZZLES!", "Master 10 Industrial Districts Across The Foundry", (89, 154, 247)),
    ("STEEL STOPS & TIGHT CORNERS!", "Navigate Immovable Barriers & Numbered Latches", (236, 112, 163)),
    ("FROST MILL THAWING MECHANIC!", "Melt Frozen Blocks As You Ship Deliveries", (0, 200, 240)),
    ("ORDER SHIPPED 3-STAR WIN!", "Beat The Workshop Clock & Claim Master Badges", (255, 200, 30)),
    ("CONQUER THE GRAND FOUNDRY!", "Solve 8-Piece Multi-Color Shift Puzzles", (174, 135, 237))
]

raw_files = [
    "raw_01_workshop_home.png",
    "raw_02_first_delivery.png",
    "raw_03_route_pathfinding.png",
    "raw_04_level_book.png",
    "raw_05_steel_stops.png",
    "raw_06_frost_mill_ice.png",
    "raw_07_order_shipped_win.png",
    "raw_08_grand_foundry.png"
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
        im = ImageEnhance.Color(im).enhance(1.18)
        im = ImageEnhance.Contrast(im).enhance(1.10)
        
        # Background
        canvas = Image.new("RGBA", (target_w, target_h), (18, 28, 44, 255))
        bg = im.copy().resize((target_w, target_h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=28))
        dark = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 95))
        bg = Image.alpha_composite(bg, dark)
        canvas.paste(bg, (0, 0))
        
        # Center frame (portrait frame scaled to 990 x 1760 with breathing margin)
        fw = 990
        fh = int(fw * 1920 / 1080)
        if fh > 1600:
            fh = 1600
            fw = int(fh * 1080 / 1920)
            
        im_frame = im.resize((fw, fh), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (fw, fh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw, fh], radius=28, fill=255)
        
        fx = (target_w - fw) // 2
        fy = (target_h - fh) // 2 + 35
        
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle([fx - 6, fy - 6, fx + fw + 6, fy + fh + 6], radius=32, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([fx - 4, fy - 4, fx + fw + 4, fy + fh + 4], radius=30, outline=(255, 191, 66, 230), width=4)
        draw.rounded_rectangle([fx - 1, fy - 1, fx + fw + 1, fy + fh + 1], radius=28, outline=(255, 255, 255, 210), width=2)
        
        canvas.paste(im_frame, (fx, fy), mask)
        
        # Top Badge Pill
        badge_w, badge_h = 840, 84
        bx = (target_w - badge_w) // 2
        by = 55
        draw.rounded_rectangle([bx + 4, by + 4, bx + badge_w + 4, by + badge_h + 4], radius=24, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=24, fill=(*b_col, 245), outline=(255, 255, 255, 235), width=3)
        draw.text((target_w // 2, by + badge_h // 2), b_title, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
        # Bottom Subtitle Ribbon
        sub_w, sub_h = 780, 60
        sx = (target_w - sub_w) // 2
        sy = fy + fh + 45
        if sy + sub_h > target_h - 20:
            sy = target_h - sub_h - 25
            
        draw.rounded_rectangle([sx + 3, sy + 3, sx + sub_w + 3, sy + sub_h + 3], radius=18, fill=(0, 0, 0, 140))
        draw.rounded_rectangle([sx, sy, sx + sub_w, sy + sub_h], radius=18, fill=(22, 34, 52, 230), outline=(255, 191, 66, 190), width=2)
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
    ("raw_01_workshop_home.png", "RIVET BLOCK ESCAPE!", (244, 106, 84)),
    ("raw_02_first_delivery.png", "SLIDE TO MATCHING GATES!", (41, 188, 165)),
    ("raw_03_route_pathfinding.png", "SMART ROUTE PATHFINDING!", (255, 191, 66)),
    ("raw_04_level_book.png", "100 WORKSHOP PUZZLES!", (89, 154, 247)),
    ("raw_05_steel_stops.png", "STEEL STOPS & OBSTACLES!", (236, 112, 163)),
    ("raw_06_frost_mill_ice.png", "FROST MILL ICE MELTING!", (0, 200, 240)),
    ("raw_07_order_shipped_win.png", "DELIVER ALL ORDERS!", (255, 200, 30))
]

# Build Portrait Slides (1080x1920)
slide_files_port = []
for idx in range(len(trailer_slides)):
    ss_path = os.path.join(dir_ss, f"screenshot_{idx+1:02d}.png")
    out_f = os.path.join(tmp_frames, f"slide_p_{idx}.png")
    with Image.open(ss_path) as im:
        im.resize((1080, 1920), Image.Resampling.LANCZOS).save(out_f, "PNG")
        slide_files_port.append(out_f)

# Portrait Endcard
end_p = Image.new("RGBA", (1080, 1920), (18, 28, 44, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((420, 420), Image.Resampling.LANCZOS)
    mask = Image.new("L", (420, 420), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 420, 420], radius=84, fill=255)
    end_p.paste(ic_res, (330, 480), mask)

draw_ep = ImageDraw.Draw(end_p)
draw_ep.rounded_rectangle([324, 474, 756, 906], radius=86, outline=(255, 191, 66, 240), width=4)
draw_ep.text((540, 1000), "RIVET BLOCK ESCAPE", font=font_title, fill=(255, 255, 255, 255), anchor="mm")
draw_ep.text((540, 1080), "Slide Studded Blocks & Ship All Orders", font=font_sub_v, fill=(255, 210, 120, 255), anchor="mm")

draw_ep.rounded_rectangle([240, 1200, 840, 1320], radius=28, fill=(255, 180, 40, 255), outline=(255, 255, 255, 220), width=3)
draw_ep.text((540, 1260), "INSTALL NOW FREE", font=font_cta, fill=(18, 28, 44, 255), anchor="mm")

draw_ep.text((540, 1390), "Google Play Store  *  100 Offline Puzzles", font=font_sub_v, fill=(180, 180, 180, 255), anchor="mm")

end_p_file = os.path.join(tmp_frames, "slide_p_end.png")
end_p.convert("RGB").save(end_p_file, "PNG")
slide_files_port.append(end_p_file)

# Build Landscape Slides (1920x1080)
slide_files_land = []
for idx, (rf, text, col) in enumerate(trailer_slides):
    im_path = os.path.join(dir_raw, rf)
    with Image.open(im_path) as raw:
        canvas_l = Image.new("RGBA", (1920, 1080), (18, 28, 44, 255))
        bg_l = raw.copy().resize((1920, 1080), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=30))
        dark_l = Image.new("RGBA", (1920, 1080), (0, 0, 0, 100))
        canvas_l.paste(Image.alpha_composite(bg_l, dark_l), (0, 0))
        
        # Center fit portrait card inside landscape
        ch = 1000
        cw = int(ch * 1080 / 1920)
        raw_res = raw.resize((cw, ch), Image.Resampling.LANCZOS)
        mask_l = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(mask_l).rounded_rectangle([0, 0, cw, ch], radius=24, fill=255)
        
        cx = (1920 - cw) // 2
        cy = (1080 - ch) // 2
        
        draw_l = ImageDraw.Draw(canvas_l)
        draw_l.rounded_rectangle([cx - 5, cy - 5, cx + cw + 5, cy + ch + 5], radius=28, fill=(0, 0, 0, 160))
        draw_l.rounded_rectangle([cx - 3, cy - 3, cx + cw + 3, cy + ch + 3], radius=26, outline=(255, 191, 66, 230), width=3)
        canvas_l.paste(raw_res, (cx, cy), mask_l)
        
        # Banner
        bw, bh = 1140, 100
        bx = (1920 - bw) // 2
        by = 50
        draw_l.rounded_rectangle([bx + 5, by + 5, bx + bw + 5, by + bh + 5], radius=24, fill=(0, 0, 0, 170))
        draw_l.rounded_rectangle([bx, by, bx + bw, by + bh], radius=24, fill=(*col, 245), outline=(255, 255, 255, 235), width=3)
        draw_l.text((1920 // 2, by + bh // 2), text, font=font_lg, fill=(255, 255, 255, 255), anchor="mm")
        
        out_f = os.path.join(tmp_frames, f"slide_l_{idx}.png")
        canvas_l.convert("RGB").save(out_f, "PNG")
        slide_files_land.append(out_f)

# Landscape Endcard
end_l = Image.new("RGBA", (1920, 1080), (18, 28, 44, 255))
with Image.open(src_icon) as ic:
    ic_res = ic.resize((360, 360), Image.Resampling.LANCZOS)
    mask = Image.new("L", (360, 360), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 360], radius=72, fill=255)
    end_l.paste(ic_res, (220, 360), mask)

draw_el = ImageDraw.Draw(end_l)
draw_el.rounded_rectangle([216, 356, 584, 724], radius=74, outline=(255, 191, 66, 240), width=4)
draw_el.text((640, 420), "RIVET BLOCK ESCAPE", font=font_title, fill=(255, 255, 255, 255))
draw_el.text((640, 500), "Slide Studded Blocks & Ship All 100 Orders!", font=font_sub_v, fill=(255, 210, 120, 255))

draw_el.rounded_rectangle([640, 580, 1140, 680], radius=24, fill=(255, 180, 40, 255), outline=(255, 255, 255, 220), width=3)
draw_el.text((890, 630), "INSTALL NOW FREE", font=font_cta, fill=(18, 28, 44, 255), anchor="mm")

end_l_file = os.path.join(tmp_frames, "slide_l_end.png")
end_l.convert("RGB").save(end_l_file, "PNG")
slide_files_land.append(end_l_file)

# Build custom audio using clear.wav and exit.wav
res_raw = os.path.join(REPO_DIR, "android", "app", "src", "main", "res", "raw")
sfx_clear = os.path.join(res_raw, "clear.wav")
sfx_exit = os.path.join(res_raw, "exit.wav")
sfx_slide = os.path.join(res_raw, "slide.wav")
sfx_tool = os.path.join(res_raw, "tool.wav")

total_dur = 2.2 * 7 + 3.5

# Generate composite audio track
audio_synth = os.path.join(tmp_frames, "soundtrack.wav")
# Build timed audio sequence with FFmpeg amix / adelay
filter_complex = (
    "[0:a]adelay=300|300[a0];"
    "[1:a]adelay=1800|1800[a1];"
    "[0:a]adelay=2500|2500[a2];"
    "[1:a]adelay=4000|4000[a3];"
    "[2:a]adelay=5200|5200[a4];"
    "[1:a]adelay=6800|6800[a5];"
    "[0:a]adelay=8800|8800[a6];"
    "[1:a]adelay=11000|11000[a7];"
    "[3:a]adelay=13500|13500[a8];"
    "[a0][a1][a2][a3][a4][a5][a6][a7][a8]amix=inputs=9:dropout_transition=2:normalize=0[aout]"
)

cmd_audio = [
    FFMPEG, "-y",
    "-i", sfx_slide,
    "-i", sfx_exit,
    "-i", sfx_tool,
    "-i", sfx_clear,
    "-filter_complex", filter_complex,
    "-map", "[aout]",
    "-t", str(total_dur),
    audio_synth
]
subprocess.run(cmd_audio, check=True)
print("Created Synced Audio:", audio_synth)

# Concat files
concat_p = os.path.join(tmp_frames, "concat_p.txt")
with open(concat_p, "w") as f:
    for s in slide_files_port[:-1]:
        f.write(f"file '{s.replace(chr(92), '/')}'\n")
        f.write("duration 2.2\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")
    f.write("duration 3.5\n")
    f.write(f"file '{slide_files_port[-1].replace(chr(92), '/')}'\n")

concat_l = os.path.join(tmp_frames, "concat_l.txt")
with open(concat_l, "w") as f:
    for s in slide_files_land[:-1]:
        f.write(f"file '{s.replace(chr(92), '/')}'\n")
        f.write("duration 2.2\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")
    f.write("duration 3.5\n")
    f.write(f"file '{slide_files_land[-1].replace(chr(92), '/')}'\n")

out_mp4_port = os.path.join(dir_vid, "rivet_trailer_portrait_9x16.mp4")
out_mp4_land = os.path.join(dir_vid, "rivet_trailer_landscape_16x9.mp4")

# Render Portrait Trailer
cmd_p = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_p,
    "-i", audio_synth,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-t", str(total_dur),
    out_mp4_port
]
subprocess.run(cmd_p, check=True)
print("Saved Portrait Trailer:", out_mp4_port)

# Render Landscape Trailer
cmd_l = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_l,
    "-i", audio_synth,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-t", str(total_dur),
    out_mp4_land
]
subprocess.run(cmd_l, check=True)
print("Saved Landscape Trailer:", out_mp4_land)
print("ALL RIVET BLOCK ESCAPE ASSETS SUCCESSFULLY COMPLETED!")
