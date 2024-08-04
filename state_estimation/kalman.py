# Kalman Filter implementation for state estimation.
#
# Author: Trevor Ablett, Jonathan Kelly, Simon Green
# University of Toronto Institute for Aerospace Studies

import numpy as np
from numpy.linalg import inv
from mpl_toolkits.mplot3d import Axes3D
from rotations import Quaternion, skew_symmetric


class Kalman:
  def __init__(self, gt, imu_f, imu_w, gnss, lidar, g, l_jac,
               h_jac, var_imu_f, var_imu_w, var_lidar, var_gnss):
    """
    Initialize the Kalman Filter with
    :param gt: Ground truth data
    :param imu_f: IMU specific force data
    :param imu_w: IMU angular velocity data
    :param gnss: GNSS data
    :param lidar: LIDAR data
    :param g: Gravity vector
    :param l_jac: Jacobian of the motion model
    :param h_jac: Jacobian of the measurement model
    :param var_imu_f: Variance of the IMU specific force
    :param var_imu_w: Variance of the IMU angular velocity
    :param var_lidar: Variance of the LIDAR measurements
    :param var_gnss: Variance of the GNSS measurements
    """

    self.gt = gt
    self.imu_f = imu_f
    self.imu_w = imu_w
    self.gnss = gnss
    self.lidar = lidar
    self.g = g
    self.l_jac = l_jac
    self.h_jac = h_jac
    self.var_imu_f = var_imu_f
    self.var_imu_w = var_imu_w
    self.var_lidar = var_lidar
    self.var_gnss = var_gnss

  def wraptopi(self, x):
    """
    Wrap angle to [-pi, pi].
    """
    if x > np.pi:
      x = x - (np.floor(x / (2 * np.pi)) + 1) * 2 * np.pi
    elif x < -np.pi:
      x = x + (np.floor(x / (-2 * np.pi)) + 1) * 2 * np.pi
    return x

  def measurement_update(self, sensor_var, p_cov_check, y_k, p_check, v_check, q_check):
    """
    Measurement update function of EKF.
    """
    # 3.1 Compute Kalman gain
    r_cov = np.eye(3) * sensor_var
    k_gain = p_cov_check @ self.h_jac.T @ np.linalg.inv(self.h_jac @ p_cov_check @ self.h_jac.T + r_cov)

    # 3.2 Compute error state
    x_error = k_gain @ (y_k - p_check) * 0.9

    # 3.3 Correct predicted state
    p_hat = p_check + x_error[:3]
    v_hat = v_check + x_error[3:6]
    q_hat = Quaternion(axis_angle=x_error[6:9]).quat_mult_left(q_check, out='Quaternion')

    # 3.4 Compute corrected covariance
    p_cov_hat = (np.eye(9) - k_gain @ self.h_jac) @ p_cov_check

    return p_hat, v_hat, q_hat, p_cov_hat

  def predict(self):
    """
    Implement the EKF prediction and update steps.
    """
    p_est = np.zeros([self.imu_f.data.shape[0], 3])  # position estimates
    v_est = np.zeros([self.imu_f.data.shape[0], 3])  # velocity estimates
    q_est = np.zeros([self.imu_f.data.shape[0], 4])  # orientation estimates as quaternions
    p_cov = np.zeros([self.imu_f.data.shape[0], 9, 9])  # covariance matrices at each timestep

    # Set initial values.
    p_est[0] = self.gt.p[0]
    v_est[0] = self.gt.v[0]
    q_est[0] = Quaternion(euler=self.gt.r[0]).to_numpy()
    p_cov[0] = np.zeros(9)  # covariance of estimate
    gnss_i = 0
    lidar_i = 0

    for k in range(1, self.imu_f.data.shape[0]):  # start at 1 b/c we have initial prediction from gt
      delta_t = self.imu_f.t[k] - self.imu_f.t[k - 1]

      # 1. Update state with IMU inputs
      c_ns = Quaternion(*q_est[k - 1]).to_mat()
      c_ns_dot_f_km = np.dot(c_ns, self.imu_f.data[k - 1])
      p_check = p_est[k - 1] + delta_t * v_est[k - 1] + (delta_t**2 / 2) * (c_ns_dot_f_km + self.g)
      v_check = v_est[k - 1] + delta_t * (c_ns_dot_f_km + self.g)
      q_from_w = Quaternion(axis_angle=self.imu_w.data[k - 1] * delta_t)
      q_check = q_from_w.quat_mult_right(q_est[k - 1], out='Quaternion')

      # 1.1 Linearize the motion model and compute Jacobians
      f_jac_km = np.eye(9)
      f_jac_km[0:3, 3:6] = np.eye(3) * delta_t
      f_jac_km[3:6, 6:9] = -skew_symmetric(c_ns_dot_f_km) * delta_t

      # 2. Propagate uncertainty
      q_cov_km = np.zeros((6, 6))
      q_cov_km[0:3, 0:3] = delta_t**2 * np.eye(3) * self.var_imu_f
      q_cov_km[3:6, 3:6] = delta_t**2 * np.eye(3) * self.var_imu_w
      p_cov_check = f_jac_km @ p_cov[k - 1] @ f_jac_km.T + self.l_jac @ q_cov_km @ self.l_jac.T

      # 3. Check availability of GNSS and LIDAR measurements
      if gnss_i < self.gnss.data.shape[0] and self.imu_f.t[k] >= self.gnss.t[gnss_i]:
        p_check, v_check, q_check, p_cov_check = self.measurement_update(self.var_gnss, p_cov_check, self.gnss.data[gnss_i].T, p_check, v_check, q_check)
        gnss_i += 1

      if lidar_i < self.lidar.data.shape[0] and self.imu_f.t[k] >= self.lidar.t[lidar_i]:
        p_check, v_check, q_check, p_cov_check = self.measurement_update(self.var_lidar, p_cov_check, self.lidar.data[lidar_i].T, p_check, v_check, q_check)
        lidar_i += 1

      # Save updated state
      p_est[k] = p_check
      v_est[k] = v_check
      q_est[k] = q_check.to_numpy()
      p_cov[k] = p_cov_check

    return p_est, v_est, q_est, p_cov
