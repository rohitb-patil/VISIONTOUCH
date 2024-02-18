# VISIONTOUCH
Phone Gesture Control via Eye Gaze

# Phone Gesture Control via Eye Gaze

Co-authored by [Co-Author 1](https://github.com/chinmayeebl).

## Project Description

This project focuses on enabling phone gesture control through eye gaze recognition. The system combines several components:

1. Eye Gaze Recognition Model Implementation: Development of an eye gaze recognition model to interpret user eye movements for gesture control.
2. Android Phone Connectivity via ADB: Establishing a connection between the computer and an Android phone using the Android Debug Bridge (ADB) tool.

 ---

# EyeGazeControl.py
This Python script (EyeGazeControl.py) is responsible for implementing the eye gaze recognition model. It utilizes OpenCV and other relevant libraries to interpret eye movements and generate corresponding control signals.

### Requirements:
- Python 3 and above
- OpenCV (4 and above)
- dlib.shape_predictor , dlib.get_frontal_face_detector (provided in repo)
- Other relevant dependencies for eye gaze recognition

---

# ADB Connectivity
Establish a connection between your computer and Android phone using the Android Debug Bridge (ADB) tool by starting the ADB server and confirming device detection.
For detailed instructions, refer to https://developer.android.com/tools/adb.

---

# Scrcpy Integration
Ensure you have scrcpy installed on your computer. To mirror and control the Android phone screen type scrcpy in terminal.
