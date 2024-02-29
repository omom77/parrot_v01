# https://pyfirmata.readthedocs.io/en/latest/pyfirmata.html

from pyfirmata import ArduinoNano, SERVO
from time import sleep

board = ArduinoNano('COM13')
print("Version - ", board.get_firmata_version())

# Define servo PWM pins
servo = {"revolute": 11, "joint1": 10, "joint2": 9, "joint3": 3, "gripper": 5}
defineservo = list(servo.values())
userinput = list(servo.keys())

# Define Joystick X & Y axis pins
Xin = 4
Yin = 5

for i in servo:
    board.digital[servo[i]].mode = SERVO


def rotate(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)


for j in range(len(userinput)):
    print(str(j) + ". " + userinput[j])

while True:
    set_angle = int(input("Set Angle : "))
    if set_angle <= 180:
        (motor_select) = int(input("Select Motor : "))
        rotate(defineservo[motor_select], set_angle)
    else:
        print("Enter a valid angle")

    # revolute = input("Revolute : ")
    # board.digital[defineservo[0]].write(revolute)
    # joint1 = input("Joint 1 : ")
    # board.digital[defineservo[1]].write(joint1)
    # joint2 = input("Joint 2 : ")
    # board.digital[defineservo[2]].write(joint2)
    # joint3 = input("Joint 3 : ")
    # board.digital[defineservo[3]].write(joint3)
    # gripper = input("Gripper : ")
    # board.digital[defineservo[4]].write(joint3)

    # for i in range(0,180):
    #     rotate(defineservo[0], i)
    # for i in reversed(range(0, 180)):
    #     rotate(defineservo[0], i)
