# 🎨 Air Canvas Pro

An advanced Computer Vision-based virtual whiteboard that transforms hand gestures into digital brushstrokes in real time. Built using Python, OpenCV, MediaPipe, and NumPy, Air Canvas Pro allows users to draw, erase, create shapes, and interact with a digital canvas without requiring a mouse, stylus, or touchscreen.

The project incorporates intelligent gesture recognition, adaptive motion filtering, and real-time visual feedback to deliver a smooth and intuitive drawing experience.

---

## 🚀 Project Overview

Air Canvas Pro leverages Computer Vision and Hand Tracking technologies to create a touchless drawing environment. The application tracks hand landmarks in real time and maps finger gestures to different drawing actions, enabling natural interaction with a virtual whiteboard.

To improve stability and responsiveness, the project implements advanced smoothing and coordinate mapping techniques that reduce hand tremors and extend the effective drawing area beyond standard webcam limitations.

---

## ✨ Features

### ✍️ Gesture-Based Drawing

Draw naturally in the air using only your index finger. The system converts finger movement into smooth digital brush strokes.

### 🧹 Smart Eraser Tool

Erase selected areas of the canvas using gesture-controlled erasing functionality.

### 🔷 Shape Drawing

Create geometric shapes with live previews:

* Rectangle Tool
* Circle Tool

### 🎨 Multiple Color Selection

Choose from multiple brush colors directly through gesture-controlled UI buttons.

### 📏 Dynamic Brush Size Control

Increase or decrease brush thickness instantly from the virtual toolbar.

### 💾 Export Artwork

Save drawings as timestamped PNG image files and preview exported artwork instantly.

### 🖥️ Interactive HUD Interface

A modern control panel provides quick access to tools, colors, brush settings, and export options.

### ⚡ Real-Time Hand Tracking

Accurate finger tracking using MediaPipe's hand landmark detection system.

---

## 🧠 Advanced Tracking Technologies

### Velocity-Adaptive Dynamic Smoothing Engine

Traditional hand-tracking systems often suffer from shaky cursor movement caused by natural hand tremors.

To overcome this challenge, Air Canvas Pro implements a custom Velocity-Adaptive Exponential Moving Average (EMA) filter that dynamically adjusts smoothing based on movement speed.

#### Benefits

* Eliminates hand jitter during detailed drawing
* Maintains smooth cursor movement
* Reduces lag during rapid hand motion
* Improves overall drawing precision

---

### Coordinate Padding Bounds Expansion Matrix

Hand-tracking accuracy often decreases near the physical boundaries of a webcam.

Air Canvas Pro solves this using a coordinate expansion system that maps an inner tracking region to the full screen workspace.

#### Benefits

* Easier access to screen corners
* Better edge-to-edge navigation
* Reduced tracking loss near camera boundaries
* Improved user comfort

---

## 🖐️ Gesture Controls

| Gesture                  | Mode             | Action                                                             |
| ------------------------ | ---------------- | ------------------------------------------------------------------ |
| ☝️ Index Finger Only     | Drawing Mode     | Draw freehand strokes or create shapes                             |
| ✌️ Index + Middle Finger | Selection Mode   | Select tools, colors, brush sizes, clear canvas, or export artwork |
| ✊ Closed Fist            | Lock / Stop Mode | Finalize shapes or pause drawing safely                            |

---

## 🛠️ Technology Stack

### Programming Language

* Python 3.12

### Libraries & Frameworks

* OpenCV
* MediaPipe
* NumPy

### Core Concepts

* Computer Vision
* Hand Tracking
* Gesture Recognition
* Real-Time Image Processing
* Human-Computer Interaction (HCI)

---

## 📂 Project Structure

```text
Air-Canvas-Pro/
│
├── config.py
├── hand_tracker.py
├── canvas_manager.py
├── ui_renderer.py
├── main.py
│
├── exports/
│   └── drawing_timestamp.png
│
└── README.md
```

### File Descriptions

| File                | Purpose                                                     |
| ------------------- | ----------------------------------------------------------- |
| `config.py`         | Stores application constants, dimensions, and color themes  |
| `hand_tracker.py`   | Handles MediaPipe hand detection and gesture interpretation |
| `canvas_manager.py` | Manages drawing operations, erasing, and shape rendering    |
| `ui_renderer.py`    | Creates the virtual toolbar and HUD interface               |
| `main.py`           | Main execution pipeline and gesture-processing engine       |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Air-Canvas-Pro.git

cd Air-Canvas-Pro
```

### 2️⃣ Create Virtual Environment

```bash
py -3.12 -m venv venv

venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip

pip install opencv-python
pip install numpy
pip install mediapipe==0.10.20
```

### 4️⃣ Run the Application

```bash
python main.py
```

---

## 📈 Mathematical Model

The adaptive smoothing engine uses an Exponential Moving Average (EMA) based filtering approach:

```text
Smoothed Point =
(α × Current Coordinate)
+
((1 − α) × Previous Coordinate)
```

Where:

* α (Alpha) changes dynamically based on hand movement velocity.
* Fast movement → Higher α → Faster response.
* Slow movement → Lower α → Stronger stabilization.

This allows the system to remain responsive during fast movements while maintaining precision during detailed drawing operations.

---


© 2026 Air Canvas Pro
