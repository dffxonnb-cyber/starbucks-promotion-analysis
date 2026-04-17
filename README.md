# 스타벅스 프로모션 분석

반정형 고객 이벤트 데이터를 분석 가능한 구조로 바꾸고, 고객·오퍼·이벤트를 하나의 테이블로 통합한 뒤 `프로모션 성과 해석 -> 고객/채널 인사이트 -> 추천 후보 생성 -> Tableau 대시보드`까지 연결한 프로젝트입니다. 핵심은 "예쁜 대시보드"가 아니라 `마케팅 담당자가 무엇을 결정할 수 있는가`를 데이터 구조부터 다시 설계한 점입니다.

## 10초 요약

- 마케팅 담당자: 어떤 고객군에 어떤 오퍼를 어떤 채널로 먼저 보낼지 결정할 수 있습니다.
- CRM/성과 담당자: 완료율, 반응률, 추천 후보를 한 화면에서 비교해 집행 우선순위를 정할 수 있습니다.
- 협업자/리더: Kaggle 원본 데이터가 `의사결정용 고객-오퍼 테이블`로 바뀌는 과정을 README만 보고 빠르게 이해할 수 있습니다.

## 바로 보는 결과

### Tableau 대시보드 미리보기

![Starbucks marketing dashboard](./docs/images/dashboard-overview.png)

![Starbucks recommendation dashboard](./docs/images/menu-recommendation-dashboard.png)

워크북은 [스벅_최종_통합본.twb](./스벅_최종_통합본.twb)에서 바로 확인할 수 있습니다.
브라우저에서 먼저 결과를 검토하려면 [docs/README.md](./docs/README.md)의 public review 경로를 따라가면 됩니다.

### 추천 결과 예시 카드

| 고객군 | 추천 오퍼 | 우선 채널 | 담당자가 내릴 결정 |
|------|------|------|------|
| 모바일 반응이 높은 기존 고객 | BOGO / 할인형 오퍼 | Mobile | 즉시 전환을 노리는 단기 프로모션을 앱 푸시 중심으로 집행 |
| 이메일 반응은 있으나 완료율이 낮은 고객 | 정보형 오퍼 | Email | 혜택보다 설명형 메시지를 먼저 보내고 후속 클릭률을 확인 |
| 여러 오퍼를 봤지만 완료 이력이 적은 고객 | 낮은 진입장벽의 할인형 오퍼 | Web + Email | 과한 혜택 남발 대신 재참여 테스트 캠페인부터 운영 |

### 고객군별 액션 시나리오

| 고객군 | 문제 해석 | 액션 시나리오 | 주로 볼 KPI |
|------|------|------|------|
| 고가치·고반응 고객 | 이미 반응하는 고객이라 과도한 할인보다 유지와 빈도 확대가 중요 | 리워드형 또는 BOGO 오퍼를 모바일 우선으로 집행해 재방문 주기를 짧게 유지 | 완료율, 재구매율, ARPU |
| 잠재 반응 고객 | 채널 반응은 있으나 전환이 불안정 | 이메일/웹에서 메시지형 오퍼를 먼저 테스트하고, 반응 고객만 모바일 재타겟팅 | 오픈율, 클릭률, 완료율 |
| 저반응·휴면 위험 고객 | 비용을 많이 써도 성과가 불확실 | 소액 할인 또는 재참여 캠페인을 저비용 채널로 제한 집행해 손실을 통제 | 재활성화율, 비용 대비 전환 |

## 빠른 판단

| 항목 | 내용 |
|------|------|
| 해결하려는 문제 | `channels`, `value`처럼 문자열로 저장된 반정형 이벤트 데이터를 그대로는 분석할 수 없음 |
| 실제 의사결정 가치 | 어떤 고객군에 어떤 오퍼를 어떤 채널로 제안할지 KPI와 추천 관점에서 판단 가능 |
| 재현 가능한 범위 | 공개 Kaggle CSV 다운로드 후 전처리, 조인, EDA, 오퍼 추천, Tableau 워크북까지 재현 가능 |
| 재현 불가능한 범위 | 저장소만 클론한 즉시 동일 결과 확인. 원본 CSV 3개 다운로드가 필요 |
| 대체 확인 방법 | [핵심 시각화](#핵심-시각화), [Tableau 워크북](./스벅_최종_통합본.twb), [재현성 가이드](./docs/reproducibility_and_validation.md) |

## 왜 이 프로젝트가 가치 있었는가

- `분석 가능한 테이블이 없는 상태`에서 시작해 문자열 파싱, ERD 설계, 조인 규칙을 직접 정의했습니다.
- 추천 모델을 단순 분류 성능에서 끝내지 않고 `Recall@k`, `NDCG`, 다양성까지 함께 봤습니다.
- 결과를 Tableau 화면으로 번역해 마케팅 담당자가 고객군, 채널, 추천 후보를 빠르게 확인할 수 있게 했습니다.

## 검증 요약

| 구분 | 핵심 수치 | 의미 | 근거 |
|------|-----------|------|------|
| 분류 성능 | AUC `0.8147` | 오퍼 완료 가능성의 분리력을 확보 | [04_오퍼_추천_ML.ipynb](./analysis/notebooks/04_오퍼_추천_ML.ipynb) |
| 운영 관점 성능 | Recall `0.8712`, Precision `0.6830`, F1 `0.7657` | 완료 가능 고객을 놓치지 않으면서도 과도한 추천을 줄이도록 균형 확인 | [04_오퍼_추천_ML.ipynb](./analysis/notebooks/04_오퍼_추천_ML.ipynb) |
| 랭킹 성능 | Recall@5% `0.0855`, Recall@10% `0.1642`, NDCG@5 `1.0000` | 상위 추천 후보가 실제 완료와 얼마나 맞물리는지 확인 | [04_오퍼_추천_ML.ipynb](./analysis/notebooks/04_오퍼_추천_ML.ipynb) |
| 추천 다양성 | 평균 diversity entropy `1.0530` | 추천 리스트가 한 종류 오퍼에만 쏠리지 않도록 점검 | [04_오퍼_추천_ML.ipynb](./analysis/notebooks/04_오퍼_추천_ML.ipynb) |
| 검증 방식 | 시간 기반 train/test split | 이벤트 데이터 특성상 미래 누수를 줄이는 방향으로 검증 | [04_오퍼_추천_ML.ipynb](./analysis/notebooks/04_오퍼_추천_ML.ipynb) |

## 핵심 시각화

### 추천/채널 결과 대시보드

![Starbucks menu nutrition dashboard](./docs/images/menu-nutrition-dashboard.png)

## 공개 저장소에서 확인할 수 있는 것

1. [재현성/검증 가이드](./docs/reproducibility_and_validation.md)에서 데이터 준비와 검증 포인트를 먼저 확인합니다.
2. [analysis/notebooks/](./analysis/notebooks/)에서 `00 -> 01 -> 02 -> 03 -> 04` 흐름을 순서대로 확인합니다.
3. [스벅_최종_통합본.twb](./스벅_최종_통합본.twb)로 Tableau 스토리텔링 구조를 확인합니다.
4. [docs/한페이지_요약.md](./docs/한페이지_요약.md)에서 문제·접근·결과·한계를 짧게 검토합니다.
5. [docs/README.md](./docs/README.md)에서 public review 순서와 핵심 이미지 자산을 한 번에 확인합니다.

## 데이터와 재현

- 원본 입력: `portfolio.csv`, `profile.csv`, `transcript.csv`
- 로컬 배치 위치: `data/`
- 생성 산출물: `portfolio_clean.csv`, `transcript_clean.csv`, `starbucks_merged.csv`, `offer_recommendations.csv`
- 데이터셋 출처: [Starbucks Capstone 데이터셋](https://www.kaggle.com/code/candicezhao28/starbucks-data-analysis-customer-segmentation)
- 저장소의 코드와 문서는 [MIT License](./LICENSE)를 따르며, 원본 데이터 사용 조건은 제공처 정책을 따릅니다.

## 한 줄 재현

원본 노트북을 순서대로 직접 실행해도 되지만, GitHub 검토나 로컬 재현용으로는 아래 명령 하나로 전체 흐름을 실행할 수 있습니다.

```bash
python run_pipeline.py --clear-artifacts --stop-on-error
```

- `run_pipeline.py`는 원본 노트북을 수정하지 않고 실행본과 로그를 `artifacts/`에 저장합니다.
- 자세한 실행 옵션과 구조 설명은 [AUTOMATION_GUIDE.md](./AUTOMATION_GUIDE.md)에서 확인할 수 있습니다.

## 노트북 기준 실행 순서

1. `pip install -r requirements.txt`
2. `data/` 폴더에 CSV 3개 배치
3. `analysis/notebooks/00_데이터_확인.ipynb`
4. `analysis/notebooks/01_데이터_전처리.ipynb`
5. `analysis/notebooks/02_데이터_조인.ipynb`
6. `analysis/notebooks/03_EDA_이상치_분석.ipynb`
7. `analysis/notebooks/04_오퍼_추천_ML.ipynb`
8. 결과 CSV를 Tableau에서 열어 [스벅_최종_통합본.twb](./스벅_최종_통합본.twb) 확인

## 엔지니어링 신호

| 항목 | 내용 |
|------|------|
| Entry points | [run_pipeline.py](./run_pipeline.py), [analysis/notebooks/](./analysis/notebooks/), [스벅_최종_통합본.twb](./스벅_최종_통합본.twb) |
| 구조화 포인트 | 전처리, 조인, EDA, 추천을 노트북 단계별로 분리 |
| 데이터 설계 | ERD 관점으로 `Profile < Transcript > Portfolio` 관계를 정리 |
| 공개 기준 | 원본 CSV 제외, 코드/문서/워크북/이미지만 공개 |

## 더 보기

- 한 페이지 요약: [docs/한페이지_요약.md](./docs/한페이지_요약.md)
- 문서 인덱스: [docs/README.md](./docs/README.md)
- 재현성/검증 가이드: [docs/reproducibility_and_validation.md](./docs/reproducibility_and_validation.md)
- 변경 이력: [CHANGELOG.md](./CHANGELOG.md)
- 자동 실행 가이드: [AUTOMATION_GUIDE.md](./AUTOMATION_GUIDE.md)
- 라이선스: [LICENSE](./LICENSE)
