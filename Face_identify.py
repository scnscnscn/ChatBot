import cv2
import time

def face_detection():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("无法打开摄像头")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    start_time = time.time()
    face_not_detected_duration = 0
    ai_active = True

    while ai_active:
        ret, frame = video_capture.read()
        if not ret:
            print("无法获取摄像头画面")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            face_not_detected_duration = 0
            start_time = time.time()

            # 在框内绘制人脸
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        else:
            face_not_detected_duration = time.time() - start_time


        if face_not_detected_duration >= 300:  # 超过5分钟未检测到人脸
            print("超过5分钟未检测到人脸，进入休眠模式...")
            video_capture.release()
            cv2.destroyAllWindows()

            # 等待用户输入来唤醒AI
            input("输入任意值以唤醒AI: ")
            print("AI已唤醒，重新检测人脸...")
            video_capture = cv2.VideoCapture(0)
            if not video_capture.isOpened():
                print("无法重新打开摄像头")
                break
            start_time = time.time()  # 重置计时
            face_not_detected_duration = 0  # 重置无检测时间

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("程序手动退出")
            break

    video_capture.release()
    cv2.destroyAllWindows()
