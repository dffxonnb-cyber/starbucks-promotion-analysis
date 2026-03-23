# Starbucks Promotion Analysis

반정형 고객 이벤트 데이터를 구조화하고, 고객·오퍼·이벤트를 하나의 분석 테이블로 통합한 뒤 Tableau 대시보드로 시각화한 프로젝트입니다.

- **핵심 흐름**: 문자열 파싱 → 고객/오퍼/이벤트 조인 → KPI·세그먼트·채널 분석
- **저장소 정책**: 원본 CSV와 대용량 전처리 결과는 GitHub에 포함하지 않음

---

## 목적

- **반정형 데이터 전처리**: CSV 내 문자열로 저장된 dict/JSON 유사 데이터 → Pandas DataFrame 컬럼 확장
- **ERD 설계**: 데이터 구조·관계 시각화, 분석 로직 설계
- **고객 그룹 식별**: 데이터 기반 프로모션 효과 분석
- **Tableau 대시보드**: KPI, 고객 세그먼트별 반응률, 채널별 성과 시각화·스토리텔링

## 데이터

이 저장소에는 원본 CSV와 전처리 결과 CSV를 포함하지 않습니다.

- 원본 입력: `portfolio.csv`, `profile.csv`, `transcript.csv`
- 로컬 배치 위치: `data/`
- 생성 산출물: `data/전처리_완료_데이터셋/`

- **Portfolio** (10행): offer_id, reward, channels, difficulty, duration, offer_type 등
- **Profile** (17,000행): customer_id, gender, age, became_member_on, income
- **Transcript** (306,534행): person, event(received/viewed/completed/transaction), value, time

`channels`는 `"['email','mobile','social']"` 형태의 문자열 리스트, `value`는 event별로 구조가 다른 문자열(dict)입니다. `ast.literal_eval` 등으로 파싱 후 컬럼 확장이 필요합니다.

### 데이터셋 출처

- **Starbucks (Udacity Capstone)**  
  [Starbucks Data Analysis - Customer Segmentation (Kaggle)](https://www.kaggle.com/code/candicezhao28/starbucks-data-analysis-customer-segmentation)  
  Portfolio·Profile·Transcript 데이터는 동일 시리즈의 Starbucks Capstone 데이터를 사용합니다. Kaggle에서 데이터셋을 다운로드한 뒤 `data/`에 넣고 노트북을 실행하면 됩니다.

## 시작하기

1. **환경 설정**  
   `pip install -r requirements.txt`  
   (Tableau 대시보드 확인용은 [Tableau](https://www.tableau.com/) 별도 설치)

2. **데이터 준비**  
   [데이터셋 출처](https://www.kaggle.com/code/candicezhao28/starbucks-data-analysis-customer-segmentation)에서 Starbucks Capstone용 CSV를 다운로드한 뒤 `data/` 폴더에 넣습니다.  
   **필요한 파일**: `portfolio.csv`, `profile.csv`, `transcript.csv` (Kaggle Starbucks Capstone 데이터셋에서 다운로드)

3. **실행 순서**  
   `analysis/notebooks/`에서 아래 순서대로 노트북을 실행합니다.  
   `00_데이터_확인.ipynb` → `01_데이터_전처리.ipynb` → `02_데이터_조인.ipynb` → `03_EDA_이상치_분석.ipynb` → `04_오퍼_추천_ML.ipynb`  
   조인 결과를 Tableau에서 불러와 `스벅_최종_통합본.twb`로 시각화합니다. 03은 EDA·이상치 분석, 04는 오퍼 완료 예측 기반 추천(시퀀스/시간, Cold start, 다양성·탐험, 오프라인 메트릭)입니다.

## 데이터 관계 (ERD 요약)

```
Profile (customer_id) ──< Transcript (person) >── Portfolio (offer_id)
       │                         │                        │
   gender, age               event, value            channels, offer_type
   income, became_member_on   (파싱 → offer_id, amount)  reward, difficulty, duration
```

- **Profile**: 고객 1명당 1행
- **Transcript**: 고객별 이벤트(오퍼 수신/조회/완료, 거래) 여러 행 → `person`=customer_id, `value` 파싱으로 offer_id·amount 추출
- **Portfolio**: 오퍼 1개당 1행, `channels` 파싱으로 channel_email·channel_mobile 등 플래그 생성

## 폴더 구조

| 폴더/파일 | 설명 |
|-----------|------|
| `analysis/notebooks/` | 00_데이터_확인, 01_데이터_전처리, 02_데이터_조인, 03_EDA_이상치_분석, 04_오퍼_추천_ML. `98.스타벅스크롤링_260112.ipynb`는 부가 참고용 |
| `docs/` | [한페이지_요약.md](./docs/한페이지_요약.md) – 문제·접근·결과·한계 요약 |
| `data/` | 로컬 원본 CSV 3개 배치 위치. 공개 저장소에는 안내 파일만 포함 |
| [스벅_최종_통합본.twb](./스벅_최종_통합본.twb) | Tableau 대시보드 원본 파일 |

## 분석 흐름

1. `00_데이터_확인.ipynb` – Portfolio·Profile·Transcript 로드, shape·컬럼·샘플 확인, channels·value 문자열 형태 확인
2. `01_데이터_전처리.ipynb` – channels 파싱 → channel_email·channel_mobile·channel_social·channel_web 등 플래그 컬럼, value 파싱 → offer_id·amount 추출, portfolio_clean·transcript_clean 생성
3. `02_데이터_조인.ipynb` – Profile↔Transcript(customer_id), Transcript↔Portfolio(offer_id) 조인 → 통합 데이터셋
4. `03_EDA_이상치_분석.ipynb` – starbucks_merged 로드 후 기초 EDA, amount 분포·Quantile/Z-Score/IQR 기반 이상치 탐지 및 시각화  
5. `04_오퍼_추천_ML.ipynb` – 오퍼 수신→유효기간 내 완료 타깃, 시퀀스/시간 피처, 시간 기반 train/test 분할, 완료 예측 모델, Recall@k·NDCG·다양성, Cold start·ε-탐험 적용 추천 리스트 생성 및 `offer_recommendations.csv` 저장

## 산출물

| 산출물 | 설명 |
|--------|------|
| `data/전처리_완료_데이터셋/portfolio_clean.csv` | channels 파싱 후 플래그 컬럼이 추가된 Portfolio |
| `data/전처리_완료_데이터셋/transcript_clean.csv` | value 파싱으로 offer_id·amount 등 추출된 Transcript |
| `data/전처리_완료_데이터셋/starbucks_merged.csv` | Profile·Transcript·Portfolio 조인 결과 (Tableau 입력용) |
| `data/전처리_완료_데이터셋/offer_recommendations.csv` | 고객별 추천 오퍼 ID·다양성 엔트로피 |
| [스벅_최종_통합본.twb](./스벅_최종_통합본.twb) | Tableau 대시보드 (KPI·세그먼트·채널 시각화) |

## 한계·향후

- 데이터 기간·지역이 제한적이므로 다른 시기·지역 확장 시 재검증 필요
- Tableau 결과 스크린샷을 추가하면 포트폴리오 가독성이 더 좋아짐

## 더 읽기

- [docs/한페이지_요약.md](./docs/한페이지_요약.md) – 문제·접근·결과·한계 요약

## GitHub 업로드 기준

- 포함 권장: `README.md`, `requirements.txt`, `analysis/notebooks/`, `docs/`, `스벅_최종_통합본.twb`
- 제외 권장: `data/*.csv`, `data/전처리_완료_데이터셋/*`, 임시 출력 파일
