# Tractor with Ackermann Steering and GUI Control

### Dependencies
Check or install the following dependencies:
```
sudo apt install ros-noetic-effort-controllers
sudo apt install ros-noetic-rqt-robot-steering
```

### Steps to launch the package
1. Clone this repo in ```catkin_ws/src``` directory

2. Make the python script (ackermann.py) executable using following command in ```catkin_ws/src/auto_tractor/auto_tractor/scripts``` directory:
   ```
   chmod +x ackermann.py
   ```
3. In catkin_ws directory use the following commands:
   ```
   catkin_make
   source devel/setup.bash
   ```
4. Now launch the package using:
```
roslaunch auto_tractor gazebo.launch
```


