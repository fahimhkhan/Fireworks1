# -*- coding: utf-8 -*-
"""
Created on Thu May 08 12:07:14 2020
CSE 30 Spring 2020 Program 3 starter code
@author: Fahim
"""
import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


class Particle:
    def __init__(self, x=0, y=0, z=0, color=(0, 0, 0, 1), lifetime=1000, depth=0, h=0):
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
            if length > 7:
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
                                            1), 1000, depth, h))
            else:
                self.plist.append(Particle(x, y, z, color, 1000, depth, h))

    def render(self):
        glEnable(GL_POINT_SMOOTH)
        glPointSize(5)
        glBegin(GL_POINTS)
        for i in range(len(self.plist)):
            length = len(self.plist[i].x)
            for j in range(length):
                if length == 1:
                    alpha = 1
                else:
                    alpha = j / length
                glColor4fv((self.plist[i].color[0], self.plist[i].color[1], self.plist[i].color[2], alpha))
                glVertex3fv((self.plist[i].x[j], self.plist[i].y[j], self.plist[i].z[j]))
            self.plist[i].update()
        glEnd()


def terrain():
    ''' Draws a simple square as the terrain '''
    glBegin(GL_QUADS)
    glColor4fv((0, 0, 1, 1))  # Colors are now: RGBA, A = alpha for opacity
    glVertex3fv((25, 0, 25))  # These are the xyz coords of 4 corners of flat terrain.
    glVertex3fv((-25, 0, 25))  # If you want to be fancy, you can replace this method
    glVertex3fv((-25, 0, -25))  # to draw the terrain from your prog1 instead.
    glVertex3fv((25, 0, -25))
    glEnd()


def main():
    pygame.init()

    # Set up the screen
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Firework Simulation")

    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0, -10, -50)
    # glRotatef(10, 2, 1, 0)

    play = True
    sim_time = 0

    # A clock object for keeping track of fps
    clock = pygame.time.Clock()

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(10, 0, 1, 0)

                if event.key == pygame.K_UP:
                    glRotatef(-10, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(10, 1, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        glRotatef(0.10, 0, 1, 0)
        # glTranslatef(0, 0.1, 0)

        glEnable(GL_DEPTH_TEST)
        '''Enable blending in OpenGL'''
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_BLEND);
        '''Create a black background'''
        glClearColor(0.0, 0.0, 0.2, 0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain()

        print(sim_time)
        if 0 < sim_time < 200:
            f2.render()
            f3.render()
            f4.render()
        if 200 < sim_time:
            f2.render()
            f4.render()
            for i in range(len(f3.plist)):
                if sim_time == 201:
                    for j in range(len(f3.plist[i].f.plist)):
                        f3.plist[i].f.plist[j].set_xyz(f3.plist[i].x[0], f3.plist[i].y[0], f3.plist[i].z[0])
                f3.plist[i].f.render()

        if sim_time > 1000:
            sim_time = 0

        if sim_time == 0:
            f2 = Firework(5, 0, 5, (0, 1, 0, 1), 50, 0, 20)
            f3 = Firework(0, 0, 0, (0, 0, 0, 1), 20, 1, 20)
            f4 = Firework(-5, 0, -5, (0, 1, 1, 1), 50, 0, 20)

        pygame.display.flip()
        sim_time += 1
        clock.tick(150)

    pygame.quit()


if __name__ == "__main__":
    main()
