import cv2
import PySimpleGUI as sg
import mediapipe as mp
from gesture_recognizer import get_straight_finger_tips, recognize_gesture
from hand_tracker import RegionTracker


sg.theme('DarkBlack1')  # 接近全黑主题

# 初始化MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands_model = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                             min_detection_confidence=0.7, min_tracking_confidence=0.5)

tracker = RegionTracker(iou_threshold=0.3, target_frames=30)

# GUI布局
layout = [
    [sg.Text('手势识别 + ROI 跟踪',
             font=("KaiTi", 28, 'bold'),
             justification='center',
             text_color='white',
             background_color='black')],
    [sg.Image(filename='',
              key='image',
              size=(640, 480),
              background_color='black')],
    [sg.Text('检测到手势: ',
             key='gesture',
             font=("KaiTi", 20),
             text_color='white',
             background_color='black')],
    [sg.Button('开始',
               font=("KaiTi", 16),
               button_color=('white', 'black')),
     sg.Button('退出',
               font=("KaiTi", 16),
               button_color=('white', 'firebrick'))]
]

# 设置整个窗口背景为黑色
window = sg.Window('Hand Gesture + ROI', layout,
                   resizable=True,
                   element_justification='center',
                   background_color='black')

cap = None
is_running = False
roi_counter = 0
# 主循环
while True:
    event, values = window.read(timeout=20)
    if event in (sg.WIN_CLOSED, '退出'):
        break
    elif event == '开始':
        if not is_running:
            cap = cv2.VideoCapture(0)
            is_running = True
            window['开始'].update('停止', button_color=('white','orange'))
        else:
            cap.release()
            is_running = False
            window['开始'].update('开始', button_color=('white','green'))

    if is_running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands_model.process(rgb_frame)

        tip_points = []
        gesture_text = "未检测到手部"

        if results.multi_hand_landmarks:
            gesture_text = recognize_gesture(results.multi_hand_landmarks)
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0,255,255), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(255,0,255), thickness=2))
                tips = get_straight_finger_tips(hand_landmarks)
                for x, y in tips:
                    tip_points.append((int(x*w), int(y*h)))

        # ROI 跟踪
        if tip_points:
            x_min = min(p[0] for p in tip_points)
            y_min = min(p[1] for p in tip_points)
            x_max = max(p[0] for p in tip_points)
            y_max = max(p[1] for p in tip_points)
            box = (x_min, y_min, x_max, y_max)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            if tracker.update(box):
                roi = frame[y_min:y_max, x_min:x_max]

                roi_counter += 1
                filename = f'hand_roi_{roi_counter:03d}.png'
                cv2.imwrite(filename, roi)
                print(f"ROI saved to {filename}")

        # 转为PySimpleGUI显示
        img_bytes = cv2.imencode('.png', frame)[1].tobytes()
        window['image'].update(data=img_bytes)
        window['gesture'].update(f'检测到手势: {gesture_text}')

if cap:
    cap.release()
window.close()
