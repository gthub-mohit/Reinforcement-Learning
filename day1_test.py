import gymnasium as gym
from stable_baselines3 import PPO
env=gym.make("CartPole-v1")
model= PPO("MlpPolicy" , env , verbose=1)
model.learn(total_timesteps=100000)
model.save("model1")
env.close()
test_env=gym.make("CartPole-v1", render_mode="human")
loaded_model=PPO.load("model1")
obs , _=test_env.reset()
for _ in range (500):
    action , _state=loaded_model.predict(obs , deterministic=True)
    obs , reward , terminated , truncated  , info =test_env.step(action)
    if terminated or truncated:
        obs , _ = test_env.reset()

test_env.close()