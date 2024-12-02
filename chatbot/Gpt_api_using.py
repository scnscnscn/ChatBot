import openai
from Doc_reading import read_docx_files


class GptAssistant:

    def __init__(self, api_key, api_base):
        # 初始化OpenAI API客户端
        self.client = openai.OpenAI(api_key=api_key, base_url=api_base)
        self.conversation_history = [
            {"role": "system", "content": "You are an AI assistant designed to engage in multi-turn conversations."}
        ]

    def chat(self, user_input):

        # 添加用户输入到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        try:
            # 发送对话请求并接收AI回复
            response = self.client.chat.completions.create(model="yi-large", messages=self.conversation_history)
            ai_response = response.choices[0].message.content
            # 将AI回复添加到对话历史中
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            # 捕捉异常并返回错误信息
            return f"Error: {e}"

    def analyze_documents(self, directory_path):

        # 使用read_docx_files读取文件内容
        file_contents = read_docx_files(directory_path)

        # 遍历每个文件，进行内容分析
        for filename, content in file_contents.items():
            # 发送请求让GPT总结内容
            summary = self.chat(f"帮我总结如下内容：{content}")
            print(f"{filename} - Summary:\n{summary}")
