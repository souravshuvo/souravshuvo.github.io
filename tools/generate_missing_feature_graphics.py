# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUTPUT_BASE = r"D:\souravshuvo.github.io\game_store_assets"

for g in sorted(os.listdir(OUTPUT_BASE)):
    g_dir = os.path.join(OUTPUT_BASE, g)
    if not os.path.isdir(g_dir):
        continue
    feat_path = os.path.join(g_dir, "feature_graphic", "feature_graphic_1024x500.png")
    icon_path = os.path.join(g_dir, "icon", "icon_512.png")
    
    if not os.path.exists(feat_path) and os.path.exists(icon_path):
        os.makedirs(os.path.join(g_dir, "feature_graphic"), exist_ok=True)
        im_icon = Image.open(icon_path).convert("RGBA")
        
        # 1024 x 500 banner canvas
        banner = Image.new("RGBA", (1024, 500), (10, 16, 28, 255))
        
        # Blurred radiant background from icon
        bg = im_icon.resize((1024, 500), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=40))
        bg = ImageEnhance.Color(bg).enhance(1.4)
        bg = ImageEnhance.Brightness(bg).enhance(0.7)
        banner.paste(bg, (0, 0))
        
        # Radiant glow in center/left
        draw = ImageDraw.Draw(banner)
        for r in range(250, 0, -20):
            alpha = int(12 * (1.0 - r / 250.0))
            draw.ellipse([250 - r, 250 - r, 250 + r, 250 + r], fill=(0, 229, 255, alpha))
            
        # Paste Icon on Left
        icon_size = 280
        ic_res = im_icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        mask = Image.new("L", (icon_size, icon_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, icon_size, icon_size], radius=56, fill=255)
        
        # Shadow
        draw.rounded_rectangle([110 + 6, 110 + 8, 110 + icon_size + 6, 110 + icon_size + 8], radius=56, fill=(0, 0, 0, 150))
        # Outline
        draw.rounded_rectangle([110 - 4, 110 - 4, 110 + icon_size + 4, 110 + icon_size + 4], radius=60, outline=(0, 229, 255, 200), width=4)
        banner.paste(ic_res, (110, 110), mask)
        
        # Title Typography on Right
        clean_title = g.replace("-", " ").upper()
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 46)
            font_sub = ImageFont.truetype("arial.ttf", 26)
            font_badge = ImageFont.truetype("arialbd.ttf", 26)
        except Exception:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            font_badge = ImageFont.load_default()
            
        draw.text((440, 160), clean_title, font=font_title, fill=(255, 255, 255, 255))
        draw.text((440, 225), "Official Hypercasual Release", font=font_sub, fill=(0, 229, 255, 255))
        draw.text((440, 270), "★ ★ ★ ★ ★   TOP RATED CASUAL HIT", font=font_sub, fill=(255, 215, 0, 255))
        
        # CTA Pill
        draw.rounded_rectangle([440, 320, 440 + 280, 320 + 60], radius=30, fill=(0, 204, 110, 255), outline=(255, 255, 255, 220), width=2)
        draw.text((440 + 140, 320 + 30), "PLAY FREE NOW", font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
        banner.convert("RGB").save(feat_path, "PNG", quality=95)
        print(f"Generated Feature Graphic for {g}")

print("All feature graphics finalized!")