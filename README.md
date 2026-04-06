# Scopus Archival Science Abstract Collector

Scopus API를 활용하여 기록학(Archival Science) 분야 주요 학술지의 논문 메타데이터 및 초록을 수집하는 Python 스크립트 모음입니다.

## 대상 저널 (ASJC 3309 상위 5개, SJR 기준)

| 저널명 | ISSN |
|--------|------|
| Archival Science | 1389-0166 |
| Archivaria | 0318-6954 |
| Records Management Journal | 0956-5698 |
| Archives and Manuscripts | 0157-6895 |
| American Archivist | 0360-9081 |

## 수집 결과 요약

- 전체 메타데이터: 4,047건 (전 기간)
- 2001년 이후: 2,034건
- 초록 포함: 1,665건 (초록 누락률 18.1%)

## 스크립트 설명

| 파일명 | 기능 |
|--------|------|
| `scopus_abstract_collector.py` | Scopus Search API + Abstract Retrieval API를 이용한 2단계 데이터 수집 |
| `extract_columns.py` | 저널별 CSV에서 title, author, year, abstract 컬럼 추출 |
| `filter_2001.py` | 2001년 이후 데이터만 필터링 |
| `check_abstracts.py` | 저널별 초록 누락 현황 확인 |
| `extract_missing_abstracts.py` | 초록 누락 항목 목록 추출 |
| `extract_with_abstracts.py` | 초록 있는 항목만 추출 |

## 실행 방법

### 1. 사전 준비

- Python 3.9+
- [Scopus API Key](https://dev.elsevier.com/) 필요
- 기관 네트워크 또는 VPN 접속 필요 (Scopus API 기관 인증)

### 2. 환경 설정

```bash
pip install requests pandas python-dotenv
```

프로젝트 루트에 `.env` 파일을 생성하고 API 키를 입력합니다:

```
SCOPUS_API_KEY=your_api_key_here
```

### 3. 실행 순서

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

## 참고

- 수집 중단 시 `scopus_progress.json`을 통해 이어받기 가능
- CSV 데이터 파일은 `.gitignore`로 제외되어 있으며, 스크립트 실행으로 재생성 가능
- Scopus API Rate Limit 초과 시 자동 60초 대기 후 재시도
