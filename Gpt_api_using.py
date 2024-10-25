import openai
import os
from docx import Document

class GptAssistant:
    def __init__(self, api_key, api_base):
        # 初始化 OpenAI 客户端
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        self.conversation_history = [
            {"role": "system", "content": "You are an AI assistant designed to engage in multi-turn conversations."}
        ]

    def chat(self, user_input):
        # 添加用户输入到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        try:
            # 获取 AI 响应
            completion = self.client.chat.completions.create(
                model="yi-large",
                messages=self.conversation_history
            )
            ai_response = completion.choices[0].message.content
            print(f"AI: {ai_response}")
            # 添加 AI 响应到对话历史
            self.conversation_history.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            print(f"Error: {e}")

    def analyze_document(self, directory_path):
        file_contents = {}
        for filename in os.listdir(directory_path):
            if filename.endswith(".docx"):
                file_path = os.path.join(directory_path, filename)
                try:
                    # 读取文档内容
                    doc = Document(file_path)
                    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    file_contents[filename] = content
                    ai_input = f"帮我总结如下内容：{content}"
                    self.chat(ai_input)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    def emotion_support(self, emotion):
        if emotion == "消极":
            ai_input = "我心情不好能安慰我一下吗"
            self.chat(ai_input)

