import pandas as pd
import os

files = {
    "Archival Science":           "Archival_Science_2001.csv",
    "Archivaria":                 "Archivaria_2001.csv",
    "Records Management Journal": "Records_Management_Journal_2001.csv",
    "American Archivist":         "American_Archivist_2001.csv",
}

print(f"{'저널명':<30} {'전체':>6} {'초록있음':>8} {'초록없음':>8} {'누락률':>8}")
print("-" * 65)

total_all = has_all = missing_all = 0

for name, filename in files.items():
    if not os.path.exists(filename):
        print(f"  [건너뜀] {filename} 없음")
        continue

    df      = pd.read_csv(filename)
    total   = len(df)
    has_abs = (df['abstract'].notna() & (df['abstract'] != '')).sum()
    missing = total - has_abs
    ratio   = missing / total * 100

    total_all   += total
    has_all     += has_abs
    missing_all += missing

    print(f"{name:<30} {total:>6} {has_abs:>8} {missing:>8} {ratio:>7.1f}%")

print("-" * 65)
print(f"{'합계':<30} {total_all:>6} {has_all:>8} {missing_all:>8} {missing_all/total_all*100:>7.1f}%")
