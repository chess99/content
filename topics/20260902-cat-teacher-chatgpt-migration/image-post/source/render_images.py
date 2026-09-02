from pathlib import Path

from PIL import Image


ROOT = Path(r"D:\code\content\topics\20260902-cat-teacher-chatgpt-migration")
OUT = ROOT / "image-post" / "images"
SOURCE = ROOT / "image-post" / "source"
MODEL_COVER = SOURCE / "model-generated" / "cover-integrated-v1.png"
W, H = 1080, 1440

def render_cover():
    cover = Image.open(MODEL_COVER).convert("RGB")
    cover = cover.resize((W, H), Image.Resampling.LANCZOS)
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
