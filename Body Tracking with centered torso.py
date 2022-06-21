import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports
import time
import math

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

def circle_shoot(c1, c2, image, arduino):
    if overlap2(c1, c2):
        # shows fire on screen when target is with the defined tolerance
        cv2.putText(image, "fire", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        # sends a message to the arduino
        arduino.write(bytes('1', 'utf-8'))

def manual_shoot(arduino, trigger):
    if cv2.waitKey(1) == ord(trigger):
        arduino.write(bytes('1', 'utf-8'))

def num_map(x, in_basis_low, in_basis_high, fin_basis_low, fin_basis_high):
    return int(((((x - in_basis_low) / (in_basis_high - in_basis_low)) 
            * (fin_basis_high - fin_basis_low)) + fin_basis_low))

def distance(c1: list, c2: list):
    x_dist = c1[0] - c2[0]
    y_dist = c1[1] - c2[1]
    return math.sqrt(x_dist**2 + y_dist**2)

# c = [x, y, r] 
# if the center of the tracking circle is in the targer shoot
def overlap(c1: list, c2: list):
    return distance(c1, c2) < max(c1[2], c2[2])

# if there is any overlap at all shoot
def overlap2(c1: list, c2: list):
    return distance(c1, c2) < (c1[2] + c2[2])


# torso_bounds / screen_bounds: [x_lower, x_upper, y_lower, y_upper]
# torso_coords: [x, y]
# returns pixel coordianates from torso coordinates
def coord_map(torso_coords: list, torso_bounds: list, screen_bounds: list):
    mapped_list = []
    mapped_list.append(num_map(torso_coords[0], torso_bounds[0], torso_bounds[1], screen_bounds[0], screen_bounds[1]))
    mapped_list.append(num_map(torso_coords[1], torso_bounds[2], torso_bounds[3], screen_bounds[2], screen_bounds[3]))

    return mapped_list


def tracking(torso_coords: list, torso_bounds: list, screen_bounds: list, image, radius=30, color=[0, 0, 200], thickness=2):
    pixel_coords = coord_map(torso_coords, torso_bounds, screen_bounds)
    cv2.circle(image, pixel_coords, radius, color, thickness)
    return [pixel_coords[0], pixel_coords[1], radius]

def main():
    cv2.namedWindow('window')
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # finds dimensions of the window
    win_width, win_height = frame.shape[1], frame.shape[0]
    c1 = [win_width//2, win_height//2, 40]
    arduino = find_arduino()

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, image = cap.read()
            image = cv2.flip(image, 1)

            
            # trigger by pressing s
            manual_shoot(arduino, 's')

            # To improve performance, optionally mark the image as not writeable to
            #dd pass by reference.
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
                torso_coords = [torso_center_x, torso_center_y]
                torso_bounds = [-0.5, 1.5, -0.5, 1.5]
                screen_bounds = [0, win_width, 0, win_height]
                # print("centered torso x cord: ", torso_center_x, "\ncentered torso y cord: ", torso_center_y)
                time.sleep(0.1)
                # Parameters (image, center_coords, radius, color, thickness) # Note: Color is bgr
                cv2.circle(image, (c1[0], c1[1]), c1[2], (225, 203, 30), 2)
                # print(coord_map(torso_coords, torso_bounds, screen_bounds))
                c2 = tracking(torso_coords, torso_bounds, screen_bounds, image)
                circle_shoot(c1, c2, image, arduino)

                # cv2.circle(image, (screenWidth//2, screenHeight//2), 40, (225, 203, 30), 2)
                # torso_shoot(torso_center_x, torso_center_y, [0.4, 0.6], [0.35, 0.7], image, arduino)

            cv2.imshow('dst', image)
            if cv2.waitKey(1) == ord ('d'):
                break

    cap.release()
    cv2.destroyAllWindows()

main()
