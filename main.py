# main.py
import cv2
import numpy as np
import time
import os
from config import WIDTH, HEIGHT, HEADER_HEIGHT, COLORS
from hand_tracker import HandTracker
from canvas_manager import CanvasManager
from ui_renderer import UIRenderer

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)

    tracker = HandTracker()
    canvas_mgr = CanvasManager(WIDTH, HEIGHT)
    ui = UIRenderer(WIDTH, HEADER_HEIGHT)

    current_color = COLORS["red"]
    current_mode = "FREEHAND"
    brush_thickness = 6
    eraser_thickness = 50

    xp, yp = 0, 0  
    start_shape_pt = None
    stable_pt = None         
    is_drawing_shape = False

    # --- ADVANCED VELOCITY-ADAPTIVE FILTER & EXPANSION BOUNDS MATRIX ---
    sm_x, sm_y = 0, 0          # Filtered output tracking point references
    base_alpha = 0.05          # Maximum tremor elimination dampening filter base
    max_alpha = 0.65           # Maximum high-speed tracking speed cap

    # Inner active cushioning box borders (Translates partial movement to true full screen)
    PAD_X = 110  # Horizontal viewport edge buffer
    PAD_Y = 80   # Vertical viewport edge buffer

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        display_frame = canvas_mgr.canvas.copy()
        
        display_frame = tracker.find_hands(frame, draw_img=display_frame, draw=True)
        lm_list = tracker.find_position(frame)
        fingers = tracker.fingers_up()

        if len(lm_list) > 0:
            raw_x, raw_y = lm_list[8][1], lm_list[8][2]   # Raw camera tracking point

            # --- STEP 1: LINEAR PAD BOUNDS EXPANSION MATRIX (EASILY HIT OUTER EDGES) ---
            mapped_x = int(np.clip(np.interp(raw_x, [PAD_X, WIDTH - PAD_X], [0, WIDTH]), 0, WIDTH))
            mapped_y = int(np.clip(np.interp(raw_y, [PAD_Y, HEIGHT - PAD_Y], [0, HEIGHT]), 0, HEIGHT))

            # --- STEP 2: VELOCITY-ADAPTIVE DYNAMIC SMOOTHING FILTER ---
            if sm_x == 0 and sm_y == 0:
                sm_x, sm_y = mapped_x, mapped_y
            else:
                # Determine absolute travel displacement distance across execution frames
                travel_distance = np.hypot(mapped_x - sm_x, mapped_y - sm_y)
                
                # Faster movement scales alpha higher to eliminate drag; slower movement drops alpha down to lock jitter
                adaptive_alpha = min(max_alpha, base_alpha + (travel_distance / 90.0))
                
                sm_x = int(adaptive_alpha * mapped_x + (1 - adaptive_alpha) * sm_x)
                sm_y = int(adaptive_alpha * mapped_y + (1 - adaptive_alpha) * sm_y)

            # --- 1. SELECTION NAV MODE (Index + Middle Extended Together) ---
            if fingers[1] and fingers[2]:
                if is_drawing_shape and start_shape_pt and stable_pt:
                    canvas_mgr.finalize_shape(start_shape_pt, stable_pt, current_mode, current_color, brush_thickness)
                is_drawing_shape = False
                start_shape_pt, stable_pt = None, None
                xp, yp = 0, 0  
                
                cv2.circle(display_frame, (sm_x, sm_y), 10, COLORS["background_dark"], 2, lineType=cv2.LINE_AA)

                if sm_y < HEADER_HEIGHT:
                    clicked_btn = ui.check_click(sm_x, sm_y)
                    if clicked_btn:
                        if clicked_btn == "CLEAR ALL":
                            canvas_mgr.reset_canvas()
                            cv2.waitKey(200)
                        elif clicked_btn == "EXPORT":
                            pure_drawing = canvas_mgr.canvas[HEADER_HEIGHT:, :]
                            
                            project_folder = os.path.dirname(os.path.abspath(__file__))
                            filename = f"drawing_{int(time.time())}.png"
                            save_path = os.path.join(project_folder, filename)
                            
                            cv2.imwrite(save_path, pure_drawing)
                            print(f"\n[SAVED TO FILE MANAGER] -> {save_path}\n")
                            
                            cv2.namedWindow("Exported Art Canvas", cv2.WINDOW_NORMAL)
                            cv2.resizeWindow("Exported Art Canvas", 800, 450)
                            cv2.imshow("Exported Art Canvas", pure_drawing)
                            cv2.waitKey(200)
                        elif clicked_btn in ["Black", "Blue", "Green", "Red", "Purple"]:
                            current_color = COLORS[clicked_btn.lower()]
                            current_mode = "FREEHAND" 
                        elif clicked_btn == "ERASER":
                            current_mode = "ERASER"
                        elif clicked_btn == "RECTANGLE":
                            current_mode = "RECTANGLE"
                        elif clicked_btn == "CIRCLE":
                            current_mode = "CIRCLE"
                        elif clicked_btn == "SIZE +":
                            if current_mode == "ERASER": eraser_thickness = min(150, eraser_thickness + 10)
                            else: brush_thickness = min(50, brush_thickness + 3)
                            cv2.waitKey(150)
                        elif clicked_btn == "SIZE -":
                            if current_mode == "ERASER": eraser_thickness = max(10, eraser_thickness - 10)
                            else: brush_thickness = max(2, brush_thickness - 3)
                            cv2.waitKey(150)

            # --- 2. DRAWING MODE (Only Index Finger Extended) ---
            elif fingers[1] and not fingers[2]:
                active_color = (255, 255, 255) if current_mode == "ERASER" else current_color
                active_thick = eraser_thickness if current_mode == "ERASER" else brush_thickness
                
                stable_pt = (sm_x, sm_y)
                cv2.circle(display_frame, stable_pt, 5, current_color, cv2.FILLED)

                if sm_y > HEADER_HEIGHT:
                    if current_mode == "FREEHAND":
                        if xp == 0 and yp == 0: xp, yp = sm_x, sm_y
                        canvas_mgr.draw_freehand((xp, yp), stable_pt, active_color, active_thick)
                        xp, yp = sm_x, sm_y
                    elif current_mode == "ERASER":
                        if xp == 0 and yp == 0: xp, yp = sm_x, sm_y
                        canvas_mgr.clear_area((xp, yp), stable_pt, active_thick)
                        xp, yp = sm_x, sm_y
                    elif current_mode in ["RECTANGLE", "CIRCLE"]:
                        if not is_drawing_shape:
                            start_shape_pt = stable_pt
                            is_drawing_shape = True
                        display_frame = canvas_mgr.preview_shape(display_frame, start_shape_pt, stable_pt, current_mode, current_color, brush_thickness)

            # --- 3. STOP/LOCK MODE (Fist Gesture / All Closed) ---
            else:
                if is_drawing_shape and start_shape_pt and stable_pt:
                    canvas_mgr.finalize_shape(start_shape_pt, stable_pt, current_mode, current_color, brush_thickness)
                is_drawing_shape = False
                start_shape_pt, stable_pt = None, None
                xp, yp = 0, 0
                sm_x, sm_y = 0, 0 
        else:
            if is_drawing_shape and start_shape_pt and stable_pt:
                canvas_mgr.finalize_shape(start_shape_pt, stable_pt, current_mode, current_color, brush_thickness)
            is_drawing_shape = False
            start_shape_pt, stable_pt = None, None
            xp, yp = 0, 0
            sm_x, sm_y = 0, 0

        display_frame = ui.draw_ui(display_frame, current_color, current_mode, eraser_thickness if current_mode == "ERASER" else brush_thickness)

        cv2.imshow("Air Drawing Whiteboard (AI HUD Window)", display_frame)
        if cv2.waitKey(1) & 0xFF == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()