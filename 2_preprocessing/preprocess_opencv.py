import os
from pathlib import Path
import cv2

IN_DIR = Path("../1_data_collection/assets/raw_images")
OUT_DIR = Path("./processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

VALID_EXT = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"]

processed_files = {f.name for f in OUT_DIR.iterdir() if f.is_file()}

print(f"[INFO] {len(processed_flies)} already processed files found")

for file in os.listdir(IN_DIR):
    in_path = IN_DIR / file
    if in_path.suffix.lower() not in VALID_EXT:
        continue
    
    if file in processed_files:
        continue
    
    img = cv2.imread(str(in_path))
    if img is None:
        print(f"[WARN] cannot read: {in_path}")
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thr = cv2.adaptiveThreshold(blur, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)
    
    out_path = OUT_DIR / file
    ok = cv2.imwrite(str(out_path), thr)
    if ok:
        print(f"[OK] {file} → {out_path}")
    else:
        print(f"[ERR] failed to write: {out_path}")

print("[INFO] Preprocessing completed")