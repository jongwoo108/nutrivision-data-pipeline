# nutrivision-data-pipeline — Progress Log

> 본 문서는 **식품 영양성분표 OCR 추출 프로젝트의 개발 과정**을 기록합니다.  
> 주요 변화, 모델 전환, 환경 설정, 향후 개선 계획을 순서대로 정리합니다.

---

## 1. 프로젝트 개요

- **목표:** 식품 영양성분표 이미지로부터 텍스트(영양 정보)를 구조적으로 추출  
- **주요 기술 스택:** Python, OpenCV, Tesseract, PaddleOCR, CUDA, cuDNN  
- **핵심 과제:**  
  - 한글 OCR 정확도 개선  
  - 표(테이블) 기반 텍스트 구조 복원  
  - 숫자·단위 추출 후 정규화

---

## 2. 환경 및 초기 설정

| 구성 요소 | 버전 |
|------------|-------|
| Python | 3.12 |
| Tesseract | 5.3.4 |
| PaddleOCR | 2.7.3 |
| PaddlePaddle | 2.6.2 |
| CUDA | 11.8 |
| cuDNN | 8.9.7 |

GPU 정상 인식 확인:
```bash
python -c "import paddle; print(paddle.device.is_compiled_with_cuda()); paddle.utils.run_check()"
