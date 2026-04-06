import pandas as pd
import os

files = [
    "American_Archivist.csv",
    "Archival_Science.csv",
    "Archivaria.csv",
    "Records_Management_Journal.csv",
]

print("2001년 이후 데이터 추출 시작...\n")

for filename in files:
    if not os.path.exists(filename):
        print(f"  [건너뜀] {filename} 없음")
        continue

    df = pd.read_csv(filename)
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    before = len(df)
    df_filtered = df[df['year'] >= 2001].copy()
    after = len(df_filtered)

    out_name = filename.replace('.csv', '_2001.csv')
    df_filtered.to_csv(out_name, index=False, encoding='utf-8-sig')
    print(f"  {filename}")
    print(f"    전체 {before}건 → 2001년 이후 {after}건 ({before - after}건 제외)")
    print(f"    저장: {out_name}\n")

print("완료")
