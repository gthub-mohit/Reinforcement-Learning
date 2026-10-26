import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
for lr in [0.0001 , 0.003 , 0.01]:
    env=gym.make("CartPole-v1")
    model=PPO("MlpPolicy", env , learning_rate=lr , verbose=0)
    model.learn(total_timesteps=30000)
    mean , std=evaluate_policy(model , env , n_eval_episodes=10)
    print(f"lr={lr} -> mean reward{mean:1f}")
    env.close()

# cd C:\Users\mohit\rl_racing
# .\rl_env\Scripts\Activate.ps1