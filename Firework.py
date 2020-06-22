import random
from OpenGL.GL import *


class Particle:
    def __init__(self, x=0, y=0, z=0, color=(0, 0, 0, 1), lifetime=500, depth=0, h=0):
        self.x = [x]
        self.y = [y]
        self.z = [z]
        self.h = h
        self.color = color
        self.exploded = False
        self.lifetime = int(lifetime * random.uniform(.9, 1.1))
        self.time_counter = 0
        self.velocity = [random.uniform(-.01, .01), random.uniform(-.01, .01), random.uniform(-.01, .01)]
        self.depth = depth
        if self.depth == 1:
            self.f = Firework(0, 0, 0, color, 20, 0, 0)

    def update(self):
        self.time_counter += 1
        length = len(self.y) - 1
        if self.y[length] > self.h:
            self.exploded = True
        if self.exploded:
            dt = 0.05
            self.x.append(self.x[length] + self.velocity[0] * dt * self.time_counter)
            self.y.append(self.y[length] + (dt * self.time_counter * self.velocity[1]
                                            - 0.5 * 0.00098 * (dt * self.time_counter) ** 2))
            self.z.append(self.z[length] + self.velocity[2] * dt * self.time_counter)
            if length > 15:
                self.x.pop(0)
                self.y.pop(0)
                self.z.pop(0)
        else:
            self.y[0] += 0.2

    def set_xyz(self, x=0, y=0, z=0):
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)


class Firework(Particle):
    def __init__(self, x=0, y=0, z=0, color=(0, 0, 0, 1), n=50, depth=0, h=0):
        self.plist = []
        for i in range(n):
            if color == (0, 0, 0, 1):
                self.plist.append(Particle(x, y, z,
                                           (random.random(),
                                            random.random(),
                                            random.random(),
                                            1), 250, depth, h))
            else:
                self.plist.append(Particle(x, y, z, color, 250, depth, h))

    def render(self):
        glEnable(GL_POINT_SMOOTH)
        glPointSize(3)
        glBegin(GL_POINTS)
        for i in range(len(self.plist)):
            length = len(self.plist[i].x)
            for j in range(length):
                if length == 1:
                    alpha = 1
                else:
                    alpha = j / length
                if self.plist[i].y[j] >= 0 and self.plist[i].time_counter < self.plist[i].lifetime:
                    glColor4fv((self.plist[i].color[0], self.plist[i].color[1], self.plist[i].color[2], alpha))
                    glVertex3fv((self.plist[i].x[j], self.plist[i].y[j], self.plist[i].z[j]))
            self.plist[i].update()
        glEnd()
