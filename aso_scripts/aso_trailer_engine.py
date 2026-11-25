import argparse
import json
import os
import shutil
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_ROOT = os.path.join(REPO_ROOT, "game_store_assets")


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


def hex_rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def font(path, size):
    if path and os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return m


def load_sprite_clean(path, max_dim):
    im = Image.open(path).convert("RGBA")
    r, g, b, a = im.split()
    clean_a = a.point(lambda p: p if p > 24 else 0)
    im.putalpha(clean_a)
    bbox = clean_a.point(lambda p: 255 if p > 24 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    sc = min(max_dim / float(im.width), max_dim / float(im.height))
    return im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.Resampling.LANCZOS)


def _resolve_sprite(cfg, sp_rel):
    if os.path.isabs(sp_rel):
        return sp_rel
    return os.path.join(cfg["sprite_dir"], sp_rel)


def build_backdrop_frame(cfg, w, h, out_path):
    top = hex_rgb(cfg["bg_top"])
    bot = hex_rgb(cfg["bg_bot"])
    orb = hex_rgb(cfg["orb"])
    acc = hex_rgb(cfg["accent"])

    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / float(h - 1)
        px[0, y] = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    bg = strip.resize((w, h), Image.Resampling.BILINEAR).convert("RGBA")

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-220, -180, int(w * 0.72), int(h * 0.55)), fill=orb + (95,))
    gd.ellipse((int(w * 0.3), int(h * 0.45), w + 260, h + 220), fill=acc + (80,))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    bg = Image.alpha_composite(bg, glow)

    sp1 = load_sprite_clean(_resolve_sprite(cfg, cfg["sprites"][0]), 230 if w < h else 270)
    sp2 = load_sprite_clean(_resolve_sprite(cfg, cfg["sprites"][1]), 220 if w < h else 260)
    if w < h:
        bg.alpha_composite(sp1, (36, h - sp1.height - 46))
        bg.alpha_composite(sp2, (w - sp2.width - 36, h - sp2.height - 46))
    else:
        bg.alpha_composite(sp1, (42, h - sp1.height - 38))
        bg.alpha_composite(sp2, (w - sp2.width - 42, h - sp2.height - 38))

    d = ImageDraw.Draw(bg)
    f_title = font(FONT_BLACK, 54 if w < h else 48)
    title = cfg["title"]
    bb = d.textbbox((0, 0), title, font=f_title)
    tw = bb[2] - bb[0]
    tx = (w - tw) // 2 - bb[0] if w < h else 58
    ty = 38
    d.text((tx, ty + 4), title, font=f_title, fill=(0, 0, 0, 175))
    d.text((tx, ty), title, font=f_title, fill=(255, 255, 255, 255))

    f_sub = font(FONT_BOLD, 28 if w < h else 25)
    sub = cfg["tag"]
    bs = d.textbbox((0, 0), sub, font=f_sub)
    sx = (w - (bs[2] - bs[0])) // 2 - bs[0] if w < h else 60
    sy = ty + (bb[3] - bb[1]) + 14
    d.text((sx, sy + 2), sub, font=f_sub, fill=(0, 0, 0, 150))
    d.text((sx, sy), sub, font=f_sub, fill=acc + (245,))

    bg.convert("RGB").save(out_path, "PNG")


def build_callout_png(text, subtext, accent_hex, out_path, max_w=780):
    acc = hex_rgb(accent_hex)
    tmp = Image.new("RGBA", (max_w, 180), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    f1 = font(FONT_BLACK, 42)
    f2 = font(FONT_BOLD, 26)
    b1 = d.textbbox((0, 0), text, font=f1)
    b2 = d.textbbox((0, 0), subtext, font=f2)
    pw = min(max_w - 20, max(b1[2] - b1[0], b2[2] - b2[0]) + 72)
    ph = (b1[3] - b1[1]) + (b2[3] - b2[1]) + 46
    box = Image.new("RGBA", (pw + 24, ph + 24), (0, 0, 0, 0))
    sh = Image.new("RGBA", box.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        (12, 16, 12 + pw, 16 + ph), radius=26, fill=(0, 0, 0, 185)
    )
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    box = Image.alpha_composite(box, sh)
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle(
        (12, 12, 12 + pw, 12 + ph),
        radius=24,
        fill=(14, 22, 38, 240),
        outline=acc + (255,),
        width=4,
    )
    x1 = 12 + (pw - (b1[2] - b1[0])) // 2 - b1[0]
    y1 = 12 + 16 - b1[1]
    bd.text((x1, y1), text, font=f1, fill=(255, 255, 255, 255))
    x2 = 12 + (pw - (b2[2] - b2[0])) // 2 - b2[0]
    y2 = 12 + 28 + (b1[3] - b1[1]) - b2[1]
    bd.text((x2, y2), subtext, font=f2, fill=acc + (255,))
    box.save(out_path, "PNG")


def build_endcard(cfg, w, h, out_path, assets_root=None):
    assets_root = assets_root or cfg.get("assets_root") or ASSETS_ROOT
    top = hex_rgb(cfg["bg_top"])
    bot = hex_rgb(cfg["bg_bot"])
    acc = hex_rgb(cfg["accent"])
    orb = hex_rgb(cfg["orb"])

    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / float(h - 1)
        px[0, y] = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    bg = strip.resize((w, h), Image.Resampling.BILINEAR).convert("RGBA")

    banner_p = os.path.join(assets_root, cfg["game"], "feature_graphic", "feature_graphic_1024x500.png")
    if os.path.exists(banner_p):
        bn = Image.open(banner_p).convert("RGBA")
        bw = min(w - 100, 960 if w < h else 1020)
        bh = int(bw * 500 / 1024.0)
        bn = bn.resize((bw, bh), Image.Resampling.LANCZOS)
        bmask = rounded_mask((bw, bh), 34)
        by = 190 if w < h else 85
        bx = (w - bw) // 2
        frame = Image.new("RGBA", (bw + 16, bh + 16), (0, 0, 0, 0))
        ImageDraw.Draw(frame).rounded_rectangle(
            (0, 0, bw + 15, bh + 15), radius=38, fill=acc + (220,)
        )
        bg.alpha_composite(frame, (bx - 8, by - 8))
        bg.paste(bn, (bx, by), bmask)

    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    icy = int(h * 0.49) if w < h else int(h * 0.56)
    ImageDraw.Draw(gl).ellipse((w // 2 - 260, icy - 260, w // 2 + 260, icy + 260), fill=orb + (130,))
    gl = gl.filter(ImageFilter.GaussianBlur(70))
    bg = Image.alpha_composite(bg, gl)

    icon_p = os.path.join(assets_root, cfg["game"], "icon", "icon_512.png")
    ico = Image.open(icon_p).convert("RGBA").resize((240, 240), Image.Resampling.LANCZOS)
    imask = rounded_mask((240, 240), 52)
    holder = Image.new("RGBA", (264, 264), (0, 0, 0, 0))
    ImageDraw.Draw(holder).rounded_rectangle((0, 0, 263, 263), radius=58, fill=(255, 255, 255, 255))
    holder.paste(ico, (12, 12), imask)
    bg.alpha_composite(holder, (w // 2 - 132, icy - 132))

    sp1 = load_sprite_clean(_resolve_sprite(cfg, cfg["sprites"][0]), 260)
    sp2 = load_sprite_clean(_resolve_sprite(cfg, cfg["sprites"][1]), 260)
    bg.alpha_composite(sp1, (max(24, w // 2 - 420), icy - sp1.height // 2))
    bg.alpha_composite(sp2, (min(w - sp2.width - 24, w // 2 + 160), icy - sp2.height // 2))

    d = ImageDraw.Draw(bg)
    f_big = font(FONT_BLACK, 64)
    bb = d.textbbox((0, 0), cfg["title"], font=f_big)
    tx = (w - (bb[2] - bb[0])) // 2 - bb[0]
    ty = icy + 165
    d.text((tx, ty + 4), cfg["title"], font=f_big, fill=(0, 0, 0, 180))
    d.text((tx, ty), cfg["title"], font=f_big, fill=(255, 255, 255, 255))

    cta = "GET IT ON GOOGLE PLAY  •  FREE OFFLINE"
    f_cta = font(FONT_BLACK, 32)
    bc = d.textbbox((0, 0), cta, font=f_cta)
    cw, ch = (bc[2] - bc[0]) + 84, (bc[3] - bc[1]) + 42
    cx = (w - cw) // 2
    cy = ty + (bb[3] - bb[1]) + 42
    d.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=ch // 2, fill=(17, 138, 76, 255), outline=(255, 255, 255, 240), width=4)
    ctx = cx + (cw - (bc[2] - bc[0])) // 2 - bc[0]
    cty = cy + (ch - (bc[3] - bc[1])) // 2 - bc[1] - 2
    d.text((ctx, cty), cta, font=f_cta, fill=(255, 255, 255, 255))

    bg.convert("RGB").save(out_path, "PNG")


def build_inset_panel(cap_path, w_target, accent_hex, out_path):
    im = Image.open(cap_path).convert("RGBA")
    h_target = int(round(w_target * im.height / float(im.width)))
    im = im.resize((w_target, h_target), Image.Resampling.LANCZOS)
    mask = rounded_mask((w_target, h_target), 22)
    panel = Image.new("RGBA", (w_target + 12, h_target + 12), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle(
        (0, 0, w_target + 11, h_target + 11),
        radius=26,
        fill=hex_rgb(accent_hex) + (235,),
    )
    panel.paste(im, (6, 6), mask)
    panel.save(out_path, "PNG")
    return panel.size


def _resolve_audio(cfg, rel_or_abs):
    if os.path.isabs(rel_or_abs):
        return rel_or_abs
    repo_dir = cfg.get("repo_dir", "")
    cand1 = os.path.join(repo_dir, rel_or_abs) if repo_dir else rel_or_abs
    if os.path.exists(cand1):
        return cand1
    if repo_dir:
        cand2 = os.path.join(repo_dir, "assets", "audio", rel_or_abs)
        if os.path.exists(cand2):
            return cand2
    return cand1


def build_audio_mix(cfg, out_wav):
    bgm = _resolve_audio(cfg, cfg["bgm"])
    if not os.path.exists(bgm):
        raise FileNotFoundError(f"Missing BGM: {bgm}")

    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", bgm]
    sfx_inputs = []
    for delay_ms, sfx_rel in cfg.get("sfx", []):
        sp = _resolve_audio(cfg, sfx_rel)
        if os.path.exists(sp):
            cmd.extend(["-i", sp])
            sfx_inputs.append((len(sfx_inputs) + 1, delay_ms))

    fc_parts = ["[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=0.45,atrim=0:17.5[bgm]"]
    mix_labels = ["[bgm]"]
    for idx, dms in sfx_inputs:
        lbl = f"[s{idx}]"
        fc_parts.append(
            f"[{idx}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,adelay={dms}|{dms},volume=1.15{lbl}"
        )
        mix_labels.append(lbl)

    n = len(mix_labels)
    fc_parts.append(
        "".join(mix_labels)
        + f"amix=inputs={n}:duration=longest:dropout_transition=0:normalize=0,atrim=0:17.5,afade=t=in:st=0:d=0.35,afade=t=out:st=16.4:d=1.1,alimiter=limit=0.92[aout]"
    )
    cmd.extend(["-filter_complex", ";".join(fc_parts), "-map", "[aout]", "-t", "17.5", out_wav])
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def render_variant(cfg, variant, tmp_dir, audio_wav, mirror_dir=None, assets_root=None):
    assets_root = assets_root or cfg.get("assets_root") or ASSETS_ROOT
    is_port = variant == "portrait"
    W, H = (1080, 1920) if is_port else (1920, 1080)
    bg_p = os.path.join(tmp_dir, f"bg_{variant}.png")
    end_p = os.path.join(tmp_dir, f"end_{variant}.png")
    ins_p = os.path.join(tmp_dir, f"inset_{variant}.png")
    build_backdrop_frame(cfg, W, H, bg_p)
    build_endcard(cfg, W, H, end_p, assets_root=assets_root)

    inset_cap = os.path.join(assets_root, cfg["game"], "raw_captures", cfg["inset_cap"])
    iw_req = (210 if cfg["src_landscape"] else 176) if is_port else (260 if cfg["src_landscape"] else 230)
    iw, ih = build_inset_panel(inset_cap, iw_req, cfg["accent"], ins_p)

    c_paths = []
    c_max_w = (720 if cfg["src_landscape"] else 760) if is_port else (880 if cfg["src_landscape"] else 590)
    for i, (t0, t1, ctitle, csub) in enumerate(cfg["callouts"], 1):
        cp = os.path.join(tmp_dir, f"c_{variant}_{i}.png")
        build_callout_png(ctitle, csub, cfg["accent"], cp, max_w=c_max_w)
        c_paths.append((cp, t0, t1))

    cmd = ["ffmpeg", "-y"]
    if cfg.get("video_type", "mp4") == "frames":
        cmd.extend(["-framerate", str(cfg["framerate"]), "-i", cfg["video_src"]])
        vin = "[0:v]"
        trim_f = "fps=30,setpts=PTS-STARTPTS"
    else:
        cmd.extend(["-ss", str(cfg.get("trim_start", 0.2)), "-t", "14.0", "-i", cfg["video_src"]])
        vin = "[0:v]"
        trim_f = "fps=30,setpts=PTS-STARTPTS"

    cmd.extend(["-loop", "1", "-t", "14.0", "-i", bg_p])
    cmd.extend(["-loop", "1", "-t", "3.5", "-i", end_p])
    cmd.extend(["-loop", "1", "-t", "14.0", "-i", ins_p])
    for cp, _, _ in c_paths:
        cmd.extend(["-loop", "1", "-t", "14.0", "-i", cp])
    cmd.extend(["-i", audio_wav])

    is_land_src = cfg["src_landscape"]
    if is_port:
        if is_land_src:
            box_w, box_h, bx, by = 1004, 492, 38, 560
            inset_xy = (W - iw - 38, 1140)
            call_xy = ("38", "1240")
        else:
            box_w, box_h, bx, by = 780, 1260, 150, 176
            inset_xy = (W - iw - 34, min(H - ih - 24, 1485))
            call_xy = ("40", "1585")
    else:
        if is_land_src:
            box_w, box_h, bx, by = 1340, 604, 54, 206
            inset_xy = (1570, 210)
            call_xy = ("355", "865")
        else:
            box_w, box_h, bx, by = 540, 960, 690, 60
            inset_xy = (1610, 60)
            call_xy = ("54", "780")

    fc = [
        f"{vin}{trim_f},setsar=1,scale=w={box_w}:h={box_h}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
        f"pad=w=max(iw\\,{box_w}):h=max(ih\\,{box_h}):x=(ow-iw)/2:y=(oh-ih)/2:color=#0B101C,tpad=stop_mode=clone:stop_duration=2[game]",
        f"[1:v]scale={W}:{H},format=rgba[bg]",
        f"[bg][game]overlay={bx}:{by}:shortest=1[s0]",
        f"[s0][3:v]overlay={inset_xy[0]}:{inset_xy[1]}:enable='between(t,1.2,13.5)'[s1]",
    ]
    prev = "[s1]"
    for idx, (_, t0, t1) in enumerate(c_paths, start=4):
        nxt = f"[sc{idx}]"
        fc.append(f"{prev}[{idx}:v]overlay={call_xy[0]}:{call_xy[1]}:enable='between(t,{t0},{t1})'{nxt}")
        prev = nxt
    fc.append(f"{prev}trim=0:14.0,setpts=PTS-STARTPTS,format=yuv420p[main14]")
    fc.append(f"[2:v]scale={W}:{H},fps=30,trim=0:3.5,setpts=PTS-STARTPTS,format=yuv420p[end35]")
    fc.append("[main14][end35]concat=n=2:v=1:a=0,format=yuv420p[vout]")

    slug = cfg["slug"]
    tag = "portrait_9x16" if is_port else "landscape_16x9"
    out_name = f"{slug}_trailer_{tag}.mp4"
    out_repo = os.path.join(assets_root, cfg["game"], "videos", out_name)
    os.makedirs(os.path.dirname(out_repo), exist_ok=True)

    cmd.extend([
        "-filter_complex", ";".join(fc),
        "-map", "[vout]",
        "-map", f"{4 + len(c_paths)}:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart", "-t", "17.5", out_repo
    ])
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mdir = mirror_dir or cfg.get("mirror_dir")
    if mdir:
        os.makedirs(mdir, exist_ok=True)
        shutil.copy2(out_repo, os.path.join(mdir, out_name))
    print(f"  -> {out_name} ({W}x{H}, {os.path.getsize(out_repo)} B)")


def render_game_trailers(cfg, mirror_dir=None, assets_root=None):
    tmp = tempfile.mkdtemp(prefix=f"aso_{cfg['slug']}_")
    try:
        awav = os.path.join(tmp, "mix.wav")
        build_audio_mix(cfg, awav)
        render_variant(cfg, "portrait", tmp, awav, mirror_dir=mirror_dir, assets_root=assets_root)
        render_variant(cfg, "landscape", tmp, awav, mirror_dir=mirror_dir, assets_root=assets_root)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="Render 9:16 & 16:9 Full HD trailers with synced BGM/SFX and Google Play endcard.")
    ap.add_argument("--config", required=True, help="Path to JSON file containing a game trailer config object (or list).")
    ap.add_argument("--assets-root", default=ASSETS_ROOT)
    ap.add_argument("--mirror-dir", default="")
    args = ap.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        data = json.load(f)
    cfgs = data if isinstance(data, list) else [data]
    mdir = args.mirror_dir or None
    for cfg in cfgs:
        print(f"=== Rendering 9:16 & 16:9 Full HD trailers for {cfg['game']} ===")
        render_game_trailers(cfg, mirror_dir=mdir, assets_root=args.assets_root)


if __name__ == "__main__":
    main()
