import pygame
from pygame.image import load
from pygame.locals import *

# Player class contains movement of dianosaur
class Player:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load("res/tyrannosaurus.png").convert()
        self.x_axis = 8
        self.y_axis = 640
        self.jump_y = 10
        self.jump = False
    def draw(self):
        self.surface.blit(self.image, (self.x_axis, self.y_axis))
        self.sun = pygame.image.load("res/sun.png").convert()
        self.surface.blit(self.sun, (90, 20))
        pygame.display.update()
    def jump_player(self, userInput):
        if self.jump is False and userInput[pygame.K_SPACE]:
            self.jump = True
        if self.jump is True:
            self.y_axis -= self.jump_y*4
            self.jump_y -= 1
            if self.jump_y < -10:
                self.jump = False
                self.jump_y = 10
        self.draw()


# This class includes all the other elements of the game.
class Obstacles:
    def __init__(self, win):
        self.win = win
        self.building = pygame.image.load("res/building.png").convert()
        self.cloud = pygame.image.load("res/cloud.png").convert()
        self.plane = pygame.image.load("res/aeroplane.png").convert()
        self.balloon = pygame.image.load("res/balloon.jpg").convert()
        self.obs_one_position = 640
        self.obs_two_position = 1200
        self.cloud_position = 720
        self.plane_position = 440
        self.balloon_position = 220
        self.width = 1280
        self.count = 0

    def obs_one(self):
        self.win.blit(self.building, (self.obs_one_position, 640))
        self.win.blit(self.building, (self.width+self.obs_one_position, 640))
        if self.obs_one_position == -self.width:
            self.win.blit(self.building, (self.width+self.obs_one_position, 640))
            self.obs_one_position = 0
            self.count += 100
        self.count += 1
        if self.count > 1000:
            self.obs_one_position -= 16
        else:
            self.obs_one_position -= 8

    def obs_two(self):
        self.win.blit(self.building, (self.obs_two_position, 640))
        self.win.blit(self.building, (self.width+self.obs_two_position, 640))
        if self.obs_two_position == -self.width:
            self.win.blit(self.building, (self.width+self.obs_two_position, 640))
            self.obs_two_position = 0
            self.count += 100
        if self.count > 1000:
            self.obs_two_position -= 16
        else:
            self.obs_two_position -= 8

    def cloud_one(self):
        self.win.blit(self.cloud, (self.cloud_position, 160))
        self.win.blit(self.cloud, (self.width+self.cloud_position, 160))
        if self.cloud_position == -self.width:
            self.win.blit(self.cloud, (self.width+self.cloud_position, 160))
            self.cloud_position = 0
        self.cloud_position -= 2

    def plane_one(self):
        self.win.blit(self.plane, (self.plane_position, 80))
        self.win.blit(self.plane, (self.width+self.plane_position, 80))
        if self.plane_position == -self.width:
            self.win.blit(self.plane, (self.width+self.plane_position, 80))
            self.plane_position = 0
        self.plane_position -= 10
    def balloon_one(self):
        self.win.blit(self.balloon, (self.balloon_position, 220))
        self.win.blit(self.balloon, (self.width+self.balloon_position, 220))
        if self.balloon_position == -self.width:
            self.win.blit(self.balloon, (self.width+self.balloon_position, 220))
            self.balloon_position = 0
        self.balloon_position -= 4



# This is the major class which controls the game
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


    # For detecting collision of Tryanosaurus against obstacles
    def collision(self, player_x, player_y, obs2_x, obs1_x):
        if player_y == 640 and (abs(obs2_x) == 40 or obs2_x == -1232 or player_x == obs2_x):
            return True
        if player_y == 640 and (abs(obs1_x) == 40 or obs1_x == -1232 or player_x == obs1_x):
            return True

    # Dispkay score
    def display_score(self):
        font = pygame.font.SysFont('Roboto', 20)
        score = font.render(f"Score: {self.obstacles.count}", True, (0, 0, 0))
        self.win.blit(score, (1100, 30))
        pygame.display.update()

    # Controls the Gameplay
    def game_play(self):
        self.obstacles.obs_one()
        self.obstacles.obs_two()
        self.obstacles.cloud_one()
        self.obstacles.plane_one()
        self.obstacles.balloon_one()
        self.player.jump_player(self.userInput)
        self.display_score()
        if self.collision(self.player.x_axis, self.player.y_axis,
                          self.obstacles.obs_two_position, self.obstacles.obs_one_position):
            raise "Game Over"
        pygame.display.update()
        pygame.time.delay(30)

    # For Game Over message
    def show_game_over(self):
        self.win.fill((255, 255, 255))
        font = pygame.font.SysFont('Roboto', 25)
        line1 = font.render(f"GAME OVER!", True, (0, 0, 0))
        self.win.blit(line1, (540, 280))
        line2 = font.render(f"Your score is {self.obstacles.count}", True, (0, 0, 0))
        self.win.blit(line2, (530, 330))
        line3 = font.render("To play again press Enter, To exit press ESc", True, (0, 0, 0))
        self.win.blit(line3,(400, 380))
        pygame.display.update()

    # To restart the game
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

            self.userInput = pygame.key.get_pressed()
            # For restating the game
            if self.userInput[pygame.K_RETURN]:
                pause = False
            # For Quiting
            if self.userInput[pygame.K_ESCAPE]:
                run = False
            # Stopping game after Game over
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
