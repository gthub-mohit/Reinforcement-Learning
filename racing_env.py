import math
import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces
from day3_track import make_track, Car, cast_rays, is_wall, W, H, MAX_RAY

CX, CY = W / 2, H / 2

def ang(car):
    return math.atan2(car.y - CY, car.x - CX)

class RacingEnv(gym.Env):
    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.track = make_track()
        self.car = Car()
        self.action_space = spaces.Box(-1.0, 1.0, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(0.0, 1.0, shape=(6,), dtype=np.float32)
        self.screen = None
        self.clock = None
        self.steps = 0

    def _obs(self):
        d = [x / MAX_RAY for x in cast_rays(self.track, self.car)]
        return np.array(d + [self.car.speed / 8.0], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.car.reset()
        self.prev = ang(self.car)
        self.steps = 0
        return self._obs(), {}

    def step(self, action):
        self.car.move(float(action[0]), float(action[1]))
        self.steps += 1
        now = ang(self.car)
        delta = (now - self.prev + math.pi) % (2 * math.pi) - math.pi
        self.prev = now
        reward = delta * 50 - 0.05
        terminated = is_wall(self.track, int(self.car.x), int(self.car.y))
        if terminated:
            reward = -10.0
        truncated = self.steps >= 2000
        return self._obs(), reward, terminated, truncated, {}

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((W, H))
            self.clock = pygame.time.Clock()
        pygame.event.pump()
        self.screen.blit(self.track, (0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.car.x), int(self.car.y)), 8)
        pygame.display.flip()
        self.clock.tick(60)