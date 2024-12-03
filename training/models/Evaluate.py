import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Windows 系统下可以使用 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 如果你在 macOS 或 Linux 上，可以尝试使用 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 定义情感标签
id2label = {0: "积极", 1: "消极", 2: "中性", 3: "愤怒"}
label2id = {v: k for k, v in id2label.items()}

# 定义模型和分词器
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

# 加载测试数据
print("加载测试数据集...")
data_path = 'D:/VsCode/Code/Python/BigHomework/finalproject/training/data/train/usual_test_labeled4.csv'
try:
    df = pd.read_csv(data_path, encoding='utf-8')  # 更改为适合你文件的编码
    print("CSV文件加载成功！")
except Exception as e:
    print(f"加载CSV文件失败: {e}")
    exit()


# 分析情感的函数
def analyze_emotion(text):
    model.eval()
    # 使用模型进行情感分析
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", max_length=128, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_class = torch.argmax(logits, dim=1).item()
        score = torch.softmax(logits, dim=1).max().item()
    emotion = id2label.get(predicted_class, "未知")
    return emotion, predicted_class


# 用来存储模型预测和真实标签
predictions = []
true_labels = []

# 对每一条测试数据进行分析
print("开始对测试集进行情感分析...")
for index, row in df.iterrows():
    text = row['文本']
    true_label = row['情绪标签']

    # 获取预测情绪
    emotion, predicted_class = analyze_emotion(text)

    # 保存预测结果和真实标签
    predictions.append(predicted_class)
    true_labels.append(label2id.get(true_label, -1))

# 计算正确率
accuracy = accuracy_score(true_labels, predictions)
print(f"模型在测试集上的准确率: {accuracy * 100:.2f}%")

# 将情感分析结果写入第三列
print("将预测结果写入到CSV文件...")
df['预测情绪'] = [id2label.get(pred, "未知") for pred in predictions]

# 保存带预测结果的文件
df.to_csv('D:/VsCode/Code/Python/BigHomework/finalproject/training/data/usual_test_labeled_with_predictions.csv', index=False)
print("预测结果已保存到 'usual_test_labeled_with_predictions.csv'")

# 绘制正确率可视化图（混淆矩阵）
print("开始绘制混淆矩阵...")

from sklearn.metrics import confusion_matrix
import seaborn as sns

# 计算混淆矩阵
cm = confusion_matrix(true_labels, predictions, labels=[0, 1, 2, 3])

# 清理掉全零行和全零列
cm_cleaned = cm[(cm != 0).any(axis=1)]  # 删除全零行
cm_cleaned = cm_cleaned[:, (cm_cleaned != 0).any(axis=0)]  # 删除全零列

# 可视化混淆矩阵
plt.figure(figsize=(8, 6))
sns.heatmap(cm_cleaned, annot=True, fmt="d", cmap="Blues", xticklabels=id2label.values(), yticklabels=id2label.values())
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix of Sentiment Analysis Model')
plt.show()

print("混淆矩阵已绘制完成。")


