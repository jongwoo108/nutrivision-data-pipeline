import os
from pathlib import Path
import pytesseract
from PIL import Image

# ⚠️ Tesseract 경로가 기본 PATH에 없다면 주석 해제하고 본인 경로로 설정
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IN_DIR = [
    Path("../2_preprocessing/processed"),
    Path("../1_data_collection/assets/raw_images"),
]
OUT_DIR = Path("./ocr_results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CONFIG = "--oem 3 --psm 6"
LANG = "kor+eng"

def list_images(folder: Path):
    if not folder.exists():
        return []
    return [p for p in folder.iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"]]

def main():
    images = []
    for d in IN_DIR:
        images = list_images(d)
        if images:
            print(f"[INFO] Using input dir: {d.resolve()} ({len(images)} files)")
            break
    if not images:
        print("[WARN] No images found in processed or raw_images.")
        return
    
    for img_path in images:
        try:
            text = pytesseract.image_to_string(Image.open(img_path), lang=LANG, config=CONFIG)
            out_txt = OUT_DIR / (img_path.stem + ".txt")
            out_txt.write_text(text, encoding="utf-8")
            print(f"[OK] {img_path.name} → {out_txt.name} ({len(text)} chars)")
            
        except Exception as e:
            print(f"[ERR] {img_path.name}: {e}")
        
    if __name__ == "__main__":
        main()
