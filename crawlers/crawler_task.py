import time
import redis
from datetime import datetime
from weibo_parser import WeiboParser, Hot, Weibo, Comment
import json


class RedisUtil:
    @staticmethod
    def get_redis_connection():
        return redis.StrictRedis(host='localhost', port=6379, db=0)


class CrawlTask:
    HOT_LIST_SIZE = 30  # 热搜数量
    WB_LIST_SIZE = 20  # 每个热搜下微博数量
    CM_LIST_SIZE = 50  # 每条微博评论页数
    KEY_EXPIRE_TIME = 60 * 60  # Redis key过期时间（秒）

    def __init__(self):
        self.redis_conn = RedisUtil.get_redis_connection()

    def run(self):
        start_time = datetime.now()
        print(f"### 开始爬取微博 {start_time.strftime('%Y-%m-%d %H:%M:%S')} ###")
        try:
            self.crawl()
        except Exception as e:
            print("爬取任务失败:", e)
        end_time = datetime.now()
        print(f"### 爬取微博结束，耗时：{(end_time - start_time).total_seconds()} 秒 ###")

    def crawl(self):
        timestamp = int(time.time())
        url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C"

        hot_list = WeiboParser.get_hot_list(url, self.HOT_LIST_SIZE)

        for i, hot in enumerate(hot_list, start=1):
            hot_key = f"{timestamp}:hot:{i}"
            self.insert_hot(hot_key, hot)

            weibo_list = WeiboParser.get_weibo_list(hot, self.WB_LIST_SIZE)
            all_pos_count, all_neg_count = 0, 0

            for j, weibo in enumerate(weibo_list, start=1):
                wb_key = f"{hot_key}:wb:{j}"
                self.insert_weibo(wb_key, weibo)

                comment_list = WeiboParser.get_comment_list(weibo, self.CM_LIST_SIZE)
                cm_key = f"{wb_key}:cm"
                pos_count, neg_count, other_count = 0, 0, 0

                for comment in comment_list:
                    score = self.classify_comment(comment.text)
                    comment.score = score
                    self.insert_comment(cm_key, comment)

                    if score > 0:
                        pos_count += 1
                        all_pos_count += 1
                    elif score < 0:
                        neg_count += 1
                        all_neg_count += 1
                    else:
                        other_count += 1

                self.redis_conn.expire(cm_key, self.KEY_EXPIRE_TIME)
                self.redis_conn.hset(wb_key,
                                     mapping={"posCount": pos_count, "negCount": neg_count, "otherCount": other_count})
                time.sleep(3)

            status = 0 if (all_pos_count + all_neg_count) == 0 else (all_pos_count - all_neg_count) / (
                        all_pos_count + all_neg_count)
            self.redis_conn.hset(hot_key, "status", status)

        self.redis_conn.lpush("timestamp", timestamp)

    def insert_hot(self, key: str, hot: Hot):
        hot_data = {"desc": hot.desc, "scheme": hot.scheme}
        self.redis_conn.hmset(key, hot_data)
        self.redis_conn.expire(key, self.KEY_EXPIRE_TIME)
        print(f"Hot Insert: {hot.desc}")

    def insert_weibo(self, key: str, weibo: Weibo):
        weibo_data = {
            "id": weibo.id,
            "url": weibo.url,
            "user": weibo.user,
            "pic": weibo.pic,
            "time": weibo.time,
            "content": weibo.content
        }
        self.redis_conn.hmset(key, weibo_data)
        self.redis_conn.expire(key, self.KEY_EXPIRE_TIME)

    def insert_comment(self, key: str, comment: Comment):
        comment_json = json.dumps(comment.__dict__)
        self.redis_conn.rpush(key, comment_json)

    def classify_comment(self, text: str) -> float:
        return len(text) % 3 - 1
