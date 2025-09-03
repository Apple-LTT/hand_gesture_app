import mediapipe as mp

mp_hands = mp.solutions.hands


def get_straight_finger_tips(hand_landmarks):
    """返回伸直手指尖坐标列表"""
    landmarks = hand_landmarks.landmark
    tips = []

    # 拇指伸直
    if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x:
        tips.append((landmarks[mp_hands.HandLandmark.THUMB_TIP].x,
                     landmarks[mp_hands.HandLandmark.THUMB_TIP].y))

    # 其他四指
    for tip, pip in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
                     (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                     (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
                     (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)]:
        if landmarks[tip].y < landmarks[pip].y:
            tips.append((landmarks[tip].x, landmarks[tip].y))
    return tips


def recognize_gesture(hand_landmarks_list):
    """
    输入：multi_hand_landmarks 列表
    输出：手势名称字符串
    支持单手和双手组合手势
    """
    gesture_names = []

    for hand_landmarks in hand_landmarks_list:
        landmarks = hand_landmarks.landmark
        fingers = []

        # 拇指
        if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # 其他四指
        for tip, pip in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
                         (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                         (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
                         (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)]:
            if landmarks[tip].y < landmarks[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)

        # 单手手势
        if total_fingers == 0:
            gesture_names.append("握拳")
        elif total_fingers == 5:
            gesture_names.append("张开手掌")
        elif fingers == [0, 1, 0, 0, 0]:
            gesture_names.append("食指指向")
        elif fingers == [0, 1, 1, 0, 0]:
            gesture_names.append("胜利手势")
        elif total_fingers == 1 and fingers[0] == 1:
            gesture_names.append("竖大拇指")
        else:
            gesture_names.append(f"{total_fingers}根手指")

    return " & ".join(gesture_names)
