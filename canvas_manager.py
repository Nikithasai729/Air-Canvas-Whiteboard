# canvas_manager.py
import cv2
import numpy as np

class CanvasManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset_canvas()

    def reset_canvas(self):
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

    def draw_freehand(self, prev_pt, curr_pt, color, thickness):
        cv2.line(self.canvas, prev_pt, curr_pt, color, thickness, lineType=cv2.LINE_AA)

    def clear_area(self, prev_pt, curr_pt, thickness):
        cv2.line(self.canvas, prev_pt, curr_pt, (255, 255, 255), thickness, lineType=cv2.LINE_AA)

    def preview_shape(self, img, start_pt, curr_pt, shape_type, color, thickness):
        preview = img.copy()
        if shape_type == "RECTANGLE":
            cv2.rectangle(preview, start_pt, curr_pt, color, thickness, lineType=cv2.LINE_AA)
        elif shape_type == "CIRCLE":
            radius = int(np.hypot(curr_pt[0] - start_pt[0], curr_pt[1] - start_pt[1]))
            cv2.circle(preview, start_pt, radius, color, thickness, lineType=cv2.LINE_AA)
        return preview

    def finalize_shape(self, start_pt, curr_pt, shape_type, color, thickness):
        if shape_type == "RECTANGLE":
            cv2.rectangle(self.canvas, start_pt, curr_pt, color, thickness, lineType=cv2.LINE_AA)
        elif shape_type == "CIRCLE":
            radius = int(np.hypot(curr_pt[0] - start_pt[0], curr_pt[1] - start_pt[1]))
            cv2.circle(self.canvas, start_pt, radius, color, thickness, lineType=cv2.LINE_AA)