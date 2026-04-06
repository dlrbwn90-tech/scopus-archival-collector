"""
frequency_analysis.py
======================
도메인 불용어 결정을 위한 단어 빈도 분석

출력 컬럼:
  - word: 단어
  - total_freq: 전체 빈도 (4개 저널 합산)
  - doc_freq: 출현 문서 수 (몇 개 초록에 등장하는지)
  - doc_ratio: 전체 문서 대비 출현 비율 (%)
  - AS_freq: Archival Science 빈도
  - AR_freq: Archivaria 빈도
  - RMJ_freq: Records Management Journal 빈도
  - AA_freq: American Archivist 빈도
"""

import pandas as pd
from collections import Counter
import os

FILES = {
    "AS":  "Archival_Science_2001_tokenized.csv",
    "AR":  "Archivaria_2001_tokenized.csv",
    "RMJ": "Records_Management_Journal_2001_tokenized.csv",
    "AA":  "American_Archivist_2001_tokenized.csv",
}

def count_words(series):
    """토큰 시리즈에서 단어 빈도 계산"""
    counter = Counter()
    for text in series.dropna():
        counter.update(text.split())
    return counter

def doc_freq(series):
    """단어별 출현 문서 수 계산"""
    df_counter = Counter()
    for text in series.dropna():
        words = set(text.split())
        df_counter.update(words)
    return df_counter

def main():
    print("단어 빈도 분석 시작...\n")

    journal_counters = {}
    all_tokens = []
    total_docs = 0

    for key, filename in FILES.items():
        if not os.path.exists(filename):
            print(f"  [건너뜀] {filename} 없음")
            continue

        df = pd.read_csv(filename)
        tokens = df["abstract_tokens"].dropna()
        journal_counters[key] = count_words(tokens)
        all_tokens.extend(tokens.tolist())
        total_docs += len(tokens)
        print(f"  {filename}: {len(tokens)}건 로드")

    # 전체 빈도
    total_counter = Counter()
    for c in journal_counters.values():
        total_counter.update(c)

    # 문서 빈도
    all_series = pd.Series(all_tokens)
    df_counter = doc_freq(all_series)

    # 결과 데이터프레임 생성
    rows = []
    for word, freq in total_counter.most_common():
        rows.append({
            "word":       word,
            "total_freq": freq,
            "doc_freq":   df_counter.get(word, 0),
            "doc_ratio":  round(df_counter.get(word, 0) / total_docs * 100, 1),
            "AS_freq":    journal_counters.get("AS",  Counter()).get(word, 0),
            "AR_freq":    journal_counters.get("AR",  Counter()).get(word, 0),
            "RMJ_freq":   journal_counters.get("RMJ", Counter()).get(word, 0),
            "AA_freq":    journal_counters.get("AA",  Counter()).get(word, 0),
        })

    result = pd.DataFrame(rows)
    result.to_csv("frequency_analysis.csv", index=False, encoding="utf-8-sig")

    print(f"\n총 고유 단어 수: {len(result)}개")
    print(f"총 문서 수: {total_docs}건")
    print(f"\n상위 50개 단어:")
    print(f"{'순위':<5} {'단어':<20} {'전체빈도':>8} {'문서빈도':>8} {'문서비율':>8}")
    print("-" * 55)
    for i, row in result.head(50).iterrows():
        print(f"{i+1:<5} {row['word']:<20} {row['total_freq']:>8} {row['doc_freq']:>8} {row['doc_ratio']:>7}%")

    print(f"\n저장 완료: frequency_analysis.csv")


if __name__ == "__main__":
    main()
