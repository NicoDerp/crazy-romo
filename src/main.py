import pygame
from random import randrange, choice
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
player_angle = 0

comet_img = pygame.image.load("../images/comet.png")
comet_img = pygame.transform.scale(comet_img, (100, 100))
comets = []

laser_img = pygame.image.load("../images/laser.png")
laser_img = pygame.transform.scale(laser_img, (60, 6))
lasers = []

time_to_spawn_comet = 1000
comet_speed = 3
laser_speed = 3

clock = pygame.time.Clock()

def is_rect_outside_screen(rect):
	return rect.x + rect.width < 0 or rect.x > screen_width or rect.y + rect.height < 0 or rect.y > screen_height

def _calc_player_rotation(img, rect):
	global player_angle
	pos = pygame.mouse.get_pos()
	angle = 270 - math.atan2(pos[1] - rect.center[1], pos[0] - rect.center[0]) * 180 / math.pi
	player_angle = angle
	rotated = pygame.transform.rotate(img, angle)
	return rotated, rotated.get_rect(center=rect.center)

def calc_player_rotation(img, rect):
	global player_angle
	pos = pygame.mouse.get_pos()
	a = rect.center[0] - pos[0]
	b = rect.center[1] - pos[1]
	hypotenuse = math.sqrt(a**2 + b**2)
	#print(hypotenuse)
	player_angle = 180 - math.degrees(math.asin(a / hypotenuse))
	if pos[1] < rect.center[1]: player_angle = 180 - player_angle
	#print(player_angle)
	rotated = pygame.transform.rotate(img, player_angle)
	return rotated, rotated.get_rect(center=rect.center)

def generate_new_comet():
	rect = comet_img.get_rect()
	p = choice(['top', 'bottom', 'left', 'right'])

	if p == 'top':
		rect.x = randrange(0, screen_width)
		rect.y = 0
		angle = randrange(20, 160)
	elif p == 'bottom':
		rect.x = randrange(0, screen_width)
		rect.y = screen_height - rect.height
		angle = randrange(200, 340)
	elif p == 'left':
		rect.x = 20
		rect.y = randrange(0, screen_height)
		angle = -randrange(110, 250)
	elif p == 'right':
		rect.x = screen_width - rect.width - 20
		rect.y = randrange(0, screen_height)
		angle = randrange(110, 250)

	radians = math.radians(angle)

	c = math.cos(radians)
	s = math.sin(radians)

	return [rect, c, s]

time = 0
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			radians = math.radians(270 - player_angle)
			c = math.cos(radians)
			s = math.sin(radians)
			rotated = pygame.transform.rotate(laser_img, player_angle+90)
			rect = rotated.get_rect(center=player_rect.center)
			lasers.append([rect, c, s, rotated])

	screen.fill((10, 10, 10))

	if time >= time_to_spawn_comet:
		comets.append(generate_new_comet())
		comet_speed += 0.1
		time = 0

	comets_outside_screen = []
	lasers_outside_screen = []

	for c in comets:
		c[0].x += c[1] * comet_speed
		c[0].y += c[2] * comet_speed

		if is_rect_outside_screen(c[0]):
			comets_outside_screen.append(comets.index(c))

		screen.blit(comet_img, c[0])

	for l in lasers:
		l[0].x += l[1] * laser_speed
		l[0].y += l[2] * laser_speed

		if is_rect_outside_screen(l[0]):
			lasers_outside_screen.append(l)

		screen.blit(l[3], l[0])

	for l in lasers_outside_screen:
		lasers.remove(l)

	for i in comets_outside_screen:
		comets[i] = generate_new_comet()

	screen.blit(*calc_player_rotation(player_img, player_rect))

	pygame.display.flip()
	time += clock.tick(60)

pygame.quit()
