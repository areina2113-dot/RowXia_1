# ai/stroke_ai.py

import cv2
import mediapipe as mp
import numpy as np
import sys

video_path = sys.argv[1]

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(video_path)

ghost_points = []
frame_count = 0

output = cv2.VideoWriter(
    "output.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    30,
    (int(cap.get(3)), int(cap.get(4)))
)

tips = []

def calculate_angle(a,b,c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba,bc)/(np.linalg.norm(ba)*np.linalg.norm(bc))

    angle = np.degrees(np.arccos(cosine))

    return angle


while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        shoulder = [landmarks[11].x, landmarks[11].y]
        hip = [landmarks[23].x, landmarks[23].y]
        knee = [landmarks[25].x, landmarks[25].y]

        back_angle = calculate_angle(shoulder, hip, knee)

        if frame_count < 30:
            ghost_points.append((shoulder, hip))

        # draw user skeleton
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # draw ghost
        if frame_count < len(ghost_points):

            g_shoulder, g_hip = ghost_points[frame_count]

            h, w, _ = frame.shape

            cv2.circle(frame,(int(g_shoulder[0]*w),int(g_shoulder[1]*h)),6,(0,255,0),-1)
            cv2.circle(frame,(int(g_hip[0]*w),int(g_hip[1]*h)),6,(0,255,0),-1)

        if back_angle < 20:
            tips.append("More forward body angle at catch")

        if back_angle > 60:
            tips.append("Too much layback at finish")

    output.write(frame)

    frame_count += 1


cap.release()
output.release()

unique_tips = list(set(tips))

print("TIPS:")
for tip in unique_tips:
    print("-",tip)
