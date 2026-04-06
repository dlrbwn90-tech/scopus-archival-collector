import pandas as pd
import os

files = {
    "Archival Science":           "Archival_Science_2001.csv",
    "Archivaria":                 "Archivaria_2001.csv",
    "Records Management Journal": "Records_Management_Journal_2001.csv",
    "American Archivist":         "American_Archivist_2001.csv",
}

all_missing = []

for name, filename in files.items():
    if not os.path.exists(filename):
        print(f"  [건너뜀] {filename} 없음")
        continue

    df = pd.read_csv(filename)
    missing = df[df['abstract'].isna() | (df['abstract'] == '')].copy()
    missing['journal'] = name
    all_missing.append(missing)
    print(f"  {name}: {len(missing)}건 누락")

result = pd.concat(all_missing, ignore_index=True)
result = result[['journal', 'title', 'author', 'year', 'doi']]
result = result.sort_values(['journal', 'year'])

result.to_csv('missing_abstracts.csv', index=False, encoding='utf-8-sig')
print(f"\n총 {len(result)}건 저장 완료: missing_abstracts.csv")
