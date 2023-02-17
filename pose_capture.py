import cv2
import mediapipe as mp
import numpy as np

def get_stick_figure_lines(landmarks, frame): 
    connections = [(12, 11), (11, 23), (24, 23), (24, 12), (24, 26), (26, 28), (23, 25), (25, 27), (28, 32), (32, 30), (28, 30), (27, 31), (29, 31), (27, 29), (14, 12), (14, 16), (11, 13), (13, 15), (8, 6), (3, 7), (10, 9), (6, 5), (5, 4), (4, 0), (3, 2), (2, 1), (1, 0), (16, 18), (18, 20), (20, 16), (16, 22), (15, 21), (15, 19), (19, 17), (17, 15), (12, 23), (11, 24)]
    lines = []
    for connection in connections:
        x1 = int(landmarks.landmark[connection[0]].x * frame.shape[1])
        y1 = int(landmarks.landmark[connection[0]].y * frame.shape[0])
        x2 = int(landmarks.landmark[connection[1]].x * frame.shape[1])
        y2 = int(landmarks.landmark[connection[1]].y * frame.shape[0])
        lines.append((x1, y1, x2, y2))
    return lines

def create_stick_figure(landmarks: mp.solutions.pose.Pose, frame: np.ndarray) -> np.ndarray:
    stick_figure = np.zeros_like(frame)
    lines = get_stick_figure_lines(landmarks, frame)
    for line in lines:
        cv2.line(stick_figure, line[0:2], line[2:4], (0, 255, 0), 2)
    return stick_figure

def blend_images(frame: np.ndarray, stick_figure: np.ndarray, alpha=0.5) -> np.ndarray:
    blended = cv2.addWeighted(frame, alpha, stick_figure, 1 - alpha, 0)
    return blended

def main():
    mp_pose = mp.solutions.pose.Pose()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = mp_pose.process(image=rgb)
        landmarks = pose.pose_landmarks
        if landmarks is not None:
            stick_figure = create_stick_figure(landmarks, frame)
            blended = blend_images(frame, stick_figure)
            cv2.imshow('Stick Figure', blended)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
