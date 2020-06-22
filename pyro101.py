# -*- coding: utf-8 -*-
"""
Created on Thu May 08 12:07:14 2020
CSE 30 Spring 2020 Program 3 starter code
@author: Fahim
"""
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from Firework import *


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

        # glRotatef(0.10, 0, 1, 0)
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
        if 0 < sim_time:
            f3.render()
        if 200 < sim_time:
            f2.render()
            f4.render()

        if sim_time > 500:
            sim_time = 0

        if sim_time == 0:
            f2 = Firework(5, 0, 5, (0, 1, 0, 1), 50, 0, 20)
            f3 = Firework(0, 0, 0, (0, 0, 0, 1), 100, 0, 20)
            f4 = Firework(-5, 0, -5, (0, 1, 1, 1), 50, 0, 20)

        pygame.display.flip()
        sim_time += 1
        clock.tick(150)

    pygame.quit()


if __name__ == "__main__":
    main()
