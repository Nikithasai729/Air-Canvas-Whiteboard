# ui_renderer.py
import cv2
from config import COLORS

class UIRenderer:
    def __init__(self, width, header_height):
        self.width = width
        self.header_height = header_height
        
        # Symmetrical distribution for button grids
        self.buttons = {
            "CLEAR ALL": (10, 15, 120, 85),
            "Black": (130, 15, 210, 85),
            "Blue": (220, 15, 300, 85),
            "Green": (310, 15, 390, 85),
            "Red": (400, 15, 480, 85),
            "Purple": (490, 15, 570, 85),
            "ERASER": (580, 15, 670, 85),
            "RECTANGLE": (680, 15, 800, 85),
            "CIRCLE": (810, 15, 910, 85),
            "SIZE -": (920, 15, 1020, 85),
            "SIZE +": (1030, 15, 1130, 85),
            "EXPORT": (1140, 15, 1260, 85)
        }

    def draw_ui(self, img, current_color, current_mode, thickness):
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.header_height), COLORS["background_dark"], -1)
        cv2.addWeighted(overlay, 0.92, img, 0.08, 0, img)

        for name, (x1, y1, x2, y2) in self.buttons.items():
            is_active = False
            btn_color = COLORS["hud_gray"]

            if name in ["Black", "Blue", "Green", "Red", "Purple"] and current_mode != "ERASER":
                btn_color = COLORS[name.lower()]
                if current_color == btn_color:
                    is_active = True
            elif name == "ERASER" and current_mode == "ERASER":
                is_active = True
            elif name == "RECTANGLE" and current_mode == "RECTANGLE":
                is_active = True
            elif name == "CIRCLE" and current_mode == "CIRCLE":
                is_active = True

            if is_active:
                cv2.rectangle(img, (x1, y1), (x2, y2), COLORS["accent_orange"], -1)
                cv2.rectangle(img, (x1 + 3, y1 + 3), (x2 - 3, y2 - 3), btn_color, -1)
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), btn_color, -1)
                cv2.rectangle(img, (x1, y1), (x2, y2), COLORS["text_white"], 1, lineType=cv2.LINE_AA)

            text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.38, 2)[0]
            tx = x1 + (x2 - x1 - text_size[0]) // 2
            ty = y1 + (y2 - y1 + text_size[1]) // 2
            cv2.putText(img, name, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.38, COLORS["text_white"], 2, cv2.LINE_AA)

        status_text = f"ACTIVE MODE: {current_mode} | SIZE: {thickness}px"
        cv2.putText(img, status_text, (20, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLORS["background_dark"], 2, cv2.LINE_AA)
        return img

    def check_click(self, x, y):
        for name, (x1, y1, x2, y2) in self.buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return name
        return None