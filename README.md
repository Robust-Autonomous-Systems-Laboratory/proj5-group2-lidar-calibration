# Project 5 Lidar Calibration 
### Michigan Tech EE5531 Intro to Robotics ###
<u>Group 2</u>: Reid Beckes + Ian Mattson

## 1. Introduction + Methodology

### Brief description of the Beam Model and calibration approach


### Data Collection Procedure


ROS2 bags were recorded at 0.5m, 1m, 1.5m, and 2m from the wall for approximately 30 seconds.  These bags are located in the [/data/ directory](/data/).

![Turtlebot laser rangefinder center at target distance](./analysis/figures/top_view_turtlebot_measurement.jpeg)

### Challenges Encountered



![Meter stick aligned with wall](./analysis/figures/side_view_turtlebot_measurement.jpeg)


## 2. Histogram Analysis

### Histograms by Target Distance

![0.5m target histogram](./analysis/figures/lidar_calibration_0.5m.png)


![1m target histogram](./analysis/figures/lidar_calibration_1m.png)


![1.5m target histogram](./analysis/figures/lidar_calibration_1.5m.png)


![2m target histogram](./analysis/figures/lidar_calibration_2m.png)

### Description of observed distribution shapes


### Discussion of any deviations from Gaussian (outliers, skewness, etc.)


## 3. Parameter Estimation and Results

### Table of estimated parameters for each distance
| Target Range [m] | $\sigma_{hit}$ [m] | Bias [m] |
|---|---|---|
| 0.5 | 0.00476 | 0.00446 |
| 1.0 | 0.00663 | 0.00594 |
| 1.5 | 0.01065 | 0.00936 |
| 2.0 | 0.01619 | 0.01464 |

### Analysis of how σ_hit varies with distance


### Proposed uncertainty model with justification (e.g., σ_hit = σ_0 + σ_1·z)


### Discussion of outlier rates and beam model mixing weights



## 4. Analysis Questions

### Does the measurement distribution match the Gaussian assumption of p_hit?


### How does measurement uncertainty vary with distance?


### Were there systematic biases? How would you correct for them?



## 5. Usage Instructions

### Build instructions for your ROS2 package


### How to run the calibration node with parameters


### How to run the offline analysis script


### Example commands and expected output



