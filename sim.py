import random
import sys
import pygame

# SMART TRAFFIC LIGHT (adaptive control).
# a 4-way intersection where cars arrive randomly. a dumb fixed-timer light just
# switches every X seconds no matter what. this AI light watches how many cars
# are waiting in each direction and gives green to whichever side has the
# longest queue - so traffic clears faster. you can see both running side by side.

W, H = 900, 640
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("smart traffic light - adaptive vs fixed timer")
font = pygame.font.SysFont("consolas", 18)
big = pygame.font.SysFont("consolas", 22, bold=True)
clock = pygame.time.Clock()


class Intersection:
    # queues[0..3] = cars waiting from N, E, S, W
    def __init__(self, adaptive):
        self.queues = [0, 0, 0, 0]
        self.green = 0          # which direction has green (0/2 = NS, 1/3 = EW)
        self.timer = 0
        self.adaptive = adaptive
        self.total_passed = 0
        self.total_wait = 0

    def update(self):
        # cars arrive randomly each frame
        for i in range(4):
            if random.random() < 0.04:
                self.queues[i] += 1

        self.timer += 1

        if self.adaptive:
            # SMART: give green to the pair of directions with the most cars.
            ns = self.queues[0] + self.queues[2]
            ew = self.queues[1] + self.queues[3]
            # switch when the current green has cleared a bit, min 30 frames
            if self.timer > 30:
                self.green = 0 if ns >= ew else 1
                self.timer = 0
        else:
            # DUMB: just flip every 120 frames no matter what
            if self.timer > 120:
                self.green = 1 - self.green
                self.timer = 0

        # cars on the green directions get to go
        green_dirs = (0, 2) if self.green == 0 else (1, 3)
        for d in green_dirs:
            if self.queues[d] > 0 and random.random() < 0.5:
                self.queues[d] -= 1
                self.total_passed += 1

        self.total_wait += sum(self.queues)


smart = Intersection(adaptive=True)
dumb = Intersection(adaptive=False)


def draw(inter, ox, title):
    cx, cy = ox + 200, 300
    # roads
    pygame.draw.rect(screen, (50, 50, 55), (cx - 30, 80, 60, 440))
    pygame.draw.rect(screen, (50, 50, 55), (ox + 20, cy - 30, 360, 60))

    # the 4 queues as stacks of cars
    dirs = [(cx, cy - 40, 0, -1), (cx + 40, cy, 1, 0),
            (cx, cy + 40, 0, 1), (cx - 40, cy, -1, 0)]
    green_dirs = (0, 2) if inter.green == 0 else (1, 3)
    for i, (x, y, dx, dy) in enumerate(dirs):
        for c in range(min(inter.queues[i], 8)):
            pygame.draw.rect(screen, (90, 160, 230),
                             (x + dx * (40 + c * 22) - 8, y + dy * (40 + c * 22) - 8, 16, 16))
        # light color for this direction
        lit = (60, 220, 90) if i in green_dirs else (220, 60, 60)
        pygame.draw.circle(screen, lit, (int(x), int(y)), 7)

    screen.blit(big.render(title, True, (240, 240, 240)), (ox + 80, 30))
    screen.blit(font.render(f"cars through: {inter.total_passed}", True, (200, 230, 200)), (ox + 60, 540))
    screen.blit(font.render(f"waiting now:  {sum(inter.queues)}", True, (230, 220, 200)), (ox + 60, 564))


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    smart.update()
    dumb.update()

    screen.fill((22, 24, 30))
    draw(dumb, 20, "FIXED TIMER")
    draw(smart, 470, "AI ADAPTIVE")
    pygame.draw.line(screen, (60, 60, 70), (450, 20), (450, 620))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
