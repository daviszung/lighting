import pygame, random, math
import time
from particle import Particle
from spark import Spark

pygame.init()
screen = pygame.display.set_mode((2048, 1152))
clock = pygame.Clock()
running = True

particles: list[Particle] = []
bg_particles: list[Particle] = []
sparks: list[Spark] = []
black = (0, 0, 0)
white = (255, 255, 255)
font = pygame.Font(None)

timer = 0

last_time = time.time()

# for i in range(25):
#     bg_particles.append(
#         Particle(
#             [random.randint(-1000, 2000), random.randint(0, 1150)],
#             random.randint(8, 10),
#         )
#     )


def circle_surface(radius: float, color: pygame.Color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey(black)
    return surf


def despawn_entities(arr: list[Particle] | list[Spark]):
    for i, e in enumerate(arr):
        if e.despawn_mark:
            del arr[i]


while running:

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    timer += 1 * dt
    if timer > 60:
        timer = 0

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    # mouse effect with particles
    # particles.append(Particle([mouse_pos[0], mouse_pos[1]], random.randint(3, 10)))
    # sparks.append(
    #     Spark(
    #         [mouse_pos[0], mouse_pos[1]],
    #         random.randint(0, 360),
    #         10,
    #         pygame.Color((80, 20, 120)),
    #     )
    # )

    if timer == 0:
        # bg_particles.append(
        #     Particle(
        #         [random.randint(-1000, 2000), random.randint(0, 1150)],
        #         random.randint(4, 8),
        #     )
        # )
        particles.append(Particle([random.randint(0, 2048), random.randint(0, 1152)], 15, [random.randint(-8, 8), random.randint(-8, 8)]))

    for i, p in enumerate(particles):
        collisions = p.move(dt)
        if len(collisions):
            p.radius -= len(collisions)
            for x in range(10):
                sparks.append(Spark([p.loc[0], p.loc[1]], random.randint(0, 180), random.randint(5, 10), pygame.Color("white")))

        p.update(dt)

    for bp in bg_particles:
        if timer == 0:
            bp.bg_move(random.randint(-4, 4) * 0.1, dt)
        else:
            bp.bg_move(0, dt)

    for s in sparks:
        s.move(dt)

    # RENDERING
    screen.fill("black")
    # pygame.draw.rect(screen, (20, 20, 255), pygame.Rect(500, 500, 500, 500))

    for p in particles:
        pygame.draw.circle(screen, (255, 255, 255), p.loc, p.radius)
        glow_radius = p.radius * 2
        screen.blit(
            circle_surface(glow_radius, pygame.Color(20, 20, 120)),
            (p.loc[0] - glow_radius, p.loc[1] - glow_radius),
            special_flags=pygame.BLEND_RGB_ADD,
        )

    for bp in bg_particles:
        pygame.draw.circle(screen, (255, 255, 255), bp.loc, bp.radius)
        glow_radius = bp.radius * 2
        screen.blit(
            circle_surface(glow_radius, pygame.Color(20, 20, 20)),
            (bp.loc[0] - glow_radius, bp.loc[1] - glow_radius),
            special_flags=pygame.BLEND_RGB_ADD,
        )

    for s in sparks:
        s.speed -= 0.1 * dt
        # s.angle += 0.1 * dt
        if s.speed <= 0:
            s.despawn_mark = True
        points = [
            (
                int(s.loc[0] + math.cos(s.angle) * s.speed * s.scale),
                int(s.loc[1] + math.sin(s.angle) * s.speed * s.scale),
            ),
            (
                int(
                    s.loc[0] + math.cos(s.angle + math.pi / 2) * s.speed * s.scale * 0.3
                ),
                int(
                    s.loc[1] + math.sin(s.angle + math.pi / 2) * s.speed * s.scale * 0.3
                ),
            ),
            (
                int(s.loc[0] - math.cos(s.angle) * s.speed * s.scale * 3.5),
                int(s.loc[1] - math.sin(s.angle) * s.speed * s.scale * 3.5),
            ),
            (
                int(
                    s.loc[0] + math.cos(s.angle - math.pi / 2) * s.speed * s.scale * 0.3
                ),
                int(
                    s.loc[1] + math.sin(s.angle - math.pi / 2) * s.speed * s.scale * 0.3
                ),
            ),
        ]
        pygame.draw.polygon(screen, s.color, points)

    fps_metric = font.render(f"{round(clock.get_fps())} FPS", False, "white")
    screen.blit(fps_metric, (20, 20))

    despawn_entities(particles)
    despawn_entities(bg_particles)
    despawn_entities(sparks)

    pygame.display.update()
    clock.tick()

pygame.quit()
