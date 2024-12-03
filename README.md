# Chatbot

Chatbot is a conversational program developed based on the Yi-Lightning framework from Moonshot AI, integrating multiple intelligent features including facial biometric unlock, screen-off detection, profanity recognition, document analysis, and semantic analysis of user input.

## Features

- **Facial Biometric Unlock**: Utilizes advanced facial recognition technology to provide secure identity authentication.
- **Screen-off Detection**: Detects whether the user is in front of the screen to optimize the interaction experience.
- **Profanity Recognition**: Automatically detects and filters out offensive language to maintain a clean communication environment. Implemented with a local profanity dictionary.
- **Document Analysis**: Analyzes the content of documents in a specified directory, extracting key information.
- **Semantic Analysis**: Utilizes a BERT model trained on the `simplifyweibo_4_moods.csv` dataset to conduct in-depth semantic analysis of user input.

## Semantic Analysis Model

The semantic analysis feature of this project uses a BERT model trained on the `simplifyweibo_4_moods.csv` dataset. This model can understand the context and emotions of user input, providing more accurate responses.

## Test Set Evaluation

We provide programs to evaluate the model's performance on given test sets. You can use these tools to test and verify the model's performance.

## Weibo Hot Search Crawler

This project also includes a Weibo hot search crawler (redis) that can crawl comments under custom numbers of hot search topics. Additionally, a program is provided to filter out unwanted content based on a local dictionary, improving the quality and relevance of the data.

## Installation Guide

1. Ensure that Python 3.8 or higher is installed in your environment.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Clone the project code to your local machine:
   ```bash
   git clone https://github.com/scnscnscn/ChatBot.git 
   ```

## Contribution

We welcome any form of contribution, including code submissions, documentation improvements, bug reports, etc. Please follow our [Contribution Guidelines](CONTRIBUTING.md).

## Project Structure
```
C:.
├─chatbot
│  └─Documents（Directory for documents to be analyzed）
├─crawlers
└─training
    ├─data
    │  ├─test（Recent test sets）
    │  └─train（Public but older datasets）
    └─models
```

## License

This project is licensed under the [MIT License](LICENSE).

---

Please note that the link provided for cloning the project may not work due to network issues. If you encounter problems accessing the link, please check the legality of the web page link and try again. If the issue persists, it may be related to the link itself or network connectivity, and you may need to seek alternative methods to obtain the project code.
