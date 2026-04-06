# Scopus Archival Science Abstract Collector

Scopus API를 활용하여 기록학(Archival Science) 분야 주요 학술지의 논문 메타데이터 및 초록을 수집·정제하는 Python 스크립트 모음입니다.

---

## 0. 연구 개요

### 연구 목적

본 레포지토리는 박사학위논문 **"디지털 기록의 물질성과 신뢰성: 하드웨어 기반 증명 메커니즘의 기록학적 함의"** (가제)의 **Part 1 코퍼스 분석**을 위한 데이터 수집 및 전처리 과정을 문서화한다.

핵심 연구 질문은 다음과 같다:

> 기록학 분야의 주요 학술 담론에서 하드웨어 계층(hardware layer)과 물질성(materiality) 관련 용어는 지난 25년간 어떻게 다루어져 왔는가?

이를 위해 기록학 분야 주요 저널 4개의 초록(2001–현재, 총 1,665건)을 코퍼스로 구축하고, 하드웨어·신뢰·물질성 관련 용어의 **구조적 부재(structural absence)**를 텍스트 데이터로 실증한다.

### 연구의 위치

본 코퍼스 분석은 논문의 3부 구조 중 **Part 1**에 해당한다.

| 구분 | 내용 |
|------|------|
| **Part 1** | 코퍼스 분석 — 기록학 담론의 구조적 공백 확인 (본 레포지토리) |
| Part 2 | 표준 비교 분석 — ISO 16363, OAIS, PREMIS 등 기록관리 표준의 하드웨어 계층 처리 방식 분석 |
| Part 3 | TPM PoC — Trusted Platform Module 기반 디지털 기록 신뢰성 검증 프로토타입 구현 |

### 이론적 배경

- **Thibodeau(2002)**: 디지털 객체의 3계층 모델 (물리적·논리적·개념적 객체)
- **Blanchette(2011)**: 컴퓨팅의 물질성과 추상화 계층의 은폐 문제
- **Sundqvist(2021)**: 디지털 기록의 신뢰성(reliability) 개념 재고
- **InterPARES Chain of Preservation 모델**: 디지털 기록 보존의 연쇄적 책임 구조

### 방법론

#### 코퍼스 구축 방법

Tognini-Bonelli(2001)와 Baker et al.(2008)의 **corpus-assisted hybrid approach**를 채택하였다. 이 접근법은 코퍼스 데이터를 통한 양적 분석과 담론 분석적 해석을 결합하는 방법론으로, 텍스트에서 드러나지 않는 **구조적 공백(what is not said)**을 탐색하는 데 유효하다.

#### 저널 선정 근거

- SCImago Journal Rank(SJR) 2024 기준 Library and Information Sciences(ASJC 3309) 분야 상위 저널 중 기록학 관련 저널 선별
- Scopus API를 통한 전체 기간 수집 가능 여부를 최종 포함 기준으로 적용
- Archives and Manuscripts는 Scopus 등재가 2013년부터로 한정되고 2022년 플랫폼 이전으로 전체 기간 수집이 불가하여 **제외**

#### 분석 기간 설정 근거

4개 저널 중 가장 늦은 창간 연도인 Archival Science(2001년)를 기준으로 분석 기간을 **2001년–현재**로 통일하였다. 이를 통해 저널 간 비교 가능성을 확보하고, 초록 누락률을 41.1%에서 18.1%로 낮추었다.

#### 초록 누락 처리

2001년 이후 수집된 2,034건 중 초록 누락 369건을 검토한 결과, 대부분이 editorial, letter to the editor, book review 등 분석 대상에서 제외 가능한 단편 형식임을 확인하였다. 따라서 초록이 있는 **1,665건**을 최종 분석 코퍼스로 확정하였다.

#### 전처리 계획 (Preprocessing Pipeline)

현재 진행 중이며, 아래 도구를 활용한 전처리 파이프라인을 구축할 예정이다.

| 단계 | 도구 | 내용 |
|------|------|------|
| 기본 정제 | Python | 특수문자 제거, 소문자화, 공백 정규화 |
| 토큰화 / 표제어 추출 | spaCy | Lemmatization, 품사 태깅 |
| 불용어 제거 | spaCy + 도메인 불용어 사전 | 일반 불용어 + 기록학 도메인 불용어 처리 |
| 키워드·공기어 분석 | AntConc | 콘코던스, 빈도, n-gram (Baker et al., 2008) |
| 토픽 모델링 | Gensim (BERTopic 검토 중) | LDA 기반 주제 분류 |

> **참고:** spaCy와 AntConc의 병행 사용은 최근 코퍼스 연구의 표준적 조합으로, 전처리 자동화(spaCy)와 탐색적 텍스트 분석(AntConc)의 역할을 분담한다.

### 참고문헌

- Baker, P., Gabrielatos, C., Khosravinik, M., Krzyżanowski, M., McEnery, T., & Wodak, R. (2008). A useful methodological synergy? Combining critical discourse analysis and corpus linguistics to examine discourses of refugees and asylum seekers in the UK press. *Discourse & Society*, 19(3), 273–306.
- Blanchette, J.-F. (2011). A material history of bits. *Journal of the American Society for Information Science and Technology*, 62(6), 1042–1057.
- Thibodeau, K. (2002). Overview of technological approaches to digital preservation and challenges in coming years. In *The State of Digital Preservation: An International Perspective*. Council on Library and Information Resources.
- Tognini-Bonelli, E. (2001). *Corpus linguistics at work*. John Benjamins.

### 인용 방법

SCImago Journal & Country Rank 데이터 출처:

> SCImago. (n.d.). SJR — SCImago Journal & Country Rank [Portal]. Retrieved April 2025, from https://www.scimagojr.com

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
- Archives and Manuscripts는 Scopus 색인 범위가 2013~2024년이며 2022년 플랫폼 이전으로 전체 기간 수집이 불가하여 최종 분석에서 제외

---

## 6. 작업 일지

| 날짜 | 작업 내용 |
|------|-----------|
| 2025-04-01 | SCImago JR에서 2024년 SJR 데이터 다운로드, 기록학 분야 상위 5개 저널 선정 |
| 2025-04-01 | Scopus API를 통한 5개 저널 전기간 메타데이터 및 초록 수집 (4,047건) |
| 2025-04-01 | 저널별 컬럼 추출, 2001년 이후 필터링, 초록 유무 분리 완료 (최종 1,665건) |
