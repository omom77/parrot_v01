import math
import numpy as np
# import pandas as pd
import xlrd

servo_pinno = {
    "j1": 11,
    "j2": 10,
    "j3": 9,
    "j4": 3,
    "gripper": 5,
}
link_length = {
    "l1": 0,
    "l2": 0.067,
    "l3": 0.067,
    "l4": 0.05,
}
joint_angles = {
    "t1": 90,
    "t2": 90,
    "t3": 90,
    "t4": 90
}

twist_angles = {
    "a1": 90,
    "a2": 0,
    "a3": 0,
    "a4": 0
}

joint_offset = {
    "jo1": 0.05,
    "jo2": 0,
    "jo3": 0,
    "jo4": 0
}

servo_pins = list(servo_pinno.values())  # store only servo pin numbers
ja = list(joint_angles.values())  # store only joint angles
ll = list(link_length.values())  # store values of link lengths
ta = list(twist_angles.values())  # store values of twist angles in degrees
jo = list(joint_offset.values())  # store values of joint offset in a list

# Convert joint angles from degrees to radians
for i in ja:
    ja_radian = np.deg2rad(ja)

# convert twist angles form degrees to radians
for i in ta:
    ta_radian = np.deg2rad(ta)

print("\nArduino Pins for Servos :\n", servo_pins)
print("\nLink Length in mm :\n", ll)
print("\nJoint Offset in degrees :\n", jo)
print("\nTwist angle(alpha) in radian :\n", ta_radian)
print("\nJoint Angle In Radian :\n", ja_radian, "\n")


def htm(theta, alpha, link_len, bi):
    ft1 = np.array([
        [np.cos(theta), (-np.sin(theta) * np.cos(alpha)), np.sin(theta) * np.sin(alpha), link_len * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), (-np.cos(theta) * np.sin(alpha)), link_len * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), bi],
        [0, 0, 0, 1]
    ])
    print(ft1.dtype)
    # T1 = ft1.astype('int32')  # Convert to Integer data type
    # print(np.round(1.039445, 2))        # Round values to 4 decimal places
    T1 = np.round(ft1, 4)
    return T1


for i in range(4):
    transform = htm(ja_radian[i], ta_radian[i], ll[i], jo[i])
    print("link", i + 1)
    print(transform, "\n")
