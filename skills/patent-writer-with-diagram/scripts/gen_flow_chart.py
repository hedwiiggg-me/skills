#!/usr/bin/env python3
"""Generate a clean interaction flow diagram PNG for the patent document."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 420
BG = (255, 255, 255)
HEADER_BG = (70, 130, 180)   # steel blue
HEADER_FG = (255, 255, 255)
BOX_BG = (240, 248, 255)     # alice blue
BOX_BORDER = (70, 130, 180)
ARROW_COLOR = (100, 100, 100)
TEXT_COLOR = (30, 30, 30)
TITLE_COLOR = (50, 50, 50)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Try to load a CJK font
font_paths = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode MS.ttf",
]
font_sm = font_lg = font_hd = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_sm = ImageFont.truetype(fp, 18)
            font_lg = ImageFont.truetype(fp, 20)
            font_hd = ImageFont.truetype(fp, 22)
            break
        except Exception:
            continue
if font_sm is None:
    font_sm = font_lg = font_hd = ImageFont.load_default()

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_rounded_rect(draw, xy, radius=10, fill=None, outline=None, width=2):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, x0, y0, x1, y1, color=ARROW_COLOR):
    draw.line([(x0, y0), (x1, y1)], fill=color, width=2)
    # arrowhead
    draw.polygon([(x1, y1), (x1-10, y1-6), (x1-10, y1+6)], fill=color)

def draw_flow_row(draw, y_top, steps, row_h=80, margin=40):
    """Draw a row of steps with arrows between them."""
    n = len(steps)
    total_w = W - 2 * margin
    arrow_w = 50
    box_w = (total_w - arrow_w * (n - 1)) // n
    x = margin
    for i, step in enumerate(steps):
        bx0, by0, bx1, by1 = x, y_top, x + box_w, y_top + row_h
        draw_rounded_rect(draw, (bx0, by0, bx1, by1), radius=8, fill=BOX_BG, outline=BOX_BORDER, width=2)
        tw, th = text_size(draw, step, font_lg)
        # wrap if needed
        lines = []
        words = list(step)
        line = ""
        for ch in step:
            test = line + ch
            tw2, _ = text_size(draw, test, font_lg)
            if tw2 > box_w - 16:
                lines.append(line)
                line = ch
            else:
                line = test
        if line:
            lines.append(line)
        total_th = len(lines) * (th + 4)
        ty = y_top + (row_h - total_th) // 2
        for ln in lines:
            lw, lh = text_size(draw, ln, font_lg)
            draw.text((bx0 + (box_w - lw) // 2, ty), ln, font=font_lg, fill=TEXT_COLOR)
            ty += lh + 4
        x += box_w
        if i < n - 1:
            ax0 = x + 5
            ax1 = x + arrow_w - 5
            ay = y_top + row_h // 2
            draw_arrow(draw, ax0, ay, ax1, ay)
            x += arrow_w

# ── Scene 1 header ──
s1_header_y = 20
draw_rounded_rect(draw, (40, s1_header_y, W-40, s1_header_y+40), radius=6, fill=HEADER_BG)
title1 = "场景1：input 吸顶交互流程"
tw, th = text_size(draw, title1, font_hd)
draw.text(((W - tw) // 2, s1_header_y + (40 - th) // 2), title1, font=font_hd, fill=HEADER_FG)

steps1 = ["用户向下滚动", "input 滚出视口顶部", "input 吸顶固定展示", "问答对应关系清晰"]
draw_flow_row(draw, s1_header_y + 50, steps1, row_h=80)

# ── Scene 2 header ──
s2_header_y = 210
draw_rounded_rect(draw, (40, s2_header_y, W-40, s2_header_y+40), radius=6, fill=HEADER_BG)
title2 = "场景2：hover 停止按钮交互流程"
tw, th = text_size(draw, title2, font_hd)
draw.text(((W - tw) // 2, s2_header_y + (40 - th) // 2), title2, font=font_hd, fill=HEADER_FG)

steps2 = ["hover 吸顶 input", "显示「停止回答」按钮", "点击停止按钮", "回答生成中止"]
draw_flow_row(draw, s2_header_y + 50, steps2, row_h=80)

# ── Footer note ──
note = "交互框架图"
nw, nh = text_size(draw, note, font_sm)
draw.text(((W - nw) // 2, H - nh - 10), note, font=font_sm, fill=(160, 160, 160))

out = "/tmp/flow_chart.png"
img.save(out, "PNG")
print(f"Saved: {out}  ({W}x{H})")
