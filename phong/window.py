import pygame
from pygame.locals import *
from scene import Scene

class Window:
    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        # self.screen = pygame.Surface((self.width, self.height))
        self.running = False
        self.scene = Scene()
    def mainloop(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), SCALED)
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(30)/1000
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.running = False
            self.scene.update(events, dt)
            self.screen.fill((0, 0, 0))
            self.scene.draw(self.screen)
            pygame.display.flip()
    def save(self, width, height):
        self.screen = pygame.Surface((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.scene.draw(self.screen)
        pygame.image.save(self.screen, "image.png")