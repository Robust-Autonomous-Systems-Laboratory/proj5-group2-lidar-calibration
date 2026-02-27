# Project 5 Lidar Calibration 
### Michigan Tech EE5531 Intro to Robotics ###
<u>Group 2</u>: Reid Beckes + Ian Mattson



## 1. Introduction + Methodology

- Brief description of the Beam Model and calibration approach
- Data collection procedure (distances tested, setup, duration)
- Any challenges encountered and how they were addresses

## 2. Histogram Analysis

- Embedded histogram figures for each distance tested
- Description of observed distribution shapes
- Discussion of any deviations from Gaussian (outliers, skewness, etc.)

## 3. Parameter Estimation and Results

- Table of estimated parameters (σ_hit, bias) for each distance
- Analysis of how σ_hit varies with distance
- Proposed uncertainty model with justification (e.g., σ_hit = σ_0 + σ_1·z)
- Discussion of outlier rates and beam model mixing weights


## 4. Analysis Questions

- Does the measurement distribution match the Gaussian assumption of p_hit?
- How does measurement uncertainty vary with distance?
- Were there systematic biases? How would you correct for them?


## 5. Usage Instructions

- Build instructions for your ROS2 package
- How to run the calibration node with parameters
- How to run the offline analysis script
- Example commands and expected output
### Install and Build
1. Create a new ros workspace
```
mkdir -p proj5_ws/src
```
2. Navigate to the src directory
```
cd proj5_ws/src
```
3. Clone this repository into the src folder
```
git clone https://github.com/Robust-Autonomous-Systems-Laboratory/proj5-group2-lidar-calibration.git
```
4. Navigate back to the head of the workspace
```
cd ..
```
5. Build the package
```
colcon build --symlink-install
```
6. Source the setup file
```
source install/setup.bash
```
### Running
The node uses three ros params for configuration: `target_distance`, `target_angle`, and `angle_offset`. Theses params can be configured in the launch file located in `lidar_calibration/launch/calibration_launch.yaml`. To run the node with these parameters, run the following command:
```
ros2 launch lidar_calibration calibration_launch.yaml
```

## Miscellaneous
ROS2 bags were recorded at 0.5m, 1m, 1.5m, and 2m from the wall for approximately 30 seconds.  These bags are located in the [/data/ directory](/data/).
