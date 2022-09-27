# Control and Trajectory Tracking for Autonomous Vehicle

# Proportional-Integral-Derivative (PID)

In this project, we implement a PID controller in order to perform vehicle trajectory tracking. Given a trajectory as an array of locations, and a simulation environment, this PID controller and its efficiency is tested on the CARLA simulator used in the industry.

### Installation

Run the following commands to install the starter code in the Udacity Workspace:

Clone the <a href="https://github.com/udacity/nd013-c6-control-starter/tree/master" target="_blank">repository</a>:

`git clone https://github.com/udacity/nd013-c6-control-starter.git`

## Run Carla Simulator

Open new window

* `su - student`
// Will say permission denied, ignore and continue
* `cd /opt/carla-simulator/`
* `SDL_VIDEODRIVER=offscreen ./CarlaUE4.sh -opengl`

## Compile and Run the Controller

Open new window

* `cd nd013-c6-control-starter/project`
* `./install-ubuntu.sh`
* `cd pid_controller/`
* `rm -rf rpclib`
* `git clone https://github.com/rpclib/rpclib.git`
* `cmake .`
* `make` (This last command compiles your c++ code, run it after every change in your code)

## Testing

To test your installation run the following commands.

* `cd nd013-c6-control-starter/project`
* `./run_main_pid.sh`
This will silently fail `ctrl + C` to stop
* `./run_main_pid.sh` (again)
Go to desktop mode to see CARLA

If error bind is already in use, or address already being used

* `ps -aux | grep carla`
* `kill id`


## Project Instructions

In the previous project a path planner is built for the autonomous vehicle. Now the steer and throttle controller are built here so that the car follows the trajectory.

In the directory [/pid_controller](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller)  you will find the files [pid.cpp](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/pid.cpp)  and [pid.h](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/pid.h). This is where pid controller is implemented.
The function pid is called in [main.cpp](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/main.cpp).

### Step 1: Build the PID controller object
Check [pid_controller.h](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/pid_controller.h) and [pid_controller.cpp](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/pid_controller.cpp).

Run the simulator and see in the desktop mode the car in the CARLA simulator. The car should not move in the simulation.
### Step 2: PID controller for throttle:
In [main.cpp](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/main.cpp), the error for the throttle pid is computed. The error is the speed difference between the actual speed and the desired speed.

### Step 3: PID controller for steer:
1) In [main.cpp](https://github.com/udacity/nd013-c6-control-starter/tree/mathilde/project_c6/project/pid_controller/main.cpp), the error for the steer pid is computed. The error is the angle difference between the actual steer and the desired steer to reach the planned position.

2) The angle betweeen the last two points on the trajectory is being used as the desried steer to compute the steer error.

3) A alternative method `find_closest_point` is implemented in `main.cpp`, and used to find a point on the planned trajectory, that is closest to the current vehicle position. The yaw of this point is the desired steer. This method is not used for the test, but can be studied later.

4) Tune the parameters of the pid until satisfying results are obtained (a perfect trajectory is not expected).

### Step 4: Evaluate the PID efficiency
The values of the error and the pid command are saved in thottle_data.txt and steer_data.txt.
Plot the saved values using the command (in nd013-c6-control-refresh/project):

```
python3 plot_pid.py
```

## Results
### Screenshots of how the vehicle avoids collision with other cars in the Carla simulator
![](/images/navigation1.png)

![](/images/navigation2.png)

![](/images/navigation3.png)


## Questions:
### 1. Add the plots to your report and explain them (describe what you see)
### PID Tests

We tested various combinations of Ki Kd Kp values for both steer and throttle before reaching a good balance, which leads our vehicle to avoid collisions
Below you'll find the plots for our best result, also due to time restrinction in our GPU computation time left.

The final choice was:
  
| KP_STEER | KI_STEER | KD_STEER | KP_THROTTLE | KI_THROTTLE | KD_THROTTLE |
|:--------:|:--------:|:--------:|:-----------:|:-----------:|:-----------:|
|   0.32   |   0.003  |  0.3     |     0.2     |     0.0009  |    0.1      |    



### Results
![](/images/result_data.png)

![](/images/steer.png)

![](/images/throttle.png)

 

### Observation
- First of all we noticed that we had to keep KP_THROTTLE low in order to limit the speed of the vehicle
- The tuning of the steering coefficients was difficult; small increase in KP_STEER would let to dramatic steering in the vehicle, 0.32 was the best choice. KI_STEER should also stay low not to lead to too fast convergence to the desired trajectory. KD_STEER could be tuned to limit the overshoot (i.e. big steering) of the vehicle.
- From the plots we can see that the steer error has some large peaks, which leads to dramatic steering.

### 2. What is the effect of the PID according to the plots, how each part of the PID affects the control command?

- Proportional term `P`: a value that is proportional to the current error. Large `P` value will result in a large change in the control output. 
- Integreal term `I`: a value that is proportional to the cumulative error over time. `I` term speeds up the process of movement to the setpoint and eliminates the residual steady state error produced by the system bias, which cannot be eliminated by a pure proportional controller.
- Derivative term `D`: a value that is proportional to the rate of change of error over time. `D` term predicts system behavior and thus improves the settling time and stability of the controller.

### 3. How would you design a way to automatically tune the PID parameters?

- In order to tune the PID parameters, the most used algorithm is the Twiddle algorithm, which is basically a cross-validation of all parameters in relation to the error produced by each tested combination of them.

### 4. PID controller is a model free controller, i.e. it does not use a model of the car. Could you explain the pros and cons of this type of controller?

Pros:
- Pid is easy to implement and feasible for many applications. It also needs to tune few parameters, via trial and error or cross-validation

Cons:
- With PID it's difficult to handle multiple constraints 

### 5. What would you do to improve the PID controller?
- I would use the twiddle algorithm to improve the performances 

