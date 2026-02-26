import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

# access bags in the data dir within the package
storage_options = rosbag2_py.StorageOptions(uri='./data/lidar_calibration_2m/', storage_id='mcap')
converter_options = rosbag2_py.ConverterOptions('', '')
reader = rosbag2_py.SequentialReader()
reader.open(storage_options, converter_options)

# iterate over all messages in bag and extract ranges
while reader.has_next():
    (topic, data, t) = reader.read_next()
    # deserialize the message
    msg_type = get_message('sensor_msgs/msg/LaserScan')
    msg = deserialize_message(data, msg_type)
    print(f"Read: {msg.ranges[0]} on topic: {topic} at {t}")