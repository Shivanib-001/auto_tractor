# auto_tractor

## Tractor with ackermann steering and GUI control

### Dependencies
```
sudo apt install 
```

### Steps to launch the package
1. Clone this repo in ```catkin_ws/src``` directory
2. Now in catkin_ws directory use the following commands:
   ```
   catkin_make
   source devel/setup.bash
   ```
3. Make the python script (ackermann.py) executable using following command in ```catkin_ws/src/auto_tractor/auto_tractor/scripts``` directory:
   ```
   chmod +x ackermann.py
   ```
5. Now launch the package using:
```
roslaunch auto_tractor gazebo.launch
```


