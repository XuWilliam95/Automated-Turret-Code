import cv2
import serial
import serial.tools.list_ports
import math

class NoArduino(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def find_arduino():
    ports = list(serial.tools.list_ports.comports())

    # looks through the ports to find if an arduino is availible for serial communication
    arduino_found = False
    for p in ports:
        if 'Arduino' in p.manufacturer:
            arduino = serial.Serial(port=p.device, baudrate=9600, timeout=.1)
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

def circle_shoot(c1, c2, image, arduino, mode):
    if overlap(c1, c2, mode):
        # shows fire on screen when target is with the defined tolerance
        cv2.putText(image, "fire", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        # sends a message to the arduino
        arduino.write(bytes('1', 'utf-8'))
    else:
        arduino.write(bytes('0', 'utf-8'))

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
# if the center of the tracking circle is in the target shoot
def overlap(c1: list, c2: list, mode: str) -> bool:
    # center of the smaller circle is in the larger one
    if mode == 'center':
        return distance(c1, c2) < max(c1[2], c2[2])
    # edges touch
    elif mode == 'edge':
        return distance(c1, c2) < (c1[2] + c2[2])

# reference full body landmarks png 
def torso_coords(results):
    torso_center_x = ((results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x)/2 + 
                      (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x)/2)/2
    torso_center_y = ((results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[23].y)/2 + 
                      (results.pose_landmarks.landmark[24].y + results.pose_landmarks.landmark[12].y)/2)/2
    # print ("centered torso x cord: ", torso_center_x, "\ncentered torso y cord: ", torso_center_y)
    return torso_center_x, torso_center_y

def upperchest_coords(results):
    upperchest_x = (results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x)/2
    upperchest_y = (results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[12].y)/2
    return upperchest_x, upperchest_y

def draw_pose(results, image, mp_drawing, mp_pose, mp_drawing_styles):
    mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

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

def servo_movment(c1, c2, arduino):
    if overlap(c1, c2, 'edge'):
        return

    # move up
    if c1[1] > c2[1]:
        arduino.write(bytes('2', 'utf-8'))
        print('up')
        # turn motor up
        ... 

    # move down
    if c1[1] < c2[1]:
        arduino.write(bytes('-2', 'utf-8'))
        print('down')
        # turn motor down
        ...

    # move right (flipped view)
    if c1[0] > c2[0]:
        arduino.write(bytes('4', 'utf-8'))
        print('right')
        # turn motor counterclockwise
        ... 

    # move left
    if c1[0] < c2[0]:
        arduino.write(bytes('-4', 'utf-8'))
        print('left')
        # turn motor clockwise
        ... 
    ...

