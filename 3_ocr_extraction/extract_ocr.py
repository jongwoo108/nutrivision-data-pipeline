import os
from pathlib import Path
import pytesseract
from PIL import Image

# Tesseract 경로
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IN_DIRS = [
    Path("../2_preprocessing/processed"),           # 전처리된 이미지가 있으면 이 폴더 우선
    Path("../1_data_collection/assets/raw_images"), # 없으면 원본으로 시도
]
OUT_DIR = Path("./ocr_results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CONFIG = (
    '--oem 1 '
    '--psm 6 '
    '-c preserve_interword_spaces=1 '
    '-c load_system_dawg=0 -c load_freq_dawg=0'
)

LANG = "kor+eng"
VALID_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}

def list_images(folder: Path):
    if not folder.exists():
        return []
    return [p for p in folder.iterdir() if p.suffix.lower() in VALID_EXT]

def main(force: bool = False):
    images = []
    chosen = None
    for d in IN_DIRS:
        images = list_images(d)
        if images:
            chosen = d
            break

    if not images:
        print("[WARN] No images found in processed or raw_images.")
        return

    print(f"[INFO] Using input dir: {chosen.resolve()} ({len(images)} files)")
    skipped = 0
    processed = 0

    for img_path in images:
        out_txt = OUT_DIR / (img_path.stem + ".txt")

        # 이미 OCR된 파일이 있으면 스킵
        if out_txt.exists() and not force:
            print(f"[SKIP] {out_txt.name} already exists.")
            skipped += 1
            continue

        try:
            with Image.open(img_path) as im:
                text = pytesseract.image_to_string(im, lang=LANG, config=CONFIG)

            out_txt.write_text(text, encoding="utf-8")
            processed += 1
            print(f"[OK] {img_path.name} → {out_txt.name} ({len(text)} chars)")
        except Exception as e:
            print(f"[ERR] {img_path.name}: {e}")

    print(f"[DONE] processed={processed}, skipped={skipped}")


if __name__ == "__main__":   
    # 필요 시 전체 재처리하려면 아래를 True로 변경하거나 argparse로 받아도 됩니다.
    main(force=True)
