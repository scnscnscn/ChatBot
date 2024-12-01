import os
from docx import Document

def read_docx_files(directory):

    file_contents = {}

    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"目录 '{directory}' 不存在。")
        return file_contents

    # 遍历目录中的文件
    for filename in os.listdir(directory):
        # 只处理 .docx 文件
        if filename.endswith(".docx"):
            file_path = os.path.join(directory, filename)
            try:
                # 读取文件内容并提取文本
                doc = Document(file_path)
                content = "\n".join(paragraph.text for paragraph in doc.paragraphs)
                file_contents[filename] = content  # 添加到字典中
            except Exception as e:
                # 错误处理，提示用户读取失败的文件
                print(f"读取文件 {filename} 时出错: {e}")

    # 如果没有找到任何 .docx 文件，则提示用户
    if not file_contents:
        print("未找到任何 .docx 文件。")

    return file_contents
