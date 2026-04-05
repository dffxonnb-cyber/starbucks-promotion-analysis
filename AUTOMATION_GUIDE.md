# 자동 실행 가이드

이 저장소는 원본 노트북을 분석 기록으로 유지하면서, 재현성을 위해 별도의 실행 진입점도 함께 제공합니다.

## 변경 내용

- `run_pipeline.py`가 원본 노트북을 수정하지 않고 전체 흐름을 실행합니다.
- 실행된 노트북 사본은 `artifacts/executed_notebooks/`에 저장됩니다.
- 실행 로그는 `artifacts/logs/`에 저장됩니다.

## 권장 GitHub 구조

- 원본 노트북은 `analysis/notebooks/` 아래에 유지
- 원본 데이터는 `data/` 아래에 두되 Git에는 포함하지 않음
- 생성 산출물은 `artifacts/` 아래에 두고 Git에는 포함하지 않음
- 스크린샷, 선별 이미지, 문서는 `docs/` 아래에 정리

## 로컬 실행

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Windows 재현 실행:

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install pandas numpy matplotlib seaborn scipy scikit-learn nbconvert nbclient ipykernel jupyter-core jupyter-client nbformat pywin32
.\.venv\Scripts\python run_pipeline.py --clear-artifacts --stop-on-error
```

선택 실행 명령:

```bash
python run_pipeline.py --include-scraping
python run_pipeline.py --clear-artifacts
python run_pipeline.py --stop-on-error
python run_pipeline.py --notebook 01_데이터_전처리.ipynb --notebook 02_데이터_조인.ipynb
```

## 왜 GitHub 공개에 적합한가

- 포트폴리오 검토에 필요한 원본 노트북 서사를 그대로 유지할 수 있습니다.
- 검토자는 한 줄 명령으로 전체 파이프라인을 실행할 수 있습니다.
- 생성 산출물이 저장소 이력을 어지럽히지 않습니다.
- 같은 패턴을 다른 노트북 중심 프로젝트에도 재사용할 수 있습니다.

## 다른 저장소에 적용할 때의 기준

리테일 프로젝트에도 같은 구조를 적용할 수 있습니다.

- 원본 노트북은 기존 노트북 폴더에 유지
- 저장소 루트에 `run_pipeline.py` 추가
- `.gitignore`에 `artifacts/` 추가
- 입력 파일, 출력 파일, 한 줄 실행 명령을 메인 README에 명시
