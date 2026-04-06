"""
02_tokenization.py
===================
전처리 2단계: 토큰화 + 표제어 추출 (Tokenization + Lemmatization)

처리 내용:
  - spaCy en_core_web_sm 모델 사용
  - 토큰화 (단어 단위 분리)
  - 표제어 추출 (lemmatization): running → run, archives → archive
  - 품사 필터링: 명사(NOUN), 고유명사(PROPN), 동사(VERB), 형용사(ADJ)만 유지
  - 구두점, 공백 토큰 제거
  - 2글자 이하 토큰 제거

입력: *_2001_cleaned.csv (4개)
출력: *_2001_tokenized.csv (4개)
      - abstract_tokens: 토큰 리스트 (공백 구분 문자열)
"""

import pandas as pd
import spacy
import os

# spaCy 모델 로드
nlp = spacy.load("en_core_web_sm")

# 유지할 품사
KEEP_POS = {"NOUN", "PROPN", "VERB", "ADJ"}

FILES = {
    "Archival Science":           "Archival_Science_2001_cleaned.csv",
    "Archivaria":                 "Archivaria_2001_cleaned.csv",
    "Records Management Journal": "Records_Management_Journal_2001_cleaned.csv",
    "American Archivist":         "American_Archivist_2001_cleaned.csv",
}


def tokenize(text: str) -> str:
    if not isinstance(text, str) or text.strip() == "":
        return ""

    doc = nlp(text)
    tokens = []
    for token in doc:
        # 품사 필터링
        if token.pos_ not in KEEP_POS:
            continue
        # 구두점, 공백 제거
        if token.is_punct or token.is_space:
            continue
        # 표제어 추출 + 2글자 이하 제거
        lemma = token.lemma_.strip()
        if len(lemma) <= 2:
            continue
        tokens.append(lemma)

    return " ".join(tokens)


def main():
    print("토큰화 + 표제어 추출 시작...\n")

    for name, filename in FILES.items():
        if not os.path.exists(filename):
            print(f"  [건너뜀] {filename} 없음")
            continue

        df = pd.read_csv(filename)
        print(f"  {name} ({len(df)}건) 처리 중...", end=" ", flush=True)

        df["abstract_tokens"] = df["abstract_clean"].apply(tokenize)

        out_name = filename.replace("_cleaned.csv", "_tokenized.csv")
        df.to_csv(out_name, index=False, encoding="utf-8-sig")

        # 샘플 출력
        sample = df["abstract_tokens"].iloc[0]
        print(f"완료")
        print(f"    저장: {out_name}")
        print(f"    샘플: {sample[:100]}...\n")

    print("완료")


if __name__ == "__main__":
    main()
