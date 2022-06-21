import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports

class NoArduino(Exception):
    pass

def find_arduino():
    ports = list(serial.tools.list_ports.comports())

    # looks through the ports to find if an arduino is availible for serial communication
    arduino_found = False
    for p in ports:
        if 'Arduino' in p.manufacturer:
            arduino = serial.Serial(port=p.device, baudrate=115200, timeout=.1)
            print (p.device)
            arduino_found = True

    # if no arduino is found, we terminate the program
    if not arduino_found:
        raise NoArduino('No Arduino Found')

    return arduino

def torso_shoot(torso_x, torso_y, bound_x, bound_y, image, arduino):
    lower_x = bound_x[0]
    upper_x = bound_x[1]
    lower_y = bound_y[0]
    upper_y = bound_y[1]


    if (lower_x < torso_x < upper_x) and (lower_y < torso_y < upper_y):
        # shows fire on screen when target is with the defined tolerance
        cv2.putText(image, "fire", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        # sends a message to the arduino
        arduino.write(bytes('1', 'utf-8'))

def manual_shoot(arduino):
    arduino.write(bytes('1', 'utf-8'))
        
   
def main():
    cap = cv2.VideoCapture(0)
    arduino = find_arduino()

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            _, image = cap.read()
            
            # trigger by pressing s
            if cv2.waitKey(1) == ord('s'):
                manual_shoot(arduino)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = pose.process(image)

            # Draw the pose annotation on the image.
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if results.pose_landmarks is not None:
                torso_center_x = ((results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x)/2 + 
                                  (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x)/2)/2
                torso_center_y = ((results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[23].y)/2 + 
                                  (results.pose_landmarks.landmark[24].y + results.pose_landmarks.landmark[12].y)/2)/2

                # print("centered torso x cord: ", torso_center_x, "\ncentered torso y cord: ", torso_center_y)
                cv2.circle(image, (320, 240), 40, (0,0,244), 2)
                torso_shoot(torso_center_x, torso_center_y, [0.4, 0.6], [0.35, 0.7], image, arduino)

            cv2.imshow('Weed Whacker', image)
            if cv2.waitKey(1) == ord ('d'):
                break

    cap.release()

main()
