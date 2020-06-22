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
from queue import Queue


class Particle:
    def __init__(self, x=0, y=0, z=0, color=(0, 0, 0, 1), lifespan=0):
        self.x = [x]
        self.y = [y]
        self.z = [z]
        self.color = color
        self.exploded = False
        self.time_counter = 0
        self.velocity = [random.uniform(-.01, .01), random.uniform(-.01, .01), random.uniform(-.01, .01)]

    def update(self):
        self.time_counter += 1
        if self.y[0] > 10:
            self.exploded = True
        if self.exploded:
            l = len(self.x) - 1
            dt = 0.05
            self.x.append(self.x[l] + self.velocity[0] * dt * self.time_counter)
            self.y.append(self.y[l] + (dt * self.time_counter * self.velocity[1] - 0.5 * 0.00098 * (dt * self.time_counter) ** 2))
            self.z.append(self.z[l] + self.velocity[2] * dt * self.time_counter)
            '''if l > 25:
                self.x.pop(0)
                self.y.pop(0)
                self.z.pop(0)'''
        else:
            self.y[0] += 0.1


class Firework(Particle):
    def __init__(self, x=0, y=0, z=0, color=(0, 0, 0, 1), n=50):
        self.plist = []
        for i in range(n):
            if color == (0, 0, 0, 1):
                self.plist.append(Particle(x, y, z, (random.random(), random.random(), random.random(), 1)))
            else:
                self.plist.append(Particle(x, y, z, color))

    def render(self):
        #glEnable(GL_POINT_SMOOTH)
        #glPointSize(3)
        glLineWidth(2)
        for i in range(len(self.plist)):
            glBegin(GL_LINE_STRIP)
            glColor4fv((self.plist[i].color[0], self.plist[i].color[1], self.plist[i].color[2], 1-(i/len(self.plist))))
            for j in range(len(self.plist[i].x)):
                if self.plist[i].y[j] >= 0:
                    glVertex3fv((self.plist[i].x[j], self.plist[i].y[j], self.plist[i].z[j]))
            self.plist[i].update()
            glEnd()


def terrain():
    ''' Draws a simple square as the terrain '''
    glBegin(GL_QUADS)
    glColor4fv((0, 0, 1, 1))  # Colors are now: RGBA, A = alpha for opacity
    glVertex3fv((10, 0, 10))  # These are the xyz coords of 4 corners of flat terrain.
    glVertex3fv((-10, 0, 10))  # If you want to be fancy, you can replace this method
    glVertex3fv((-10, 0, -10))  # to draw the terrain from your prog1 instead.
    glVertex3fv((10, 0, -10))
    glEnd()


def fireworks(plist):
    ''' Accepts a list of particles then draws and updates each particle '''
    #glEnable(GL_POINT_SMOOTH)
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in range(len(plist)):
        glColor4fv(plist[p].color[0], )
        glVertex3fv((plist[p].x, plist[p].y, plist[p].z))
        plist[p].update()
    glEnd()


def main():
    pygame.init()

    # Set up the screen
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Firework Simulation")

    gluPerspective(45, (display[0] / display[1]), 0.1, 75.0)
    glTranslatef(0, -5, -25)
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
        glClearColor(0.0, 0.0, 0.0, 0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain()

        if 0 < sim_time <= 10000:
            f1.render()
        #if 500 < sim_time <= 1500:
            #f2.render()
            #f3.render()
        #if sim_time > 1500:
            #sim_time = 0

        if sim_time == 0:
            f1 = Firework()
            f2 = Firework(-5, 0, -5, (1, 0, 0, 1), 100)
            f3 = Firework(5, 0, 5, (0, 1, 0, 1), 100)

        pygame.display.flip()
        sim_time += 1
        clock.tick(25)

    pygame.quit()


if __name__ == "__main__":
    main()
