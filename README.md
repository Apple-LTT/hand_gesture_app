Hand Gesture Recognition & ROI Tracking

这是一个基于 MediaPipe Hands 的手势识别程序，结合 ROI（Region of Interest）跟踪，支持 GUI 显示和保存手部 ROI 图像。程序可以检测单手或双手手势，并在屏幕上绘制手势关键点，同时跟踪伸直手指形成的矩形区域并保存图片。

功能特点：
- 手势识别：
  - 握拳
  - 张开手掌
  - 食指指向
  - 胜利手势
  - 竖大拇指
  - （可自定义手势）
- ROI跟踪：
  - 使用两手伸直手指的关键点构建矩形区域
  - 对ROI进行IOU跟踪
  - 自动保存ROI图片，支持连续多张保存
- GUI界面：
  - PySimpleGUI显示摄像头画面
  - 显示当前检测到的手势
  - 黑色背景、白色/彩色文字美化
  - “开始/停止”按钮控制摄像头

环境依赖：
- Python 3.9+
  - 建议使用 Anaconda 虚拟环境：
    conda create -n hand_gesture python=3.9
    conda activate hand_gesture
  必需的 Python 库：
  安装方法（在激活虚拟环境后执行）：
  pip install opencv-python==4.12.0
  pip install opencv-contrib-python==4.11.0
  pip install mediapipe==0.10.21
  pip install PySimpleGUI==5.0.10
  pip install numpy==1.26.4
  pip install torch==2.8.0+cpu torchvision==0.23.0+cpu torchaudio==2.8.0+cpu
  注：PyTorch 依赖仅在你需要扩展自定义手势识别模型时使用，如果只使用 MediaPipe 的预训练手势识别，则可不安装。

文件结构：
hand_gesture_app/
├─ main.py                  # 主程序入口
├─ gesture_recognizer.py    # 手势识别函数
├─ hand_tracker.py          # ROI 跟踪逻辑
├─ roi_images/              # 保存的ROI图片
└─ README.txt               # 使用说明

运行方法：
1. 打开终端或 PyCharm，进入项目目录：
   cd D:/pycharm/hand_gesture_app
2. 确保已创建 roi_images 文件夹（程序首次运行会自动创建）
3. 启动程序：
   python main.py
4. GUI界面操作：
   - 点击 “开始”：启动摄像头，进行手势识别与ROI跟踪
   - 点击 “停止”：停止摄像头
   - 点击 “退出”：关闭程序
   - 当检测到ROI时，图片会自动保存到 roi_images 文件夹，文件名按序号递增，例如：
     hand_roi_001.png, hand_roi_002.png, ...

代码结构说明：
- main.py：主程序，启动 GUI、处理摄像头画面、调用手势识别和 ROI 跟踪
- gesture_recognizer.py：根据手部关键点识别手势（握拳、张开手掌、食指指向、胜利手势、竖大拇指等）
- hand_tracker.py：实现 ROI 跟踪逻辑，包括 IOU 判断和连续帧目标保存
- roi_images/：保存截取的手部区域图像

注意事项：
- 确保摄像头可用且驱动正常
- ROI 图片文件会按序号自动保存，避免覆盖
- 手势识别基于 MediaPipe 提供的关键点算法，属于基于深度学习的预训练模型
- 可根据需要扩展手势类型或调整识别逻辑

扩展与优化：
- 可增加动态ROI选择，通过鼠标拖拽指定区域
- 可实现多手势组合识别（例如双手爱心手势）
- 可将ROI保存改成按日期自动分类，便于管理大量图片
- 可结合 PyTorch 或 TensorFlow 自定义手势分类模型，实现更多复杂手势识别

作者：
陆婷婷
辽宁大学 计算机科学与技术专业
lu.c.lu@outlook.com
