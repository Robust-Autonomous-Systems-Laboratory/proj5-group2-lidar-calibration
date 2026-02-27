# TODO:
#   - Make custom statistics msg (mean, std deviation, outlier count)
#   - 


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64

class CalibrationNode(Node):
    def __init__(self):
        super().__init__('kf_node')
        # Params
        self.declare_parameter('target_distance', 0.0)
        self.declare_parameter('target_angle', 0.0)
        self.declare_parameter('angle_window', 0.1)
        # Subs
        self.scan_sub = self.create_subscription(
                LaserScan,
                '/scan',
                self.scanSub,
                20)
        # Pubs
        self.error_pub = self.create_publisher(
                Float64,
                '/calibration/range_error',
                20)
        self.stat_pub = self.create_publisher(
                Float64,    # TODO Change this!!!
                '/calibration/statistics',
                20)
    
    def scanSub(self, msg):
        pass
