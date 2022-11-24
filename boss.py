import pygame
import numpy as np
import os
import random 
import math

class Boss():
	def __init__(self, gwidth, gheight):
		self.head = bossHead()
		self.pupil = bossPupil()
		self.top = bossTop()
		self.mid = bossMid()
		self.bot = bossBot()
		self.body_parts = {'top':self.top, 'mid':self.mid, 'bot':self.bot, 'head':self.head}
		self.body_part_offset = {'top':[0,0], 'mid':[0,0], 'bot':[0,0], 'head':[0,0]}
		self.og_widthts = {'top':[self.top.width, self.top.height], 'mid':[self.mid.width, self.mid.height], 'bot':[self.bot.width, self.bot.height]}
		self.og_pos = {'top':self.top.pos, 'mid':self.mid.pos, 'bot':self.bot.pos}
		
		self.attack_stack = [('bot',1)]
		self.state = 0 #0-IDLE, 1-ATTACKING_1, 2-ATTACKING_2
		self.frame = 0

	def update(self, events, delta, keys, player_pos):
		obstacles = []
		self.frame = self.frame + 1
		for key in self.body_parts:
			if self.body_parts[key].state == 2:
				self.body_parts[key].attack_init(1, player_pos)
			elif self.body_parts[key].state == 3:
				self.body_parts[key].attack_update(1, player_pos)
				for ob in self.body_parts[key].getObstacles():
					obstacles.append(ob)
			elif self.body_parts[key].state == 4:
				self.body_parts[key].reset()
			self.body_parts[key].update(delta, keys)

		if keys[pygame.K_SPACE] and self.top.state == 0:
			pass
			#self.top.state = 1
		if keys[pygame.K_UP] and self.mid.state == 0:
			self.mid.state = 1
		if keys[pygame.K_DOWN] and self.bot.state == 0:
			self.bot.state = 1

		return obstacles


	def render(self, surface, player_pos):
		if self.frame % 10 == 0:
			self.getOffsets(2, 4, 10)

		for part in self.body_parts:
			self.body_parts[part].render(surface, self.body_part_offset[part])

		pup_coord_x = self.head.pos[0] + 2 + (player_pos[0] - 180)//40 + self.body_part_offset['head'][0]
		pup_coord_y = self.head.pos[1] + 42 + (player_pos[1] - 640)//50 + self.body_part_offset['head'][1]
		self.pupil.render(surface, [pup_coord_x, pup_coord_y])

	def getOffsets(self, strength, max_off_x, max_off_y):
		ops = [-1 * strength, 0, strength]
		for key in self.body_part_offset:
			tempx = self.body_part_offset[key][0] + random.choice(ops)
			tempy = self.body_part_offset[key][1] + random.choice(ops)
			if tempx < max_off_x and tempx > -1 * max_off_x:
				self.body_part_offset[key][0] = tempx
			if tempy < max_off_y and tempy > -1 * max_off_y:
				self.body_part_offset[key][1] = tempy

class bossPiece():
	def __init__(self):
		self.getPart()
		self.frame = 0
		self.state = 0 #0-IDLE, 1-INTROATTACK, 2-ATTACK_INIT, 3-ATTACKING, 4-RECOVERY
		self.prev_state = 0
		self.current_attack = 0
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.scalable_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.retreat_val = 0

	def update(self, delta, keys):
		self.frame = self.frame + 1

		if self.state == 0:
			pass
		elif self.state == 1:
			pass
		elif self.state == 2:
			pass
		elif self.state == 3:
			self.attack_update(delta, keys)
		elif self.state == 4:
			pass

		self.updateRect()
	
	def render(self, surface, offset):
		if self.state == 0:
			self.getFrame(self.idle_sheet, 20, self.frame)
			surface.blit(self.surf, (self.rect.x + offset[0], self.rect.y + offset[1]))
		elif self.state == 1:
			self.getFrame(self.idle_sheet, 20, self.frame)
			if self.retreat_val < 254:
				self.retreat_val = self.retreat_val + 3
				scale_val = 1- (0.25 * self.retreat_val/255)
				temp = pygame.transform.scale(self.surf, (self.width * scale_val, self.height * scale_val))
				temp_rect = pygame.Rect(self.pos[0]-(self.width * scale_val)/2, self.pos[1]-(self.height * scale_val)/2, self.width * scale_val, self.height * scale_val)
				surface.blit(temp, temp_rect)
				pygame.draw.rect(surface,(35,24,36,self.retreat_val*.3), temp_rect)
			else:
				temp_rect = pygame.Rect(self.pos[0]-(self.width * 0.75)/2, self.pos[1]-(self.height * 0.75)/2, self.width * 0.75, self.height * 0.75)
				self.pos[1] = self.pos[1] + 20
				pygame.draw.rect(surface,(35,24,36), temp_rect)
				if self.pos[1] > 640:
					self.state = 2
					self.retreat_val = 0
		elif self.state == 3:
			self.attack_render(surface)


	def attack_init(self, attack, player_pos):
		self.state = 3
		pass

	def attack_update(self, delta, keys):
		pass

	def attack_render(self, surface):
		pass

	def getPart(self, part_id):
		pass

	def getObstacles(self):
		return []

	def updateRect(self):
		self.rect.x = self.pos[0]-self.width/2
		self.rect.y = self.pos[1]-self.height/2

	def getFrame(self, sheet, speed, frame):
		num_frames = sheet.get_width()/self.width
		index = (frame // speed) % num_frames
		self.surf.blit(sheet, (0,0), (index * self.width, 0, (index+1) * self.width, self.height))

class bossTop(bossPiece):
	
	def getPart(self):
		self.width, self.height = 224, 96
		self.scalable_width, self.scalable_height = 224, 96
		self.idle_sheet = pygame.image.load('assets/boss/boss_body_top_idle_sheet.png').convert_alpha()
		self.idle_sheet = pygame.transform.scale(self.idle_sheet, (self.width * (self.idle_sheet.get_width()/224), self.height))
		self.pos = [180, 310]

	def reset(self):
		self.pos = [180, 310]
		self.frame = 0
		self.state = 0 #0-IDLE, 1-INTROATTACK, 2-ATTACK, 3-RECOVERY
		self.prev_state = 0
		self.current_attack = 0
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.scalable_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.retreat_val = 0

class bossMid(bossPiece):

	def getPart(self):
		self.width, self.height = 160, 68
		self.scalable_width, self.scalable_height = 160, 68
		self.idle_sheet = pygame.image.load('assets/boss/boss_body_mid_idle_sheet.png').convert_alpha()
		self.idle_sheet = pygame.transform.scale(self.idle_sheet, (self.width * (self.idle_sheet.get_width()/160), self.height))
		self.pos = [180, 420]

	def reset(self):
		self.pos = [180, 420]
		self.frame = 0
		self.state = 0 #0-IDLE, 1-INTROATTACK, 2-ATTACK, 3-RECOVERY
		self.prev_state = 0
		self.current_attack = 0
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.scalable_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.retreat_val = 0

class bossBot(bossPiece):

	def getPart(self):
		self.width, self.height = 48, 64
		self.scalable_width, self.scalable_height = 48, 64
		self.idle_sheet = pygame.image.load('assets/boss/boss_body_bot_idle_sheet.png').convert_alpha()
		self.idle_sheet = pygame.transform.scale(self.idle_sheet, (self.width * (self.idle_sheet.get_width()/48), self.height))
		self.pos = [180, 520]

		self.attack1surf = pygame.Surface((self.width*1.5, self.height*1.5))
		self.attack1rect = pygame.Rect((0,0),(self.width*1.5, self.height*1.5))
		self.attack1rect_speed = 5
		
	
	def reset(self):
		self.pos = [180, 520]
		self.frame = 0
		self.state = 0 #0-IDLE, 1-INTROATTACK, 2-ATTACK, 3-RECOVERY
		self.prev_state = 0
		self.current_attack = 0
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.scalable_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.retreat_val = 0

	def attack_init(self, attack, player_pos):
		if attack == 1:
			self.attack1rect.x = player_pos[0] + random.randint(-20,20)
			self.attack1rect.y = 0 - self.attack1rect.height
			self.state = 3
			self.current_attack = 1

	def attack_update(self, delta, keys):
		if self.current_attack == 1:
			self.attack1rect.y = self.attack1rect.y + self.attack1rect_speed
			if self.attack1rect.y > 640:
				self.state = 4

	def attack_render(self, surface):
		if self.current_attack == 1:
			pygame.draw.rect(surface, (35,24,36), self.attack1rect)

	def getObstacles(self):
		if self.current_attack == 1:
			return [Obstacle(self.attack1surf, self.attack1rect)]

class bossHead(bossPiece):
	
	def __init__(self):
		self.width, self.height = 188, 180
		self.head_idle_sheet = pygame.image.load('assets/boss/boss_head_idle_sheet.png').convert_alpha()
		self.head_idle_sheet = pygame.transform.scale(self.head_idle_sheet, (self.width * (self.head_idle_sheet.get_width()/188), self.height))
		self.pos = [180, 150]
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height/2, self.width, self.height)

		self.state = 0 #0-IDLE, 
		self.frame = 0

	def update(self, delta, keys):
		self.frame = self.frame + 1
		self.updateRect() 
	
	def render(self, surface, offset):
		new_pos = (self.rect.x+offset[0], self.rect.y+offset[1])
		self.getFrame(self.head_idle_sheet, 10, self.frame)
		surface.blit(self.surf, new_pos)

class bossPupil():
	def __init__(self):
		self.pupil_image = pygame.image.load('assets/boss/boss_pupil.png').convert_alpha()
		self.width = self.pupil_image.get_width()
		self.height = self.pupil_image.get_height()


	def render(self, surface, coords):
		surface.blit(self.pupil_image, (coords[0] - self.width//2, coords[1] - self.height//2))

	def getCoords(self, coords):
		return

class Obstacle():
	def __init__(self, surface, rect):
		self.surf = surface
		self.rect = rect

	def render(self, surface):
		surface.blit(self.surf, self.rect)
