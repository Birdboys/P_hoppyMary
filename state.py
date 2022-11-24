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

		self.bg_img = pygame.image.load('assets/backgrounds/test_plx/background_v2.png').convert_alpha()
		self.fg_img = pygame.image.load('assets/backgrounds/test_plx/foreground_v2.png').convert_alpha()
		self.mg_img = pygame.image.load('assets/backgrounds/test_plx/midground_v2.png').convert_alpha()
		self.p_img = pygame.image.load('assets/backgrounds/test_plx/platform_v2.png').convert_alpha()
		self.spotlight = pygame.image.load('assets/fluff/spotlight.png').convert_alpha()
		self.spotlight_bottom = pygame.image.load('assets/fluff/spotlight_bottom.png').convert_alpha()
		self.spotlight_pos = [0,0]
		self.spotlight_width, self.spotlight_height = self.spotlight.get_width(), self.spotlight.get_height()
		self.spotlight_rect = pygame.Rect(0,0,self.spotlight_width,self.spotlight_height)
		self.bg_color_v2 = (205,104,61)
		self.bg_color_v1 = (169,178,162)
		self.parallax_speed = 3
		self.obstacles = []




	def update(self, events, delta, keys):

		for event in events:
			if event.type == pygame.QUIT:
				self.game.playing = False
				self.game.running = False

		self.obstacles = self.game.boss.update(events, delta, keys, self.game.player.pos)
		self.game.player.update(delta, keys)
		self.updateSpotlight(self.game.player.pos)

	def render(self, surface):
		p_val_x = (4 + self.game.player.quadrant_x) * self.parallax_speed
		p_val_y = self.game.player.quadrant_y * self.parallax_speed
		surface.fill(self.bg_color_v2)
		surface.blit(self.bg_img, (0,0), (0+p_val_x, 10 - p_val_y, self.game.WIDTH, self.game.HEIGHT))
		surface.blit(self.mg_img, (0,0), (p_val_x*2, 80 - p_val_y*2, self.game.WIDTH, self.game.HEIGHT))
		self.game.boss.render(surface, self.game.player.pos)
		surface.fill((251,185,84), special_flags = 4)
		surface.blit(self.p_img, (0,0))
		surface.blit(self.spotlight_bottom, (self.spotlight_rect.x, self.spotlight_rect.y + self.spotlight_height-4), special_flags = 0)
		self.game.player.render(surface)
		for obstacle in self.obstacles:
			obstacle.render(surface)
		surface.blit(self.spotlight, self.spotlight_rect, special_flags = 1)
		surface.blit(self.fg_img, (0,0), (p_val_x*3, 150 - p_val_y*3, self.game.WIDTH, self.game.HEIGHT))

	def updateSpotlight(self, player_pos):
		self.spotlight_pos[0] = player_pos[0]
		self.spotlight_rect.x = self.spotlight_pos[0]-self.spotlight_width/2

"""
surface.blit(self.bg_img, (0,0), (0+p_val_x, 10 - p_val_y, self.game.WIDTH, self.game.HEIGHT))
surface.blit(self.mg_img, (0,0), (p_val_x*2, 80 - p_val_y*2, self.game.WIDTH, self.game.HEIGHT))
surface.blit(self.fg_img, (0,0), (p_val_x*3, 160 - p_val_y*3, self.game.WIDTH, self.game.HEIGHT))
"""

""" NON -UPDOWN
surface.blit(self.bg_img, (0,0), (0+p_val_x, 20, self.game.WIDTH, self.game.HEIGHT))
surface.blit(self.mg_img, (0,0), (p_val_x*2, 80, self.game.WIDTH, self.game.HEIGHT))
surface.blit(self.fg_img, (0,0), (p_val_x*3, 160, self.game.WIDTH, self.game.HEIGHT))
"""