from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\code\content\topics\20260902-cat-teacher-chatgpt-migration")
OUT = ROOT / "image-post" / "images"
SOURCE = ROOT / "image-post" / "source"
MARK = ROOT / "image-post" / "source" / "model-generated" / "cat-teacher-ip-cute-v1.png"
W, H = 1080, 1440

PAPER = "#FAF9F6"
INK = "#171717"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"


def render_cover():
    cover = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(cover)

    title_font = ImageFont.truetype(FONT_BOLD, 100)
    lines = ["ChatGPT 现在可能", "比我自己还了解我了"]
    title_x = 76
    title_y = 430
    line_gap = 44
    line_height = title_font.getbbox("猫")[3] - title_font.getbbox("猫")[1]

    for index, line in enumerate(lines):
        y = title_y + index * (line_height + line_gap)
        draw.text((title_x, y), line, fill=INK, font=title_font)

    ledge_y = title_y + 2 * line_height + line_gap + 94

    mark = Image.open(MARK).convert("RGBA")
    alpha_box = mark.getchannel("A").getbbox()
    mark = mark.crop(alpha_box)
    mark.thumbnail((215, 215), Image.Resampling.LANCZOS)
    mark = mark.rotate(-8, resample=Image.Resampling.BICUBIC, expand=True)
    cover.paste(mark, (808, ledge_y - 132), mark)

    OUT.mkdir(parents=True, exist_ok=True)
    cover.save(OUT / "01-chatgpt-knows-me.png")


def render_qa_contact_sheet():
    paths = [
        OUT / "01-chatgpt-knows-me.png",
        OUT / "02-project-settings.png",
        OUT / "03-sources.png",
        OUT / "04-diary-analysis.png",
    ]
    sheet = Image.new("RGB", (1180, 400), "#D8D6D1")
    cell_w, cell_h = 270, 360
    for index, path in enumerate(paths):
        image = Image.open(path).convert("RGB")
        image.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = 20 + index * 290 + (cell_w - image.width) // 2
        y = 20 + (cell_h - image.height) // 2
        sheet.paste(image, (x, y))
    sheet.save(SOURCE / "qa-contact-sheet.png")


if __name__ == "__main__":
    render_cover()
    render_qa_contact_sheet()
