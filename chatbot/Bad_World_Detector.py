import os
def load_bad_words(file_path):
    if not os.path.exists(file_path):
        print(f"敏感词文件 '{file_path}' 不存在。")
        return []

    bad_words = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            bad_words.add(line.strip())
    return bad_words


def check_for_bad_words(text, bad_words):
    text = text.lower()

    for bad_word in bad_words:
        if bad_word in text:
            return True

    return False
