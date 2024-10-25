import os
from docx import Document

def read_docx_files(directory):
    file_contents = {}

    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            file_path = os.path.join(directory, filename)
            try:
                doc = Document(file_path)
                content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                file_contents[filename] = content
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return file_contents



