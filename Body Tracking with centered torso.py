import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports
import time

def shoot(torso_x, torso_y, bound_x, bound_y, image):
    lower_x = bound_x[0]
    upper_x = bound_x[1]
    lower_y = bound_y[0]
    upper_y = bound_y[1]

    ports = list(serial.tools.list_ports.comports())

    if (lower_x < torso_x < upper_x) and (lower_y < torso_y < upper_y):
        x = 6
        for p in ports:
            if 'Arduino' in p.manufacturer:
                arduino = serial.Serial(port=p.device, baudrate=115200, timeout=.1)
                print (p.device)
                while True:
                    arduino.write(bytes('6', 'utf-8'))
                    time.sleep(0.1)
                    break
        cv2.putText(image, "fire", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
   
def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = int(width)
    height = int(height)
    print(type(width), type(height))

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():

            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            print("results", results)
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if results.pose_landmarks is None:
                success, image = cap.read()
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                torso_center_x = ((results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x)/2 + (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x)/2)/2
                torso_center_y = ((results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[23].y)/2 + (results.pose_landmarks.landmark[24].y + results.pose_landmarks.landmark[12].y)/2)/2
                print ("centered torso x cord: ", torso_center_x, "\ncentered torso y cord: ", torso_center_y)
                cv2.circle(image, (320, 240), 40, (0,0,244), 2)

                shoot(torso_center_x, torso_center_y, [0.4, 0.6], [0.35, 0.7], image)

            cv2.imshow('Weed Whacker', image)
            if cv2.waitKey(20) == ord ('d'):
                break

        cap.release()

main()
