import numpy as np
import pandas as pd
import math

# Store each Joints Homogenous Transformation Matrix(htm) in a list
transformation_matrix = []

# Set print options to display numbers within a fixed precision
np.set_printoptions(precision=6, suppress=True)

df = pd.read_csv('Test_Codes/Book1.csv')
print(df)

# Radian - Default Unit for angles
j_offset = df['joint offset'].tolist()
j_angle = df['joint angle'].tolist()
l_length = df['link length'].tolist()
t_angle = df['twist angle'].tolist()
t_angle_rad = np.deg2rad(t_angle)

print("\n Joint Angle : ", j_angle)
print("\n Twist Angle : ", t_angle)
print("\n Twist Angle Radian : ", t_angle_rad)
print("\n Joint Offset : ", j_offset)
print("\n Link Length : ", l_length)

# Pin Layout of each servo motor for each joint
servo_joints = {
    "joint1": 11,
    "joint2": 10,
    "joint3": 9,
    "joint4": 3,
    "gripper": 5,
}
servo = list(servo_joints.values())  # store only servo pin numbers


# print(servo)
# print(j_angle)
# print(type(l_length))

def htm(theta, alpha, link_len, bi):
    transform = np.array([
        [np.cos(theta), (-np.sin(theta) * np.cos(alpha)), np.sin(theta) * np.sin(alpha), link_len * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), (-np.cos(theta) * np.sin(alpha)), link_len * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), bi],
        [0, 0, 0, 1]
    ])

    # Check the data type of the above numpy array
    print(transform.dtype)

    # T1 = ft1.astype('int32')  # Convert to Integer data type
    # print(np.round(1.039445, 2))        # Round values to 4 decimal places
    T1 = np.round(transform, 4)
    return T1


ee = [80.0, 80.0, 50.0]

# All angles in radian, convert to degrees before exporting the values

# Finding Ø1 - Link1 angle
j_angle[0] = np.arctan(ee[1] / ee[0])

# Finding Ø3 - Link3 angle
pre_theta2 = ((np.square(ee[0]) + np.square(ee[1]) - np.square(l_length[2]) - np.square(l_length[3]))
              / (2 * l_length[2] * l_length[3]))
print("Pre theta3 : ", pre_theta2)

j_angle[2] = np.arccos(pre_theta2)

# Finding Ø2 - Link2 angle
beta = np.arctan(ee[1] / ee[0])

sq_xy = np.sqrt(np.square(ee[0]) + np.square(ee[1]))
alpha = np.arccos((np.square(ee[0]) + np.square(ee[1]) + np.square(l_length[2]) - np.square(l_length[3])) /
                  (2 * l_length[2] * sq_xy))

# theta = +ve if theta > 0
if j_angle[2] > 0:
    j_angle[1] = alpha + beta
# theta = -ve if theta < 0
if j_angle[2] < 0:
    j_angle[1] = alpha - beta

print("beta  ", np.rad2deg(beta))
print("alpha ", np.rad2deg(alpha))

# Print HTM Matrix for the first 3 Joints
for i in range(3):
    tt = htm(j_angle[i], t_angle_rad[i], l_length[i], j_offset[i])
    transformation_matrix.append(tt)
    print(transformation_matrix[i])

# Multiply the HTM matrix of J1, J2, J3 to get the position of Joint3
# Joint 3 position is used to find the position of the end effector
multiply = np.dot(transformation_matrix[0], transformation_matrix[1])
joint3_position = np.dot(multiply, transformation_matrix[2])
T1 = np.round(joint3_position, 4)
print("Link 3 position : \n", joint3_position)

# Next thing, convert the aboce list into array to access the elements of the HTM array stored in multiply

# Finding Ø4 - Link4 angle
# Q(Xq, Zq) Coordinates of joint 4
xq = ee[0] - joint3_position[0, 3]
zq = ee[2] - joint3_position[2, 3]

print("\nJoint 3 Tx :", joint3_position[0, 3])
print("Joint 3 Ty :", joint3_position[2, 3])

print("\nXq :", xq)
print("zq :", zq, "\n")

j_angle[3] = np.arctan(zq / xq)
# print("\nØ4 = ", np.rad2deg(j_angle[3]))

j_angle_degrees = np.rad2deg(j_angle)
for i in range(4):
    print("Ø", i + 1, " = ", j_angle_degrees[i])

# Finding Htm for 4th Joint
j4 = htm(j_angle[3], t_angle_rad[3], l_length[3], j_offset[3])

print("\n ParrotV1 Transformation Matrix :\n", np.dot(joint3_position, j4))

# j_angle[3] = np.arctan(ee[2] / ee[0]) - j_angle[1] - j_angle[2]

# print("Ø1 : ", np.rad2deg(j_angle[0]))
# print("Ø2 : ", np.rad2deg(j_angle[1]))
# print("Ø3 : ", np.rad2deg(j_angle[2]))
# print("Ø4 : ", np.rad2deg(j_angle[3]))

# j_angle[1] + j_angle[2] + j_angle[3] = np.arctan()
