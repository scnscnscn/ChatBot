import pandas as pd
import os


def get_keywords_from_txt(txt_file):
    """从txt文件中读取关键词"""
    with open(txt_file, 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file.readlines() if line.strip()]
    return keywords


def remove_rows_with_keywords_and_duplicates(keywords):
    # 获取当前目录下的所有CSV文件
    files = [f for f in os.listdir('.') if f.endswith('.csv')]

    for file in files:
        # 读取CSV文件
        df = pd.read_csv(file, encoding='utf-8')  # 读取时指定编码

        # 初始化一个布尔值掩码，表示哪些行包含了指定的关键词
        mask = pd.Series([False] * len(df))

        # 遍历每个关键词，找出包含该关键词的行
        for keyword in keywords:
            # 对每一行进行检查，看看是否含有这个关键词
            mask = mask | df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)

        # 移除包含任意关键词的行
        df_filtered = df[~mask]

        # 去除重复行
        df_filtered = df_filtered.drop_duplicates()

        # 保存修改后的CSV文件（覆盖原文件），使用utf-8-sig编码
        df_filtered.to_csv(file, index=False, encoding='utf-8-sig')
        print(f"{file} 中包含指定关键词的行及重复内容已移除。")


# 使用示例
txt_file = "dictionary.txt"  # 请替换为你存储关键词的txt文件路径
keywords = get_keywords_from_txt(txt_file)
remove_rows_with_keywords_and_duplicates(keywords)
