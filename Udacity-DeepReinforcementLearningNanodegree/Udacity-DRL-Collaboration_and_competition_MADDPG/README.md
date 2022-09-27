# Udacity-DRL-Collaboration_and_competition_MADDPG
Code for the final project of the Udacity Deep Reinforcement Learning Nanodegree, on Collaboration and Competition Multiagent algorithm


For this project, the work is done in the Tennis environment.

<p align="center"> <img src="images/play.gif" align="middle" alt="drawing" width="500px"> </p> 

In this environment, two agents control rackets to bounce a ball over a net. If an agent hits the ball over the net, it receives a reward of +0.1. If an agent lets a ball hit the ground or hits the ball out of bounds, it receives a reward of -0.01. Thus, the goal of each agent is to keep the ball in play.

## Environment details

The project uses a Unity ML agent environment 
The observation space consists of 8 variables corresponding to the position and velocity of the ball and racket. Each agent receives its own, local observation. Two continuous actions are available, corresponding to movement toward (or away from) the net, and jumping.

### Solving the Environment

The task is episodic, and in order to solve the environment, **the agents must get an average score of +0.5 (over 100 consecutive episodes, after taking the maximum over both agents)**. Specifically,

- After each episode, we add up the rewards that each agent received (without discounting), to get a score for each agent. This yields 2 (potentially different) scores. We then take the maximum of these 2 scores.
- This yields a single score for each episode.

The environment is considered solved, **when the average (over 100 episodes) of those scores is at least +0.5**.


## Getting started

### Installation requirements

- To begin with, you need to configure a Python 3.6 / PyTorch 0.4.0 environment with the requirements described in [Udacity repository](https://github.com/udacity/deep-reinforcement-learning#dependencies)
- Then you need to clone this project and have it accessible in your Python environment
- For this project, you will not need to install Unity. This is because we have already built the environment for you, and you can download it from one of the links below. You need to only select the environment that matches your operating system:

    - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P3/Tennis/Tennis_Linux.zip)
    - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P3/Tennis/Tennis.app.zip)
    - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P3/Tennis/Tennis_Windows_x86.zip)
    - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P3/Tennis/Tennis_Windows_x86_64.zip)
    
    (_For Windows users_) Check out [this link](https://support.microsoft.com/en-us/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64) if you need help with determining if your computer is running a 32-bit version or 64-bit version of the Windows operating system.

    (_For AWS_) If you'd like to train the agent on AWS (and have not [enabled a virtual screen](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md)), then please use [this link](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P3/Tennis/Tennis_Linux_NoVis.zip) to obtain the "headless" version of the environment.  You will **not** be able to watch the agent without enabling a virtual screen, but you will be able to train the agent.  (_To watch the agent, you should follow the instructions to [enable a virtual screen](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md), and then download the environment for the **Linux** operating system above._)

- Finally, unzip the environment archive in the 'project's environment' directory and eventually adjust the path to the UnityEnvironment in the code.

## Instructions

### Training an agent
    
You can either run `Tennis.ipynb` in the Udacity Online Workspace for "Project3: Collaboration and Competition" step by step or build your own local environment and set the path to the UnityEnvironment in the code.

**Note:** The Workspace does not allow you to see the simulator of the environment; so, if you want to watch the agent while it is training, you should train locally.    
