from stable_baselines3 import PPO
from racing_env import RacingEnv

env = RacingEnv(render_mode="human")
model = PPO.load("car_v1")
obs, _ = env.reset()
for _ in range(3000):
    action, _ = model.predict(obs, deterministic=True)
    obs, r, term, trunc, _ = env.step(action)
    env.render()
    if term or trunc:
        obs, _ = env.reset()