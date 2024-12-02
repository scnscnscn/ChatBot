import requests
import re
from typing import List, Tuple

class Hot:
    def __init__(self, desc: str, scheme: str):
        self.desc = desc
        self.scheme = scheme

class Weibo:
    def __init__(self, id: str, user: str, pic: str, time: str, url: str, content: str):
        self.id = id
        self.user = user
        self.pic = pic
        self.time = time
        self.url = url
        self.content = content

class Comment:
    def __init__(self, text: str, time: str, like_count: int):
        self.text = text
        self.time = time
        self.like_count = like_count

class WeiboParser:

    @staticmethod
    def get_hot_list(url: str, size: int) -> List[Hot]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print("获取热搜列表失败:", e)
            return []

        hot_list = []
        groups = data.get("data", {}).get("cards", [])[0].get("card_group", [])
        for count, node in enumerate(groups[1:size + 1], start=1):  # 跳过置顶热搜
            desc = node.get("desc", "")
            scheme = node.get("scheme", "")
            hot_list.append(Hot(desc, scheme))

        return hot_list

    @staticmethod
    def get_weibo_list(hot: Hot, size: int) -> List[Weibo]:
        api_url = hot.scheme.replace("https://m.weibo.cn/search",
                                     "https://m.weibo.cn/api/container/getIndex") + "&page_type=searchall"
        weibo_list = []

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            cards = data.get("data", {}).get("cards", [])

            for count, card in enumerate(cards):
                if card.get("card_type", 0) != 9:
                    continue
                if count >= size:
                    break

                mblog = card.get("mblog", {})
                weibo_id = mblog.get("id", "")
                user = mblog.get("user", {}).get("screen_name", "")
                pic = mblog.get("user", {}).get("profile_image_url", "")
                url = f"https://m.weibo.cn/status/{weibo_id}"
                html_content = requests.get(url).text
                time = WeiboParser.get_time(html_content)
                content = WeiboParser.get_content(html_content)

                weibo_list.append(Weibo(weibo_id, user, pic, time, url, content))

        except Exception as e:
            print("解析微博列表失败:", e)

        return weibo_list

    @staticmethod
    def get_comment_list(weibo: Weibo, page_size: int) -> List[Comment]:
        comment_list = []
        next_params = ("0", "0")
        for _ in range(page_size):
            max_id, max_id_type = next_params
            next_params = WeiboParser.parse_comment(weibo, comment_list, max_id, max_id_type)
            if not next_params or next_params == "00":
                break

        return comment_list

    @staticmethod
    def parse_comment(weibo: Weibo, comment_list: List[Comment], max_id: str, max_id_type: str) -> Tuple[str, str]:
        url = f"https://m.weibo.cn/comments/hotflow?id={weibo.id}&mid={weibo.id}&max_id={max_id}&max_id_type={max_id_type}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            comments_data = data.get("data", {}).get("data", [])
            max_id = data.get("data", {}).get("max_id", "0")
            max_id_type = data.get("data", {}).get("max_id_type", "0")

            for node in comments_data:
                time = node.get("created_at", "")
                like_count = node.get("like_count", 0)
                text = WeiboParser.process_text(node.get("text", ""))

                if text.strip() and text not in ["图片评论", "转发微博"]:
                    comment_list.append(Comment(text, time, like_count))

            return max_id_type + max_id if max_id and max_id_type else "00"

        except Exception as e:
            print("解析评论列表失败:", e)
            return "00"

    @staticmethod
    def get_time(html: str) -> str:
        match = re.search(r'"created_at": "([^"]+)"', html)
        return match.group(1) if match else "获取时间失败"

    @staticmethod
    def get_content(html: str) -> str:
        match = re.search(r'"text": "([^"]+)"', html)
        return WeiboParser.process_text(match.group(1)) if match else "获取正文失败"

    @staticmethod
    def process_text(text: str) -> str:
        text = re.sub(r'<span class="url-icon"><img alt="([^"]+)"[^>]*></span>', r'\1', text)
        return re.sub(r'<[^>]+>', '', text)
