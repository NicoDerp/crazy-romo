import pygame
import random
import math

pygame.init()

screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crazy Romo!")

player_img = pygame.image.load("../images/ship.png")
player_rect = player_img.get_rect()
player_rect.width /= 10
player_rect.height /= 10
player_img = pygame.transform.scale(player_img, (player_rect.width, player_rect.height))
player_rect.center = screen.get_rect().center

comet_img = pygame.image.load("../images/comet.png")
# [[rect, 0.2, -0.3], [rect, 0.7, 0.7], [rect, 0.0, 0.0]]
comets = []

# 1 second = 1000ms
time_to_spawn_comet = 1000

clock = pygame.time.Clock()

def calc_player_rotation(img, rect):
	pos = pygame.mouse.get_pos()
	angle = 270 - math.atan2(pos[1] - rect.center[1], pos[0] - rect.center[0]) * 180 / math.pi
	rotated = pygame.transform.rotate(img, angle)
	return rotated, rotated.get_rect(center=rect.center)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if pygame.time.get_ticks() >= time_to_spawn_comet:
		comet_rects.append([])
		time_to_spawn_comet -= 1

	screen.fill((10, 10, 10))

	screen.blit(*calc_player_rotation(player_img, player_rect))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
