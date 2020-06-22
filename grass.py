import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


class Particle:
    def __init__(self, x=0, y=0, z=0, length=0, color=(0, 1, 0, 1)):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.velocity = [random.uniform(-1, 1), random.uniform(5, 15), random.uniform(-1, 1), ]
        self.length = length

        # calculate path of a particle
        self.trajectory = [(self.x, self.y, self.z)]
        dt = 0.05
        for i in range(1, self.length):
            x = self.x + self.velocity[0] * dt * i
            y = self.y + self.velocity[1] * dt * i - 0.5 * 9.8 * (dt * i) ** 2
            z = self.z + self.velocity[2] * dt * i
            if y < 0:
                y = 0
            self.trajectory.append((x, y, z))

    def draw(self):
        # draw the trajectory of a particle
        glLineWidth(5.0)
        glBegin(GL_LINE_STRIP)
        glColor4fv(self.color)
        for i in range(len(self.trajectory)):
            glVertex3fv(self.trajectory[i])
        glEnd()


'''======================================================'''


class Grass(Particle):
    def __init__(self, x1, z1, x2, z2, n, color, length, stddev):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2
        self.n = n
        self.color = color
        self.length = length
        self.stddev = stddev
        self.blades = []

        for i in range(n):
            # random position
            x = random.uniform(x1, x2)
            y = 0
            z = random.uniform(z1, z2)
            # add some randomness to color
            dr = random.uniform(0.1, 0.3)
            dg = random.uniform(0.1, 0.3)
            db = random.uniform(0.1, 0.3)
            color = (self.color[0] + dr, self.color[1] + dg, self.color[2] + db, self.color[3])
            self.blades.append(Particle(x, y, z, length, color))

    def drawPath(self):
        # draw patch
        glBegin(GL_QUADS)
        glColor4fv((0.5, 0.2, 0, 1))
        glVertex3fv((self.x1, 0, self.z1))
        glVertex3fv((self.x1, 0, self.z2))
        glVertex3fv((self.x2, 0, self.z2))
        glVertex3fv((self.x2, 0, self.z1))
        glEnd()

        # draw blades
        for item in self.blades:
            item.draw()