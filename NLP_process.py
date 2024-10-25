import os
from transformers import pipeline
import os
import tensorflow as tf

def get_emotion_classifier():
    return pipeline(
        "sentiment-analysis",
        model="IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",  # 使用中文情绪分析模型
    )

def analyze_emotion(text):
    emotion_classifier = get_emotion_classifier()
    result = emotion_classifier(text)
    label = result[0]['label']
    score = result[0]['score']

    if label == "positive":
        emotion = "积极"
    elif label == "negative":
        emotion = "消极"
    else:
        emotion = "中立"

    return emotion, score

if __name__ == "__main__":
    user_input = input("请输入一句话进行情绪分析: ")
    emotion, score = analyze_emotion(user_input)
    print(f"分析结果: 情绪为{emotion}，置信度为{score:.2f}")
