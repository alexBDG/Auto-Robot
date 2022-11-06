# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 19:00:00 2022

@author: alspe

cd "Documents\Python Scripts\Auto-Robot\autorobot\server"
conda activate Pi
python server_camera.py

cd "Documents\Python Scripts\Auto-Robot\autorobot\server"
conda activate Pi
python server_commands.py
"""

# System imports.
import os
import gym
import json
import torch
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Gym and Stable Baselines imports.
import gym
from gym import spaces
from stable_baselines3 import DQN

HEIGHT = 480
WIDTH = 640
N_CHANNELS = 3
N_FRAMES = 5
N_DISCRETE_ACTIONS = 4
MAX_STEPS = 1000
RESULTS_FOLDER = os.path.join(
    "results", datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
)



class AutoRobotEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8
        )
        if not os.path.exists(RESULTS_FOLDER):
            os.makedirs(RESULTS_FOLDER)

    def step(self, action):
        # Execute one time step within the environment
        self._take_action(action)

        self.current_step += 1
        delay_modifier = self.current_step / MAX_STEPS

        reward = delay_modifier
        done = self.current_step >= MAX_STEPS

        obs = self._next_observation()
        self.frame = obs

        if self.current_step%1 == 0:
            self.render()

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.current_step = 0
        return self._next_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        shape = self.frame.shape
        fig = plt.figure()
        fig.set_size_inches(1, 1. * shape[0] / shape[1], forward = False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(self.frame)
        fig.savefig(os.path.join(RESULTS_FOLDER, f"{self.current_step:09d}.png"), dpi=shape[0])
        plt.close()

    def _next_observation(self):
        r = requests.get("http://127.0.0.1:9000/frame")
        obs = np.array(json.loads(r.text)["frame"])
        return obs

    def _take_action(self, action):
        if action == 0:
            vector = [1, -1]
        elif action == 1:
            vector = [-1, -1]
        if action == 2:
            vector = [1, 1]
        elif action == 3:
            vector = [-1, 1]

        requests.post(
            "http://127.0.0.1:9500",
            json={
                "vector": vector,
                "speedVelocity": 1.,
                "speedRotation": 1.,
            }
        )


if __name__ == "__main__":
    print("[INFO] Device index used:", torch.cuda.current_device())
    print("[INFO] Device count:", torch.cuda.device_count())
    print("[INFO] Current Device:", torch.cuda.get_device_name(0))

    env = AutoRobotEnv()

    model = DQN("MlpPolicy", env, buffer_size=10 , verbose=1)
    model.learn(total_timesteps=MAX_STEPS)
    model.save(os.path.join(RESULTS_FOLDER, "model"))
