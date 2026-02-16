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


## Miscellaneous
ROS2 bags were recorded at 0.5m, 1m, 1.5m, and 2m from the wall for approximately 30 seconds.  These bags are located in the [/data/ directory](/data/).
