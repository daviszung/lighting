import random


class Particle():
    def __init__(self, loc: list[float], radius: float, velocity: list[float] | None = None) -> None:
        self.loc = loc
        self.radius = radius
        self.velocity: list[float] =  velocity or [random.randint(-3, 3), random.randint(-5, -2)]
        self.despawn_mark = False
    
    def move(self, dt: float, wall_collisions: bool = True):
        collisions: list[str] = []
        if wall_collisions:
            self.loc[0] += self.velocity[0] * dt
            if self.loc[0] <= 0 and self.velocity[0] < 0:
                collisions.append("left")
                self.loc[0] -= self.velocity[0] * dt
                self.velocity[0] = self.velocity[0] * -1.1
            elif self.loc[0] >= 2048 and self.velocity[0] > 0:
                collisions.append("right")
                self.loc[0] -= self.velocity[0] * dt
                self.velocity[0] = self.velocity[0] * -1.1
            
            self.loc[1] += self.velocity[1] * dt
            if self.loc[1] <= 0 and self.velocity[1] < 0:
                collisions.append("up")
                self.loc[1] -= self.velocity[1] * dt
                self.velocity[1] = self.velocity[1] * -1.1
            elif self.loc[1] >= 1152 and self.velocity[1] > 0:
                collisions.append("down")
                self.loc[1] -= self.velocity[1] * dt
                self.velocity[1] = self.velocity[1] * -1.1

        else:
            self.loc[0] += self.velocity[0] * dt
            self.loc[1] += self.velocity[1] * dt

        return collisions



    def update(self, dt: float):
        # self.velocity[1] += 0.1 * dt
        # self.radius -= 0.1 * dt
        if self.radius <= 0:
            self.despawn_mark = True
        
    def bg_move(self, direction: float, dt: float):
        if direction > 0 or direction < 0:
            self.velocity[1] = direction
        self.loc[0] += 0.7 * dt
        self.loc[1] += self.velocity[1] * dt
        self.radius += random.randint(-1, 1) * 0.2 * dt
        self.radius = min(self.radius, 10)
        if self.loc[0] > 2100 or self.loc[0] < -1100 or self.radius <= 0:
            self.despawn_mark = True

