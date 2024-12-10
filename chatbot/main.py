import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel,
    QHBoxLayout, QDialog, QFileDialog, QMessageBox
)
import threading
import os
import Bad_World_Detector
import Gpt_api_using
import NLP_process
import Face_identify
from docx import Document

def read_docx_file(file_path):
    if not os.path.exists(file_path):
        print(f"文件 '{file_path}' 不存在。")
        return None

    try:
        doc = Document(file_path)
        content = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return content
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None
class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_key = "2d87d52dc0314e2599cf37f16639ab61"
        self.assistant = Gpt_api_using.GptAssistant(api_key=self.api_key, api_base="https://api.lingyiwanwu.com/v1")
        self.bad_words = Bad_World_Detector.load_bad_words('bad_words.txt')
        self.face_detection_event = threading.Event()
        self.initUI()
        self.register_or_unlock_face()

    def initUI(self):
        self.setWindowTitle("智能聊天助手")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        self.exit_button = QPushButton("退出")
        self.exit_button.clicked.connect(self.exit_program)
        self.analyze_button = QPushButton("分析文档")
        self.analyze_button.clicked.connect(self.analyze_document)
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.exit_button)
        input_layout.addWidget(self.analyze_button)
        layout.addLayout(input_layout)

        self.emotion_label = QLabel("情绪分析结果：")
        layout.addWidget(self.emotion_label)
        self.score_label = QLabel("置信度：")
        layout.addWidget(self.score_label)

        self.user_input.returnPressed.connect(self.send_message)

        threading.Thread(target=Face_identify.face_detection, args=(self.face_detection_event,), daemon=True).start()

    def register_or_unlock_face(self):
        face_dir = 'registered_faces'
        if not os.path.exists(face_dir) or len(os.listdir(face_dir)) == 0:
            face_id = self.prompt_for_face_id()
            if face_id:
                Face_identify.register_face(face_id)
            else:
                self.close()
                return False
        else:
            if not Face_identify.face_unlock():
                self.close()
                return False
        return True

    def prompt_for_face_id(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("人脸录入")
        layout = QVBoxLayout(dialog)
        label = QLabel("请录入您的ID以注册人脸：")
        line_edit = QLineEdit()
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)
        dialog.exec_()
        return line_edit.text()

    def send_message(self):
        user_input = self.user_input.text().strip()
        self.user_input.clear()

        if user_input.lower() == 'exit':
            self.exit_program()
            return

        self.append_to_chat(f"你: {user_input}")
        emotion, score = NLP_process.analyze_emotion(user_input)
        self.emotion_label.setText(f"情绪分析结果：{emotion}")
        self.score_label.setText(f"置信度：{score:.2f}")

        if Bad_World_Detector.check_for_bad_words(user_input, self.bad_words):
            self.append_to_chat("请避免使用不恰当的语言。")
            return

        response = self.assistant.chat(user_input)

        self.append_to_chat(f"AI: {response}")

    def append_to_chat(self, message):
        self.text_area.append(message)

    def analyze_document(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择Word文档", "", "Word Documents (*.docx)")
        if filename:
            content = read_docx_file(filename)
            if content:
                summary = self.assistant.chat(f"请总结以下内容：\n{content}")
                self.append_to_chat(f"文件 '{filename}' 的总结：\n{summary}")
            else:
                self.append_to_chat("文件读取失败或文件为空。")

    def exit_program(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = ChatApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()