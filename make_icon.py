from PIL import Image, ImageDraw, ImageFont

def make_icon(size):
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 背景 (深藍)
    d.rectangle([0, 0, s, s], fill="#1A3A6B")

    # 粗體 "E" 字 (白色，直接畫在目標尺寸，邊緣最清晰)
    t = max(2, int(s * 0.12))
    px = int(s * 0.20)
    py = int(s * 0.16)
    pw = int(s * 0.60)
    ph = int(s * 0.68)

    d.rectangle([px, py, px + t, py + ph], fill="white")           # 左豎
    d.rectangle([px, py, px + pw, py + t], fill="white")           # 上橫
    my = py + ph // 2 - t // 2
    d.rectangle([px, my, px + int(pw * 0.80), my + t], fill="white")  # 中橫
    d.rectangle([px, py + ph - t, px + pw, py + ph], fill="white") # 下橫

    return img


img256 = make_icon(256)
img256.save("icon.ico", format="ICO",
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("icon.ico created")
