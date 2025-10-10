from paddleocr import PaddleOCR
from pathlib import Path

IN_DIRS = [
    Path("../2_preprocessing/roi"),          # 있으면 ROI 먼저 사용
    Path("../2_preprocessing/processed"),    # 없으면 전처리본
    Path("../1_data_collection/assets/raw_images"),  # 최후 원본
]
OUT_DIR = Path("./ocr_results_paddle")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ocr = PaddleOCR(
    lang="korean",
    use_angle_cls=True,
    use_gpu=True,
    det_db_box_thresh=0.5,   # 박스 검출 임계값 (0.5~0.6 시도)
    det_db_unclip_ratio=1.6, # 박스 확장 비율
    rec_batch_num=8,         # GPU에서 인식 배치 증대
    show_log=False
)

VALID_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}

def list_images(folder: Path):
    if not folder.exists():
        return []
    return [p for p in folder.iterdir() if p.suffix.lower() in VALID_EXT]

def main(force=False):
    chosen, images = None, []
    for d in IN_DIRS:
        images = list_images(d)
        if images:
            chosen = d
            break
    if not images:
        print("[WARN] No images found.")
        return
    print(f"[INFO] Using input dir: {chosen.resolve()} ({len(images)} files)")

    processed = skipped = 0
    for img_path in images:
        out_txt = OUT_DIR / f"{img_path.stem}.txt"
        if out_txt.exists() and not force:
            skipped += 1
            continue
        try:
            result = ocr.ocr(str(img_path), cls=True)
            lines = []
            for res in result:
                for line in res:
                    lines.append(line[1][0])
            out_txt.write_text("\n".join(lines), encoding="utf-8")
            processed += 1
            print(f"[OK] {img_path.name} → {out_txt.name} ({len(lines)} lines)")
        except Exception as e:
            print(f"[ERR] {img_path.name}: {e}")
    print(f"[DONE] processed={processed}, skipped={skipped}")

if __name__ == "__main__":
    main()
