from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"D:\code\content\topics\20260902-cat-teacher-chatgpt-migration")
OUT = ROOT / "image-post" / "images"
SHARED = ROOT / "shared"
W, H = 1080, 1440

PAPER = "#FAF9F6"
INK = "#171717"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255
    )
    return mask


def screenshot_block(base, source, crop_box, box, radius=18):
    """把真实截图完整装进指定区域，不拉伸、不二次裁掉文字。"""
    x1, y1, x2, y2 = box
    target_w, target_h = x2 - x1, y2 - y1
    crop = source.crop(crop_box)
    scale = min(target_w / crop.width, target_h / crop.height)
    crop = crop.resize(
        (round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS
    )

    block = Image.new("RGB", (target_w, target_h), "#FFFFFF")
    left = (target_w - crop.width) // 2
    top = (target_h - crop.height) // 2
    block.paste(crop, (left, top))

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_mask = Image.new("L", (target_w + 36, target_h + 36), 0)
    ImageDraw.Draw(shadow_mask).rounded_rectangle(
        (18, 18, target_w + 17, target_h + 17), radius=radius, fill=45
    )
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(13))
    shadow.paste((0, 0, 0, 60), (x1 - 18, y1 - 10), shadow_mask)
    base.paste(shadow, (0, 0), shadow)
    base.paste(block, (x1, y1), rounded_mask((target_w, target_h), radius))


def page1():
    im = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(im)

    # 整句话保持同一字号、同一字重，不把 ChatGPT 降成不显眼的小前缀。
    lines = ["ChatGPT 现在可能", "比我自己还了解我了"]
    f = font(76)
    y = 590
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f)
        width = bbox[2] - bbox[0]
        draw.text(((W - width) // 2, y), line, fill=INK, font=f)
        y += 126

    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / "01-chatgpt-knows-me.png")


def page2():
    im = Image.new("RGB", (W, H), "#F1F1EF")

    settings = Image.open(SHARED / "chatgpt-project-settings.png").convert("RGB")
    sources = Image.open(SHARED / "chatgpt-sources.png").convert("RGB")
    result = Image.open(SHARED / "chatgpt-diary-analysis.png").convert("RGB")

    # 上面两块是真实配置：项目设置，以及 2016—2026 日记资料库。
    screenshot_block(im, settings, (690, 350, 1510, 1197), (42, 320, 526, 820))
    screenshot_block(im, sources, (690, 360, 1890, 1600), (554, 320, 1038, 820))

    # 下面一块是真实效果：猫猫老师跨年份读出“长期变量”的原始回复。
    screenshot_block(im, result, (665, 500, 2100, 810), (42, 870, 1038, 1085))

    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / "02-how-it-works.png")


if __name__ == "__main__":
    page1()
    page2()
