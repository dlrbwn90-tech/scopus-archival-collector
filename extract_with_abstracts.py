import pandas as pd
import os

files = {
    "Archival Science":           "Archival_Science_2001.csv",
    "Archivaria":                 "Archivaria_2001.csv",
    "Records Management Journal": "Records_Management_Journal_2001.csv",
    "American Archivist":         "American_Archivist_2001.csv",
}

print("초록 있는 항목만 추출 시작...\n")

total_all = 0
extracted_all = 0

for name, filename in files.items():
    if not os.path.exists(filename):
        print(f"  [건너뜀] {filename} 없음")
        continue

    df = pd.read_csv(filename)
    before = len(df)

    # 초록 있는 것만 추출
    df_filtered = df[df['abstract'].notna() & (df['abstract'] != '')].copy()
    after = len(df_filtered)

    out_name = filename.replace('.csv', '_abstracts_only.csv')
    df_filtered.to_csv(out_name, index=False, encoding='utf-8-sig')

    total_all     += before
    extracted_all += after

    print(f"  {name}")
    print(f"    전체 {before}건 → 초록 있음 {after}건 ({before - after}건 제외)")
    print(f"    저장: {out_name}\n")

print("-" * 50)
print(f"  합계: 전체 {total_all}건 → 초록 있음 {extracted_all}건 ({total_all - extracted_all}건 제외)")
print("\n완료")
