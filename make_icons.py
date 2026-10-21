from PIL import Image, ImageDraw
import math, os

def draw_icon(size):
    S = size * 4  # supersample
    img = Image.new("RGBA", (S, S), "#102b29")
    d = ImageDraw.Draw(img)
    # solid soft disc behind the card
    d.ellipse((S*0.12, S*0.12, S*0.88, S*0.88), fill='#173b37')
    # card (inside the maskable safe zone: central ~70%)
    cw, ch = S * 0.40, S * 0.56
    card = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    x0, y0 = S/2 - cw/2, S/2 - ch/2
    cd.rounded_rectangle((x0 + S*0.012, y0 + S*0.02, x0 + cw + S*0.012, y0 + ch + S*0.02), radius=S*0.05, fill="#967a4c")
    cd.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=S*0.05, fill="#ffefd4", outline="#fff6d0", width=int(S*0.008))
    # evil-eye motif
    cx, cy = S/2, S/2
    for r, col in [(0.150, "#f5c96a"), (0.115, "#ffefd4"), (0.085, "#78c7c0"), (0.045, "#153631")]:
        cd.ellipse((cx - S*r, cy - S*r, cx + S*r, cy + S*r), fill=col)
    # corner pips
    for dx, dy in [(-1, -1), (1, 1)]:
        px, py = cx + dx * cw * 0.34, cy + dy * ch * 0.38
        cd.ellipse((px - S*0.022, py - S*0.022, px + S*0.022, py + S*0.022), fill="#173b37")
    card = card.rotate(-8, resample=Image.BICUBIC, center=(S/2, S/2))
    img = Image.alpha_composite(img, card)
    return img.resize((size, size), Image.LANCZOS).convert("RGB")

os.makedirs("icons", exist_ok=True)
for name, size in [("icon-192.png", 192), ("icon-512.png", 512), ("icon-maskable-512.png", 512), ("icon-180.png", 180)]:
    draw_icon(size).save(os.path.join("icons", name), optimize=True)
print(sorted(os.listdir("icons")))
