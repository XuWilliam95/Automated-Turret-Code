import cv2
import mediapipe as mp
import tracking_functions as tf
import cv2 

def main():
    cv2.namedWindow('window')
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # finds dimensions of the window
    win_width, win_height = frame.shape[1], frame.shape[0]
    c1 = [win_width//2, win_height//2, 40]
    arduino = tf.find_arduino()

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, image = cap.read()
            image = cv2.flip(image, 1)

            # To improve performance, optionally mark the image as not writeable to
            # dd pass by reference.
            image.flags.writeable = False   
            results = pose.process(image)

            # Draw the pose annotation on the image.
            tf.draw_pose(results, image, mp_drawing, mp_pose, mp_drawing_styles)

            if results.pose_landmarks is not None:
                
                torso_coords = tf.torso_coords(results)
                torso_bounds1 = [-0.5, 1.5, -0.5, 1.5] # upper chest (Note: Heavily Biased)
                torso_bounds2 = [0, 1, 0, 1] # center torso (Note: Unbiased)
                screen_bounds = [0, win_width, 0, win_height]
                # Parameters (image, center_coords, radius, color, thickness) # Note: Color is bgr
                cv2.circle(image, (c1[0], c1[1]), c1[2], (225, 203, 30), 2)
                c2 = tf.tracking(torso_coords, torso_bounds1, screen_bounds, image)
                tf.circle_shoot(c1, c2, image, arduino, mode='edge')
                tf.servo_movment(c1, c2, arduino)
                # torso_shoot(torso_center_x, torso_center_y, [0.4, 0.6], [0.35, 0.7], image, arduino)

            cv2.imshow('window', image)
            if cv2.waitKey(1) == ord ('d'):
                break
    
    arduino.write(bytes('0', 'utf-8'))
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
