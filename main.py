import pygame
import tkinter as tk
import time

#SCREEN WIDTH AND HEIGHT
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

def smooth_value3(prev_num, current_num, scale):
    return (prev_num * 2  + current_num) / scale

#INIT
pygame.init()
display = pygame.display.set_mode(((int(0.9 * screen_width), int(0.9 * screen_height))), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
last_time = time.time()

#VAR
screen = pygame.Surface((int(0.9 * screen_width), int(0.9 * screen_height)))
screen_rect = screen.get_rect()
font = pygame.font.Font(r'Xirod.otf', 100)
scene = 'GAME' #INIT SCENE
dt = 0

class Obstacle1(pygame.sprite.Sprite):
    def __init__(self, color, size, x, y):
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.fill(color)
    def update(self):
        pass
obstacles_group = []
obstacle1 = Obstacle1((255, 255, 255), (1000, 50), 0, 1000)
obstacle2 = Obstacle1((255, 255, 255), (50, 100), 100, 900)
obstacles_group.append(obstacle1)
obstacles_group.append(obstacle2)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.pre_left_key = False
        self.pre_right_key = False
        self.pre_up_key = False
        self.left = False
        self.right = False
        self.up = False
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.5
    def update(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.left_key = True
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.right_key = True
        if self.keys[pygame.K_UP] or self.keys[pygame.K_w] or self.keys[pygame.K_SPACE]:
            self.up_key = True
        if not self.keys[pygame.K_LEFT] and not self.keys[pygame.K_a]:
            self.left_key = False
        if not self.keys[pygame.K_RIGHT] and not self.keys[pygame.K_d]:
            self.right_key = False
        if not self.keys[pygame.K_UP] and not self.keys[pygame.K_w] and not self.keys[pygame.K_SPACE]:
            self.up_key = False
        
        if self.left_key and not self.right_key:
            self.left = True
            self.right = False
        if self.right_key and not self.left_key:
            self.right = True
            self.left = False
        if self.left_key and self.right_key:
            self.right = False
            self.left = False
        if not self.left_key and not self.right_key:
            self.right = False
            self.left = False
        if self.up_key and not self.up:
            self.up = True
        if not self.up_key:
            self.up = False
        
        self.pre_left_key = self.left_key
        self.pre_right_key = self.right_key
        self.pre_up_key = self.up_key

        if self.left:
            self.x_speed = (-2 * dt)
        if self.right:
            self.x_speed = (2 * dt)
        if (not self.left and not self.right) or (self.left and self.right):
            self.x_speed = 0
        if self.up:
            print('up')
            self.y_speed = -10 * dt
        self.y_speed += (self.gravity * dt)
        
        run_x_positive = True
        run_x_negative = True
        run_y_positive = True
        run_y_negative = True

        if self.x_speed > 0:
            x_speed_int = int(self.x_speed)
            x_speed_float = self.x_speed - x_speed_int
            for i in range(x_speed_int):
                self.rect.x += 1
                for obstacle in obstacles_group:
                    if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(obstacle.image), (obstacle.rect.x - self.rect.x, obstacle.rect.y - self.rect.y)):
                        self.rect.x -= 1
                        run_x_positive = False
                        break
                if not run_x_positive:
                    break
            if run_x_positive:
                self.rect.x += x_speed_float
        if self.x_speed < 0:
            x_speed_int = int(self.x_speed)
            x_speed_float = self.x_speed - x_speed_int
            for i in range(abs(x_speed_int)):
                self.rect.x -= 1
                for obstacle in obstacles_group:
                    if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(obstacle.image), (obstacle.rect.x - self.rect.x, obstacle.rect.y - self.rect.y)):
                        self.rect.x += 1
                        run_x_negative = False
                        break
                if not run_x_negative:
                    break
            if run_x_negative:
                self.rect.x -= x_speed_float
        
        if self.y_speed > 0:
            y_speed_int = int(self.y_speed)
            y_speed_float = self.y_speed - y_speed_int
            for i in range(y_speed_int):
                self.rect.y += 1
                for obstacle in obstacles_group:
                    if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(obstacle.image), (obstacle.rect.y - self.rect.y, obstacle.rect.x - self.rect.x)):
                        self.rect.y -= 1
                        run_y_positive = False
                        print('collided')
                        break
                if not run_y_positive:
                    break
            if run_y_positive:
                self.rect.y += y_speed_float
        if self.y_speed < 0:
            y_speed_int = int(self.y_speed)
            y_speed_float = self.y_speed - y_speed_int
            for i in range(abs(y_speed_int)):
                self.rect.y -= 1
                for obstacle in obstacles_group:
                    if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(obstacle.image), (obstacle.rect.y - self.rect.y, obstacle.rect.x - self.rect.x)):
                        self.rect.y += 1
                        run_y_negative = False
                        break
                if not run_y_negative:
                    break
            if run_y_negative:
                self.rect.y -= y_speed_float
        
        




player = Player()
game_group = []
game_group.append(player)

#MAIN
running = True

while running:
    screen = pygame.Surface(display.get_size())
    screen_rect = screen.get_rect()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if scene == 'GAME':
        for element in game_group:
            element.update()
            screen.blit(element.image, element.rect)
        for element in obstacles_group:
            element.update()
            screen.blit(element.image, element.rect)
    display.blit(screen, (0, 0))
    pygame.display.flip()
    dt = clock.tick(10) / 10
pygame.quit()
quit()