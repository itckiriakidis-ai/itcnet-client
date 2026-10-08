#!/usr/bin/env python3
"""ITCNET branding for the RustDesk source tree.

Run from the repository root:
    python3 branding/apply_branding.py
Optional environment variables (fill in when the ITCNET server is ready):
    ITCNET_SERVER  host or IP of the ID/relay server (hbbs/hbbr)
    ITCNET_KEY     public key of that server (contents of id_ed25519.pub)
    ITCNET_FONT    path to a bold .ttf used for the wordmark in the logo

ITCNET is based on RustDesk (https://github.com/rustdesk/rustdesk),
licensed under AGPL-3.0. This script only changes branding and defaults.
"""
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "branding"

APP_NAME = "ITCNET"
DESCRIPTION = "ITCNET Remote Support - I.T. Center KiriakidiS"
COPYRIGHT = ("ITCNET by I.T. Center KiriakidiS. Based on RustDesk "
             "(c) Purslane Tech Pte. Ltd., AGPL-3.0")
RED = "E81820"
DARK = "484848"

SERVER = os.environ.get("ITCNET_SERVER", "").strip()
KEY = os.environ.get("ITCNET_KEY", "").strip()


def edit(path, pairs, required=True):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if isinstance(old, re.Pattern):
            s2 = old.sub(new, s)
        else:
            s2 = s.replace(old, new)
        if s2 == s and required:
            already = (not isinstance(old, re.Pattern) and new in s) or \
                      (isinstance(old, re.Pattern) and new in s)
            if not already:
                sys.exit(f"pattern not found in {path}: {old}")
        s = s2
    p.write_text(s, encoding="utf-8")
    print("edited", path)


# ---------- icons ----------
def icons():
    from PIL import Image
    src = Image.open(B / "icon-1024.png").convert("RGBA")

    def png(size, path):
        out = ROOT / path
        out.parent.mkdir(parents=True, exist_ok=True)
        src.resize((size, size), Image.LANCZOS).save(out)

    png(1024, "res/icon.png")
    png(1024, "res/mac-icon.png")
    png(32, "res/32x32.png")
    png(64, "res/64x64.png")
    png(128, "res/128x128.png")
    png(256, "res/128x128@2x.png")
    png(256, "flutter/assets/icon.png")

    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    src.save(ROOT / "res/icon.ico", sizes=ico_sizes)
    src.save(ROOT / "flutter/windows/runner/resources/app_icon.ico", sizes=ico_sizes)
    src.save(ROOT / "res/tray-icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48)])

    # Android launcher icons
    dens = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    for d, s in dens.items():
        base = ROOT / f"flutter/android/app/src/main/res/mipmap-{d}"
        if not base.exists():
            continue
        for name in ("ic_launcher.png", "ic_launcher_round.png"):
            if (base / name).exists():
                bg = Image.new("RGBA", (s, s), (255, 255, 255, 255))
                inner = int(s * 0.8)
                bg.alpha_composite(src.resize((inner, inner), Image.LANCZOS),
                                   ((s - inner) // 2, (s - inner) // 2))
                bg.save(base / name)
        fg = base / "ic_launcher_foreground.png"
        if fg.exists():
            fs = Image.open(fg).size[0]
            canvas = Image.new("RGBA", (fs, fs), (0, 0, 0, 0))
            inner = int(fs * 0.5)  # adaptive icon safe zone
            canvas.alpha_composite(src.resize((inner, inner), Image.LANCZOS),
                                   ((fs - inner) // 2, (fs - inner) // 2))
            canvas.save(fg)
    print("icons generated")


# ---------- logo (max 300x60) ----------
def logos():
    from PIL import Image, ImageDraw, ImageFont
    font_path = os.environ.get("ITCNET_FONT") or str(B / "Poppins-Bold.ttf")
    try:
        font = ImageFont.truetype(font_path, 88)
    except OSError:
        font = ImageFont.load_default()
    icon = Image.open(B / "icon-1024.png").convert("RGBA").resize((112, 112), Image.LANCZOS)
    for name, color in (("logo_light.png", "#" + DARK), ("logo_dark.png", "#FFFFFF")):
        W, H = 600, 120
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        im.alpha_composite(icon, (0, 4))
        d = ImageDraw.Draw(im)
        x = 132
        d.text((x, 60), "ITC", font=font, fill="#" + RED, anchor="lm")
        x += d.textlength("ITC", font=font)
        d.text((x, 60), "NET", font=font, fill=color, anchor="lm")
        bbox = im.getbbox()
        im = im.crop((0, 0, bbox[2] + 4, H))
        im.save(ROOT / "flutter/assets" / name)
    # default logo = light version
    Image.open(ROOT / "flutter/assets/logo_light.png").save(ROOT / "flutter/assets/logo.png")
    print("logos generated")


# ---------- names, colors, defaults ----------
def code():
    edit("libs/hbb_common/src/config.rs", [
        ('RwLock::new("RustDesk".to_owned())', f'RwLock::new("{APP_NAME}".to_owned())'),
    ])
    if SERVER and KEY:
        edit("libs/hbb_common/src/config.rs", [
            (re.compile(r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];'),
             f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];'),
            (re.compile(r'pub const RS_PUB_KEY: &str = "[^"]*";'),
             f'pub const RS_PUB_KEY: &str = "{KEY}";'),
        ])
    else:
        print("ITCNET_SERVER / ITCNET_KEY not set: server defaults left unchanged")

    edit("Cargo.toml", [
        ('ProductName = "RustDesk"', f'ProductName = "{APP_NAME}"'),
        ('FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{DESCRIPTION}"'),
        (re.compile(r'LegalCopyright = "[^"]*"'), f'LegalCopyright = "{COPYRIGHT}"'),
        ('[package.metadata.bundle]\nname = "RustDesk"', f'[package.metadata.bundle]\nname = "{APP_NAME}"'),
    ])
    edit("flutter/windows/runner/Runner.rc", [
        ('"RustDesk Remote Desktop"', f'"{DESCRIPTION}"'),
        ('VALUE "ProductName", "RustDesk"', f'VALUE "ProductName", "{APP_NAME}"'),
    ])
    edit("flutter/windows/runner/main.cpp", [
        ('std::wstring app_name = L"RustDesk";', f'std::wstring app_name = L"{APP_NAME}";'),
    ])
    edit("flutter/lib/common.dart", [
        ("static const Color accent = Color(0xFF0071FF);", f"static const Color accent = Color(0xFF{RED});"),
        ("static const Color accent50 = Color(0x770071FF);", f"static const Color accent50 = Color(0x77{RED});"),
        ("static const Color accent80 = Color(0xAA0071FF);", f"static const Color accent80 = Color(0xAA{RED});"),
        ("static const Color button = Color(0xFF2C8CFF);", f"static const Color button = Color(0xFF{RED});"),
    ])


if __name__ == "__main__":
    # --code-only: used by the CI build (the icons/logos are already committed,
    # but libs/hbb_common is a submodule and must be patched at build time)
    if "--code-only" not in sys.argv:
        icons()
        logos()
    code()
    print("ITCNET branding applied")
