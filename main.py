# 导入必要的模块
import os
# 禁用 oneDNN 自定义操作日志输出
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import threading
import Bad_World_Detector
import Gpt_api_using
import NLP_process
import Face_identify
import sys
import tensorflow as tf
from transformers import logging as transformers_logging

# 设置 TensorFlow 和 Transformers 的日志级别以抑制不必要的输出
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('FATAL')
transformers_logging.set_verbosity_error()

def main():
    # 硬编码 API 密钥
    api_key = "2d87d52dc0314e2599cf37f16639ab61"
    assistant = Gpt_api_using.GptAssistant(api_key=api_key, api_base="https://api.lingyiwanwu.com/v1")
    bad_words = Bad_World_Detector.load_bad_words('bad_words.txt')

    print("与 AI 聊天（输入 'exit' 结束，输入 'analyze doc' 分析文档）：")
    while True:
        user_input = input("你: ").strip()

        if user_input.lower() == 'exit':
            print("再见！")
            break

        if user_input.lower() == 'analyze doc':
            directory_path = "./documents"
            try:
                assistant.analyze_document(directory_path)
            except FileNotFoundError:
                print(f"未找到目录 '{directory_path}'。")
            continue

        if Bad_World_Detector.check_for_bad_words(user_input, bad_words):
            print("请避免使用不恰当的语言。")
            continue

        emotion, score = NLP_process.analyze_emotion(user_input)
        print(f"情绪分析结果: {emotion}，置信度为: {score:.2f}")

        assistant.emotion_support(emotion)

        assistant.chat(user_input)

if __name__ == "__main__":
    # 启动人脸识别线程
    camera_thread = threading.Thread(target=Face_identify.face_detection)
    camera_thread.start()
    main()