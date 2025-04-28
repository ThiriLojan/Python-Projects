import cv2
import argparse
import os
from utils import *
import mediapipe as mp
from body_part_angle import BodyPartAngle
from types_of_exercise import TypeOfExercise
from utils import score_table, draw_progress_bar
from pose_correction import pose_correction

# Argument Parsing
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--exercise_type", type=str, required=True, help='Type of activity to do')
ap.add_argument("-vs", "--video_source", type=str, help='Video source file name (optional)')
args = vars(ap.parse_args())

# MediaPipe Setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video Source Setup
video_source = os.path.join("Exercise Videos", args["video_source"]) if args["video_source"] else 0
cap = cv2.VideoCapture(video_source)

cap.set(3, 800)  # Width
cap.set(4, 480)  # Height

exercise_type = args["exercise_type"].lower()   # <--- Moved outside the loop!

# Pose Detection Setup
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    counter = 0
    status = True
    start_time = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read video feed.")
            break

        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)

        # RGB Conversion for MediaPipe
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = pose.process(frame)

        # BGR Conversion for Display
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Pose Landmarks and Exercise Counting
        try:
            landmarks = results.pose_landmarks.landmark
            exercise = TypeOfExercise(landmarks)

            if exercise_type == "plank":
                counter, start_time, status = exercise.plank(start_time, status)
            else:
                counter, status = exercise.calculate_exercise(exercise_type, counter, status)
        
        except AttributeError:
            pass  # Handles cases when no landmarks are detected

        # Display Score and Status
        frame = score_table(exercise_type, frame, counter, status)

        # Progress bar logic
        if exercise_type == "plank":
            progress = min(counter / 30, 1.0)  
        else:
            progress = min(counter / 15, 1.0)  

        draw_progress_bar(frame, progress)

        frame = pose_correction(frame, args["exercise_type"])

        # Render Pose Landmarks
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(174, 139, 45), thickness=2, circle_radius=2),
        )

        cv2.imshow('Video', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
