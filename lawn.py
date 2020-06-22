import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from grass import Grass, Particle


def main():
    pygame.init()

    # Set up the screen
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Grass Simulation")
    glEnable(GL_DEPTH_TEST)

    gluPerspective(60, (display[0] / display[1]), 0.1, 60.0)
    glTranslatef(0, -5, -40)

    # define corners for placing the 4 patches, and subdivide into 4 patches
    x1, z1 = (-20, -20)
    x2, z2 = (20, 20)

    p1c1 = (x1, z2)
    p1c2 = (x1 + (x2 - x1) / 2 - 1, z1 + (z2 - z1) / 2 + 1)
    p2c1 = (x1, z1 + (z2 - z1) / 2 - 1)
    p2c2 = (x1 + (x2 - x1) / 2 - 1, z1)
    p3c1 = (x1 + (x2 - x1) / 2 + 1, z2)
    p3c2 = (x2, z1 + (z2 - z1) / 2 + 1)
    p4c1 = (x1 + (x2 - x1) / 2 + 1, z1 + (z2 - z1) / 2 - 1)
    p4c2 = (x2, z1)

    # Create 4 patches with different params
    # Model is static, unlike fireworks which is dynamic
    # The patches are:
    # nice lawn -- blades are more or less same height, mostly green
    #              freshly mowed; blades are straight -- 1 line segment each.
    # dried lawn -- similar to 1st, but mostly brown -- could use same points,
    #               just different color
    # weedy lawn -- fewer but longer blades, multiple line segments per blade.
    #               higher variability in blade length.
    # dried weedy lawn -- even fewer blades, brownish

    # patch 1, dense grass
    n = 250
    color = (0.2, 0.8, 0.1, 1)
    length = 10
    stddev = 0.1
    g1 = Grass(p1c1[0], p1c1[1], p1c2[0], p1c2[1], n, color, length, stddev)

    # patch 2, dried lawn
    n = 250
    color = (0.5, 0.4, 0.1, 1)
    length = 10
    stddev = 0.1
    g2 = Grass(p2c1[0], p2c1[1], p2c2[0], p2c2[1], n, color, length, stddev)

    # patch 3, weedy lawn
    n = 200
    color = (0.2, 0.8, 0, 1)
    length = 25
    stddev = 0.5
    g3 = Grass(p3c1[0], p3c1[1], p3c2[0], p3c2[1], n, color, length, stddev)

    # patch 4, dried weedy lawn
    n = 150
    color = (0.7, 0.6, 0, 1)
    length = 15
    stddev = 0.5
    g4 = Grass(p4c1[0], p4c1[1], p4c2[0], p4c2[1], n, color, length, stddev)

    # A clock object for keeping track of fps
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(0.50, 0, 1, 0)
        # glTranslatef(0, 0.1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw patches of grass
        g1.drawPath()
        g2.drawPath()
        g3.drawPath()
        g4.drawPath()

        pygame.display.flip()
        clock.tick(150)

    pygame.quit()


if __name__ == "__main__":
    main()