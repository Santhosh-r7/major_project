# backend/rl_env.py
import gym
from gym import spaces
import numpy as np

class CropEnv(gym.Env):
    """Simple placeholder environment for crop management."""
    def __init__(self):
        super(CropEnv, self).__init__()
        # Example: 4-dimensional state (e.g., [soil_moisture, nutrient, plant_health, time])
        self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        # Example: 3 actions (e.g., 0=water,1=fertilize,2=harvest)
        self.action_space = spaces.Discrete(3)
        self.state = np.zeros(4)

    def reset(self):
        self.state = np.array([50, 50, 50, 0], dtype=np.float32)
        return self.state

    def step(self, action):
        # Randomly update state and assign a dummy reward
        self.state = np.random.rand(4) * 100
        reward = 0
        if action == 0:
            reward = 1
        elif action == 1:
            reward = 2
        else:
            reward = 0
        done = False
        info = {}
        return self.state, reward, done, info

# Example (commented out) of training with Stable Baselines3 PPO:
# from stable_baselines3 import PPO
# env = CropEnv()
# model = PPO("MlpPolicy", env, verbose=1)  # see SB3 example:contentReference[oaicite:7]{index=7}
# model.learn(total_timesteps=10000)
