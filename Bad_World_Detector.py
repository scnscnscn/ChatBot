import os
# 脏话词典文件路径
bad_words_file = 'bad_words.txt'

def load_bad_words(bad_words_file):
    # 加载脏话词典
    with open(bad_words_file, 'r', encoding='utf-8') as file:
        bad_words = set(word.strip() for word in file.readlines())
    return bad_words

def check_for_bad_words(user_input, bad_words):
    # 检查用户输入是否包含脏话
    for word in bad_words:
        if word in user_input:
            print(f"警告：检测到不文明用语'{word}'")
            return True
    return False


