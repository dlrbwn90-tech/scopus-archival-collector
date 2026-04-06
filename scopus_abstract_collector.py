"""
Scopus Abstract Collector v4
=============================
2단계 수집 방식:
  1단계: Search API  → 전체 논문 EID/메타데이터 수집
  2단계: Abstract Retrieval API → EID별 초록 개별 수집

수정 내역 (v4):
  - ISSN 앞자리 0 누락 버그 수정 (8자리 강제 패딩)
  - Archives and Manuscripts 정상 수집

대상 저널: ASJC 3309 기록학 관련 상위 5개 저널 (SJR 순)
수집 범위: 전체 기간

주의:
  - 기관 네트워크 또는 VPN 필수
  - 총 ~3,800건 → 약 1~2시간 소요
  - 중단되어도 progress 파일로 이어서 재시작 가능
"""

import requests
import pandas as pd
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ── 설정 ──────────────────────────────────────────────────────────────────────
SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY", "")
OUTPUT_FILE    = "scopus_abstracts_top5.csv"
PROGRESS_FILE  = "scopus_progress.json"
DELAY_SEARCH   = 0.5
DELAY_ABSTRACT = 1.0
PAGE_SIZE      = 25

JOURNALS = [
    {"name": "Archival Science",           "issn": "1389-0166", "eissn": None},
    {"name": "Archivaria",                 "issn": "0318-6954", "eissn": None},
    {"name": "Records Management Journal", "issn": "0956-5698", "eissn": None},
    {"name": "Archives and Manuscripts",   "issn": "0157-6895", "eissn": "2164-6058"},
    {"name": "American Archivist",         "issn": "0360-9081", "eissn": None},
]

# ── 공통 ──────────────────────────────────────────────────────────────────────
def get_headers():
    return {"X-ELS-APIKey": SCOPUS_API_KEY, "Accept": "application/json"}


def format_issn(issn: str) -> str:
    """ISSN에서 하이픈 제거 후 8자리로 패딩 (앞자리 0 보정)"""
    cleaned = issn.replace("-", "").strip()
    return cleaned.zfill(8)  # 8자리 미만이면 앞에 0 채움


# ── 1단계: 메타데이터 수집 ────────────────────────────────────────────────────
def build_query(journal: dict) -> str:
    issn = format_issn(journal["issn"])
    q = f'ISSN({issn})'
    if journal.get("eissn"):
        eissn = format_issn(journal["eissn"])
        q += f' OR EISSN({eissn})'
    return q


def fetch_search_page(query: str, start: int) -> dict:
    resp = requests.get(
        "https://api.elsevier.com/content/search/scopus",
        params={"query": query, "start": start, "count": PAGE_SIZE, "sort": "coverDate"},
        headers=get_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def parse_meta(e: dict, journal_name: str) -> dict:
    cover = e.get("prism:coverDate", "")
    return {
        "journal": journal_name,
        "title":   e.get("dc:title", ""),
        "author":  e.get("dc:creator", ""),
        "year":    cover[:4] if cover else "",
        "volume":  e.get("prism:volume", ""),
        "issue":   e.get("prism:issueIdentifier", ""),
        "doi":     e.get("prism:doi", ""),
        "eid":     e.get("eid", ""),
        "abstract": "",
    }


def collect_metadata(journal: dict) -> list:
    query = build_query(journal)
    name  = journal["name"]
    issn_display = journal["issn"]
    print(f"\n[1단계] {name} (ISSN: {issn_display}) 메타데이터 수집 중...")

    first = fetch_search_page(query, 0)
    total = int(first["search-results"]["opensearch:totalResults"])
    print(f"  -> 총 {total}건 확인")

    if total == 0:
        print(f"  [경고] 0건 — ISSN 확인 필요: {format_issn(issn_display)}")
        return []

    records = [parse_meta(e, name) for e in first["search-results"].get("entry", [])]

    for start in range(PAGE_SIZE, total, PAGE_SIZE):
        time.sleep(DELAY_SEARCH)
        page = fetch_search_page(query, start)
        records.extend(parse_meta(e, name) for e in page["search-results"].get("entry", []))
        print(f"  {min(start + PAGE_SIZE, total)}/{total}건...", end="\r")

    print(f"\n  -> {len(records)}건 메타데이터 완료")
    return records


# ── 2단계: 초록 수집 ──────────────────────────────────────────────────────────
def fetch_abstract(eid: str) -> str:
    url  = f"https://api.elsevier.com/content/abstract/eid/{eid}"
    resp = requests.get(url, headers=get_headers(), timeout=30)

    if resp.status_code == 404:
        return ""
    if resp.status_code == 429:
        print("\n  [경고] API 한도 초과. 60초 대기 후 재시도...")
        time.sleep(60)
        return fetch_abstract(eid)

    resp.raise_for_status()
    data = resp.json()

    try:
        ab = data["abstracts-retrieval-response"]["coredata"].get("dc:description", "")
        if ab:
            return str(ab).strip()
    except (KeyError, TypeError):
        pass
    return ""


def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  [이어받기] 기존 진행 {len(data)}건 로드")
        return data
    return {}


def save_progress(done: dict):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)


def fill_abstracts(records: list) -> list:
    total    = len(records)
    done_map = load_progress()
    print(f"\n[2단계] 초록 수집 시작 (총 {total}건)...")

    for i, rec in enumerate(records):
        eid = rec.get("eid", "")
        if not eid:
            continue
        if eid in done_map:
            rec["abstract"] = done_map[eid]
            continue

        abstract       = fetch_abstract(eid)
        rec["abstract"] = abstract
        done_map[eid]  = abstract

        if (i + 1) % 50 == 0:
            save_progress(done_map)
            filled = sum(1 for v in done_map.values() if v)
            print(f"  {i+1}/{total}건 완료 (초록 {filled}건 수집)", end="\r")

        time.sleep(DELAY_ABSTRACT)

    save_progress(done_map)
    print(f"\n  -> 초록 수집 완료")
    return records


# ── 메인 ──────────────────────────────────────────────────────────────────────
def main():
    if not SCOPUS_API_KEY:
        print("ERROR: .env 파일에 SCOPUS_API_KEY를 설정해주세요.")
        return

    # 1단계
    all_records = []
    for journal in JOURNALS:
        try:
            recs = collect_metadata(journal)
            all_records.extend(recs)
        except Exception as e:
            print(f"  [오류] {journal['name']}: {e}")
        time.sleep(1)

    print(f"\n1단계 완료: 총 {len(all_records)}건 메타데이터 수집")

    # 2단계
    all_records = fill_abstracts(all_records)

    # 저장
    result = pd.DataFrame(all_records)
    result["year"] = pd.to_numeric(result["year"], errors="coerce")
    result = result.sort_values(["journal", "year"], ascending=[True, True])
    result = result.drop(columns=["eid"])
    result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"\n저장 완료: {OUTPUT_FILE}")
    print(f"\n저널별 현황 (전체 / 초록포함):")
    for j, grp in result.groupby("journal"):
        total    = len(grp)
        with_abs = (grp["abstract"] != "").sum()
        print(f"  {j}: {total}건 / 초록 {with_abs}건")


if __name__ == "__main__":
    main()
