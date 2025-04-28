import numpy as np
import time
from body_part_angle import BodyPartAngle
from utils import *

class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    def push_up(self, counter, status):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_right_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2

        if status:
            if avg_arm_angle < 70:
                counter += 1
                status = False
        else:
            if avg_arm_angle > 160:
                status = True

        return [counter, status]

    def pull_up(self, counter, status):
        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        if status:
            if nose[1] > avg_shoulder_y:
                counter += 1
                status = False
        else:
            if nose[1] < avg_shoulder_y:
                status = True

        return [counter, status]

    def squat(self, counter, status):
        left_leg_angle = self.angle_of_the_right_leg()
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        if status:
            if avg_leg_angle < 70:
                counter += 1
                status = False
        else:
            if avg_leg_angle > 160:
                status = True

        return [counter, status]

    import time

    def plank(self, start_time, status):
            """
            Tracks duration the user holds a correct plank position.

            Args:
                start_time (float): Time when plank position was first correctly detected.
                status (bool): Whether the user is currently in correct plank form.

            Returns:
                Tuple[int, float, bool]: (elapsed time in seconds, updated start_time, updated status)
            """
            plank_angle = self.angle_of_the_plank()
            print(f"Plank angle: {plank_angle}")

            # Check if plank posture is correct
            if 140 <= plank_angle <= 180:
                if not status:
                    start_time = time.time()
                    status = True
                elapsed_time = int(time.time() - start_time)
            else:
                # When posture breaks, reset start_time
                elapsed_time = 0
                start_time = None
                status = False

            return elapsed_time, start_time, status

    def lunges(self, counter, status):
        knee_angle = self.angle_of_the_left_leg()
        if status:
            if knee_angle < 70:
                counter += 1
                status = False
        else:
            if knee_angle > 160:
                status = True

        return [counter, status]

    def bicep_curl(self, counter, status):
        elbow_angle = self.angle_of_the_left_arm()
        if status:
            if elbow_angle < 40:
                counter += 1
                status = False
        else:
            if elbow_angle > 150:
                status = True

        return [counter, status]

    def dumbbell_shoulder_press(self, counter, status):
        arm_angle = self.angle_of_the_left_arm()
        if status:
            if arm_angle > 160:
                counter += 1
                status = False
        else:
            if arm_angle < 90:
                status = True

        return [counter, status]

    def crunches(self, counter, status):
        abdomen_angle = self.angle_of_the_abdomen()
        if status:
            if abdomen_angle < 45:
                counter += 1
                status = False
        else:
            if abdomen_angle > 100:
                status = True

        return [counter, status]

    def russian_twists(self, counter, status):
        torso_angle = self.angle_of_the_torso()
        if status:
            if torso_angle < 45 or torso_angle > 135:
                counter += 1
                status = False
        else:
            if 80 < torso_angle < 100:
                status = True

        return [counter, status]

    def jumping_jacks(self, counter, status):
        hand_position = detection_body_part(self.landmarks, "LEFT_WRIST")
        if status:
            if hand_position[1] < detection_body_part(self.landmarks, "LEFT_SHOULDER")[1]:
                counter += 1
                status = False
        else:
            if hand_position[1] > detection_body_part(self.landmarks, "LEFT_HIP")[1]:
                status = True

        return [counter, status]

    def sit_up(self, counter, status):
        angle = self.angle_of_the_abdomen()
        if status:
            if angle < 55:
                counter += 1
                status = False
        else:
            if angle > 105:
                status = True

        return [counter, status]

    def calculate_exercise(self, exercise_type, counter, status):
        if exercise_type == "push-up":
            counter, status = TypeOfExercise(self.landmarks).push_up(
                counter, status)
        elif exercise_type == "pull-up":
            counter, status = TypeOfExercise(self.landmarks).pull_up(
                counter, status)
        elif exercise_type == "squat":
            counter, status = TypeOfExercise(self.landmarks).squat(
                counter, status)
        elif exercise_type == "plank":
            counter, status = TypeOfExercise(self.landmarks).plank(
                counter, status)
        elif exercise_type == "lunges":
            counter, status = TypeOfExercise(self.landmarks).lunges(
                counter, status)
        elif exercise_type == "bicep-curl":
            counter, status = TypeOfExercise(self.landmarks).bicep_curl(
                counter, status)
        elif exercise_type == "dumbbell-shoulder-press":
            counter, status = TypeOfExercise(self.landmarks).dumbbell_shoulder_press(
                counter, status)
        elif exercise_type == "crunches":
            counter, status = TypeOfExercise(self.landmarks).crunches(
                counter, status)
        elif exercise_type == "russian-twist":
            counter, status = TypeOfExercise(self.landmarks).russian_twists(
                counter, status)
        elif exercise_type == "jumping-jacks":
            counter, status = TypeOfExercise(self.landmarks).jumping_jacks(
                counter, status)
        elif exercise_type == "sit-up":
            counter, status = TypeOfExercise(self.landmarks).sit_up(
                counter, status)

        return [counter, status]
