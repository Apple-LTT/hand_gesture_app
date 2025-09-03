import cv2
import numpy as np
import PySimpleGUI as sg
import mediapipe as mp


class HandGestureApp:
    def __init__(self):
        # 初始化MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # 初始化GUI
        self.layout = [
            [sg.Text('手势识别程序', size=(30, 1), justification='center', font=("Helvetica", 25))],
            [sg.Image(filename='', key='image')],
            [sg.Text('检测到的手势: ', size=(20, 1), font=("Helvetica", 15), key='gesture')],
            [sg.Button('开始', size=(10, 1)), sg.Button('退出', size=(10, 1))]
        ]

        self.window = sg.Window('手势识别', self.layout, location=(100, 100))
        self.cap = None
        self.is_running = False

    def recognize_gesture(self, hand_landmarks):
        """根据手部关键点识别手势"""
        # 获取关键点坐标
        landmarks = hand_landmarks.landmark

        # 计算手指状态
        fingers = []

        # 拇指: 比较拇指尖和拇指根部的x坐标
        if landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x < landmarks[self.mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # 其他四指: 比较指尖和指关节的y坐标
        for tip, pip in [(self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP),
                         (self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                         (self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP),
                         (self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP)]:
            if landmarks[tip].y < landmarks[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)

        # 根据手指状态判断手势
        total_fingers = fingers.count(1)

        if total_fingers == 0:
            return "握拳"
        elif total_fingers == 5:
            return "张开手掌"
        elif fingers == [0, 1, 0, 0, 0]:
            return "食指指向"
        elif fingers == [0, 1, 1, 0, 0]:
            return "胜利手势"
        elif total_fingers == 1 and fingers[0] == 1:
            return "竖大拇指"
        else:
            return f"{total_fingers}根手指"

    def run(self):
        """运行主程序"""
        while True:
            event, values = self.window.read(timeout=20)

            if event == '退出' or event == sg.WIN_CLOSED:
                break

            elif event == '开始':
                if not self.is_running:
                    self.cap = cv2.VideoCapture(0)
                    self.is_running = True
                    self.window['开始'].update('停止')
                else:
                    self.cap.release()
                    self.is_running = False
                    self.window['开始'].update('开始')

            if self.is_running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # 水平翻转图像
                    frame = cv2.flip(frame, 1)

                    # 转换颜色空间 BGR to RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # 处理图像并检测手部
                    results = self.hands.process(rgb_frame)

                    gesture_text = "未检测到手部"

                    # 绘制手部关键点和连接线
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                            # 识别手势
                            gesture_text = self.recognize_gesture(hand_landmarks)

                    # 更新GUI
                    img_bytes = cv2.imencode('.png', frame)[1].tobytes()
                    self.window['image'].update(data=img_bytes)
                    self.window['gesture'].update(f'检测到的手势: {gesture_text}')

        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.window.close()


if __name__ == '__main__':
    app = HandGestureApp()
    app.run()