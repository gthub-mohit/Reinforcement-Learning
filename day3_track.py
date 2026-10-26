import pygame, math

W, H = 900, 600
RAY_ANGLES = [-90, -45, 0, 45, 90]   # relative to car direction
MAX_RAY = 200

def make_track():
    surf = pygame.Surface((W, H))
    surf.fill((0, 0, 0))
    pygame.draw.ellipse(surf, (255, 255, 255), (50, 50, W - 100, H - 100))
    pygame.draw.ellipse(surf, (0, 0, 0), (200, 150, W - 400, H - 300))
    return surf

def is_wall(track, x, y):
    if x < 0 or y < 0 or x >= W or y >= H:
        return True
    return track.get_at((x, y)).r < 128

class Car:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.y = W // 2, 100
        self.angle = 0.0   # degrees, 0 = facing right
        self.speed = 0.0

    def move(self, steer, throttle):
        self.angle += steer * 4
        self.speed = max(0.0, min(8.0, self.speed + throttle * 0.3))
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

def cast_rays(track, car):
    dists = []
    for rel in RAY_ANGLES:
        a = math.radians(car.angle + rel)
        d = 0
        while d < MAX_RAY:
            px = int(car.x + math.cos(a) * d)
            py = int(car.y + math.sin(a) * d)
            if is_wall(track, px, py):
                break
            d += 2
        dists.append(d)
    return dists

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    track, car = make_track(), Car()
    frame, running = 0, True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        k = pygame.key.get_pressed()
        steer = int(k[pygame.K_RIGHT]) - int(k[pygame.K_LEFT])
        throttle = int(k[pygame.K_UP]) - int(k[pygame.K_DOWN])
        car.move(steer, throttle)
        if is_wall(track, int(car.x), int(car.y)):
            print("CRASH")
            car.reset()
        dists = cast_rays(track, car)
        screen.blit(track, (0, 0))
        for rel, d in zip(RAY_ANGLES, dists):
            a = math.radians(car.angle + rel)
            end = (car.x + math.cos(a) * d, car.y + math.sin(a) * d)
            pygame.draw.line(screen, (0, 200, 0), (car.x, car.y), end, 1)
        pygame.draw.circle(screen, (255, 0, 0), (int(car.x), int(car.y)), 8)
        pygame.display.flip()
        frame += 1
        if frame % 30 == 0:
            print(dists, round(car.speed, 1))
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()