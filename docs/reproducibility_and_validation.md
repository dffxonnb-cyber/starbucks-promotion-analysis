# 재현성 및 검증 가이드

## 공개 저장소 기준 재현 가능한 범위

| 범위 | 확인 방법 | 비고 |
|------|-----------|------|
| 반정형 데이터 파싱 | [01_데이터_전처리.ipynb](../analysis/notebooks/01_데이터_전처리.ipynb) | `channels`, `value` 파싱 로직 확인 |
| 조인 구조 | [02_데이터_조인.ipynb](../analysis/notebooks/02_데이터_조인.ipynb) | `Profile < Transcript > Portfolio` 통합 흐름 |
| EDA/이상치 분석 | [03_EDA_이상치_분석.ipynb](../analysis/notebooks/03_EDA_이상치_분석.ipynb) | KPI와 분포 점검 |
| 추천 모델 검증 | [04_오퍼_추천_ML.ipynb](../analysis/notebooks/04_오퍼_추천_ML.ipynb) | 시간 기반 분할, AUC, Recall@k, NDCG |
| 시각화 검토 | [README](../README.md), [스벅_최종_통합본.twb](../스벅_최종_통합본.twb) | Tableau 결과 확인 |

## 재현 불가능한 범위

- 저장소만 클론한 직후의 즉시 실행
- 원본 CSV 없이 동일한 추천 결과 재생성

즉, 이 프로젝트는 `비공개 데이터 프로젝트`가 아니라 `공개 데이터 다운로드가 필요한 프로젝트`입니다.

## 재현 절차

1. `pip install -r requirements.txt`
2. Kaggle에서 `portfolio.csv`, `profile.csv`, `transcript.csv` 다운로드
3. `data/` 폴더에 배치
4. 노트북 `00 -> 01 -> 02 -> 03 -> 04` 순서로 실행
5. 생성된 CSV를 Tableau에서 열어 워크북 확인

## 검증 포인트

- 분류 성능: AUC `0.8147`, Recall `0.8712`, Precision `0.6830`, F1 `0.7657`
- 랭킹 성능: Recall@5% `0.0855`, Recall@10% `0.1642`, NDCG@5 `1.0000`
- 추천 다양성: 평균 diversity entropy `1.0530`
- 검증 방식: 시간 기반 train/test split

## 면접에서 설명하기 좋은 포인트

- 왜 `반정형 이벤트`를 먼저 파싱해야 했는가
- 왜 단순 분류 점수 외에 `Recall@k`, `NDCG`, 다양성까지 봤는가
- 대시보드가 실제로 어떤 마케팅 결정을 돕는가
