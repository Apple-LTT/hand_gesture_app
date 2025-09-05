import mediapipe as mp

mp_hands = mp.solutions.hands

def get_straight_finger_tips(hand_landmarks, hand_label='Right'):
    """
    返回伸直手指尖坐标列表
    hand_label: 'Left' 或 'Right'
    """
    landmarks = hand_landmarks.landmark
    tips = []

    # 拇指
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
    if (hand_label == 'Right' and thumb_tip.x < thumb_ip.x) or \
       (hand_label == 'Left' and thumb_tip.x > thumb_ip.x):
        tips.append((thumb_tip.x, thumb_tip.y))

    # 其他四指
    for tip_id, pip_id in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
                           (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                           (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
                           (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)]:
        tip = landmarks[tip_id]
        pip = landmarks[pip_id]
        if tip.y < pip.y:  # y 越小表示越靠上
            tips.append((tip.x, tip.y))
    return tips

def recognize_gesture(hand_landmarks_list, handedness_list, debug=False):
    """
    输入：
        hand_landmarks_list: multi_hand_landmarks 列表
        handedness_list: multi_handedness 列表
        debug: 是否打印每根手指伸直情况
    输出：
        手势名称字符串（单手或双手组合）
    """
    gesture_names = []

    for hand_landmarks, handedness in zip(hand_landmarks_list, handedness_list):
        landmarks = hand_landmarks.landmark
        hand_label = handedness.classification[0].label  # 'Left' 或 'Right'

        fingers = []

        # 拇指
        thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
        if (hand_label == 'Right' and thumb_tip.x < thumb_ip.x) or \
           (hand_label == 'Left' and thumb_tip.x > thumb_ip.x):
            fingers.append(1)
        else:
            fingers.append(0)

        # 其他四指
        for tip_id, pip_id in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
                               (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                               (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
                               (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)]:
            tip = landmarks[tip_id]
            pip = landmarks[pip_id]
            fingers.append(1 if tip.y < pip.y else 0)

        if debug:
            finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            status = [f"{name}:{'伸直' if f else '弯曲'}" for name, f in zip(finger_names, fingers)]
            print(f"{hand_label}手指状态: {', '.join(status)}")

        total_fingers = fingers.count(1)

        # 手势识别
        if total_fingers == 0:
            gesture_names.append(f"{hand_label}握拳")
        elif total_fingers == 5:
            gesture_names.append(f"{hand_label}张开手掌")
        elif fingers == [0, 1, 0, 0, 0]:
            gesture_names.append(f"{hand_label}食指指向")
        elif fingers == [0, 1, 1, 0, 0]:
            gesture_names.append(f"{hand_label}胜利手势")
        elif total_fingers == 1 and fingers[0] == 1:
            gesture_names.append(f"{hand_label}竖大拇指")
        else:
            gesture_names.append(f"{hand_label}{total_fingers}根手指")

    return " & ".join(gesture_names)
