import sys
import pygame
from pygame.locals import *


vec = pygame.math.Vector2

pygame.init()
FPS = 60
fps_clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)

MAX_SPEED = 9


t = [texture_001 = 1, texture_002 = 2]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (50, 120, 180), ((35, 0), (0, 35), (70, 35)))
        self.original_image = self.image
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)  # The acceleration vec points upwards.
        self.angle_speed = 0
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle_speed = -1
            player.rotate()
        if keys[K_RIGHT]:
            self.angle_speed = 1
            player.rotate()
        # If up or down is pressed, accelerate the ship by
        # adding the acceleration to the velocity vector.
        if keys[K_UP]:
            self.vel += self.acceleration
        if keys[K_DOWN]:
            self.vel -= self.acceleration

        # max speed
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):
        # Rotate the acceleration vector.
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def wrap_around_screen(self):
        """Wrap around screen."""
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y <= 0:
            self.position.y = HEIGHT
        if self.position.y > HEIGHT:
            self.position.y = 0


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    player.wrap_around_screen()
    all_sprites.update()

    DISPLAY.fill(BLACK)
    all_sprites.draw(DISPLAY)
    pygame.display.set_caption('angle {:.1f} accel {} accel angle {:.1f}'.format(
        player.angle, player.acceleration, player.acceleration.as_polar()[1]))
    pygame.display.update()
    fps_clock.tick(FPS)
