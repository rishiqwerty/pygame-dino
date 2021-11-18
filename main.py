from os import SEEK_END
import pygame
from pygame.image import load
from pygame.locals import *
from pygame.constants import K_RETURN

class Player:
    def __init__(self, win):
        self.win = win
        self.image = pygame.image.load("res/tyrannosaurus.png").convert()
        self.x = 8
        self.y = 640
        self.jump_x = 10
        self.jump_y = 10
        self.jump = False
    def draw(self):
        self.win.blit(self.image, (self.x, self.y))
        self.sun = pygame.image.load("res/sun.png").convert()
        self.win.blit(self.sun, (90, 20))
        pygame.display.update()
    def jump_player(self, userInput):
        if self.jump is False and userInput[pygame.K_SPACE]:
            self.jump = True
        if self.jump is True:
            self.y -= self.jump_y*4
            self.jump_y -= 1
            if self.jump_y < -10:
                self.jump = False
                self.jump_y = 10
        self.draw()
        
class Obstacles:
    def __init__(self, win):
        self.win = win
        self.building = pygame.image.load("res/building.png").convert()
        self.cloud = pygame.image.load("res/cloud.png").convert()
        self.plane = pygame.image.load("res/aeroplane.png").convert()
        self.balloon = pygame.image.load("res/balloon.jpg").convert()
        self.i = 640
        self.j = 1200
        self.k = 720
        self.l = 440
        self.m = 220
        self.width = 1280
        self.count = 0
        
    def obs_one(self):
        self.win.blit(self.building, (self.i, 640))
        self.win.blit(self.building, (self.width+self.i, 640))
        if self.i == -self.width:
            self.win.blit(self.building, (self.width+self.i, 640))
            self.i = 0
            self.count += 100
        self.i -= 8
        self.count += 1
        

    def obs_two(self):
        self.win.blit(self.building, (self.j, 640))
        self.win.blit(self.building, (self.width+self.j, 640))
        if self.j == -self.width:
            self.win.blit(self.building, (self.width+self.j, 640))
            self.j = 0
            self.count += 100
        self.j -= 8
    def cloud_one(self):
        self.win.blit(self.cloud, (self.k, 160))
        self.win.blit(self.cloud, (self.width+self.k, 160))
        if self.k == -self.width:
            self.win.blit(self.cloud, (self.width+self.k, 160))
            self.k = 0
            self.count += 100
        self.k -= 8
    def plane_one(self):
        self.win.blit(self.plane, (self.l, 80))
        self.win.blit(self.plane, (self.width+self.l, 80))
        if self.l == -self.width:
            self.win.blit(self.plane, (self.width+self.l, 80))
            self.l = 0
        self.l -= 10
    def balloon_one(self):
        self.win.blit(self.balloon, (self.m, 220))
        self.win.blit(self.balloon, (self.width+self.m, 220))
        if self.m == -self.width:
            self.win.blit(self.balloon, (self.width+self.m, 220))
            self.m = 0
        self.m -= 4
        pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1280, 720))
        self.player = Player(self.win)
        self.player.draw()
        self.obstacles = Obstacles(self.win)
        self.obstacles.obs_one()
        self.obstacles.obs_two()
        self.obstacles.cloud_one()
        self.obstacles.plane_one()
        self.obstacles.balloon_one()


        
    def collision(self, x1, y1, x2, x3):
        print(x3)
        if y1 == 640 and (abs(x2)==40 or x2 == -1232 or x1 == x2):
            return True
        if y1 == 640 and (abs(x3) == 40 or x3 == -1232 or x1 == x3):
            return True
    def display_score(self):
        font = pygame.font.SysFont('Roboto',30)
        score = font.render(f"Score: {self.obstacles.count}", True, (0, 0, 0))
        self.win.blit(score, (800,30))
        pygame.display.update()
    def game_play(self):
        self.obstacles.obs_one()
        self.obstacles.obs_two()
        self.obstacles.cloud_one()
        self.obstacles.plane_one()
        self.obstacles.balloon_one()
        self.player.jump_player(self.userInput)
        self.display_score()
        if self.collision(self.player.x, self.player.y, self.obstacles.j, self.obstacles.i):
            raise "Game Over"
        pygame.display.update()
        pygame.time.delay(30)
    def show_game_over(self):
        self.win.fill((255,255,255))
        font = pygame.font.SysFont('Roboto',30)
        line1 = font.render(f"Game is over! Your score is {self.obstacles.count}", True, (0, 0, 0))
        self.win.blit(line1, (200,300))
        line2 = font.render("To play again press Enter, To exit press Escape", True, (0, 0, 0))
        self.win.blit(line2,(200, 350))
        pygame.display.update()
    def game_reset(self):
        self.player = Player(self.win)
        self.obstacles = Obstacles(self.win)
    def run(self):
        run = True
        pause = False
        while run:

            self.win.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
            # Movement
            self.userInput = pygame.key.get_pressed()
            #Jump
            if self.userInput[pygame.K_RETURN]:
                pause = False
            if self.userInput[pygame.K_ESCAPE]:
                run = False
            try:
                if not pause:
                    self.game_play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.game_reset()
            
            

if __name__ == '__main__':
    game = Game()
    game.run()