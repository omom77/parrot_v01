# All measurements in millimeters
import numpy as np

# offset for joint 0
d1 = 0.05
servo_joints = {
    "joint0": 11,
    "joint1": 10,
    "joint2": 9,
    "joint3": 3,
    "gripper": 5,
}
link_length = {
    "link0": 0,
    "link1": 67.4,
    "link2": 67.4,
    "link3": 53,
}
joint_angles = {
    "theta0": 0,
    "theta1": 0,
    "theta2": 0,
    "theta3": 0
}

twist_angles = {
    "alpha0": 0,
    "alpha1": 0,
    "alpha2": 45,
    "alpha3": 0,
}

define_servo = list(servo_joints.values())  # store only servo pin numbers
j_angles = list(joint_angles.values())  # store only joint angles
list_link_length = list(link_length.values())

# for i in joint_angles:
#     radian_angles = np.deg2rad(j_angles)  # Convert joint angles from degrees to radians
ee = [100, 80, 40]
# sigma = j_angles[1] + j_angles[2] + j_angles[3]
sigma = 180

# gamma = arc tan((z - d1)/ sqrt(x^2 + y^2))
# gamma = np.arctan((ee[2] - 0) / np.sqrt((np.square(ee[0])) + np.square(ee[1])))
gamma = np.arctan(ee[1] / ee[0])
print("ga    ", gamma)

# xq = x - a4 sin(sigma)
xq = ee[1] - (list_link_length[3] * np.sin(sigma))
print("xq   ", xq)

# xq = z - a4 sin(sigma)
zq = ee[2] - (list_link_length[3] * np.sin(sigma))
print("zq   ", zq)

# cq = square root ((xq - a1)^2 + y^2 + (zq - d1)^2)
cq = np.sqrt(np.square(xq - list_link_length[0]) + np.square(ee[1]) + np.square(zq - d1))
print("cq   ", cq)

#  cp = square root ((x-a1)^2 + y^2 + (zq - d1)^2)
cp = np.sqrt(np.square(ee[0] - list_link_length[0]) + np.square(ee[1]) + np.square(ee[2] - d1))
print("cp   ", cp)

# beta = arc cos((cq^2 + cp^2 - a4^2) / 2 * cp * cq)
# beta = np.arc cos((np.square(cq) + np.square(cp) + np.square(list_link_length[3])) / 2 * cq * cp)
arg = (np.square(cq) + np.square(cp) + np.square(list_link_length[3])) / (2 * cq * cp)
beta = np.arccos(np.clip(arg, -1, 1))
print("beta   ", beta)

# alpha = arc cos((cq^2 + a2^2 - a3^2) / 2 * cq * a2)
alpha = np.arccos((np.square(cq) + np.square(list_link_length[1]) - np.square(list_link_length[2])) / 2 * cq
                  * list_link_length[1])

j_angles[0] = np.arctan(ee[1] / ee[0])


j_angles[1] = alpha + beta + gamma

j_angles[2] = np.pi - np.arccos((np.square(list_link_length[1]) + np.square(list_link_length[2]) - np.square(cq))
                                / 2 * list_link_length[1] * list_link_length[2])

j_angles[3] = sigma - j_angles[1] - j_angles[2]
