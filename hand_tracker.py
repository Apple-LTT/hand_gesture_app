from utils import iou

class RegionTracker:
    """IOU跟踪器"""
    def __init__(self, iou_threshold=0.3, target_frames=30):
        self.prev_box = None
        self.frame_count = 0
        self.iou_threshold = iou_threshold
        self.target_frames = target_frames

    def update(self, box):
        if self.prev_box is None:
            self.prev_box = box
            self.frame_count = 1
            return False
        else:
            score = iou(box, self.prev_box)
            if score > self.iou_threshold:
                self.frame_count += 1
            else:
                self.frame_count = 1
            self.prev_box = box
            if self.frame_count >= self.target_frames:
                self.frame_count = 0
                return True
        return False
