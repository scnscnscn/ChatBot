import redis
import json
import csv
import re


# 连接 Redis
def get_redis_connection():
    return redis.StrictRedis(host='localhost', port=6379, db=0)


# 判断评论是否符合条件
def is_valid_comment(comment_text, existing_comments):
    # 1. 删除冒号前的内容
    comment_text = re.sub(r'^.*?：', '', comment_text)

    # 2. 删除【】符号内的内容
    comment_text = re.sub(r'【.*?】', '', comment_text)

    # 3. 删除所有非中文、英文、数字及常见标点符号字符
    # 允许的标点符号包括: 。！…，、；：“”‘’、【】,.;?!-()[]{}等
    comment_text = re.sub(r'[^a-zA-Z0-9一-鿿。！？…、，；：“”‘’【】,.?!;:\-\(\)\[\]\{\}]', '', comment_text)

    # 4. 删除所有 [] 和 【】 符号内的内容
    comment_text = re.sub(r'\[.*?\]', '', comment_text)
    comment_text = re.sub(r'【.*?】', '', comment_text)

    # 5. 检查评论长度
    if len(comment_text) < 5:
        return False

    # 6. 检查是否为重复内容
    if comment_text in existing_comments:
        return False

    # 7. 添加到已存在评论集合中以便后续检测重复
    existing_comments.add(comment_text)

    return comment_text  # 返回清洗后的评论内容


# 获取符合条件的评论数据
def get_comments_from_redis(redis_conn, keys_pattern):
    keys = redis_conn.keys(keys_pattern)
    comments = []
    existing_comments = set()  # 存储已收录评论内容以检查重复

    for key in keys:
        comment_list = redis_conn.lrange(key, 0, -1)  # 获取该键下的所有评论
        for comment_json in comment_list:
            # 确保使用 UTF-8 解码评论数据，防止乱码
            comment_json = comment_json.decode("utf-8")
            comment = json.loads(comment_json)  # 解析 JSON 格式的评论
            comment_text = comment.get("text", "")

            # 判断评论是否有效并返回清洗后的评论内容
            cleaned_text = is_valid_comment(comment_text, existing_comments)
            if cleaned_text:
                comments.append({"text": cleaned_text})  # 只保留文本内容

    return comments


# 将评论数据写入 CSV 文件（追加模式）
def export_comments_to_csv(comments, filename="data3.csv"):
    # 判断评论数据是否存在
    if not comments:
        print("没有找到符合条件的评论数据！")
        return

    # 打开 CSV 文件并追加数据
    with open(filename, mode='a', newline='', encoding='utf_8_sig') as file:
        # 创建 CSV 写入器，列名设置为 "label" 和 "text"
        writer = csv.DictWriter(file, fieldnames=["label", "text"])

        # 如果文件为空（第一次写入），则写入表头
        if file.tell() == 0:  # 检查文件指针位置，如果为 0，说明文件为空
            writer.writeheader()

        # 写入内容部分，只填充 text 列，label 列留空
        for comment in comments:
            writer.writerow({"label": "", "text": comment["text"]})

    print(f"符合条件的评论已追加到 {filename}")


# 主函数
def main():
    redis_conn = get_redis_connection()
    keys_pattern = "*:cm"  # 使用 Redis 键模式查找所有评论键（假设所有评论键以 ":cm" 结尾）

    comments = get_comments_from_redis(redis_conn, keys_pattern)
    export_comments_to_csv(comments)


if __name__ == "__main__":
    main()
