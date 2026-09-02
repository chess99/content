from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\code\content\topics\20260902-cat-teacher-chatgpt-migration")
OUT = ROOT / "image-post" / "images"
MARK = ROOT / "image-post" / "source" / "model-generated" / "cat-teacher-ip-v2-transparent.png"
W, H = 1080, 1440

PAPER = "#FAF9F6"
INK = "#171717"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"


def render_cover():
    cover = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(cover)

    mark = Image.open(MARK).convert("RGBA")
    alpha_box = mark.getchannel("A").getbbox()
    mark = mark.crop(alpha_box)
    mark.thumbnail((310, 310), Image.Resampling.LANCZOS)
    mark_x = (W - mark.width) // 2
    cover.paste(mark, (mark_x, 230), mark)

    title_font = ImageFont.truetype(FONT_BOLD, 76)
    lines = ["ChatGPT 现在可能", "比我自己还了解我了"]
    y = 700
    for line in lines:
        box = draw.textbbox((0, 0), line, font=title_font)
        line_width = box[2] - box[0]
        draw.text(((W - line_width) // 2, y), line, fill=INK, font=title_font)
        y += 126

    OUT.mkdir(parents=True, exist_ok=True)
    cover.save(OUT / "01-chatgpt-knows-me.png")


if __name__ == "__main__":
    render_cover()
