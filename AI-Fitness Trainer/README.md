# AI-Fitness Trainer 

AI-powered fitness trainer that recognizes and classifies human exercises using real-time pose detection and a rule-based system for repetition counting. Using [MediaPipe], the application analyzes body posture and angles to track form, count repetitions, and help improve workout performance.

---

## 🔍 About This Project

The **AI-Fitness-Trainer** project is designed to guide users through fitness exercises by detecting their movements and posture in real-time. Currently It supports **11 exercises** and uses **rule-based logic** (angle comparisons between joints) to track repetitions.

This tool is ideal for:
- Fitness tracking at home 
- Real-time workout correction 
- Exercise monitoring in rehab centers 

---

## 🧠 Key Components

### Pose Detection
- Uses **MediaPipe** for extracting 33 human body landmarks from video or webcam feed.
- Calculates angles between joints to determine movement patterns.

### Rule-Based Exercise Classification
- Each exercise has custom logic for detecting correct form using calculated joint angles.
- No ML model required — purely based on pose geometry and rules.

### Repetition Counter
- Tracks full reps based on up and down movement thresholds.
- Outputs total rep count in terminal or webcam window.

### Pose Correction Feedback
- Compares live pose angles with expected angle ranges for each exercise.
- Detects common mistakes (e.g., improper knee bend, arched back).
- Displays real-time text feedback like "Straighten your back", "Lower deeper", or "Adjust arm position".

---

## ✅ Supported Exercises (11)

- Push-up
- Pull-up
- Sit-up
- Squat
- Jumping Jacks
- Russian Twist
- Crunches
- Dumbbell Shoulder Press
- Bicep Curl
- Plank
- Lunges

---

## 🎬 Exercise Commands

> Run any video file and detect reps:

→ python main.py -t push-up -vs push-up.mp4

→ python main.py -t pull-up -vs pull-up.mp4

→ python main.py -t sit-up -vs sit-up.mp4

→ python main.py -t squat -vs squat.mp4

→ python main.py -t jumping-jacks -vs jumping-jacks.mp4

→ python main.py -t russian-twist -vs russian-twist.mp4

→ python main.py -t crunches -vs crunches.mp4

→ python main.py -t plank -vs plank.mp4

→ python main.py -t lunges -vs lunges.mp4

→ python main.py -t deadlift -vs deadlift.mp4

→ python main.py -t bicep-curl -vs bicep-curl.mp4

→ python main.py -t dumbbell-shoulder-press -vs dumbbell-shoulder-press.mp4

> To use your webcam for real-time rep counting:

→ python main.py -t push-up

→ python main.py -t pull-up

→ python main.py -t sit-up

→ python main.py -t squat

→ python main.py -t jumping-jacks

→ python main.py -t russian-twist

→ python main.py -t crunches

→ python main.py -t plank

→ python main.py -t lunges

→ python main.py -t deadlift

→ python main.py -t bicep-curl

→ python main.py -t dumbbell-shoulder-press
