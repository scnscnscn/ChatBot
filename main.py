import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import threading
import Bad_World_Detector
import Gpt_api_using
import NLP_process
import Face_identify
import tensorflow as tf
from transformers import logging as transformers_logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('FATAL')
transformers_logging.set_verbosity_error()

def initialize_assistant():
    # 初始化GPT助手和敏感词过滤库
    api_key = "2d87d52dc0314e2599cf37f16639ab61"
    assistant = Gpt_api_using.GptAssistant(api_key=api_key, api_base="https://api.lingyiwanwu.com/v1")
    bad_words = Bad_World_Detector.load_bad_words('bad_words.txt')
    return assistant, bad_words


def register_or_unlock_face():
    # 人脸注册或解锁：首次运行要求注册人脸，后续直接解锁
    face_dir = 'registered_faces'
    if not os.path.exists(face_dir) or len(os.listdir(face_dir)) == 0:
        # 如果没有注册人脸，则提示用户进行人脸录入
        print("首次使用，请录入人脸信息。")
        face_id = input("请输入您的ID以录入人脸：")
        Face_identify.register_face(face_id)
    else:
        # 检测已注册人脸，进行解锁尝试
        print("正在进行人脸检测解锁。")
        if Face_identify.face_unlock():
            print("系统解锁成功，您现在可以继续与AI进行交互。")
            return True
        else:
            print("解锁失败，程序将退出。")
            return False
    return True


def chat_with_ai(assistant, bad_words):
    # 与AI进行互动聊天，支持文档分析和敏感词过滤
    print("与AI聊天（输入 'exit' 退出，'analyze doc' 分析文档）：")
    while True:
        user_input = input("你: ").strip()

        # 输入 'exit' 退出程序
        if user_input.lower() == 'exit':
            print("再见！")
            break

        # 输入 'analyze doc' 触发文档分析功能
        elif user_input.lower() == 'analyze doc':
            try:
                assistant.analyze_documents("./Documents")
            except FileNotFoundError:
                print("未找到目录 'Documents'。")
            continue

        # 检查输入内容是否包含敏感词
        elif Bad_World_Detector.check_for_bad_words(user_input, bad_words):
            print("请避免使用不恰当的语言。")
            continue

        # 情绪分析并显示结果
        emotion, score = NLP_process.analyze_emotion(user_input)
        print(f"情绪分析结果: {emotion}，置信度: {score:.2f}")

        # 调用GPT助手生成回应
        response = assistant.chat(user_input)
        print(f"AI的回应: {response}")


def main():
    # 初始化助手和敏感词库
    assistant, bad_words = initialize_assistant()

    # 人脸注册或解锁
    if not register_or_unlock_face():
        return

    # 启动人脸监控线程，持续检测人脸
    threading.Thread(target=Face_identify.face_detection, daemon=True).start()

    # 进入聊天功能
    chat_with_ai(assistant, bad_words)


# 程序入口
if __name__ == "__main__":
    main()
