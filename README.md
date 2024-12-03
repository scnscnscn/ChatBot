# Chatbot

Chatbot是一个基于零一万物的Yi-Lightning框架开发的聊天程序，集成了多种智能功能，包括人脸生物信息解锁、离屏检测、脏话识别、文档分析以及用户输入的语义分析。

## 功能特点

- **人脸生物信息解锁**：利用先进的人脸识别技术，提供安全的身份验证。
- **离屏检测**：能够检测用户是否在屏幕前，以优化交互体验。
- **脏话识别**：自动检测并过滤不文明用语，保持交流环境的清洁。本地脏话字典实现
- **文档分析**：分析指定目录下文档内容，提取关键信息。
- **语义分析**：基于`simplifyweibo_4_moods.csv`训练的BERT模型，对用户输入进行深入的语义分析。

## 语义分析模型

本项目的语义分析功能使用了基于`simplifyweibo_4_moods.csv`数据集训练的BERT模型。该模型能够理解用户输入的语境和情感，提供更精准的响应。

## 测试集评估

我们提供了程序来评估模型对给定测试集的效果。您可以使用这些工具来测试和验证模型的性能。

## 微博热搜爬虫

本项目还包含了一个微博热搜爬虫（redis），它可以爬取自定义数量的热搜话题下的评论。此外，还提供了一个能够根据本地字典过滤掉不需要内容的程序，以提高数据的质量和相关性。

## 安装指南

1. 确保您的环境中安装了Python 3.8或更高版本。
2. 安装所需的依赖项：
   ```bash
   pip install -r requirements.txt
   ```
3. 克隆项目代码到本地：
   ```bash
   git clone https://github.com/yourusername/yi-lightning-chat-program.git
   cd yi-lightning-chat-program
   ```
## 贡献

我们欢迎任何形式的贡献，包括代码提交、文档改进、bug报告等。请遵循我们的[贡献指南](CONTRIBUTING.md)。
##项目结构
C:.
├─chatbot
│  └─Documents（存放需要分析的文档）
├─crawlers
└─training
    ├─data
    │  ├─test（较新的测试集）
    │  └─train（公开但是较老的数据集）
    └─models

## 许可证

本项目采用[MIT License](LICENSE)。

