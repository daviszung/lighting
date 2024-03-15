import math
import pygame


class Spark:
    def __init__(
        self,
        loc: list[float],
        angle: float,
        speed: float,
        color: pygame.Color,
        scale: float = 1,
    ):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.color = color
        self.scale = scale
        self.despawn_mark = False

    def move(self, dt: float):
        movement = [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]