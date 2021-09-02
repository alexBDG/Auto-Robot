# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 22:35:22 2021

@author: Alexandre
"""

import os, time
import pygame



def text_surface(text, size, color, font):
    text_font = pygame.font.SysFont(font, size)
    return text_font.render(text, True, color)

def screen_text(text, size, color, frame, pos, font="Calibri"):
    surface = text_surface(text, size, color, font)
    rect = surface.get_rect()
    frame.blit(surface, (pos[0] - rect.w/2, pos[1] - rect.h/2))
    
    
class RealFPS:
    def __init__(self, precision):
        self.precision = precision
        self.fps = [0]*precision
        self.start = time.time()
        
    def update(self):
        stop = time.time()
        self.fps = [1./(stop - self.start)] + self.fps[:-1]
        self.start = stop
        
    def get_value(self):
        return int(sum(self.fps)/self.precision)
    
    
class FuturePath:
    def __init__(self, player, boundaries, precision=2):
        self.player = player
        self.boundaries = boundaries
        self.precision = precision
        self.path = [[0,0]]*precision
        
    def update(self):
        self.path = [[0,0]]*self.precision
        for i in range(self.precision):
            self.path[i] = [
                self.player.pos[0] - i*10*self.player.direction.x,
                self.player.pos[1] - i*10*self.player.direction.y
            ]
            
            # Valid or not the x-position
            if self.path[i][0] < self.boundaries[0][0]:
                self.path = self.path[:i]
                return
            elif self.path[i][0] > self.boundaries[0][1]:
                self.path = self.path[:i]
                return
            
            # Valid or not the y-position
            if self.path[i][1] < self.boundaries[1][0]:
                self.path = self.path[:i]
                return
            elif self.path[i][1] > self.boundaries[1][1]:
                self.path = self.path[:i]
                return
        
    def get_values(self):
        return self.path
        


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, pos, speed, rotation_speed, img):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.speed = speed
        self.angle_speed = rotation_speed
        self.scale = 1.5
        
        self.rotation = 0
        self.direction = pygame.math.Vector2(0, 1)

        self.image_origin = img

        self.image = img
        self.rect = self.image.get_rect()


    def update(self):
        self.image = pygame.transform.rotozoom(
            self.image_origin, self.rotation, self.scale
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def move(self, x_axis, y_axis):
        delta_rot = x_axis*self.angle_speed
        self.rotation -= delta_rot

        vec = pygame.math.Vector2(0, 1)
        vec.y = y_axis*self.speed
        vec.rotate_ip(-self.rotation)
        
        self.direction.rotate_ip(delta_rot)
        self.direction.normalize_ip()

        self.pos = (self.pos[0] + vec.x, self.pos[1] + vec.y)



class Game:
    def __init__(self, res, fps):
        self.res = res
        self.fps = fps
        self.real_fps = RealFPS(10)
        
        self.player_boundaries = [[20, self.res[0] - 20],
                                  [20, self.res[1] - 20]]
        
        # Define the colors we will use in RGB format
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.RED   = (255,   0,   0)
        self.GREEN = (  0, 255,   0)
        self.BLUE  = (  0,   0, 255)

        self.window_title = "Robot Path"
        self.is_running = True
        self.iterr_moved = False
        self.clock = pygame.time.Clock()
        
        self.player_ship_img = pygame.image.load(os.path.join(
            os.path.dirname(__file__), "res", "sprites", "carF1.png"
        ))
        self.player = SpaceShip(
            (self.res[0]/2, self.res[1]/2), 2, 1., self.player_ship_img
        )
        
        # Create the list of car's path
        self.path = []
        self.future = FuturePath(self.player, self.player_boundaries, 100)

        self.start()


    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(self.window_title)

        self.run()


    def run(self):
        while self.is_running:
            for evt in pygame.event.get():
                self.manage_events(evt)
            self.manage_pressed_keys()
            self.update()
        self.quit()


    def manage_events(self, evt):
        if evt.type == pygame.QUIT:
            self.is_running = False
            
        elif evt.type == pygame.KEYDOWN:
            # To quit
            if ((evt.mod & pygame.KMOD_CTRL) and (evt.key == pygame.K_c)):
                self.is_running = False


    def manage_pressed_keys(self):
        pressed = pygame.key.get_pressed()

        vector = [0, 0]
        if pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            vector[0] -= 1
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            vector[0] += 1
        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            vector[1] -= 1
        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            vector[1] += 1
        
        # Only if non nul velocity
        if vector[1]!=0:
            self.iterr_moved = True
            self.player.move(vector[0], vector[1])
            
            # Valid or not the x-position
            if self.player.pos[0] < self.player_boundaries[0][0]:
                self.player.pos = (
                    self.player_boundaries[0][0], self.player.pos[1]
                )
            elif self.player.pos[0] > self.player_boundaries[0][1]:
                self.player.pos = (
                    self.player_boundaries[0][1], self.player.pos[1]
                )
            
            # Valid or not the y-position
            if self.player.pos[1] < self.player_boundaries[1][0]:
                self.player.pos = (
                    self.player.pos[0], self.player_boundaries[1][0]
                )
            elif self.player.pos[1] > self.player_boundaries[1][1]:
                self.player.pos = (
                    self.player.pos[0], self.player_boundaries[1][1]
                )
                
        else:
            self.iterr_moved = False


    def draw(self):
        if len(self.path)>1:
            # Draw the path
            pygame.draw.lines(self.screen, self.RED, False, self.path, 2)
        
        # Draw the future path
        future_path = self.future.get_values()
        if len(future_path)>1:
            # If enought of future path
            pygame.draw.lines(
                self.screen, self.BLUE, False, future_path, 2
            )
        
        self.screen.blit(self.player.image, self.player.rect)
        screen_text(
            "{:<3d} FPS".format(self.real_fps.get_value()), 
            40, self.GREEN, self.screen, (40+30, 30)
        )
        

    def update(self):
        self.screen.fill(self.BLACK)
        
        self.player.update()
        if self.iterr_moved:
            self.path.append([self.player.pos[0], self.player.pos[1]])
            self.future.update()
        self.real_fps.update()
        self.draw()
        
        self.clock.tick(self.fps)
        pygame.display.update()
    
    
    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self
        


if __name__ == "__main__":
    RESOLUTION = (1280, 720)
    FPS = 50
    Game(RESOLUTION, FPS)
