import pygame
import os
import random
import numpy as np

pygame.init()
class State():

	def __init__(self, game):
		#pygame.mixer.init()
		self.game = game

	def update(self, events, delta, keys):
		pass

	def render(self, surface):
		pass

	def enter_state(self):
		self.game.state_stack.append(self)

	def exit_state(self):
		self.game.state_stack.pop()

class testState(State):

	def __init__(self, game):
		self.game = game
		self.frame = 0

		self.bg_img = pygame.image.load('assets/backgrounds/test_plx/background.png').convert_alpha()
		self.fg_img = pygame.image.load('assets/backgrounds/test_plx/foreground.png').convert_alpha()
		self.mg_img = pygame.image.load('assets/backgrounds/test_plx/midground.png').convert_alpha()
		self.p_img = pygame.image.load('assets/backgrounds/test_plx/platform.png').convert_alpha()

		self.temp_boss = pygame.image.load('assets/temp_boss.png').convert_alpha()
		self.parallax_speed = 3


	def update(self, events, delta, keys):

		for event in events:
			if event.type == pygame.QUIT:
				self.game.playing = False
				self.game.running = False

		self.game.player.update(delta, keys)

	def render(self, surface):
		p_val_x = (4 + self.game.player.quadrant_x) * self.parallax_speed
		#p_val_y = self.game.player.quadrant_y * self.parallax_speed
		surface.fill((213,60,106))
		surface.blit(self.bg_img, (0,0), (0+p_val_x, 20, self.game.WIDTH, self.game.HEIGHT))
		surface.blit(self.mg_img, (0,0), (p_val_x*2, 80, self.game.WIDTH, self.game.HEIGHT))

		surface.blit(self.fg_img, (0,0), (p_val_x*3, 160, self.game.WIDTH, self.game.HEIGHT))
		surface.blit(self.temp_boss, (self.game.player.quadrant_x * 4, 0))
		surface.blit(self.p_img, (0,0))

		self.game.player.render(surface)






"""
surface.blit(self.bg_img, (0,0), (0+p_val_x, 10 - p_val_y, self.game.WIDTH, self.game.HEIGHT))
surface.blit(self.mg_img, (0,0), (p_val_x*2, 80 - p_val_y*2, self.game.WIDTH, self.game.HEIGHT))
surface.blit(self.fg_img, (0,0), (p_val_x*3, 160 - p_val_y*3, self.game.WIDTH, self.game.HEIGHT))
"""