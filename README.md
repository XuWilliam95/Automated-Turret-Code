Automated Laser Turret

The idea is an inexpensive, flexible robotic system which would automatically target people and shine a laser at their center of mass. 

Design goals:
Small, inexpensive two-servo design. \n
Utilizing as many common, off-the-shelf components to allow for easy repair/replacement of parts.\n
Arduino Uno or compatible microcontroller board
Serial communication between microcontroller board and PC
One 5V laser diode to indicate firing path
Utilizing OpenCV and MediaPipe libraries to help with computer vision and target recognition

The current platform is built around a set of servos. The two servos each have a turn radius of 180°. Everything is attached together using common screws, metal bars, and hot glue. The webcam is attached to the servo via a metal offset and a screw. A laser diode is attached to directly above the camera lens via hot glue,
The servos, along with the laser diode are connected to an Arduino Uno and the Arduino is attached to a PC setup for serial communication via Pyserial (constant back-and-forth communication between PC and Arduino). On the PC is the main code for the turret, which is written in Python 3. As stated above, OpenCV is used for computer vision  while MediaPipe is used for body recognition. 

Future Goals: 
Replace servo motors with stepper motors 
Incorporate PID controllers to allow for smoother tracking
Create wooden/plastic frame
Replace laser diode with electric airsoft/NERF gun
Utilize 3D printed fittings to replace the need to use metal bars and 
 
