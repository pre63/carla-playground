
import numpy as np


class LateralModel:
  def __init__(self):
    self.k_e = 0.3

  def calculate_crosstrack_error(self, waypoints, current_pos):
    waypoints = np.array(waypoints)
    diffs = waypoints[:, :2] - current_pos
    dists = np.hypot(diffs[:, 0], diffs[:, 1])
    min_dist_index = np.argmin(dists)
    nearest_waypoint = waypoints[min_dist_index]
    return dists[min_dist_index], nearest_waypoint

  def compute_control(self, waypoints, x, y, yaw, v):
    current_pos = np.array([x, y])
    crosstrack_error, nearest_waypoint = self.calculate_crosstrack_error(waypoints, current_pos)

    yaw_path = np.arctan2(
        nearest_waypoint[1] - waypoints[0][1],
        nearest_waypoint[0] - waypoints[0][0]
    )

    yaw_diff_heading = yaw_path - yaw
    yaw_diff_heading = (yaw_diff_heading + np.pi) % (2 * np.pi) - np.pi

    yaw_cross_track = np.arctan2(y - nearest_waypoint[1], x - nearest_waypoint[0])
    yaw_path2ct = yaw_path - yaw_cross_track
    yaw_path2ct = (yaw_path2ct + np.pi) % (2 * np.pi) - np.pi

    crosstrack_error = abs(crosstrack_error) if yaw_path2ct > 0 else -abs(crosstrack_error)
    yaw_diff_crosstrack = np.arctan(self.k_e * crosstrack_error / (v + 1e-5))

    steer_expect = yaw_diff_crosstrack + yaw_diff_heading
    steer_expect = (steer_expect + np.pi) % (2 * np.pi) - np.pi
    steer_expect = np.clip(steer_expect, -1.22, 1.22)

    return steer_expect
