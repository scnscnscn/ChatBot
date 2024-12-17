from transformers import BertTokenizer, BertForSequenceClassification
from safetensors.torch import load_file
import torch
id2label = {0: "积极", 1: "消极", 2: "中性", 3: "愤怒"}
label2id = {v: k for k, v in id2label.items()}

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=4)
model.config.id2label = id2label
model.config.label2id = label2id

model_path = "model.safetensors"
try:
    state_dict = load_file(model_path)
    model.load_state_dict(state_dict)
    print("模型权重加载成功。")
except Exception as e:
    print(f"模型权重加载失败: {e}")
    exit()

def analyze_emotion(text):
    model.eval()

    inputs = tokenizer(text, return_tensors="pt", padding="max_length", max_length=128, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_class = torch.argmax(logits, dim=1).item()
        score = torch.softmax(logits, dim=1).max().item()
    emotion = id2label.get(predicted_class, "未知")
    return emotion, score
