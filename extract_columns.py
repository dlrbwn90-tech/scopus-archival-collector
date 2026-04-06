import pandas as pd
import os

files = [
    "American_Archivist.csv",
    "Archival_Science.csv",
    "Archivaria.csv",
    "Archives_and_Manuscripts.csv",
    "Records_Management_Journal.csv",
]

for filename in files:
    if not os.path.exists(filename):
        print(f"  [건너뜀] {filename} 없음")
        continue

    df = pd.read_csv(filename)
    extracted = df[['title', 'author', 'year', 'abstract']].copy()

    out_name = filename.replace('.csv', '_extracted.csv')
    extracted.to_csv(out_name, index=False, encoding='utf-8-sig')
    print(f"  저장: {out_name} ({len(extracted)}건)")

print("\n완료")
