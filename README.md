# AI Virtual Mouse 🖱️

Control your computer mouse with hand gestures using AI! This Python application uses **MediaPipe** for hand detection and **OpenCV** for video processing to enable gesture-based mouse control.

## ✨ Features

- **Real-time Hand Detection**: Uses MediaPipe to detect and track hand landmarks
- **Gesture-based Mouse Control**: 
  - Move mouse cursor with index finger
  - Click by bringing index and middle fingers together
- **Smooth Cursor Movement**: Implements smoothing algorithm to prevent jittery movement
- **Live FPS Display**: Real-time performance metrics
- **Full Screen Control**: Map camera coordinates to screen coordinates
- **Click Detection**: Proximity-based click detection with configurable delay

## 🎮 How to Use

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AkshatYadav-bit/AI_Virtual_Mouse.git
   cd AI_Virtual_Mouse
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python AiVirtualMouse.py
```

Press **'q'** to quit the application.

## 🎯 Gesture Controls

| Hand Gesture | Action |
|---|---|
| **Index Finger Extended (alone)** | Move mouse cursor |
| **Index + Middle Finger Extended** | Left mouse click |
| **Hand outside detection box** | No control |

## 📋 Requirements

- Python 3.7+
- Webcam/Camera
- All dependencies listed in requirements.txt

### Key Dependencies

- mediapipe==0.10.9 - Hand detection and tracking
- opencv-python==4.13.0.92 - Video capture and image processing
- autopy==4.0.1 - Mouse control
- cvzone==1.6.1 - OpenCV utilities
- numpy==2.2.6 - Numerical operations

## 📁 Project Structure

```
AI_Virtual_Mouse/
├── AiVirtualMouse.py         # Main application script
├── handTrackingModule.py      # Hand detection module
├── requirements.txt           # Project dependencies
└── README.md                  # This file
```

## 🔧 Configuration

You can customize parameters in AiVirtualMouse.py (lines 11-17):

- wCam, hCam = 640, 480: Webcam resolution
- frameR = 100: Frame reduction (active control area boundaries)
- smoothening = 7: Smoothing factor for cursor movement (higher = smoother but delayed)
- clickDelay = 0.3: Minimum delay between clicks in seconds

## 📚 How It Works

### Main Algorithm

1. Capture frames from webcam
2. Detect hand landmarks using MediaPipe
3. Extract index and middle finger positions
4. Map camera coordinates to screen coordinates
5. Apply smoothing to cursor movement
6. Control mouse and detect clicks
7. Display FPS and visualization

### Hand Tracking Module

The handDetector class provides:
- findHands(img, draw=True): Detects and visualizes hand landmarks
- findPosition(img, handNo=0, draw=True): Returns coordinates of all 21 hand landmarks
- findFingersUp(): Detects which fingers are raised
- findDistance(img, id1, id2, draw=True): Calculates distance between two landmarks

## 🐛 Troubleshooting

### Webcam not detected
- Verify webcam is connected
- Check camera permissions (macOS/Linux)
- Try changing camera index in line 20

### Hand detection not working
- Ensure adequate lighting
- Keep hand clearly visible
- Avoid cluttered backgrounds
- Move hand within purple detection box

### Cursor moves too fast/slow
- Increase smoothening value for slower movement
- Decrease smoothening value for faster movement

### Clicks not registering
- Reduce clickDelay for faster repeated clicks
- Bring fingers closer together for click detection

## 🚀 Future Enhancements

- Multi-hand gesture support
- Scrolling gestures
- Right-click functionality
- Drag and drop support
- Settings GUI
- Performance optimization

## 📝 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions are welcome! Feel free to report bugs, suggest features, or submit pull requests.

## 📚 References

- MediaPipe Hand Tracking: https://mediapipe.dev/solutions/hands
- OpenCV Documentation: https://docs.opencv.org/
- AutoPy Documentation: https://github.com/mshafer/autopy
- CVZone: https://github.com/cvzone/cvzone

---

**Note**: This application requires camera access. Ensure proper lighting and keep your hand within the detection frame for optimal performance.