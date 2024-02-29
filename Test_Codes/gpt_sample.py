import numpy as np

def inverse_kinematics(end_effector_position, link_lengths):
    x, y, z = end_effector_position
    l1, l2, l3, l4 = link_lengths

    # Calculate theta1 (base joint angle)
    theta1 = np.arctan2(y, x)

    # Calculate theta3 (wrist joint angle)
    r = np.sqrt(x**2 + y**2)
    D = (r**2 + (z - l1)**2 - l2**2 - l4**2) / (2 * l2 * l4)
    theta3 = np.arctan2(np.sqrt(1 - D**2), D)

    # Calculate theta2 (shoulder joint angle)
    alpha = np.arctan2(z - l1, r)
    beta = np.arctan2(l4 * np.sin(theta3), l2 + l4 * np.cos(theta3))
    theta2 = alpha - beta

    # Calculate theta4 (gripper joint angle)
    theta4 = np.arctan2(l3, l4)

    return np.degrees([theta1, theta2, theta3, theta4])

# Example usage
end_effector_position = [80, 80, 80]
link_lengths = [0, 67, 67, 53]

joint_angles = inverse_kinematics(end_effector_position, link_lengths)
print("Joint Angles:", joint_angles)
