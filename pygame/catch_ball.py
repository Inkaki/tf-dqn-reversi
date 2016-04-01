import numpy as np
import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class CatchBall:
    def __init__(self):
        pygame.init()
        self.unit_size = 32
        # variables
        self.screen = pygame.display.set_mode((8 * self.unit_size, 8 * self.unit_size))
        self.player_width = 3 * self.unit_size
        self.player_height = self.unit_size
        self.ball_width = self.unit_size
        self.ball_height = self.unit_size
        self.enable_actions = [0, K_LEFT, K_RIGHT]

        # states
        self.reset()

    def update(self, action):
        # update player position
        if action == K_LEFT:
            # move left
            self.player_x = max(0, self.player_x - self.unit_size)
        elif action == K_RIGHT:
            # move right
            self.player_x = min(self.player_x + self.unit_size, self.screen.get_width() - self.player_x)
        else:
            # do nothing
            pass

        # update ball position
        self.ball_y += self.unit_size

        # update other states
        self.reward = 0
        self.terminal = False
        if self.ball_y == self.screen.get_height() - self.unit_size:
            self.terminal = True
            if self.player_x <= self.ball_x < self.player_x + self.player_width:
                # catch
                self.reward = 1
            else:
                # drop
                self.reward = -1

    def draw(self):
        # initialize screen
        self.screen.fill((0, 0, 0))

        # draw player
        pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                Rect(self.player_x, self.player_y, self.player_width, self.player_height))

        # draw ball
        pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                Rect(self.ball_x, self.ball_y, self.ball_width, self.ball_height))

    def observe(self):
        self.draw()
        return self.screen, self.reward, self.terminal

    def execute_action(self, action):
        self.update(action)

    def reset(self):
        # reset player position
        self.player_x = np.random.randint(
                (self.screen.get_width() - self.player_width) / self.unit_size) * self.unit_size
        self.player_y = self.screen.get_height() - self.player_height

        # reset ball position
        self.ball_x = np.random.randint(self.screen.get_width() / self.unit_size) * self.unit_size
        self.ball_y = 0

        # reset other states
        self.reward = 0
        self.terminal = False