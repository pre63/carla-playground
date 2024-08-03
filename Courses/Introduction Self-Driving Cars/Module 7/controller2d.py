#!/usr/bin/env python3

"""
2D Controller Class to be used for the CARLA waypoint follower demo.
"""

import cutils
import numpy as np

from longitudinal_model import LongitudinalModel
from lateral_model import LateralModel

class Controller2D:
  def __init__(self, waypoints):
    self.vars = cutils.CUtils()
    self._current_x = 0
    self._current_y = 0
    self._current_yaw = 0
    self._current_speed = 0
    self._desired_speed = 0
    self._current_frame = 0
    self._current_timestamp = 0
    self._start_control_loop = False
    self._set_throttle = 0
    self._set_brake = 0
    self._set_steer = 0
    self._waypoints = waypoints
    self._conv_rad_to_steer = 180.0 / 70.0 / np.pi
    self._pi = np.pi
    self._2pi = 2.0 * np.pi

    self.longitudinal_model = LongitudinalModel()
    self.lateral_model = LateralModel()

  def update_values(self, x, y, yaw, speed, timestamp, frame):
    self._current_x = x
    self._current_y = y
    self._current_yaw = yaw
    self._current_speed = speed
    self._current_timestamp = timestamp
    self._current_frame = frame
    if self._current_frame:
      self._start_control_loop = True

  def update_desired_speed(self):
    min_idx = 0
    min_dist = float("inf")
    desired_speed = 0
    for i in range(len(self._waypoints)):
      dist = np.linalg.norm(np.array([
          self._waypoints[i][0] - self._current_x,
          self._waypoints[i][1] - self._current_y]))
      if dist < min_dist:
        min_dist = dist
        min_idx = i
    if min_idx < len(self._waypoints) - 1:
      desired_speed = self._waypoints[min_idx][2]
    else:
      desired_speed = self._waypoints[-1][2]
    self._desired_speed = desired_speed

  def update_waypoints(self, new_waypoints):
    self._waypoints = new_waypoints

  def get_commands(self):
    return self._set_throttle, self._set_steer, self._set_brake

  def set_throttle(self, input_throttle):
    throttle = np.fmax(np.fmin(input_throttle, 1.0), 0.0)
    self._set_throttle = throttle

  def set_steer(self, input_steer_in_rad):
    input_steer = self._conv_rad_to_steer * input_steer_in_rad
    steer = np.fmax(np.fmin(input_steer, 1.0), -1.0)
    self._set_steer = steer

  def set_brake(self, input_brake):
    brake = np.fmax(np.fmin(input_brake, 1.0), 0.0)
    self._set_brake = brake

  def update_controls(self):
    x = self._current_x
    y = self._current_y
    yaw = self._current_yaw
    v = self._current_speed
    self.update_desired_speed()
    v_desired = self._desired_speed
    t = self._current_timestamp
    waypoints = self._waypoints

    if self._start_control_loop:
      throttle_output, brake_output = self.longitudinal_model.compute_control(v_desired, v, t)
      steer_output = self.lateral_model.compute_control(waypoints, x, y, yaw, v)

      self.set_throttle(throttle_output)
      self.set_steer(steer_output)
      self.set_brake(brake_output)

    self.vars.v_previous = v
    self.vars.throttle_previous = throttle_output
    self.vars.t_previous = t
    self.vars.error_previous = v_desired - v
    self.vars.integral_error_previous = self.longitudinal_model.vars['integral_error_previous']
