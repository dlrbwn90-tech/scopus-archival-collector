# Scopus Archival Science Abstract Collector

Scopus API를 활용하여 기록학(Archival Science) 분야 주요 학술지의 논문 메타데이터 및 초록을 수집·정제하는 Python 스크립트 모음입니다.

---

## 1. 대상 저널 선정

### 선정 기준

[SCImago Journal Rank(SJR)](https://www.scimagojr.com/journalrank.php?category=3309) 포털에서 ASJC(All Science Journal Classification) 코드 **3309 (Library and Information Sciences)** 분류의 **2024년 SJR 순위 데이터**를 다운로드하여 기록학 관련 저널을 선별하였습니다.

- 원본 파일: `scimagojr_2024_Library_and_Information_Sciences.csv`

### 선정 저널 (5개)

| SJR 순위 (3309 내) | 저널명 | ISSN | SJR | 분위 | H-index |
|:---:|--------|------|:---:|:---:|:---:|
| 57 | Archival Science | 1389-0166 | 0.671 | Q1 | 44 |
| 110 | Archivaria | 0318-6954 | 0.347 | Q2 | 33 |
| 131 | Records Management Journal | 0956-5698 | 0.274 | Q2 | 27 |
| 159 | Archives and Manuscripts | 0157-6895 | 0.224 | Q3 | 15 |
| 171 | American Archivist | 0360-9081 | 0.207 | Q3 | 34 |

> **비고:** Library and Information Sciences(3309) 전체 252개 저널 중, 기록학(archival science / records management / archives) 분야에 해당하는 저널만 추출하여 SJR 상위 5개를 선정하였습니다.

---

## 2. 데이터 처리 흐름

아래 도표는 전체 데이터 수집·정제 과정을 나타냅니다.

```
scopus_abstract_collector.py
│
│  [1단계] Scopus Search API → 전기간 메타데이터 수집
│  [2단계] Abstract Retrieval API → EID별 초록 수집
│
├─→ scopus_abstracts_top5.csv (통합 원본: 4,047건, 초록 2,419건)
│
│   저널별 현황 (전체 / 초록 포함):
│     American Archivist ············ 2,079건 / 초록 829건
│     Archival Science ·············· 579건 / 초록 535건
│     Archivaria ···················· 485건 / 초록 381건
│     Archives and Manuscripts ····· 247건 / 초록 182건
│     Records Management Journal ··· 657건 / 초록 492건
│
│
│  extract_columns.py
│  : title, author, year, abstract 컬럼 추출
│
├─→ 저널별 원본 CSV (전기간)
│     ├── American_Archivist.csv ············ 2,079건
│     ├── Archival_Science.csv ·············· 579건
│     ├── Archivaria.csv ··················· 485건
│     ├── Archives_and_Manuscripts.csv ····· 247건
│     └── Records_Management_Journal.csv ··· 657건
│
│
│  filter_2001.py
│  : 2001년 이후 데이터만 필터링
│
├─→ 저널별 2001년 이후 CSV
│     ├── American_Archivist_2001.csv ·········· 571건 (-1,508)
│     ├── Archival_Science_2001.csv ············ 579건 (-0)
│     ├── Archivaria_2001.csv ················· 374건 (-111)
│     └── Records_Management_Journal_2001.csv · 510건 (-147)
│     * Archives and Manuscripts: Scopus 색인 시작이 2013년이므로 별도 필터링 불필요
│
│
│  check_abstracts.py → 초록 누락 현황 확인
│  extract_missing_abstracts.py → 누락 목록 추출
│
├─→ missing_abstracts.csv (369건)
│
│     저널명                    전체    초록있음   초록없음   누락률
│     ─────────────────────────────────────────────────────
│     Archival Science          579      535       44     7.6%
│     Archivaria                374      323       51    13.6%
│     Records Management J.     510      408      102    20.0%
│     American Archivist        571      399      172    30.1%
│     ─────────────────────────────────────────────────────
│     합계                     2,034    1,665      369    18.1%
│
│
│  extract_with_abstracts.py
│  : 초록 있는 항목만 추출
│
└─→ 최종 분석용 CSV (2001~ / 초록 포함)
      ├── American_Archivist_2001_abstracts_only.csv ·········· 399건
      ├── Archival_Science_2001_abstracts_only.csv ············ 535건
      ├── Archivaria_2001_abstracts_only.csv ················· 323건
      └── Records_Management_Journal_2001_abstracts_only.csv · 408건
                                                    총 1,665건
```

---

## 3. 스크립트 설명

| 실행 순서 | 파일명 | 기능 |
|:---:|--------|------|
| 1 | `scopus_abstract_collector.py` | Scopus Search API + Abstract Retrieval API를 이용한 2단계 데이터 수집 |
| 2 | `extract_columns.py` | 저널별 CSV에서 title, author, year, abstract 컬럼 추출 |
| 3 | `filter_2001.py` | 2001년 이후 데이터만 필터링 |
| 4 | `check_abstracts.py` | 저널별 초록 누락 현황 확인 |
| 5 | `extract_missing_abstracts.py` | 초록 누락 항목 목록 추출 |
| 6 | `extract_with_abstracts.py` | 초록 있는 항목만 추출 |

---

## 4. 실행 방법

### 사전 준비

- Python 3.9+
- [Scopus API Key](https://dev.elsevier.com/) 필요
- 기관 네트워크 또는 VPN 접속 필요 (Scopus API 기관 인증)

### 환경 설정

```bash
pip install requests pandas python-dotenv
```

프로젝트 루트에 `.env` 파일을 생성하고 API 키를 입력합니다:

```
SCOPUS_API_KEY=your_api_key_here
```

### 실행 순서

```bash
# 1) 메타데이터 + 초록 수집 (약 1~2시간 소요)
python3 scopus_abstract_collector.py

# 2) 저널별 컬럼 추출
python3 extract_columns.py

# 3) 2001년 이후 필터링
python3 filter_2001.py

# 4) 초록 현황 확인
python3 check_abstracts.py

# 5) 누락 목록 추출
python3 extract_missing_abstracts.py

# 6) 초록 있는 항목만 추출
python3 extract_with_abstracts.py
```

---

## 5. 참고 사항

- 수집 중단 시 `scopus_progress.json`을 통해 이어받기 가능
- Scopus API Rate Limit 초과 시 자동 60초 대기 후 재시도
- Archives and Manuscripts는 Scopus 색인 범위가 2013~2024년이므로 `filter_2001.py` 대상에서 제외

---

## 6. 작업 일지

| 날짜 | 작업 내용 |
|------|-----------|
| 2025-04-01 | SCImago JR에서 2024년 SJR 데이터 다운로드, 기록학 분야 상위 5개 저널 선정 |
| 2025-04-01 | Scopus API를 통한 5개 저널 전기간 메타데이터 및 초록 수집 (4,047건) |
| 2025-04-01 | 저널별 컬럼 추출, 2001년 이후 필터링, 초록 유무 분리 완료 (최종 1,665건) |
