from os import SEEK_END
import pygame
from pygame import display

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
        self.i = 640
        self.j = 1200
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
        self.count += 1

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1280, 720))
        self.player = Player(self.win)
        self.player.draw()
        self.obstacles = Obstacles(self.win)
        self.obstacles.obs_one()
        
    def collision(self, x1, y1, x2, y2):
        if y1 == 640 and (x1>=x2 and x1<=x2+64):
                return True
    def display_score(self):
        font = pygame.font.SysFont('Roboto',30)
        score = font.render(f"Score: {self.obstacles.count}", True, (0, 0, 0))
        self.win.blit(score, (800,30))

    def run(self):
        run = True
        while run:

            self.win.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.obstacles.obs_one()
            self.obstacles.obs_two()
            # Movement
            self.userInput = pygame.key.get_pressed()
            #Jump
            self.player.jump_player(self.userInput)
            self.display_score()
            if self.collision(self.player.x, self.player.y, self.obstacles.j, self.obstacles.i):
                print ("Game Over")
            pygame.display.update()
            pygame.time.delay(30)

if __name__ == '__main__':
    game = Game()
    game.run()