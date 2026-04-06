"""
01_basic_cleaning.py
=====================
전처리 1단계: 기본 정제 (Basic Cleaning)

처리 내용:
  - 소문자화
  - HTML 태그 제거
  - 특수문자 제거 (하이픈 제외 — 복합어 보존)
  - 숫자 제거
  - 연속 공백 정규화
  - 정제 후 빈 초록 제거

입력: *_2001_abstracts_only.csv (4개)
출력: *_2001_cleaned.csv (4개)
"""

import pandas as pd
import re
import os

FILES = {
    "Archival Science":           "Archival_Science_2001_abstracts_only.csv",
    "Archivaria":                 "Archivaria_2001_abstracts_only.csv",
    "Records Management Journal": "Records_Management_Journal_2001_abstracts_only.csv",
    "American Archivist":         "American_Archivist_2001_abstracts_only.csv",
}

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # 소문자화
    text = text.lower()

    # HTML 태그 제거
    text = re.sub(r"<[^>]+>", " ", text)

    # 하이픈으로 연결된 복합어 보존 (예: record-keeping → record-keeping)
    # 그 외 특수문자 제거
    text = re.sub(r"[^\w\s\-]", " ", text)

    # 숫자 제거
    text = re.sub(r"\b\d+\b", " ", text)

    # 연속 공백 정규화
    text = re.sub(r"\s+", " ", text).strip()

    return text


def main():
    print("기본 정제 시작...\n")

    total_before = 0
    total_after  = 0

    for name, filename in FILES.items():
        if not os.path.exists(filename):
            print(f"  [건너뜀] {filename} 없음")
            continue

        df = pd.read_csv(filename)
        before = len(df)

        # abstract 정제
        df["abstract_clean"] = df["abstract"].apply(clean_text)

        # 정제 후 빈 초록 제거
        df = df[df["abstract_clean"].str.strip() != ""].copy()
        after = len(df)

        out_name = filename.replace("_abstracts_only.csv", "_cleaned.csv")
        df.to_csv(out_name, index=False, encoding="utf-8-sig")

        total_before += before
        total_after  += after

        print(f"  {name}")
        print(f"    {before}건 → 정제 후 {after}건 ({before - after}건 제거)")
        print(f"    저장: {out_name}\n")

    print("-" * 50)
    print(f"  합계: {total_before}건 → {total_after}건 ({total_before - total_after}건 제거)")
    print("\n완료")


if __name__ == "__main__":
    main()
