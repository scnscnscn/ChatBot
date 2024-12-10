import pandas as pd
import os


def get_keywords_from_txt(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file.readlines() if line.strip()]
    return keywords


def remove_rows_with_keywords_and_duplicates(keywords):
    files = [f for f in os.listdir('.') if f.endswith('.csv')]

    for file in files:
        df = pd.read_csv(file, encoding='utf-8')
        mask = pd.Series([False] * len(df))
        for keyword in keywords:
            mask = mask | df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)

        df_filtered = df[~mask]
        df_filtered = df_filtered.drop_duplicates()
        df_filtered.to_csv(file, index=False, encoding='utf-8-sig')
        print(f"{file} 中包含指定关键词的行及重复内容已移除。")

txt_file = "dictionary.txt"
keywords = get_keywords_from_txt(txt_file)
remove_rows_with_keywords_and_duplicates(keywords)
