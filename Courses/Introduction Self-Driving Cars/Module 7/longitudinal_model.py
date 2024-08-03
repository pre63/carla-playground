
import numpy as np


class LongitudinalModel:
  def __init__(self):
    self.kp = 1.0
    self.ki = 0.2
    self.kd = 0.01
    self.vars = {
        'v_previous': 0.0,
        't_previous': 0.0,
        'error_previous': 0.0,
        'integral_error_previous': 0.0,
        'throttle_previous': 0.0
    }

  def compute_control(self, v_desired, v, t):
    st = t - self.vars['t_previous']
    if st <= 0:
      st = 1e-5  # Small threshold to prevent division by zero

    e_v = v_desired - v
    max_integral = 10.0
    inte_v = np.clip(self.vars['integral_error_previous'] + e_v * st, -max_integral, max_integral)
    derivate = (v - self.vars['v_previous']) / st

    acc = self.kp * e_v + self.ki * inte_v + self.kd * derivate

    throttle_output = (np.tanh(acc) + 1) / 2 if acc > 0 else 0
    if throttle_output - self.vars['throttle_previous'] > 0.1:
      throttle_output = self.vars['throttle_previous'] + 0.1

    self.vars['v_previous'] = v
    self.vars['t_previous'] = t
    self.vars['error_previous'] = e_v
    self.vars['integral_error_previous'] = inte_v
    self.vars['throttle_previous'] = throttle_output

    return throttle_output, 0  # Returning throttle_output and brake_output (not used)
