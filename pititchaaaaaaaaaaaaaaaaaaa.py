#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 17:10:11 2021

@author: userlfa
"""

import pygame
import sys
pygame.init()
from pygame.locals import *
import numpy as np

class Cam:
    def __init__(self):
        self.posx=0
        self.posy=0
        
    def update(self):
        difx = -self.posx + chat.position[0] - 400
        self.posx += difx / 10
        
        dify = -self.posy + chat.position[1] - 300
        self.posy += dify / 10
        if self.posy > +1000:
            self.posy = +1000
            
        if self.posx < 0:
            self.posx = +0

        

TAILLE_BLOC = 32
        
        
class Chat:
    def __init__(self, tileset, longueur_des_animations, ralentissement_des_animations,
                 tile_size,
                 aggrandissement, vitesse_de_deplacement, position):
        self.tileset = tileset
        self.longueur_des_animations = longueur_des_animations
        self.ralentissement_des_animations = ralentissement_des_animations
        self.aggrandissement = aggrandissement
        self.vitesse_de_deplacement = vitesse_de_deplacement
        
        self.tile_size = tile_size * aggrandissement
        
        self.position = position
        
        tileset_rect = tileset.get_rect()
        self.tileset = pygame.transform.scale(self.tileset,
                                              (tileset_rect.width * self.aggrandissement,
                                              tileset_rect.height * self.aggrandissement))
        
        self.width = 28
        self.height = 42 - TAILLE_BLOC
        
        self.direction = 1
        self.state = 'sleeping'
        
        self.animation_id = 6
        self.animation_advance = 0
        self.compteur = 0
        
        self.air_velocity = 0
        
        self.vx = 0
        self.vy = 0
        
        self.on_ground = False
        
        self.name = 'ERNESTO'
        
        self.current_checkpoint = 0
        
    def afficher(self, window):
        rect = Rect(self.animation_advance * self.tile_size,
                    self.animation_id * self.tile_size,
                    self.tile_size, self.tile_size)
        img = self.tileset.subsurface(rect)
        if self.direction == -1:
            img = pygame.transform.flip(img, True, False)
        
        position_affichage = self.position[0] - 32 - camera.posx, self.position[1] - 32 - 64 + 1 - camera.posy
        
        window.blit(img, position_affichage)
        
    def changer_detat(self, nouveau_etat):
        if self.state != nouveau_etat:
            
            self.compteur = 0
            self.animation_advance = 0
            
            if nouveau_etat == 'idle':
                self.animation_id = 0
            elif nouveau_etat == 'walking':
                self.animation_id = 4
            elif nouveau_etat == 'running':
                self.animation_id = 5
            elif nouveau_etat == 'sleeping':
                self.animation_id = 6
            elif nouveau_etat == 'jumping':
                if self.on_ground:
                    self.vy = -15
                self.animation_id = 8
                if self.state == 'walking':
                    self.air_velocity = self.vitesse_de_deplacement * self.direction
                elif self.state == 'running':
                    self.air_velocity = self.vitesse_de_deplacement * self.direction * 3
                elif self.state =='idle':
                        self.air_velocity = 0
                

            self.state = nouveau_etat

                
    def update(self):

        for (x_tab_activation, sertarien, sertariennonpluslul, identifiant) in checkpoints:
            if self.position[0] // TAILLE_BLOC == x_tab_activation:
                self.current_checkpoint = identifiant
        
        
        if self.state == 'walking':
            self.vx = self.vitesse_de_deplacement * self.direction
        elif self.state == 'running':
            self.vx = self.vitesse_de_deplacement * self.direction * 3
        elif self.state == 'jumping':
            self.vx = self.air_velocity
        elif self.state == 'idle':
            self.vx /= 1.5
        
        self.vy = 1 + self.vy
                    
        nouveau_x = self.position[0] + self.vx
        nouveau_y = self.position[1] + self.vy
        
        positions_tableau_depart = []  # [bas_gauche, haut_gauche, bas_droite, haut_droite]
        positions_tableau_arrivee = []
        
        for decalage_x in (0, self.width):
            for decalage_y in (0, -self.height):
                pos_tab = (round(self.position[0] + decalage_x) // TAILLE_BLOC, round(self.position[1] + decalage_y) // TAILLE_BLOC)
                pos_tab_arrivee = (round(nouveau_x + decalage_x) // TAILLE_BLOC, round(nouveau_y + decalage_y) // TAILLE_BLOC)
                
                positions_tableau_depart.append(pos_tab)
                positions_tableau_arrivee.append(pos_tab_arrivee)
                
        va_etre_sur_le_sol = False
        
        a_une_collision_en_diagonale = (
            level.tableau[positions_tableau_arrivee[0][0], positions_tableau_arrivee[0][1]] in {1, 2} or
            level.tableau[positions_tableau_arrivee[1][0], positions_tableau_arrivee[1][1]] in {1, 2} or
            level.tableau[positions_tableau_arrivee[2][0], positions_tableau_arrivee[2][1]] in {1, 2} or
            level.tableau[positions_tableau_arrivee[3][0], positions_tableau_arrivee[3][1]] in {1, 2})

        a_une_collision_horizontale = False
        
        
        if (level.tableau[positions_tableau_arrivee[0][0], positions_tableau_depart[0][1]] in {1, 2} or
            level.tableau[positions_tableau_arrivee[1][0], positions_tableau_depart[1][1]] in {1, 2} or
            level.tableau[positions_tableau_arrivee[2][0], positions_tableau_depart[2][1]] in {1, 2} or
            level.tableau[positions_tableau_arrivee[3][0], positions_tableau_depart[3][1]] in {1, 2}):
            
            
            a_une_collision_horizontale = True
            self.vx=0
        
        if ((a_une_collision_en_diagonale and not a_une_collision_horizontale) or 
                
            level.tableau[positions_tableau_depart[0][0], positions_tableau_arrivee[0][1]] in {1, 2} or
            level.tableau[positions_tableau_depart[1][0], positions_tableau_arrivee[1][1]] in {1, 2} or
            level.tableau[positions_tableau_depart[2][0], positions_tableau_arrivee[2][1]] in {1, 2} or
            level.tableau[positions_tableau_depart[3][0], positions_tableau_arrivee[3][1]] in {1, 2}):
                        
            if self.vy > 0:                
                va_etre_sur_le_sol = True
                
                self.vy = positions_tableau_arrivee[0][1] * TAILLE_BLOC - 1 - self.position[1] 
                
            else:
                self.vy = positions_tableau_arrivee[1][1] * TAILLE_BLOC + 33 + self.height - self.position[1]
            
            if abs(self.vy) > TAILLE_BLOC:
                self.vy = 0
                
            

        
        
        if not self.on_ground and va_etre_sur_le_sol:
            event_handler.land()
            
        self.on_ground = va_etre_sur_le_sol
        
        if not self.on_ground:
            self.changer_detat('jumping')
                
        self.position[0] += self.vx
        self.position[1] += self.vy
        
        self.compteur = (self.compteur + 1) % self.ralentissement_des_animations
        if self.compteur == 0:
            self.animation_advance = (self.animation_advance + 1)
            
            if self.state == 'jumping':
                if self.vy > 2:
                    self.animation_advance = 3
                elif self.vy < -2:
                    self.animation_advance = 1
                else:
                    self.animation_advance = 2
            
            if self.animation_advance >= self.longueur_des_animations[self.animation_id]:
                self.animation_advance %= self.longueur_des_animations[self.animation_id]
                


class EventHandler:
    def __init__(self, player):
        self.player = player
        
        self.actions = {
                K_RIGHT: (self.walk_right, self.stop_walking_right),
                K_LEFT: (self.walk_left, self.stop_walking_left),
                K_UP: (self.jump,),
                K_RCTRL: (self.stop_running, self.start_running_instead_of_walking),
                K_s: (self.sleep,),
                K_u: (self.wake_up,),
                1: (self.place_block,),
                3: (self.remove_block,),
                4: (self.ajouter_1_a_block_id,),
                5: (self.retirer_1_a_block_id,)
                }
        
        self.still_walking = False
        self.still_running = False
        
        self.start_running_instead_of_walking()
        
    def handle(self, event):
        if event.type == KEYDOWN:
            
            if event.key in self.actions:
                action_tuple = self.actions[event.key]
                action_tuple[0]()
            
        elif event.type == KEYUP:
            if event.key in self.actions:
                action_tuple = self.actions[event.key]
                if len(action_tuple) == 2:
                    action_tuple[1]()
                    
        elif event.type == MOUSEBUTTONDOWN:
            if event.button in self.actions:
                action_tuple = self.actions[event.button] 
                action_tuple[0](event.pos)
       
    
    def land(self):
        self.player.changer_detat('idle')
    
        if self.still_walking:
            if self.player.direction == -1:
                self.walk_left()
            else:
                self.walk_right()
    
    def walk_left(self):
        self.player.direction = -1
        self._walk()
        
    def walk_right(self):
        self.player.direction = 1
        self._walk()
    
    def _walk(self):
        self.still_walking = True
        
        if self.still_running:
            if self.player.state in ('idle', 'walking'):
                self.player.changer_detat('running')
        
        else:
            if self.player.state in ('idle',):
                self.player.changer_detat('walking')
                
        if self.player.state in ('jumping',):
            if self.still_running:
                self.player.air_velocity = 3 * self.player.vitesse_de_deplacement * self.player.direction
            elif self.still_walking:
                self.player.air_velocity = self.player.vitesse_de_deplacement * self.player.direction
    
    def stop_walking_left(self):
        if self.player.direction == -1:
            self._stop_walking()
    
    def stop_walking_right(self):
        if self.player.direction == 1:
            self._stop_walking()
    
    def _stop_walking(self):
        self.still_walking = False
        if self.player.state in ('walking', 'running'):
            self.player.changer_detat('idle')
    
    def start_running_instead_of_walking(self):
        self.still_running = True
        
        if self.player.state == 'walking':
            self.player.changer_detat('running')
        
    def stop_running(self):
        
        self.still_running = False
        
        if self.player.state == 'running':
            if self.still_walking:
                self.player.changer_detat('walking')
            else:
                self.player.changer_detat('idle')

    def jump(self):
        
        self.player.vy -= 10 * 1
        
        
        if self.player.on_ground:
            
            self.player.changer_detat('jumping')

    def sleep(self):
        if self.player.state == 'idle':
            self.player.changer_detat('sleeping')
            
        level.save()
        
    def wake_up(self):
        if self.player.state == 'sleeping':
            self.player.changer_detat('idle')
            
    def place_block(self, pos):
        mods = pygame.key.get_mods()
        
        shift = mods & KMOD_SHIFT
        
        print(level.selected_block)
        
        if shift:
            liste_dpos = [(0, 0), (0, 1), (1, 0), (1, 1)]
        else:
            liste_dpos = [(0, 0)]

        
        x, y = pos
        x += camera.posx
        y += camera.posy
        
        pos_x_grille_de_base = int(x) // TAILLE_BLOC
        pos_y_grille_de_base = int(y) // TAILLE_BLOC
        
        for (dx, dy) in liste_dpos:
            
            pos_x_grille = pos_x_grille_de_base + dx
            pos_y_grille = pos_y_grille_de_base + dy
            
            level.tableau[pos_x_grille, pos_y_grille] = 1
            level.tableau_image[pos_x_grille, pos_y_grille] = level.selected_block + dx + dy * 10
    
            level.refresh_image_portion(pos_x_grille, pos_y_grille, 2, 2)
            if level.tableau[pos_x_grille, pos_y_grille + 1] != 1:
                level.tableau[pos_x_grille, pos_y_grille + 1] = 2
    
    def ajouter_1_a_block_id(self, _):
        level.selected_block += 1
        level.selected_block = min(level.selected_block, 139)
    
    def retirer_1_a_block_id(self, _):
        level.selected_block -= 1
        if level.selected_block == 0:
            level.selected_block = 1
    
    def remove_block(self, pos):
        x, y = pos
        x += camera.posx
        y += camera.posy
        
        pos_x_grille = int(x) // TAILLE_BLOC
        pos_y_grille = int(y) // TAILLE_BLOC
        
        print(pos_x_grille, pos_y_grille)
        
        level.tableau[pos_x_grille, pos_y_grille] = 0
        level.tableau_image[pos_x_grille, pos_y_grille] = 0

        level.refresh_image_portion(pos_x_grille, pos_y_grille, 2, 2)
        if level.tableau[pos_x_grille, pos_y_grille + 1] != 1:
            level.tableau[pos_x_grille, pos_y_grille + 1] = 0

        


class Level:
    def __init__(self):
        
        self.taille = (300, 200)
        self.tableau = np.zeros(self.taille, dtype=np.int8)
        self.tableau_image = np.zeros(self.taille, dtype=np.int8)
        tab = np.load("level.npy")
        self.tableau[:tab.shape[0], :tab.shape[1]] = tab
        tab2 = np.load("level_image_data.npy")
        self.tableau_image[:tab2.shape[0], :tab2.shape[1]] = tab2


        
        
        self.selected_block = 1
        
        # chargement du tileset:
        self.tileset = pygame.image.load("inca_front.png").convert_alpha()
        
        self.tileset = pygame.transform.scale2x(self.tileset)
        
        self.find_checkpoint()
        
    def find_checkpoint(self):
        cpx = None
        
        for x in range(self.taille[0]):
            for y in range(self.taille[1]):
                if cpx is None:
                    if self.tableau_image[x, y] == 104:
                        cpx = x
                else:
                    if self.tableau_image[x, y] == 105:
                        identifiant = len(checkpoints)
                        position_activation = cpx
                        respawn_x = x * TAILLE_BLOC
                        respawn_y = (y + 20) * TAILLE_BLOC
                        checkpoints.append((position_activation, respawn_x, respawn_y, identifiant))
                        cpx = None
                
    
    def get_subsurface(self, block_id):
        if block_id == 0:
            img = pygame.Surface((TAILLE_BLOC, TAILLE_BLOC), SRCALPHA).convert_alpha()
            img.fill((152, 188, 250, 255))
            return img
        else:
            block_id -= 1
            
        rect = Rect((block_id % 10) * TAILLE_BLOC, (block_id // 10) * TAILLE_BLOC, TAILLE_BLOC, TAILLE_BLOC)
        return self.tileset.subsurface(rect)
        
    def initialiser_image(self):
        self.image = pygame.Surface((TAILLE_BLOC*self.taille[0],TAILLE_BLOC*self.taille[1])).convert_alpha()
        
        for x in range(0, self.taille[0]):
            for y in range(0, self.taille[1]):
                x2 = x * TAILLE_BLOC
                y2 = y * TAILLE_BLOC
                
                rect = Rect(x2, y2, TAILLE_BLOC, TAILLE_BLOC)
                
                block_id = self.tableau_image[x, y]
                self.image.blit(self.get_subsurface(block_id), rect)
                    
    def ajouter_blocs_en_dessous_de_position(self, position, type_de_bloc):
        position_tableau = position[0] // TAILLE_BLOC, position[1] // TAILLE_BLOC
        
        self.tableau[position_tableau[0], position_tableau[1]] = type_de_bloc
        self.tableau[position_tableau[0], position_tableau[1] + 1] = type_de_bloc
        
        rect = Rect(position_tableau[0] * TAILLE_BLOC, position_tableau[1] * TAILLE_BLOC, TAILLE_BLOC, TAILLE_BLOC)
        self.image.fill((0, 0, 0, 255 * self.tableau[position_tableau[0], position_tableau[1]]), rect)

    
    def ajouter_blocs_invisibles(self):
        for x in range(0, self.taille[0]):
            for y in range(self.taille[1] - 2, -1, -1):
                if self.tableau[x, y] == 1:
                    if self.tableau[x, y + 1] != 1:
                        self.tableau[x, y + 1] = 2
                
    def draw(self):
        window.blit(self.image, (0 - camera.posx, 0 - camera.posy))
        window.blit(self.get_subsurface(self.selected_block), (0, 0))
    
    def save(self):
        print("yeet")
        np.save("level_image_data", self.tableau_image)
        np.save("level", self.tableau)

        
    def refresh_image_portion(self, x_depart, y_depart, w, h):
        for x in range(x_depart, x_depart + w):
            for y in range(y_depart, y_depart + h):
                x2 = x *TAILLE_BLOC
                y2 = y*TAILLE_BLOC
                
                rect = Rect(x2, y2, TAILLE_BLOC, TAILLE_BLOC)
                block_id = self.tableau_image[x, y]
                self.image.blit(self.get_subsurface(block_id), rect)


checkpoints = [(-425244854544, 200, 1500, 0)]


window = pygame.display.set_mode((800, 600))

level = Level()

tileset = pygame.image.load('cat.png').convert_alpha()

lengths = [4, 4, 4, 4, 8, 8, 4, 6, 6, 8]

camera = Cam()

chat = Chat(tileset, lengths, 4, 32, 3, 1.8, [200.0, 300.0])
event_handler = EventHandler(chat)




def main():
    f = pygame.Surface((5000, 5000), SRCALPHA)
    opacity = 255
    run = True

    clock = pygame.time.Clock()    

    level.initialiser_image()
    level.ajouter_blocs_invisibles()

    chat.changer_detat('idle')
    p=chat.position[1]
    
    print(checkpoints)
    while run:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            
            event_handler.handle(event)
        
        camera.update()
        
        #window.fill((50, 200, 200))
        level.draw()
        
        chat.update()
        chat.afficher(window)
        if chat.position[1] // 32 > 80:
            chat.position[1]=checkpoints[chat.current_checkpoint][2]
            chat.position[0]=checkpoints[chat.current_checkpoint][1]
            chat.vy=0
            chat.vx=0
            
        if opacity > 1:
            f.fill((0, 0, 0, opacity))
            window.blit(f, (0, 0))
            opacity -= 3

        pygame.display.flip()
        
        clock.tick(40)
    
    pygame.display.quit()
    
    
if __name__ == '__main__':
    main() 