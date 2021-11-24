#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 15:50:08 2021

@author: userlfa
"""
import pygame
import sys
pygame.init()
from pygame.locals import *
import numpy as np
from collections import deque
import random

import time

"""
tableau 50*50
"""

grid_size = (50, 50)

RIEN = 0
POMME = 1
TETE = 2
CORPS = 3
MUR = 4


grid = np.zeros(grid_size, dtype=np.int8)  # 0: rien; 1: pomme; 2: tête; 3: corps, 4: mur
pos = np.array([4, 30])

corps = deque()

vie = 1

def initialiser_niveau():
    for x in (0, grid_size[0] - 1):
        for y in range(grid_size[1]):
            grid[x, y] = MUR
            
    for x in range(grid_size[0]):
        for y in (0, grid_size[1] - 1):
            grid[x, y] = MUR
            
    grid[pos[0], pos[1]] = TETE

def recuperer_pomme(position_de_depart):
    creer_pomme()
    corps.appendleft(position_de_depart)
    
def mourir():
    global vie
    vie -= 1
    print("welp")

def deplacer(dx, dy):
    global pos
    position_arrivee = pos + (dx, dy)
    
    if (dx, dy) == (0, 0):
        return
    
    if len(corps) != 0:
        couleur = (100, 180, 0)
    else:
        couleur = (255, 255, 255)
    rect = Rect(pos[0] * TAILLE_CASE, pos[1] * TAILLE_CASE, TAILLE_CASE - 1, TAILLE_CASE - 1)
    fenetre.fill(couleur, rect)

    
    case_darrivee = grid[position_arrivee[0], position_arrivee[1]]

    if case_darrivee in {CORPS, MUR}:
        mourir()
    elif case_darrivee in {POMME, RIEN}:
        if case_darrivee == POMME:
            recuperer_pomme(pos.tolist())
        elif len(corps) != 0:
            dernier_element = corps.pop()
            corps.appendleft(pos.tolist())
            
            rect = Rect(dernier_element[0] * TAILLE_CASE, dernier_element[1] * TAILLE_CASE, TAILLE_CASE - 1, TAILLE_CASE - 1)
            fenetre.fill((255, 255, 255), rect)
            grid[dernier_element[0], dernier_element[1]] = RIEN
            
        if len(corps) != 0:
            grid[pos[0], pos[1]] = CORPS
        else:
            grid[pos[0], pos[1]] = RIEN
            
        pos += (dx, dy)
        grid[pos[0], pos[1]] = TETE

        rect = Rect(pos[0] * TAILLE_CASE, pos[1] * TAILLE_CASE, TAILLE_CASE - 1, TAILLE_CASE - 1)
        fenetre.fill((125, 200, 0), rect)

def creer_pomme():
    pos = 0, 0
    while grid[pos] != RIEN:
        pos = random.randint(1, 48), random.randint(1, 48)
        
    grid[pos] = POMME
    rect = Rect(pos[0] * TAILLE_CASE, pos[1] * TAILLE_CASE, TAILLE_CASE - 1, TAILLE_CASE - 1)
    fenetre.fill((255, 0, 0), rect)


initialiser_niveau()

# initialisation de pygame
fenetre = pygame.display.set_mode((1200, 800))

clock = pygame.time.Clock()

TAILLE_CASE = 16


def afficher_grille():
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            
            rect = Rect(x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE - 1, TAILLE_CASE - 1)
            
            case = grid[x, y]
            if case == MUR:
                couleur = (25, 15, 15)
            elif case == TETE:
                couleur = (125, 200, 0)
            elif case == CORPS:
                couleur = (100, 180, 0)
            elif case == RIEN:
                couleur = (255, 255, 255)
            elif case == POMME:
                couleur = (255, 0, 0)
            
            
            fenetre.fill(couleur, rect)


afficher_grille()

direction = [0, 0]

counter = 0
creer_pomme()

while  vie > 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            vie = -42
            
        elif event.type == KEYDOWN:
            if event.key == K_UP: 
                if direction != [0, 1]:
                    direction[:] = 0, -1
            elif event.key == K_DOWN: 
                if direction != [0, -1]:
                    direction[:] = 0, 1
            elif event.key == K_LEFT: 
                if direction != [1, 0]:
                    direction[:] = -1, 0
            elif event.key == K_RIGHT: 
                if direction != [-1, 0]:
                    direction[:] = 1, 0
    
    if counter % 5 == 0:
        deplacer(*direction)
    
    counter += 1
    
    pygame.display.flip()
    clock.tick(60)
    
    
pygame.display.quit()
pygame.quit()
    
    
    
    
    
    
    
    
    


