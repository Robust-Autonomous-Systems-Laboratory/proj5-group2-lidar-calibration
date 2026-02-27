# TODO:
#   - Save data to YAML when exited


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import math
import yaml

class CalibrationNode(Node):
    def __init__(self):
        super().__init__('calibration_node')
        # Params
        self.declare_parameter('target_distance', 1.0)  # TODO Change this to actual distance to target
        self.declare_parameter('target_angle', 0.0)
        self.declare_parameter('angle_window', 0.1)
        # Subs
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.scan_sub = self.create_subscription(
                LaserScan,
                '/scan',
                self.scanSub,
                qos)
        # Pubs
        self.error_pub = self.create_publisher(
                Float64,
                '/calibration/range_error',
                20)
        self.stat_pub = {
                'range_mean' : self.create_publisher(Float64, '/calibration/statistics/range_mean', 20),
                'range_sd' : self.create_publisher(Float64, '/calibration/statistics/range_sd', 20),
                'outlier_count' : self.create_publisher(Float64, '/calibration/statistics/outlier_count', 20),
                'hit_sd' : self.create_publisher(Float64, '/calibration/statistics/hit_sd', 20),
                         }
        # Vars
        self.mean = self.get_parameter('target_distance').get_parameter_value().double_value
        self.n = 0
        self.M2 = 0.0
        self.variance = None
        self.outlier_count = 0
    
    def scanSub(self, msg):
        target_distance = self.get_parameter('target_distance').get_parameter_value().double_value
        target_angle = self.get_parameter('target_angle').get_parameter_value().double_value
        angle_window = self.get_parameter('angle_window').get_parameter_value().double_value
        ranges = msg.ranges
        i = int((target_angle - msg.angle_min) / msg.angle_increment)
        self.get_logger().info(f"Range measured {ranges[i]}")
        # Publish error
        error = Float64()
        e = ranges[i] - target_distance
        error.data = e
        self.error_pub.publish(error)
        # Calculate hit sd
        self.n += 1
        hit_sd = math.sqrt(e**2/self.n)
        if self.variance is not None:
            if ranges[i] < target_distance - 3*math.sqrt(self.variance) or ranges[i] > target_distance + 3*math.sqrt(self.variance):
                self.get_logger().warn(f"Outlier detected: {ranges[i]}")
                self.outlier_count += 1
        # Welford's online algorithm
        delta = ranges[i] - self.mean
        self.mean += delta / self.n
        self.M2 += delta * (ranges[i] - self.mean)
        self.variance = self.M2 / (self.n)
        # Publish statistics
        for stat_name in self.stat_pub:
            stat_msg = Float64()
            if stat_name == 'range_mean':
                stat_msg.data = self.mean
            elif stat_name == 'range_sd':
                stat_msg.data = math.sqrt(self.variance)
            elif stat_name == 'outlier_count':
                stat_msg.data = float(self.outlier_count)
            elif stat_name == 'hit_sd':
                stat_msg.data = hit_sd
            self.stat_pub[stat_name].publish(stat_msg)
    
    def destroy_node(self):
        data = {
                'range_mean': self.mean,
                'range_std_deviation': math.sqrt(self.variance) if self.variance is not None else None,
                'outlier_count': self.outlier_count,
                'hit_std_deviation': math.sqrt(self.M2 / self.n),
                }
        with open('calibration_results.yaml', 'w') as f:
            yaml.dump(data, f)
            self.get_logger().info("Interrupt detected! Logging results...")
        super().destroy_node()

def main():
    rclpy.init()
    node = CalibrationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except:
            pass

if __name__ == '__main__':
    main()
