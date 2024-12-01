import cv2
import os
import time
import sys

def register_face(face_id, output_dir='registered_faces', screenshot_dir='screenshots'):
    # 创建用于存储人脸和截图的文件夹
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    #初始化摄像头
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("无法打开摄像头")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("请保持正对摄像头，按 'q' 退出录入。")
    count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("无法读取摄像头画面")
            break

        #转换为灰度图以减少错误
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            # 保存人脸和截图
            cv2.imwrite(f"{output_dir}/{face_id}_{count}.png", face_roi)
            cv2.imwrite(f"{screenshot_dir}/{face_id}_{count}.png", frame)
            count += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Register Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print(f"人脸录入完成")


def load_registered_faces(face_dir='registered_faces'):
    # 加载已注册的人脸数据
    return [cv2.imread(os.path.join(face_dir, filename), cv2.IMREAD_GRAYSCALE)
            for filename in os.listdir(face_dir) if
            cv2.imread(os.path.join(face_dir, filename), cv2.IMREAD_GRAYSCALE) is not None]


def compare_faces(face1, face2):
    # 比较两张人脸图片的直方图相似度
    hist1 = cv2.calcHist([face1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([face2], [0], None, [256], [0, 256])
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)


def face_unlock():
    # 使用摄像头检测人脸并与注册人脸对比解锁
    registered_faces = load_registered_faces()
    if not registered_faces:
        print("未检测到录入人脸数据，请先录入人脸。")
        return False

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("无法打开摄像头")
        return False

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("开始人脸检测")

    start_time = time.time()
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("无法获取摄像头画面")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        # 超过15秒未检测到匹配人脸则退出
        if time.time() - start_time > 15:
            print("超过15秒未检测到指定人脸，程序终止。")
            video_capture.release()
            cv2.destroyAllWindows()
            sys.exit("警告：程序因未检测到指定人脸而终止。")

        for (x, y, w, h) in faces:
            face_roi = gray_frame[y:y + h, x:x + w]
            for registered_face in registered_faces:
                resized_face = cv2.resize(face_roi, (registered_face.shape[1], registered_face.shape[0]))
                if compare_faces(resized_face, registered_face) > 0.75:
                    print("人脸解锁成功！")
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return True

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Face Unlock", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return False


def face_detection():
    # 持续监控摄像头中的人脸，超过5分钟无检测则进入休眠模式
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("无法打开摄像头")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    start_time = time.time()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("无法获取摄像头画面")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            start_time = time.time()  # 检测到人脸则重置计时
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        elif time.time() - start_time >= 300:
            # 超过5分钟未检测到人脸则进入休眠模式
            video_capture.release()
            cv2.destroyAllWindows()
            print("超过5分钟未检测到人脸，进入休眠模式...")
            return

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("程序手动退出")
            break

    video_capture.release()
    cv2.destroyAllWindows()
