import csv
import math
import statistics
import rosbag2_py
import matplotlib.pyplot as plt
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

bag_name = 'lidar_calibration_2m' # adjust this for each bag to test
target_distance = 2 # adjust for each distance, in meters

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

# remove nan values from ranges for processing/math
ranges = [x for x in ranges if not math.isnan(x)]

# 2.3 parameter estimation
# sigma_hit: compute the standard deviation of measurements around the true range
sum = 0

for i in ranges:
    sum = sum + ((i - target_distance)**2)

sigma_hit = math.sqrt(sum/len(ranges))

# bias: check if mean measurement differs systematically from the true range
bias = statistics.mean(ranges) - target_distance

# save to /data/parameter_estimation.csv and print
with open('./data/parameter_estimation.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([target_distance, round(sigma_hit,5), round(bias,5)])

print(f"Target Distance: {target_distance}, Sigma_hit: {round(sigma_hit,5)} [m], Bias: {round(bias,5)} [m]")

# 2.2 histogram analysis
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


