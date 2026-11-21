#!/usr/bin/env python3
"""Compose the make.fun news-image entry: a newspaper front page for 21 Nov 2026.
Panels are AI-generated editorial photos; all text is drawn with PIL (crisp, no garble).
Output: entry.png, 1024x1024, must stay under 1 MiB."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

BASE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(BASE, 'panels')
W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (178, 32, 44)
GREY = (90, 86, 76)

SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SERIF_IT = '/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

def crop_fill(im, tw, th):
    """Center-crop to target aspect, then resize."""
    w, h = im.size
    ta, sa = tw / th, w / h
    if sa > ta:
        nw = int(h * ta)
        x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / ta)
        y = (h - nh) // 2
        im = im.crop((0, y, w, y + nh))
    return im.resize((tw, th), Image.LANCZOS)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def main():
    page = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 28  # margin
    right = W - mx

    # --- masthead ---
    f_mast = font(SERIF, 56)
    d.text((W // 2, 26), 'THE WORLD IN ONE PICTURE', font=f_mast, fill=INK, anchor='ma')
    d.line([(mx, 96), (right, 96)], fill=INK, width=3)
    d.line([(mx, 102), (right, 102)], fill=INK, width=1)

    # --- dateline row ---
    f_date = font(SANS_B, 21)
    d.text((mx, 112), 'SATURDAY, 21 NOVEMBER 2026', font=f_date, fill=RED, anchor='la')
    f_tag = font(SANS, 19)
    d.text((right, 113), 'ONE DAY  •  ONE IMAGE', font=f_tag, fill=GREY, anchor='ra')
    d.line([(mx, 146), (right, 146)], fill=INK, width=1)

    # --- headline ---
    f_head = font(SERIF, 47)
    d.text((W // 2, 158), 'THREE LEADERS TALK PEACE,', font=f_head, fill=INK, anchor='ma')
    d.text((W // 2, 210), 'THEN THE MISSILES FLY', font=f_head, fill=INK, anchor='ma')

    # --- hero photo (summit) ---
    hero = Image.open(os.path.join(PANELS, 'media-generation-summit-0-a30a15df-ff14-4a85-9097-45c58f7e1625.webp')).convert('RGB')
    hero = crop_fill(hero, right - mx, 310)
    hero = ImageEnhance.Color(hero).enhance(1.06)
    hero = ImageEnhance.Contrast(hero).enhance(1.03)
    page.paste(hero, (mx, 272))
    d.rectangle([mx, 272, right, 582], outline=INK, width=2)

    # --- hero caption ---
    f_cap = font(SERIF_IT, 20)
    cap = ('SHENZHEN — Trump, Xi and Putin hold the first trilateral summit in history '
           'and sign a peace declaration. Hours later, Russia fires 110+ missiles '
           'and 400 drones at Ukraine.')
    lines = wrap(d, cap, f_cap, right - mx)
    y = 594
    for ln in lines:
        d.text((mx, y), ln, font=f_cap, fill=INK, anchor='la')
        y += 26

    # --- three panels ---
    cols = [
        ('media-generation-kyiv-0-bdec28e1-cd0d-4575-8326-4bc5e3e2e42f.webp',
         'KYIV', 'Bridges hit, power cut',
         'At least 8 killed; three Dnipro bridges hit.'),
        ('media-generation-jets-0-05b838d8-2b13-4cec-9384-32cf18183df9.webp',
         'POLAND', 'Missiles land in NATO state',
         'Russian missiles fall in Poland; NATO jets scramble.'),
        ('media-generation-court-0-31d106e4-d4c6-48f2-97fd-9c99e2ec4b61.webp',
         'THE HAGUE', 'World Court: genocide',
         'ICJ: Myanmar committed genocide on Rohingya.'),
    ]
    gap = 12
    cw = (right - mx - 2 * gap) // 3
    img_h, img_y = 158, 656
    f_kick = font(SANS_B, 19)
    f_sub = font(SANS_B, 17)
    f_body = font(SANS, 16)
    for i, (fn, kick, sub, body) in enumerate(cols):
        x = mx + i * (cw + gap)
        im = Image.open(os.path.join(PANELS, fn)).convert('RGB')
        im = crop_fill(im, cw, img_h)
        im = ImageEnhance.Color(im).enhance(1.05)
        page.paste(im, (x, img_y))
        d.rectangle([x, img_y, x + cw, img_y + img_h], outline=INK, width=2)
        ty = img_y + img_h + 10
        d.text((x, ty), kick, font=f_kick, fill=RED, anchor='la')
        d.text((x, ty + 24), sub, font=f_sub, fill=INK, anchor='la')
        blines = wrap(d, body, f_body, cw)
        by = ty + 48
        for ln in blines:
            d.text((x, by), ln, font=f_body, fill=INK, anchor='la')
            by += 20

    # --- bottom dark strip: markets + more ---
    strip_y, strip_h = 916, 72
    d.rectangle([mx, strip_y, right, strip_y + strip_h], fill=INK)
    f_strip = font(SANS, 17)
    f_strip_b = font(SANS_B, 17)
    s1 = 'MARKETS  ▼  S&P 500 slides into correction as AI stocks plunge'
    s2 = 'GAZA — Four nations urge Israel to let aid reach flooded Gaza  •  CYCLONE AKVAN slams India’s east coast'
    d.text((mx + 14, strip_y + 10), s1, font=f_strip_b, fill=(248, 244, 232), anchor='la')
    d.text((mx + 14, strip_y + 38), s2, font=f_strip, fill=(210, 205, 190), anchor='la')

    # --- footer ---
    f_foot = font(SANS, 13)
    d.text((W // 2, 996), 'Illustrated summary of the world’s news  •  21 November 2026', font=f_foot, fill=GREY, anchor='ma')

    out = os.path.join(BASE, 'entry.png')
    page.save(out, 'PNG', optimize=True, compress_level=9)
    size = os.path.getsize(out)
    print(f'entry.png: {page.size} {size} bytes ({size/1048576:.2f} MiB) limit 1048576')
    if size > 1048576:
        print('OVER LIMIT — needs recompression')

if __name__ == '__main__':
    main()
