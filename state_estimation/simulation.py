# Starter code for the Coursera SDC Course 2 final project.
#
# Author: Trevor Ablett and Jonathan Kelly
# University of Toronto Institute for Aerospace Studies

import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from rotations import angle_normalize, rpy_jacobian_axis_angle, Quaternion

from kalman import Kalman


#### 6. Results and Analysis ###################################################################

################################################################################################
# Now that we have state estimates for all of our sensor data, let's plot the results. This plot
# will show the ground truth and the estimated trajectories on the same plot. Notice that the
# estimated trajectory continues past the ground truth. This is because we will be evaluating
# your estimated poses from the part of the trajectory where you don't have ground truth!
################################################################################################


################################################################################################
# We can also plot the error for each of the 6 DOF, with estimates for our uncertainty
# included. The error estimates are in blue, and the uncertainty bounds are red and dashed.
# The uncertainty bounds are +/- 3 standard deviations based on our uncertainty (covariance).
################################################################################################


def report(p_est, v_est, q_est, p_cov, gt):
  est_traj_fig = plt.figure()
  ax = est_traj_fig.add_subplot(111, projection='3d')
  ax.plot(p_est[:, 0], p_est[:, 1], p_est[:, 2], label='Estimated')
  ax.plot(gt.p[:, 0], gt.p[:, 1], gt.p[:, 2], label='Ground Truth')
  ax.set_xlabel('Easting [m]')
  ax.set_ylabel('Northing [m]')
  ax.set_zlabel('Up [m]')
  ax.set_title('Ground Truth and Estimated Trajectory')
  ax.set_xlim(0, 200)
  ax.set_ylim(0, 200)
  ax.set_zlim(-2, 2)
  ax.set_xticks([0, 50, 100, 150, 200])
  ax.set_yticks([0, 50, 100, 150, 200])
  ax.set_zticks([-2, -1, 0, 1, 2])
  ax.legend(loc=(0.62, 0.77))
  ax.view_init(elev=45, azim=-50)
  plt.show()

  error_fig, ax = plt.subplots(2, 3)
  error_fig.suptitle('Error Plots')
  num_gt = gt.p.shape[0]
  p_est_euler = []
  p_cov_euler_std = []

  # Convert estimated quaternions to euler angles
  for i in range(len(q_est)):
    qc = Quaternion(*q_est[i, :])
    p_est_euler.append(qc.to_euler())

    # First-order approximation of RPY covariance
    J = rpy_jacobian_axis_angle(qc.to_axis_angle())
    p_cov_euler_std.append(np.sqrt(np.diagonal(J @ p_cov[i, 6:, 6:] @ J.T)))

  p_est_euler = np.array(p_est_euler)
  p_cov_euler_std = np.array(p_cov_euler_std)

  # Get uncertainty estimates from P matrix
  p_cov_std = np.sqrt(np.diagonal(p_cov[:, :6, :6], axis1=1, axis2=2))

  titles = ['Easting', 'Northing', 'Up', 'Roll', 'Pitch', 'Yaw']
  for i in range(3):
    ax[0, i].plot(range(num_gt), gt.p[:, i] - p_est[:num_gt, i])
    ax[0, i].plot(range(num_gt), 3 * p_cov_std[:num_gt, i], 'r--')
    ax[0, i].plot(range(num_gt), -3 * p_cov_std[:num_gt, i], 'r--')
    ax[0, i].set_title(titles[i])
  ax[0, 0].set_ylabel('Meters')

  for i in range(3):
    ax[1, i].plot(range(num_gt),
                  angle_normalize(gt.r[:, i] - p_est_euler[:num_gt, i]))
    ax[1, i].plot(range(num_gt), 3 * p_cov_euler_std[:num_gt, i], 'r--')
    ax[1, i].plot(range(num_gt), -3 * p_cov_euler_std[:num_gt, i], 'r--')
    ax[1, i].set_title(titles[i + 3])
  ax[1, 0].set_ylabel('Radians')
  plt.show()


#### 7. Submission #############################################################################

################################################################################################
# Now we can prepare your results for submission to the Coursera platform. Uncomment the
# corresponding lines to prepare a file that will save your position estimates in a format
# that corresponds to what we're expecting on Coursera.
################################################################################################

def save_estimates(p_est, indices, filename):
  """
  Save the position estimates to a file.

  Args:
      p_est (np.ndarray): Position estimates array.
      indices (list): List of indices to save.
      filename (str): Name of the file to save the estimates.
  """
  result_str = ''
  for val in indices:
    for i in range(3):
      result_str += '%.3f ' % (p_est[val, i])
  with open(filename, 'w') as file:
    file.write(result_str)


#### 1. Data ###################################################################################

################################################################################################
# This is where you will load the data from the pickle files. For parts 1 and 2, you will use
# p1_data.pkl. For Part 3, you will use pt3_data.pkl.
################################################################################################
with open('data/pt3_data.pkl', 'rb') as file:
  data = pickle.load(file)

################################################################################################
# Each element of the data dictionary is stored as an item from the data dictionary, which we
# will store in local variables, described by the following:
#   gt: Data object containing ground truth. with the following fields:
#     a: Acceleration of the vehicle, in the inertial frame
#     v: Velocity of the vehicle, in the inertial frame
#     p: Position of the vehicle, in the inertial frame
#     alpha: Rotational acceleration of the vehicle, in the inertial frame
#     w: Rotational velocity of the vehicle, in the inertial frame
#     r: Rotational position of the vehicle, in Euler (XYZ) angles in the inertial frame
#     _t: Timestamp in ms.
#   imu_f: StampedData object with the imu specific force data (given in vehicle frame).
#     data: The actual data
#     t: Timestamps in ms.
#   imu_w: StampedData object with the imu rotational velocity (given in the vehicle frame).
#     data: The actual data
#     t: Timestamps in ms.
#   gnss: StampedData object with the GNSS data.
#     data: The actual data
#     t: Timestamps in ms.
#   lidar: StampedData object with the LIDAR data (positions only).
#     data: The actual data
#     t: Timestamps in ms.
################################################################################################
gt = data['gt']
imu_f = data['imu_f']
imu_w = data['imu_w']
gnss = data['gnss']
lidar = data['lidar']

################################################################################################
# Let's plot the ground truth trajectory to see what it looks like. When you're testing your
# code later, feel free to comment this out.
################################################################################################
gt_fig = plt.figure()
ax = gt_fig.add_subplot(111, projection='3d')
ax.plot(gt.p[:, 0], gt.p[:, 1], gt.p[:, 2])
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')
ax.set_title('Ground Truth trajectory')
ax.set_zlim(-1, 5)
# plt.show()

################################################################################################
# Remember that our LIDAR data is actually just a set of positions estimated from a separate
# scan-matching system, so we can insert it into our solver as another position measurement,
# just as we do for GNSS. However, the LIDAR frame is not the same as the frame shared by the
# IMU and the GNSS. To remedy this, we transform the LIDAR data to the IMU frame using our
# known extrinsic calibration rotation matrix C_li and translation vector t_i_li.
#
# THIS IS THE CODE YOU WILL MODIFY FOR PART 2 OF THE ASSIGNMENT.
################################################################################################
# Correct calibration rotation matrix, corresponding to Euler RPY angles (0.05, 0.05, 0.1).
C_li = np.array([
    [0.99376, -0.09722, 0.05466],
    [0.09971, 0.99401, -0.04475],
    [-0.04998, 0.04992, 0.9975]
])

t_i_li = np.array([0.5, 0.1, 0.5])

# Transform from the LIDAR frame to the vehicle (IMU) frame.
lidar.data = (C_li @ lidar.data.T).T + t_i_li

#### 2. Constants ##############################################################################

################################################################################################
# Now that our data is set up, we can start getting things ready for our solver. One of the
# most important aspects of a filter is setting the estimated sensor variances correctly.
# We set the values here.
################################################################################################

var_imu_f = 1.0
var_imu_w = 1.0
var_gnss = 25.0
var_lidar = 0.5

################################################################################################
# We can also set up some constants that won't change for any iteration of our solver.
################################################################################################

g = np.array([0, 0, -9.81])  # gravity
l_jac = np.zeros([9, 6])
l_jac[3:, :] = np.eye(6)  # motion model noise jacobian
h_jac = np.zeros([3, 9])
h_jac[:, :3] = np.eye(3)  # measurement model jacobian


#### 5. Main Filter Loop #######################################################################

################################################################################################
# Now that everything is set up, we can start taking in the sensor data and creating estimates
# for our state in a loop.
################################################################################################

kalman = Kalman(gt, imu_f, imu_w, gnss, lidar, g, l_jac, h_jac, var_imu_f, var_imu_w, var_gnss, var_lidar)
p_est, v_est, q_est, p_cov = kalman.predict()

# Usage for Part 1
save_estimates(p_est, [9000, 9400, 9800, 10200, 10600], 'output/pt1_submission.txt')

# Usage for Part 2
save_estimates(p_est, [9000, 9400, 9800, 10200, 10600], 'output/pt2_submission.txt')

# Usage for Part 3
save_estimates(p_est, [6800, 7600, 8400, 9200, 10000], 'output/pt3_submission.txt')

report(p_est, v_est, q_est, p_cov, gt)
