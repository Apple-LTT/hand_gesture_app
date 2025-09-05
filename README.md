# Hand Gesture Recognition & ROI Tracking

这是一个基于 **MediaPipe Hands** 的手势识别程序，结合 **ROI（Region of Interest）跟踪**，支持 GUI 界面显示和保存手部 ROI 图像。  
程序可以检测单手或双手手势，并在屏幕上绘制手势关键点，同时跟踪伸直手指形成的矩形区域并保存图片。

---

## ✨ 功能特点
- **手势识别**  
  - 握拳 ✊  
  - 张开手掌 🖐  
  - 食指指向 👉  
  - 胜利手势 ✌  
  - 竖大拇指 👍  
  - （可扩展更多手势，例如双手爱心 💖）

- **ROI 跟踪**  
  - 使用双手伸直手指的关键点构建矩形区域  
  - 基于 IoU（Intersection over Union）进行连续帧跟踪  
  - 自动保存 ROI 图片（支持 30 帧累积），文件名自动递增

- **GUI 界面**  
  - 使用 **PySimpleGUI** 展示摄像头画面  
  - 黑色背景 + 白色/彩色文字，美观简洁  
  - 按钮控制摄像头的 **开始 / 停止 / 退出**  

---

## 🛠 环境依赖

建议使用 **Python 3.9+**，推荐创建虚拟环境（例如 conda）：

```bash
conda create -n hand_gesture python=3.9
conda activate hand_gesture
```
---

## 🛠 安装依赖

建议使用 **Python 3.9+**。  

```bash
pip install opencv-python==4.12.0
pip install opencv-contrib-python==4.11.0
pip install mediapipe==0.10.21
pip install PySimpleGUI==5.0.10
pip install numpy==1.26.4
```
可选：如果要扩展为深度学习手势分类，可安装 PyTorch：
```bash
pip install torch==2.8.0+cpu torchvision==0.23.0+cpu torchaudio==2.8.0+cpu
```
---
## 📂 文件结构

```plaintext
hand_gesture_app/
├─ main.py                  # 主程序入口
├─ gesture_recognizer.py    # 手势识别函数
├─ hand_tracker.py          # ROI 跟踪逻辑
├─ roi_images/              # 保存的ROI图片
└─ README.md                # 使用说明
```

---
##🚀 运行方法

克隆项目或下载源码到本地

```bash
git clone https://github.com/yourname/hand_gesture_app.git
cd hand_gesture_app
```

启动程序

```bash
python main.py
```
---
# 🎮 GUI 操作说明

- **点击 开始**：启动摄像头，进行手势识别与 ROI 跟踪  
- **点击 停止**：暂停摄像头  
- **点击 退出**：关闭程序  

当检测到 ROI 时，程序会自动保存图片到当前目录  

## 📁 文件命名示例

```python-repl
hand_roi_001.png
hand_roi_002.png
hand_roi_003.png
