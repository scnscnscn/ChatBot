import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
id2label = {0: "积极", 1: "消极", 2: "中性", 3: "愤怒"}
label2id = {v: k for k, v in id2label.items()}

print("加载BERT模型和分词器...")
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=4)
model.config.id2label = id2label
model.config.label2id = label2id

model_path = "D:/VsCode/Code/Python/BigHomework/finalproject/training/model.safetensors"
try:
    from safetensors.torch import load_file

    state_dict = load_file(model_path)
    model.load_state_dict(state_dict)
    print("模型权重加载成功。")
except Exception as e:
    print(f"模型权重加载失败: {e}")
    exit()

print("加载测试数据集...")
data_path = r'C:\Users\WLQVi\Desktop\python\finalproject\body\training\data\test\test.csv'
try:
    df = pd.read_csv(data_path, encoding='utf-8')
    print("CSV文件加载成功！")
except Exception as e:
    print(f"加载CSV文件失败: {e}")
    exit()

def analyze_emotion(text):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", max_length=128, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_class = torch.argmax(logits, dim=1).item()
        score = torch.softmax(logits, dim=1).max().item()
    emotion = id2label.get(predicted_class, "未知")
    return emotion, predicted_class

predictions = []
true_labels = []

print("开始对测试集进行情感分析...")
for index, row in df.iterrows():
    text = row['文本']
    true_label = row['情绪标签']

    emotion, predicted_class = analyze_emotion(text)

    predictions.append(predicted_class)
    true_labels.append(label2id.get(true_label, -1))

accuracy = accuracy_score(true_labels, predictions)
print(f"模型在测试集上的准确率: {accuracy * 100:.2f}%")

print("将预测结果写入到CSV文件...")
df['预测情绪'] = [id2label.get(pred, "未知") for pred in predictions]

df.to_csv('usual_test_labeled_with_predictions.csv', index=False)
print("预测结果已保存到 'usual_test_labeled_with_predictions.csv'")



from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np

def analyze_emotion(text):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", max_length=128, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]  # 获取概率分布
        predicted_class = torch.argmax(logits, dim=1).item()
    emotion = id2label.get(predicted_class, "未知")
    return emotion, predicted_class, probabilities

predictions_prob = []
true_labels = []

for index, row in df.iterrows():
    text = row['文本']
    true_label = row['情绪标签']
    emotion, predicted_class, probabilities = analyze_emotion(text)
    predictions_prob.append(probabilities)
    true_labels.append(label2id.get(true_label, -1))

true_labels_binarized = label_binarize(true_labels, classes=[0, 1, 2, 3])

n_classes = 4
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(true_labels_binarized[:, i], np.array(predictions_prob)[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

plt.figure()
colors = ['aqua', 'darkorange', 'cornflowerblue', 'green']
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=2,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic for multi-class')
plt.legend(loc="lower right")
plt.show()
print("混淆矩阵已绘制完成。")


