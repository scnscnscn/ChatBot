import redis
import json
import csv
import re

def get_redis_connection():
    return redis.StrictRedis(host='localhost', port=6379, db=0)


def is_valid_comment(comment_text, existing_comments):
    comment_text = re.sub(r'^.*?：', '', comment_text)
    comment_text = re.sub(r'【.*?】', '', comment_text)
    comment_text = re.sub(r'[^a-zA-Z0-9一-鿿。！？…、，；：“”‘’【】,.?!;:\-\(\)\[\]\{\}]', '', comment_text)
    comment_text = re.sub(r'\[.*?\]', '', comment_text)
    comment_text = re.sub(r'【.*?】', '', comment_text)

    if len(comment_text) < 5:
        return False
    if comment_text in existing_comments:
        return False
    existing_comments.add(comment_text)

    return comment_text

def get_comments_from_redis(redis_conn, keys_pattern):
    keys = redis_conn.keys(keys_pattern)
    comments = []
    existing_comments = set()

    for key in keys:
        comment_list = redis_conn.lrange(key, 0, -1)
        for comment_json in comment_list:
            comment_json = comment_json.decode("utf-8")
            comment = json.loads(comment_json)
            comment_text = comment.get("text", "")

            cleaned_text = is_valid_comment(comment_text, existing_comments)
            if cleaned_text:
                comments.append({"text": cleaned_text})

    return comments

def export_comments_to_csv(comments, filename="data3.csv"):
    if not comments:
        print("没有找到符合条件的评论数据！")
        return

    with open(filename, mode='a', newline='', encoding='utf_8_sig') as file:
        writer = csv.DictWriter(file, fieldnames=["label", "text"])

        if file.tell() == 0:
            writer.writeheader()

        for comment in comments:
            writer.writerow({"label": "", "text": comment["text"]})

    print(f"符合条件的评论已追加到 {filename}")

def main():
    redis_conn = get_redis_connection()
    keys_pattern = "*:cm"

    comments = get_comments_from_redis(redis_conn, keys_pattern)
    export_comments_to_csv(comments)


if __name__ == "__main__":
    main()
