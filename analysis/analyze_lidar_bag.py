import rosbag2_py
import matplotlib.pyplot as plt
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

bag_name = 'lidar_calibration_0.5m' # adjust this for each bag to test
target_distance = 0.5 # adjust for each distance, in meters

# currently +/- 5 degrees (10 degree forward slice)
start_index = -5
stop_index = 6

# aggregated list
ranges = []

# access bags in the data dir within the package
storage_options = rosbag2_py.StorageOptions(uri='./data/' + bag_name, storage_id='mcap')
converter_options = rosbag2_py.ConverterOptions('', '')
reader = rosbag2_py.SequentialReader()
reader.open(storage_options, converter_options)

# iterate over all messages in bag and extract ranges
while reader.has_next():
    (topic, data, t) = reader.read_next()
    # deserialize the message
    msg_type = get_message('sensor_msgs/msg/LaserScan')
    msg = deserialize_message(data, msg_type)

    # iterate over desired angles and collect range data in list
    for i in range(start_index, stop_index):
        ranges.append(msg.ranges[i])

# plot histogram for each distance (bag)
plt.figure(figsize=(10,4))
plt.hist(ranges, bins=10, color='xkcd:sky blue')

# plot vertical line
plt.axvline(target_distance, color='r', linestyle='dashed', linewidth=2)

# plot labels
plt.xlabel("Range [m]")
plt.ylabel("Frequency")
plt.title(f"{target_distance}m Range Data Analysis")

plt.savefig('./analysis/figures/' + bag_name + '.png')  # adjust so filename is a param
plt.show()

