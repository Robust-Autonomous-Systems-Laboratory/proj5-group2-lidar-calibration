# TODO:
#   - Make custom statistics msg (mean, std deviation, outlier count)
#   - Publish statistics every N samples instead of every scan 
#   - Add outlier rejection (e.g. if error > 3 std dev, ignore sample)
#   - Save data to YAML when exited


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64

class CalibrationNode(Node):
    def __init__(self):
        super().__init__('calibration_node')
        # Params
        self.declare_parameter('target_distance', 0.5)  # TODO Change this to actual distance to target
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
        self.stat_pub = self.create_publisher(
                Float64,    # TODO Change this!!!
                '/calibration/statistics',
                20)
        # Vars
        self.mean = self.get_parameter('target_distance').get_parameter_value().double_value
        self.n = 0
        self.M2 = 0.0
    
    def scanSub(self, msg):
        target_distance = self.get_parameter('target_distance').get_parameter_value().double_value
        target_angle = self.get_parameter('target_angle').get_parameter_value().double_value
        angle_window = self.get_parameter('angle_window').get_parameter_value().double_value
        ranges = msg.ranges
        i = int((target_angle - msg.angle_min) / msg.angle_increment)
        # Publish error
        error = Float64()
        error.data = ranges[i] - target_distance
        self.error_pub.publish(error)
        # Welford's online algorithm
        self.n += 1
        delta = ranges[i] - self.mean
        self.mean += delta / self.n
        self.M2 += delta * (ranges[i] - self.mean)
        variance = self.M2 / (self.n)
        # TODO Publish statistics

def main():
    rclpy.init()
    node = CalibrationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
