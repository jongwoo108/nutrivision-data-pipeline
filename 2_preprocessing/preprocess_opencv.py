import os
from pathlib import Path
import cv2
import numpy as np

IN_DIR = Path("../1_data_collection/assets/raw_images")
OUT_DIR = Path("./processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for file in os.listdir(IN_DIR):
    in_path = IN_DIR / file
    if not in_path.suffix.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    img = cv2.imread(str(in_path))
    if img is None:
        continue

    # ① 흑백 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ② CLAHE(국부적 명암대비 향상)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # ③ 업스케일 (1.5배 확대)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # ④ 가우시안 블러
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # ⑤ 샤프닝 커널
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp = cv2.filter2D(blur, -1, kernel)

    # ⑥ 임계처리
    thr = cv2.adaptiveThreshold(
        sharp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    )

    out_path = OUT_DIR / file
    cv2.imwrite(str(out_path), thr)
    print(f"[OK] {file} processed → {out_path}")
