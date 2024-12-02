import os


def load_bad_words(file_path):
    """
    从指定文件加载敏感词，返回敏感词列表。
    """
    if not os.path.exists(file_path):
        print(f"敏感词文件 '{file_path}' 不存在。")
        return []

    bad_words = set()  # 使用 set 以去重
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            bad_words.add(line.strip())  # 去掉每行的空格和换行符
    return bad_words


def check_for_bad_words(text, bad_words):
    """
    检查输入文本是否包含敏感词，返回 True 表示包含敏感词，False 表示不包含。
    """
    # 将文本转为小写字母进行无关大小写的匹配
    text = text.lower()

    # 遍历敏感词列表，检查是否有词汇出现在输入文本中
    for bad_word in bad_words:
        if bad_word in text:
            return True  # 如果包含敏感词，返回 True

    return False  # 如果没有敏感词，返回 False
