import argparse
import json
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_ROOT = os.path.join(REPO_ROOT, "game_store_assets")
W, H = 1080, 1920


def _detect_flutter_root():
    env_root = os.environ.get("FLUTTER_ROOT", "").strip()
    if env_root and os.path.isdir(env_root):
        return env_root
    for name in ("flutter.bat", "flutter"):
        w = shutil.which(name)
        if w:
            return os.path.dirname(os.path.dirname(os.path.realpath(w)))
    for d in (r"C:\flutter", r"C:\src\flutter", r"D:\flutter", os.path.expanduser(r"~\flutter")):
        if os.path.isdir(d):
            return d
    return None


def _pick_font(rel_material_name, win_fallbacks):
    fl = _detect_flutter_root()
    if fl:
        p = os.path.join(fl, "bin", "cache", "artifacts", "material_fonts", rel_material_name)
        if os.path.exists(p):
            return p
    win_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for fn in win_fallbacks:
        p = os.path.join(win_fonts, fn)
        if os.path.exists(p):
            return p
    return None


FONT_BLACK = _pick_font("roboto-black.ttf", ["segoeuib.ttf", "arialbd.ttf", "impact.ttf"])
FONT_BOLD = _pick_font("roboto-bold.ttf", ["segoeuib.ttf", "arialbd.ttf"])
FONT_REG = _pick_font("roboto-regular.ttf", ["segoeui.ttf", "arial.ttf"])


def hex_rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def load_font(path, size):
    if path and os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_gradient_bg(top_hex, mid_hex, bot_hex, orb_hex, accent_hex, seed=1):
    top = hex_rgb(top_hex)
    mid = hex_rgb(mid_hex)
    bot = hex_rgb(bot_hex)
    orb = hex_rgb(orb_hex)
    acc = hex_rgb(accent_hex)

    strip = Image.new("RGB", (1, H))
    px = strip.load()
    for y in range(H):
        t = y / (H - 1)
        if t < 0.48:
            u = t / 0.48
            c = tuple(int(top[i] + (mid[i] - top[i]) * u) for i in range(3))
        else:
            u = (t - 0.48) / 0.52
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * u) for i in range(3))
        px[0, y] = c
    bg = strip.resize((W, H), Image.Resampling.BILINEAR).convert("RGBA")

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx1 = 220 if seed % 2 == 0 else 860
    cy1 = 560 + (seed % 3) * 90
    gd.ellipse((cx1 - 480, cy1 - 480, cx1 + 480, cy1 + 480), fill=orb + (95,))
    cx2 = W - cx1
    cy2 = 1480 - (seed % 3) * 80
    gd.ellipse((cx2 - 520, cy2 - 520, cx2 + 520, cy2 + 520), fill=acc + (82,))
    gd.ellipse((W // 2 - 440, 1520, W // 2 + 440, 2140), fill=orb + (72,))
    glow = glow.filter(ImageFilter.GaussianBlur(115))
    bg = Image.alpha_composite(bg, glow)

    streaks = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(streaks)
    for k in range(-2, 6):
        x0 = k * 270 + (seed * 45) % 180
        sd.polygon(
            [(x0, 0), (x0 + 95, 0), (x0 - 460, H), (x0 - 555, H)],
            fill=(255, 255, 255, 11),
        )
    streaks = streaks.filter(ImageFilter.GaussianBlur(12))
    bg = Image.alpha_composite(bg, streaks)
    return bg


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255
    )
    return mask


def draw_phone_frame(cap_img, target_w, radius=46, accent_hex="#FFE27A"):
    """Frame Portrait or Landscape capture in a Titanium smartphone bezel."""
    is_land = cap_img.width > cap_img.height
    acc = hex_rgb(accent_hex)
    pad = 16 if not is_land else 18
    inner_w = target_w - pad * 2
    aspect = cap_img.height / float(cap_img.width)
    inner_h = int(round(inner_w * aspect))
    if not is_land and inner_h > 1420:
        inner_h = 1420
        inner_w = int(round(inner_h / aspect))
    outer_w = inner_w + pad * 2
    outer_h = inner_h + pad * 2

    sh_pad = 64
    canvas = Image.new("RGBA", (outer_w + sh_pad * 2, outer_h + sh_pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle(
        (sh_pad + 6, sh_pad + 18, sh_pad + outer_w + 6, sh_pad + outer_h + 18),
        radius=radius + 10,
        fill=(6, 10, 22, 165),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    canvas = Image.alpha_composite(canvas, sh)

    body = Image.new("RGBA", (outer_w, outer_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle(
        (0, 0, outer_w - 1, outer_h - 1),
        radius=radius + 8,
        fill=(32, 38, 52, 255),
        outline=acc + (210,),
        width=4,
    )
    bd.rounded_rectangle(
        (4, 4, outer_w - 5, outer_h - 5),
        radius=radius + 5,
        fill=(14, 18, 28, 255),
        outline=(255, 255, 255, 85),
        width=2,
    )

    screen = cap_img.convert("RGBA").resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    mask = rounded_mask((inner_w, inner_h), radius)
    body.paste(screen, (pad, pad), mask)

    glare = Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.polygon(
        [(0, 0), (inner_w * 0.62, 0), (inner_w * 0.22, inner_h * 0.45), (0, inner_h * 0.45)],
        fill=(255, 255, 255, 20),
    )
    glare.putalpha(ImageChops.darker(glare.getchannel("A"), mask))
    body.paste(glare, (pad, pad), glare)

    if not is_land:
        nw = max(78, int(inner_w * 0.14))
        nx = pad + (inner_w - nw) // 2
        bd = ImageDraw.Draw(body)
        bd.rounded_rectangle((nx, pad + 8, nx + nw, pad + 24), radius=8, fill=(10, 12, 18, 235))
        bd.ellipse((nx + nw - 18, pad + 11, nx + nw - 8, pad + 21), fill=(48, 76, 128, 255))
    else:
        nh = max(68, int(inner_h * 0.18))
        ny = pad + (inner_h - nh) // 2
        bd = ImageDraw.Draw(body)
        bd.rounded_rectangle((pad + 8, ny, pad + 22, ny + nh), radius=7, fill=(10, 12, 18, 235))

    canvas.alpha_composite(body, (sh_pad, sh_pad))
    return canvas, sh_pad


def paste_sticker_pill(canvas, text, cx, cy, bg_hex, fg_hex="#FFFFFF", glow_hex=None):
    font = load_font(FONT_BLACK, 30)
    tmp = ImageDraw.Draw(canvas)
    bbox = tmp.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pw, ph = tw + 56, th + 28
    pad = 24
    pill = Image.new("RGBA", (pw + pad * 2, ph + pad * 2), (0, 0, 0, 0))
    glow = Image.new("RGBA", pill.size, (0, 0, 0, 0))
    gc = hex_rgb(glow_hex or bg_hex)
    ImageDraw.Draw(glow).rounded_rectangle(
        (pad - 2, pad + 4, pad + pw + 2, pad + ph + 4),
        radius=ph // 2 + 4,
        fill=gc + (145,),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    pill = Image.alpha_composite(pill, glow)

    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle(
        (pad, pad, pad + pw, pad + ph),
        radius=ph // 2,
        fill=hex_rgb(bg_hex) + (255,),
        outline=(255, 255, 255, 235),
        width=4,
    )
    tx = pad + (pw - tw) // 2 - bbox[0]
    ty = pad + (ph - th) // 2 - bbox[1] - 1
    pd.text((tx, ty + 2), text, font=font, fill=(0, 0, 0, 95))
    pd.text((tx, ty), text, font=font, fill=hex_rgb(fg_hex) + (255,))
    canvas.alpha_composite(pill, (int(cx - pill.width // 2), int(cy - pill.height // 2)))


def draw_header(canvas, pill_text, line1, line2, subtitle, pill_bg, accent_hex, line2_hex="#FFE66D"):
    paste_sticker_pill(canvas, pill_text, W // 2, 74, pill_bg, "#FFFFFF", accent_hex)

    d = ImageDraw.Draw(canvas)
    size = 82
    while size >= 54:
        f = load_font(FONT_BLACK, size)
        b1 = d.textbbox((0, 0), line1, font=f)
        b2 = d.textbbox((0, 0), line2, font=f)
        if max(b1[2] - b1[0], b2[2] - b2[0]) <= 980:
            break
        size -= 4
    f_head = load_font(FONT_BLACK, size)
    b1 = d.textbbox((0, 0), line1, font=f_head)
    b2 = d.textbbox((0, 0), line2, font=f_head)
    h1 = b1[3] - b1[1]
    y1 = 122
    y2 = y1 + h1 + 14

    for txt, y, col in ((line1, y1, (255, 255, 255, 255)), (line2, y2, hex_rgb(line2_hex) + (255,))):
        bb = d.textbbox((0, 0), txt, font=f_head)
        tw = bb[2] - bb[0]
        x = (W - tw) // 2 - bb[0]
        for ox, oy in ((0, 5), (-3, -3), (3, -3), (-3, 3), (3, 3), (0, 8)):
            d.text((x + ox, y + oy), txt, font=f_head, fill=(10, 14, 26, 210 if oy <= 5 else 110))
        d.text((x, y), txt, font=f_head, fill=col)

    sub_size = 33
    while sub_size >= 24:
        fs = load_font(FONT_BOLD, sub_size)
        bs = d.textbbox((0, 0), subtitle, font=fs)
        if bs[2] - bs[0] <= 980:
            break
        sub_size -= 2
    fs = load_font(FONT_BOLD, sub_size)
    bs = d.textbbox((0, 0), subtitle, font=fs)
    sx = (W - (bs[2] - bs[0])) // 2 - bs[0]
    sy = y2 + (b2[3] - b2[1]) + 22
    d.text((sx, sy + 2), subtitle, font=fs, fill=(0, 0, 0, 150))
    d.text((sx, sy), subtitle, font=fs, fill=(235, 242, 255, 245))


def paste_popout_sprite(canvas, path, cx, cy, max_dim=360, angle=0.0, glow_hex="#FFE66D"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing sprite: {path}")
    im = Image.open(path).convert("RGBA")
    r, g, b, a = im.split()
    clean_a = a.point(lambda p: p if p > 24 else 0)
    im.putalpha(clean_a)
    mask_tight = clean_a.point(lambda p: 255 if p > 24 else 0)
    bbox = mask_tight.getbbox()
    if bbox:
        im = im.crop(bbox)

    scale = min(max_dim / float(im.width), max_dim / float(im.height))
    nw = max(1, int(round(im.width * scale)))
    nh = max(1, int(round(im.height * scale)))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    if abs(angle) > 0.1:
        im = im.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

    pad = 44
    layer = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    alpha_mask = im.getchannel("A")

    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 195), (pad + 4, pad + 14), alpha_mask)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    layer = Image.alpha_composite(layer, sh)

    gl = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    gl.paste(hex_rgb(glow_hex) + (155,), (pad, pad), alpha_mask)
    gl = gl.filter(ImageFilter.GaussianBlur(16))
    layer = Image.alpha_composite(layer, gl)

    rim = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    rim.paste((255, 255, 255, 190), (pad, pad), alpha_mask.filter(ImageFilter.MaxFilter(5)))
    layer = Image.alpha_composite(layer, rim)
    layer.alpha_composite(im, (pad, pad))

    px = int(cx - layer.width // 2)
    py = int(cy - layer.height // 2)
    px = max(-18, min(W - layer.width + 18, px))
    py = max(10, min(H - layer.height - 10, py))
    canvas.alpha_composite(layer, (px, py))


def paste_floating_chip(canvas, text, cx, cy, bg_hex="#132238", border_hex="#7DF3FF"):
    font = load_font(FONT_BLACK, 28)
    d = ImageDraw.Draw(canvas)
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw, ph = tw + 46, th + 26
    pad = 18
    chip = Image.new("RGBA", (pw + pad * 2, ph + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", chip.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        (pad, pad + 6, pad + pw, pad + ph + 6), radius=ph // 2, fill=(0, 0, 0, 180)
    )
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    chip = Image.alpha_composite(chip, sh)
    cd = ImageDraw.Draw(chip)
    cd.rounded_rectangle(
        (pad, pad, pad + pw, pad + ph),
        radius=ph // 2,
        fill=hex_rgb(bg_hex) + (242,),
        outline=hex_rgb(border_hex) + (255,),
        width=3,
    )
    tx = pad + (pw - tw) // 2 - bb[0]
    ty = pad + (ph - th) // 2 - bb[1] - 1
    cd.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    px = max(18, min(W - chip.width - 18, int(cx - chip.width // 2)))
    py = max(18, min(H - chip.height - 18, int(cy - chip.height // 2)))
    canvas.alpha_composite(chip, (px, py))


def build_card(cfg, card_idx, card_spec, mirror_dir=None, assets_root=None):
    assets_root = assets_root or cfg.get("assets_root") or ASSETS_ROOT
    game = cfg["game"]
    slug = cfg["slug"]
    cap_path = os.path.join(assets_root, game, "raw_captures", card_spec["capture"])
    cap_img = Image.open(cap_path).convert("RGBA")
    is_land = cap_img.width > cap_img.height

    bg = make_gradient_bg(
        cfg["top"], cfg["mid"], cfg["bot"], cfg["orb"], cfg["accent"], seed=card_idx
    )
    draw_header(
        bg,
        card_spec["pill"],
        card_spec["h1"],
        card_spec["h2"],
        card_spec["sub"],
        cfg["pill_bg"],
        cfg["accent"],
        cfg["h2_color"],
    )

    layout = card_spec["layout"]
    if is_land:
        phone_w = 970
        phone_canvas, _ = draw_phone_frame(cap_img, phone_w, radius=36, accent_hex=cfg["accent"])
        ang = 0.0 if layout in ("hero", "victory") else (-1.8 if layout == "left" else 1.8)
        if abs(ang) > 0.1:
            phone_canvas = phone_canvas.rotate(ang, resample=Image.Resampling.BICUBIC, expand=True)
        px = (W - phone_canvas.width) // 2
        py = 875 - phone_canvas.height // 2
        bg.alpha_composite(phone_canvas, (px, py))

        sp_slots = [
            (255, 520, 325, -6.5),
            (825, 520, 325, 6.5),
            (265, 1465, 360, 5.0),
            (815, 1465, 360, -5.0),
        ]
        for s_idx, sp_rel in enumerate(card_spec["sprites"][:4]):
            sp_path = sp_rel if os.path.isabs(sp_rel) else os.path.join(cfg["sprite_dir"], sp_rel)
            sx, sy, sdim, sang = sp_slots[s_idx]
            paste_popout_sprite(bg, sp_path, sx, sy, max_dim=sdim, angle=sang, glow_hex=cfg["accent"])
        paste_floating_chip(bg, card_spec["chip"], W // 2, 1795, cfg["chip_bg"], cfg["accent"])
    else:
        if layout == "hero":
            phone_w, ang = 710, 0.0
            cx, cy = W // 2, 1135
            sp_slots = [
                (175, 1440, 330, -8.0),
                (905, 1440, 330, 8.0),
                (165, 760, 250, -5.0),
                (915, 760, 250, 5.0),
            ]
            chip_xy = (W // 2, 1835)
        elif layout == "left":
            phone_w, ang = 670, -2.4
            cx, cy = 410, 1125
            sp_slots = [
                (855, 770, 340, 7.0),
                (845, 1210, 380, -6.0),
                (820, 1595, 330, 5.0),
                (165, 1615, 260, -7.0),
            ]
            chip_xy = (775, 1815)
        elif layout == "right":
            phone_w, ang = 670, 2.4
            cx, cy = 670, 1125
            sp_slots = [
                (225, 770, 340, -7.0),
                (235, 1210, 380, 6.0),
                (260, 1595, 330, -5.0),
                (915, 1615, 260, 7.0),
            ]
            chip_xy = (305, 1815)
        else:
            phone_w, ang = 700, 0.0
            cx, cy = W // 2, 1135
            sp_slots = [
                (170, 1435, 355, -8.0),
                (910, 1435, 355, 8.0),
                (175, 725, 275, -6.0),
                (905, 725, 275, 6.0),
            ]
            chip_xy = (W // 2, 1835)

        phone_canvas, _ = draw_phone_frame(cap_img, phone_w, radius=44, accent_hex=cfg["accent"])
        if abs(ang) > 0.1:
            phone_canvas = phone_canvas.rotate(ang, resample=Image.Resampling.BICUBIC, expand=True)
        bg.alpha_composite(phone_canvas, (cx - phone_canvas.width // 2, cy - phone_canvas.height // 2))

        for s_idx, sp_rel in enumerate(card_spec["sprites"][:4]):
            sp_path = sp_rel if os.path.isabs(sp_rel) else os.path.join(cfg["sprite_dir"], sp_rel)
            sx, sy, sdim, sang = sp_slots[s_idx]
            paste_popout_sprite(bg, sp_path, sx, sy, max_dim=sdim, angle=sang, glow_hex=cfg["accent"])
        paste_floating_chip(bg, card_spec["chip"], chip_xy[0], chip_xy[1], cfg["chip_bg"], cfg["accent"])

    if card_idx == 1:
        icon_p = os.path.join(assets_root, game, "icon", "icon_512.png")
        if os.path.exists(icon_p):
            ico = Image.open(icon_p).convert("RGBA").resize((132, 132), Image.Resampling.LANCZOS)
            mask = rounded_mask((132, 132), 28)
            badge = Image.new("RGBA", (144, 144), (0, 0, 0, 0))
            ImageDraw.Draw(badge).rounded_rectangle(
                (0, 0, 143, 143), radius=32, fill=(255, 255, 255, 245)
            )
            badge.paste(ico, (6, 6), mask)
            bg.alpha_composite(badge, (60 if is_land else 860, 415 if is_land else 435))

    out_name = f"{slug}_screenshot_{card_idx:02d}.png"
    out_repo = os.path.join(assets_root, game, "screenshots", out_name)
    os.makedirs(os.path.dirname(out_repo), exist_ok=True)
    rgb = bg.convert("RGB")
    rgb.save(out_repo, "PNG", optimize=True)
    mdir = mirror_dir or cfg.get("mirror_dir")
    if mdir:
        os.makedirs(mdir, exist_ok=True)
        shutil.copy2(out_repo, os.path.join(mdir, out_name))
    print(f"  -> {out_name} ({rgb.width}x{rgb.height}, {os.path.getsize(out_repo)} B, land={is_land})")


def main():
    ap = argparse.ArgumentParser(description="Render 8 Twin-Tower 3D ASO screenshots from a JSON config.")
    ap.add_argument("--config", required=True, help="Path to JSON file containing a game config object (or list of objects).")
    ap.add_argument("--assets-root", default=ASSETS_ROOT)
    ap.add_argument("--mirror-dir", default="")
    args = ap.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        data = json.load(f)
    cfgs = data if isinstance(data, list) else [data]
    mdir = args.mirror_dir or None
    for cfg in cfgs:
        print(f"=== Rendering 8 3D ASO screenshots for {cfg['game']} ===")
        for idx, card in enumerate(cfg["cards"], 1):
            build_card(cfg, idx, card, mirror_dir=mdir, assets_root=args.assets_root)


if __name__ == "__main__":
    main()
