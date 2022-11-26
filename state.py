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
		self.fight_started = False

		self.temp_font = pygame.font.SysFont("harrington",56)

		self.bg_img = pygame.image.load('assets/backgrounds/test_plx/background_v2.png').convert_alpha()
		self.fg_img = [pygame.image.load('assets/backgrounds/test_plx/foreground_base.png').convert_alpha(), 
						pygame.image.load('assets/backgrounds/test_plx/foreground_only_left.png').convert_alpha(),
						pygame.image.load('assets/backgrounds/test_plx/foreground_only_right.png').convert_alpha(),
						pygame.image.load('assets/backgrounds/test_plx/foreground_both.png').convert_alpha()]
		self.mg_img = pygame.image.load('assets/backgrounds/test_plx/midground_v2.png').convert_alpha()
		self.p_img = pygame.image.load('assets/backgrounds/test_plx/platform_v2.png').convert_alpha()
		self.spotlight = pygame.image.load('assets/fluff/spotlight.png').convert_alpha()
		self.spotlight_pos = [0,-2]
		self.spotlight_width, self.spotlight_height = self.spotlight.get_width(), self.spotlight.get_height()
		self.spotlight_rect = pygame.Rect(0,-2,self.spotlight_width,self.spotlight_height)
		self.spotlight_scaled = pygame.transform.scale(self.spotlight, (10, self.spotlight_rect.height)).convert_alpha()
		self.bg_color_v2 = (205,104,61)
		self.bg_color_v1 = (169,178,162)
		self.parallax_speed = 3
		
		self.progress_bar_img = pygame.image.load('assets/ui/progress_bar.png').convert_alpha()
		self.progress_bar_pos = (38, 10)
		self.progress_mark_img = pygame.image.load('assets/ui/tracker.png').convert_alpha()
		self.progress_mark_pos = [120, 3]
		self.progress_blocker_rect = pygame.Rect(38+6, 10+8, self.progress_bar_img.get_width()-12, self.progress_bar_img.get_height()-16)
		self.rumble_prev = False

		self.obstacles = []
		self.particles = []
		self.laser_left_check = False
		self.laser_right_check = False
		self.game.player.pos[0] = -20

	def update(self, events, delta, keys):
		for event in events:
			if event.type == pygame.QUIT:
				self.game.playing = False
				self.game.running = False


		self.obstacles, new_particles = self.game.boss.update(events, delta, keys, self.game.player.pos)
		for p in new_particles:
			self.particles.append(p)
		for p1 in self.particles:
			p1.update()
			if p1.rect.width == 0 or p1.rect.height == 2:
				self.particles.remove(p1)

		self.game.player.update(delta, keys, self.obstacles)
		self.updateSpotlight(self.game.player.pos)
		if self.game.player.dead:
			new_state = endState(self.game, False, int((pygame.time.get_ticks()-self.initial_time)/20000 * 100))
			new_state.enter_state()

		if pygame.time.get_ticks() - self.initial_time > 21000:
			for part in self.game.boss.body_parts:
				self.game.boss.body_parts[part].reset()
			new_state = endState(self.game, True, int((pygame.time.get_ticks()-self.initial_time)/20000 * 100))
			new_state.enter_state()

		if pygame.time.get_ticks() - self.initial_time > 5000:
			self.game.boss.num_attacks = 2

		if self.game.boss.head.has_right_lasered == True:
			if self.laser_right_check == False:
				pass
				#Particle()
			self.laser_right_check = True
		if self.game.boss.head.has_left_lasered == True:
			if self.laser_left_check == False:
				pass
				#self.particles.append(Particle('circle', self.attack1rect.x + random.randint(0,self.attack1rect.width),  self.attack1rect.y + self.attack1rect.height, 10 + random.randint(-2,2), 10 + random.randint(-2,2), -self.attack1rect_speed/2 + random.randint(-3, -1), random.randint(-7,-3), 0, 0.3, (28,20,29), 0.03)
			self.laser_left_check = True

	def render(self, surface):
		p_val_x = (4 + self.game.player.quadrant_x) * self.parallax_speed
		p_val_y = self.game.player.quadrant_y * self.parallax_speed
		surface.fill(self.bg_color_v2)
		surface.blit(self.bg_img, (0,0), (0+p_val_x, 10 - p_val_y, self.game.WIDTH, self.game.HEIGHT))
		surface.blit(self.mg_img, (0,0), (p_val_x*2, 80 - p_val_y*2, self.game.WIDTH, self.game.HEIGHT))
		self.game.boss.render(surface, self.game.player.pos)
		surface.fill((251,185,84), special_flags = 4)
		rumby = self.getRumble(self.game.boss.groundedMoves)
		surface.blit(self.p_img, rumby)
		
		self.game.player.render(surface)
		
		for obstacle in self.obstacles:
			obstacle.renderShadow(surface, rumby)
			obstacle.render(surface)

		for particle in self.particles:
			particle.render(surface)

		surface.blit(self.spotlight_scaled, self.spotlight_rect, special_flags = 1)
		#surface.blit(self.spotlight_bottom, (self.spotlight_rect.x, self.spotlight_rect.y + self.spotlight_height-4), special_flags = 1)
		surface.blit(self.fg_img[self.game.boss.head.has_left_lasered + self.game.boss.head.has_right_lasered * 2], (0,0), (p_val_x*3, 150 - p_val_y*3, self.game.WIDTH, self.game.HEIGHT))

		self.renderUI(surface)

	def updateSpotlight(self, player_pos):
		self.spotlight_rect.width = 20 + (pygame.time.get_ticks() - self.initial_time)/20000 * self.game.WIDTH
		self.spotlight_scaled = pygame.transform.scale(self.spotlight, (int(self.spotlight_rect.width), self.spotlight_rect.height)).convert_alpha()
		self.spotlight_pos[0] = player_pos[0]
		self.spotlight_rect.y = -2
		self.spotlight_rect.x = self.spotlight_pos[0]-self.spotlight_rect.width/2

	def renderUI(self, surface):
		self.progress_mark_pos[0] = (44 + 260 * ((pygame.time.get_ticks()-self.initial_time)/20000) - self.progress_mark_img.get_width()//2)
		self.progress_blocker_rect.width = 260 * ((pygame.time.get_ticks()-self.initial_time)/20000)
		
		surface.blit(self.progress_bar_img, self.progress_bar_pos)
		pygame.draw.rect(surface, (255, 255, 255), self.progress_blocker_rect)
		surface.blit(self.progress_mark_img, self.progress_mark_pos)

		#temp_text = self.temp_font.render(str((pygame.time.get_ticks()-self.initial_time)//1000), True, (255,255,255))
		#surface.blit(temp_text, (5,5)) #temp

	def getRumble(self, r_moves):
		rumble = False
		if len(self.game.boss.attack_stack) > 0:
			for attack in self.game.boss.attack_stack:
				if attack in r_moves and self.game.boss.body_parts[attack[0]].state == 3:
					rumble = True

		if rumble and not self.rumble_prev:
			self.rumble_prev = True
			return (random.randint(-1,1) - 2, random.randint(-2,2) - 2)
		else:
			self.rumble_prev = False
			return (-2,-2)

class homeState(State):
	def __init__(self, game):
		self.game = game
		self.surf = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
		self.credits_button_sheet = pygame.image.load('assets/ui/credits_text_sheet.png').convert_alpha()
		self.options_button_sheet = pygame.image.load('assets/ui/options_text_sheet.png').convert_alpha()
		self.tutorial_button_sheet = pygame.image.load('assets/ui/tutorial_text_sheet.png').convert_alpha()
		self.pray_button_sheet = pygame.image.load('assets/ui/pray_text_sheet.png').convert_alpha()
		self.background = pygame.image.load('assets/ui/home_menu_sheet.png').convert_alpha()
		self.torch_glow = pygame.image.load('assets/ui/home_menu_torch_glow.png')
		self.torch_glow_pos = [(360-self.torch_glow.get_width())/2, 400]
		self.buttons = [[0,self.pray_button_sheet, ((360-self.pray_button_sheet.get_width()/3)/2, 74)], [0, self.credits_button_sheet, ((360-self.credits_button_sheet.get_width()/3)/2,257)], [0,self.options_button_sheet, ((360-self.options_button_sheet.get_width()/3)/2, 352)], [0,self.tutorial_button_sheet,((360-self.tutorial_button_sheet.get_width()/3)/2, 444)]]
		self.cursor_index = 0
		self.on_timer = True
		self.cursor_timer = 0 
		self.cursor_downtime = 100
		self.animation_speed = 10
		self.frame = 0
		self.pressed_play = False

		self.player_idle = pygame.image.load('assets/player/player_ground_idle.png').convert_alpha()
		self.player_walk = pygame.image.load('assets/player/player_walk_right_sheet.png').convert_alpha()
		self.player_pos = [20, 630]
		self.player_rect = pygame.Rect(0,0,32,32)

	def update(self, events, delta, keys):
		self.frame = self.frame + 1
		if keys[pygame.K_SPACE]:
			if not self.on_timer:
				self.cursor_timer = pygame.time.get_ticks()
				self.on_timer = True
			
			elif pygame.time.get_ticks() - self.cursor_timer > self.cursor_downtime:
				self.cursor_index = (self.cursor_index + 1) % 4
				self.on_timer = False

		if keys[pygame.K_RETURN]:
			if self.cursor_index == 0:
				self.pressed_play = True

		
		
		if self.pressed_play:
			self.player_pos[0] = self.player_pos[0] + 2.5
			for button in self.buttons:
				button[0] = button[0] + 1
			if self.player_pos[0] > 370:
				new_state = fightState(self.game)
				new_state.enter_state()

		else:
			self.buttons[self.cursor_index][0] = self.buttons[self.cursor_index][0] + 1

		self.updatePlayerRect()

	def render(self, surface):
		self.getBackround()
		for button in self.buttons:
			self.getFrame(button[2], button[1], self.animation_speed, button[0])

		if self.pressed_play:
			self.getFrame((self.player_rect.x, self.player_rect.y), self.player_walk, 10, self.frame)
			surface.blit(self.surf, (0,0))
			surface.blit(self.torch_glow, self.torch_glow_pos)
		else:
			surface.blit(self.surf, (0,0))
			surface.blit(self.player_idle, self.player_rect)
			surface.blit(self.torch_glow, self.torch_glow_pos)
			


	def getBackround(self):
		self.surf.fill((0,0,0,0))
		index = (self.frame//10) % 4
		self.surf.blit(self.background, (0,0), (index * self.background.get_width()//4, 0, (index+1) * self.background.get_width()//4, self.background.get_height()))

	def getFrame(self, loc, sheet, speed, frame):
		if loc[1] == 598:
			num_frames = 12

		else:
			num_frames = 3
		index = (frame // speed) % num_frames
		self.surf.blit(sheet, loc, (index * sheet.get_width()//num_frames, 0, sheet.get_width()//num_frames, sheet.get_height()))

	def updatePlayerRect(self):
		self.player_rect.x, self.player_rect.y = self.player_pos[0]-32/2, self.player_pos[1]-32


class endState(State):
	def __init__(self, game, win, percent):
		self.game = game
		self.win = win
		self.percent = percent
		self.counter = 0

		self.background = pygame.image.load('assets/ui/end_screen.png')
		self.initial_time = pygame.time.get_ticks()
		self.big_font = pygame.font.SysFont('gothic', 48)
		self.big_font.bold = True
		self.med_font = pygame.font.SysFont('gothic', 32)
		self.med_font.bold = True
		self.num_font = pygame.font.SysFont('gothic', 64)
		self.num_font.bold = True
		self.num_font.italic = True
		self.text = [[self.big_font.render('YOU', True, (255,255,255)), self.big_font.render('DIED TO', True, (255,255,255)), self.med_font.render('AZALGANOTH... JR.', True, (255,255,255)), self.med_font.render('AFTER SAYING', True, (255,255,255)), self.med_font.render('OF THEIR NAME', True, (255,255,255))],[self.big_font.render('YOU', True, (255,255,255)), self.big_font.render('DEFEATED', True, (255,255,255)), self.med_font.render('AZALGANOTH... JR.', True, (255,255,255)), self.med_font.render('BY SAYING', True, (255,255,255)), self.med_font.render('OF THEIR NAME', True, (255,255,255))]]
		self.num_text = self.num_font.render('%{0}'.format(str(0)), True, (255,255,255))

		self.render_true = [False,False,False,False,False]

	def update(self, events, delta, keys):
		self.game.boss.head.update(delta, keys)

	def render(self, surface):
		delta = (pygame.time.get_ticks()-self.initial_time) / 1000

		surface.blit(self.background, (0,0))
		for x in range(4):
			if x < delta:
				self.render_true[x] = True
			if self.render_true[x]:
				surface.blit(self.text[self.win][x], ((360-self.text[self.win][x].get_width())/2,100+150*x/2))

		if delta > 4:
			if delta > 4.3:
				speed = 3
			else:
				speed = 1
			val = (pygame.time.get_ticks()-self.initial_time - 4000) * 	3//40 
			if val > 100:
				val = 100
			self.num_text = self.num_font.render('%{0}'.format(val), True, (255,255,255))
			surface.blit(self.num_text, ((360-self.num_text.get_width())/2, 375))
			surface.blit(self.text[self.win][4], ((360-self.text[self.win][4].get_width())/2, 425))


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