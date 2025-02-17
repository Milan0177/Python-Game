# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *
import sys
import random
import time
import sys
path = './game/'
sys.path.append(path)
path = './game/'
class DoodleJump:
    def __init__(self, FPS=30000):
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Airjump")  # Set the window title to "Airjump"
        self.green = pygame.image.load(path + "assets/green.png").convert_alpha()
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.blue = pygame.image.load(path + "assets/blue.png").convert_alpha()
        self.red = pygame.image.load(path + "assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load(path + "assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load(path + "assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load(path + "assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load(path + "assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load(path + "assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load(path + "assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load(path + "assets/spring_1.png").convert_alpha()
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.FPSCLOCK = clock = pygame.time.Clock()
        self.FPS = FPS
        self.timer = None
        self.generatePlatforms()
        
    def updatePlayer(self):
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 750:
            #self.playerx = -50
            self.playerx = 750
        elif self.playerx < 0:
            #self.playerx = 850
            self.playerx = 0

        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlayerByAction(self, actions):
        """
            actions = [ 'ACTION_RIGHT', 'ACTION_LEFT']
            actions: a list that contains two boolean value.
        """
        #assert actions[0] == actions[1] and actions[0] == True
        
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1

        if actions[0]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif actions[1]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        if len(actions) == 3:
            if actions[2]:
                if self.xmovement > 0:
                    self.xmovement -= 1
                elif self.xmovement < 0:
                    self.xmovement += 1

        if self.playerx > 750:
            #self.playerx = -50
            self.playerx = 750
        elif self.playerx < 0:
            #self.playerx = 850
            self.playerx = 0

        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
     for p in self.platforms:
        rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
        player = pygame.Rect(self.playerx, self.playery + 5, self.playerRight.get_width() - 10, self.playerRight.get_height())
        if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
            if p[2] != 2:
                self.jump = 15
                self.gravity = 0
            else:
                p[-1] = 1
            if p[2] == 1:  # Blue platform
               p[0] += p[3]  # Apply horizontal speed
            # Reverse direction if hitting screen edges
            if p[0] <= 0 or p[0] + self.blue.get_width() >= 800:
                p[3] *= -1

    def drawPlatforms(self):
        if_score_add = False
        for p in self.platforms:
            if p[1] - self.cameray > 800:
                platform = random.randint(0, 10)
                if platform < 8:
                    platform = 0  # green
                elif platform < 9:
                    platform = 1  # blue
                else:
                    platform = 2  # red

                self.platforms.append([random.randint(100, 650), self.platforms[-1][1] - 50, platform, 0])
                self.platforms.pop(0)
                self.score += 1
                if_score_add = True

            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))


        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50

        return if_score_add

    def generatePlatforms(self):
        y = 800  # Starting from the bottom of the screen
        buffer_height = 400  # Add 400px as the buffer above the screen
        while y > -100 - buffer_height:  # Extend the generation above the visible area
            x = random.randint(100, 650)
            platform = random.randint(0, 10)
            if platform < 8:
                platform = 0  # green
            elif platform < 9:
                platform = 1  # blue
                move_speed = random.choice([-2, 2])  # Random horizontal speed
            else:
                platform = 2  # red
            self.platforms.append([x, y, platform, 0])
            y -= 60

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 800))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))
            
            
    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()

        while True:
            self.screen.fill((0, 0, 0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            if self.playery - self.cameray > 700:
                self.cameray = 0
                self.score = 0
                self.s = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400

            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            pygame.display.update()
    
    def frame_step(self, input_actions , threads=1):
        last_cameray = self.cameray
        terminal = False
        reward = 0

        if self.playery - self.cameray > 700:
                # print ("End!!")
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
                
                terminal = True
                reward = -1
                print("terminated")

        self.screen.fill((0, 0, 0))
        
        if_score_add = self.drawPlatforms()
        self.updatePlayerByAction(input_actions)
        self.updatePlatforms()

        if if_score_add:
            reward = 2
            self.timer = time.time()
        else:
            if last_cameray == self.cameray:
                if self.timer == None:
                    self.timer = time.time()

                elif self.timer != None:
                    now_time = time.time()
                    #print("now:", now_time, "timer:", self.timer)
                    if (now_time - self.timer) > 10 * threads:
                        
                        self.cameray = 0
                        self.score = 0
                        self.springs = []
                        self.platforms = [[400, 500, 0, 0]]
                        self.generatePlatforms()
                        self.playerx = 400
                        self.playery = 400
                        
                        terminal = True
                        reward = -1
                        print("terminated")
                        self.timer = time.time()

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        
        pygame.display.update()

        self.FPSCLOCK.tick(self.FPS)
        return image_data, reward, terminal

    def getCurrentFrame(self):
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        return image_data

if __name__ == "__main__":
    DoodleJump().run()     

