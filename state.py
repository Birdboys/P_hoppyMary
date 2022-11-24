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

class fightState(State):

	def __init__(self, game):
		self.game = game
		self.frame = 0
		self.initial_time = pygame.time.get_ticks()

		self.temp_font = pygame.font.SysFont("harrington",56)

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
		
		self.progress_bar_img = pygame.image.load('assets/ui/progress_bar.png').convert_alpha()
		self.progress_bar_pos = (38, 10)
		self.progress_mark_img = pygame.image.load('assets/ui/tracker.png').convert_alpha()
		self.progress_mark_pos = [120, 3]
		self.progress_blocker_rect = pygame.Rect(38+6, 10+8, self.progress_bar_img.get_width()-12, self.progress_bar_img.get_height()-16)

		self.obstacles = []

	def update(self, events, delta, keys):

		for event in events:
			if event.type == pygame.QUIT:
				self.game.playing = False
				self.game.running = False

		self.obstacles = self.game.boss.update(events, delta, keys, self.game.player.pos)
		self.game.player.update(delta, keys, self.obstacles)
		self.updateSpotlight(self.game.player.pos)
		if self.game.player.dead:
			new_state = endState(self.game, False)
			new_state.enter_state()

		if pygame.time.get_ticks() - self.initial_time > 21000:
			new_state = endState(self.game, True)
			new_state.enter_state()

	def render(self, surface):
		p_val_x = (4 + self.game.player.quadrant_x) * self.parallax_speed
		p_val_y = self.game.player.quadrant_y * self.parallax_speed
		surface.fill(self.bg_color_v2)
		surface.blit(self.bg_img, (0,0), (0+p_val_x, 10 - p_val_y, self.game.WIDTH, self.game.HEIGHT))
		surface.blit(self.mg_img, (0,0), (p_val_x*2, 80 - p_val_y*2, self.game.WIDTH, self.game.HEIGHT))
		self.game.boss.render(surface, self.game.player.pos)
		surface.fill((251,185,84), special_flags = 4)
		surface.blit(self.p_img, (0,0))
		for obstacle in self.obstacles:
			obstacle.renderShadow(surface)
		surface.blit(self.spotlight_bottom, (self.spotlight_rect.x, self.spotlight_rect.y + self.spotlight_height-4), special_flags = 1)
		self.game.player.render(surface)
		for obstacle in self.obstacles:
			obstacle.render(surface)

		surface.blit(self.spotlight, self.spotlight_rect, special_flags = 1)
		surface.blit(self.fg_img, (0,0), (p_val_x*3, 150 - p_val_y*3, self.game.WIDTH, self.game.HEIGHT))

		self.renderUI(surface)

	def updateSpotlight(self, player_pos):
		self.spotlight_pos[0] = player_pos[0]
		self.spotlight_rect.x = self.spotlight_pos[0]-self.spotlight_width/2

	def renderUI(self, surface):
		self.progress_mark_pos[0] = (44 + 260 * ((pygame.time.get_ticks()-self.initial_time)/20000) - self.progress_mark_img.get_width()//2)
		self.progress_blocker_rect.width = 260 * ((pygame.time.get_ticks()-self.initial_time)/20000)
		
		surface.blit(self.progress_bar_img, self.progress_bar_pos)
		pygame.draw.rect(surface, (255, 255, 255), self.progress_blocker_rect)
		surface.blit(self.progress_mark_img, self.progress_mark_pos)

		#temp_text = self.temp_font.render(str((pygame.time.get_ticks()-self.initial_time)//1000), True, (255,255,255))
		#surface.blit(temp_text, (5,5)) #temp

class endState(State):
	def __init__(self, game, win):
		self.game = game
		self.win = win

	def update(self, events, delta, keys):
		pass

	def render(self, surface):
		if self.win:
			pygame.draw.rect(surface, (255, 200, 255), pygame.Rect(0,0,self.game.WIDTH, self.game.HEIGHT) )
		else:
			pygame.draw.rect(surface, (0, 200, 255), pygame.Rect(0,0,self.game.WIDTH, self.game.HEIGHT) )

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