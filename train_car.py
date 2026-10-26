from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from racing_env import RacingEnv

env = RacingEnv()
check_env(env)          # fix any error this prints before training
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=200000)
model.save("car_v1")