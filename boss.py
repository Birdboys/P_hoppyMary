import pygame
import numpy as np
import os
import random 
import math
from particle import *

class Boss():
	def __init__(self, gwidth, gheight, init_time):
		self.head = bossHead()
		self.pupil = bossPupil()
		self.top = bossTop()
		self.mid = bossMid()
		self.bot = bossBot()
		self.body_parts = {'top':self.top, 'mid':self.mid, 'bot':self.bot, 'head':self.head}
		self.body_part_offset = {'top':[0,0], 'mid':[0,0], 'bot':[0,0], 'head':[0,0]}
		self.og_widthts = {'top':[self.top.width, self.top.height], 'mid':[self.mid.width, self.mid.height], 'bot':[self.bot.width, self.bot.height]}
		self.og_pos = {'top':self.top.pos, 'mid':self.mid.pos, 'bot':self.bot.pos}
		
		self.current_attack = []
		self.attacks = [('top',1), ('mid',1), ('mid',2), ('bot', 1), ('bot', 2), ('bot', 3), ('head', 1), ('head', 2)]
		self.atk_probs = [1, 1, 1, 1, 1, 1, 1, 1]
		self.attack_stack = []
		self.attack2_timer = 0
		self.groundedMoves = [('bot', 2), ('bot', 3), ('top',1)]
		self.num_attacks = 1
		self.state = 0 #0-IDLE, 1-ATTACKING_1, 2-ATTACKING_2
		self.frame = 0
		self.init_time = init_time


	def update(self, events, delta, keys, player_pos):
		obstacles = []
		particles = []
		self.frame = self.frame + 1

		idle = True
		for part in self.body_parts:
			if self.body_parts[part].state != 0:
				idle = False

		if pygame.time.get_ticks() - self.init_time > 250:
			if len(self.attack_stack) == 0:
				self.attack_stack.append(random.choices(self.attacks, weights=self.atk_probs)[0])
				self.body_parts[self.attack_stack[0][0]].state = 1
				self.body_parts[self.attack_stack[0][0]].current_attack = self.attack_stack[0][1]
				self.attack2_timer = pygame.time.get_ticks()
			
			elif len(self.attack_stack) < self.num_attacks and (pygame.time.get_ticks() - self.attack2_timer) > 1500:
				while len(self.attack_stack) < self.num_attacks:
					attack = random.choices(self.attacks, weights=self.atk_probs)[0]
					if attack[0] != self.attack_stack[0][0]:
						self.attack_stack.append(attack)
						self.body_parts[attack[0]].state = 1
						self.body_parts[attack[0]].current_attack = attack[1]
				self.attack2_timer = pygame.time.get_ticks()

			for attack in self.attack_stack:
				if self.body_parts[attack[0]].state == 2:
					self.body_parts[attack[0]].attack_init(attack[1], player_pos)
				elif self.body_parts[attack[0]].state == 3:
					impact_parts = self.body_parts[attack[0]].attack_update(attack[1], player_pos)
					for ob in self.body_parts[attack[0]].getObstacles():
						obstacles.append(ob)
					for pa in self.body_parts[attack[0]].getParts():
						particles.append(pa)
					for doodad in impact_parts:
						particles.append(doodad)
				elif self.body_parts[attack[0]].state == 4:
					self.body_parts[attack[0]].reset_pos()
				elif self.body_parts[attack[0]].state == 5:
					self.body_parts[attack[0]].reset()
					self.attack_stack.remove(attack)

		for key in self.body_parts:
			self.body_parts[key].update(delta, keys)

		return obstacles, particles

	def render(self, surface, player_pos):
		if self.frame % 10 == 0:
			self.getOffsets(2, 4, 10)

		for part in self.body_parts:
			self.body_parts[part].render(surface, self.body_part_offset[part])

		pup_coord_x = self.head.pos[0] + 2 + (player_pos[0] - 180)//40 
		pup_coord_y = self.head.pos[1] + 42 + (player_pos[1] - 640)//50
		if self.head.state == 0:
			pup_coord_y = pup_coord_y + self.body_part_offset['head'][1]
			pup_coord_x = pup_coord_x + self.body_part_offset['head'][0]
		if self.head.state == 1:
			if self.head.current_attack == 1:
				pup_coord_y =  self.head.pos[1] + 27
				pup_coord_x = self.head.pos[0] + -7
			else:
				pup_coord_y =  self.head.pos[1] + 27
				pup_coord_x = self.head.pos[0] + 11
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
		self.state = 0 #0-IDLE, 1-INTROATTACK, 2-ATTACK_INIT, 3-ATTACKING, 4-REFORM, 5-RECOVERY
		self.prev_state = 0
		self.current_attack = 0
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.scalable_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.retreat_val = 0
		self.reform_trigger = False

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
		elif self.state == 5:
			pass 

		self.updateRect()
	
	def render(self, surface, offset):
		if self.state == 0:
			self.getFrame(self.idle_sheet, 20, self.frame)
			surface.blit(self.surf, (self.rect.x + offset[0], self.rect.y + offset[1]))
		elif self.state == 1:
			self.attack_render_intro(surface)
		elif self.state == 2:
			pass
		elif self.state == 3:
			self.attack_render(surface)
		elif self.state == 4:
			i = self.reformRender(surface)
			if i == 0 and self.reform_trigger:
				self.state = 5		
			if i > 0: 
				self.reform_trigger = True
		elif self.state == 5:
			pass


	def reset_pos(self):
		pass

	def attack_init(self, attack, player_pos):
		self.state = 3
		pass

	def attack_render_intro(self, surface):
		pass

	def attack_update(self, delta, keys):
		return []

	def attack_render(self,surface):
		pass

	def getPart(self, part_id):
		pass

	def getObstacles(self):
		return []

	def getParts(self):
		return []

	def updateRect(self):
		self.rect.x = self.pos[0]-self.width/2
		self.rect.y = self.pos[1]-self.height/2

	def getFrame(self, sheet, speed, frame):
		num_frames = sheet.get_width()/self.width
		index = (frame // speed) % num_frames
		self.surf.blit(sheet, (0,0), (index * self.width, 0, (index+1) * self.width, self.height))
		return index

	def reformRender(self, surface):
		i = self.getFrame(self.reform_sheet, self.reform_speed, self.frame)
		surface.blit(self.surf, self.rect)
		return i

class bossTop(bossPiece):
	
	def getPart(self):
		self.width, self.height = 224, 96
		self.scalable_width, self.scalable_height = 224, 96
		self.idle_sheet = pygame.image.load('assets/boss/boss_body_top_idle_sheet.png').convert_alpha()
		self.idle_sheet = pygame.transform.scale(self.idle_sheet, (self.width * (self.idle_sheet.get_width()/224), self.height))
		self.reform_sheet = pygame.image.load('assets/boss/boss_body_top_reform_sheet.png').convert_alpha()
		self.reform_sheet = pygame.transform.scale(self.reform_sheet, (self.width * (self.reform_sheet.get_width()/224), self.height))
		self.pos = [180, 310]
		self.attack1rect = pygame.Rect((0,0,self.width*1.25/2, self.height*1.25))
		self.attack1rect_speed = 1
		self.reform_speed = 10

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

	def reset_pos(self):
		self.pos = [180, 310]
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.surf.fill((0,0,0,0))


	def attack_init(self, attack, player_pos):
		if attack == 1:
			self.attack1rect.x = -50 - self.attack1rect.width
			self.attack1rect.y = 630 - self.attack1rect.height

			self.state = 3
			self.current_attack = 1

	def attack_render_intro(self, surface):
		if self.current_attack == 1:
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
				temp_rect_left = pygame.Rect(temp_rect.x, temp_rect.y, temp_rect.width/2-1, temp_rect.height)
				temp_rect_right = pygame.Rect(360 - temp_rect.x - self.width*0.75/2, temp_rect.y, temp_rect.width/2-1, temp_rect.height)
				self.pos[0] = self.pos[0] - 10
				pygame.draw.rect(surface,(35,24,36), temp_rect_left)
				pygame.draw.rect(surface,(35,24,36), temp_rect_right)
				if self.pos[0] < 0:
					self.state = 2
					self.retreat_val = 0

	def attack_update(self, delta, keys):
		if self.current_attack == 1:
			self.attack1rect.x = self.attack1rect.x + self.attack1rect_speed
			if self.attack1rect.x + self.attack1rect.width > 180:
				self.state = 4
				self.surf.fill((0,0,0,0))
				self.frame = 0
				party = [Particle('circle', 180, 620, 16 + random.randint(-4,4), 16 + random.randint(-4,4), 10 * (0.5-random.random()), -7 * random.random(), 0, 0.5, (28,20,29), 0.03) for x in range(40)]
				return party

		return []

	def getObstacles(self):
		if self.current_attack == 1:
			surf = pygame.Surface((self.attack1rect.width, self.attack1rect.height))
			surf.fill((35,24,36))
			other_rect = pygame.Rect(360 - self.attack1rect.x - self.attack1rect.width, self.attack1rect.y, self.attack1rect.width, self.attack1rect.height)
			return [Obstacle(surf, self.attack1rect), Obstacle(surf, other_rect)]

	def getParts(self):
		if self.current_attack == 1:
			parts = []
			num_parts = 3
			for pp in range(num_parts):
				parts.append(Particle('circle', self.attack1rect.x + random.randint(0,self.attack1rect.width),  self.attack1rect.y + self.attack1rect.height, 10 + random.randint(-2,2), 10 + random.randint(-2,2), -self.attack1rect_speed/2 + random.randint(-3, -1), random.randint(-7,-3), 0, 0.3, (28,20,29), 0.03))
			for pp in range(num_parts):
				parts.append(Particle('circle', 360 - self.attack1rect.x - self.attack1rect.width + random.randint(0,self.attack1rect.width),  self.attack1rect.y + self.attack1rect.height, 10+ random.randint(-2,2), 10+ random.randint(-2,2), self.attack1rect_speed/2 + random.randint(1,3), random.randint(-7,-3), 0, 0.3, (28,20,29), 0.03))
		return parts

class bossMid(bossPiece):

	def getPart(self):
		self.width, self.height = 160, 68
		self.scalable_width, self.scalable_height = 160, 68
		self.idle_sheet = pygame.image.load('assets/boss/boss_body_mid_idle_sheet.png').convert_alpha()
		self.idle_sheet = pygame.transform.scale(self.idle_sheet, (self.width * (self.idle_sheet.get_width()/160), self.height))
		self.reform_sheet = pygame.image.load('assets/boss/boss_body_mid_reform_sheet.png').convert_alpha()
		self.reform_sheet = pygame.transform.scale(self.reform_sheet, (self.width * (self.reform_sheet.get_width()/160), self.height))
		self.reform_speed = 8
		self.pos = [180, 420]

		self.attack1surf = pygame.Surface((self.width*1.25, self.height*1.25))
		self.attack1surf.fill((28, 20, 29))
		self.attack1rect = pygame.Rect((0,0),(self.width*1.25, self.height*1.25))
		self.attack1rect_speed = 2

		self.attack2rects = []
		self.attack2rect_speed = 5

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
	
	def reset_pos(self):
		self.pos = [180, 420]
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.surf.fill((0,0,0,0))

	def attack_init(self, attack, player_pos):
		if attack == 1:
			self.attack1rect.x = player_pos[0] + random.randint(-20,20)
			self.attack1rect.y = 0 - self.attack1rect.height
			
			if self.attack1rect.x < 0:
				self.attack1rect.x = 0
			elif self.attack1rect.x > 360 - self.attack1rect.width:
				self.attack1rect.x = 360-self.attack1rect.width

			self.state = 3
			self.current_attack = 1

		if attack == 2:

			self.attack2rects = [pygame.Rect(random.randint(0, 330), 0-self.height*1.25, self.width/4, self.height*1.25) for x in range(4)]
			self.attack2rects[0].x = player_pos[0] + random.randint(-20,20)
			if self.attack2rects[0].x < 0:
				self.attack2rects[0].x = 0
			if self.attack2rects[0].x + self.attack2rects[0].width > 360:
				self.attack2rects[0].x = 360 - self.attack2rects[0].width

			self.state = 3
			self.current_attack = 2


	def attack_render_intro(self, surface):
		if self.current_attack == 1:
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

		elif self.current_attack == 2:
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
					temp_rects = [pygame.Rect((temp_rect.x + temp_rect.width * 1/4*p + 6, temp_rect.y), (temp_rect.width * 1/4 - 6, temp_rect.height)) for p in range(4)]
					pos_old = self.pos[1]
					self.pos[1] = self.pos[1] + 10
					for r in range(len(temp_rects)):
						pygame.draw.rect(surface, (35,24,36), temp_rects[r])
					if temp_rects[0].y + temp_rects[0].height > 640:
						self.state = 2
						self.retreat_val = 0


	def attack_update(self, delta, keys):
		party = []
		if self.current_attack == 1:
			self.attack1rect.y = self.attack1rect.y + self.attack1rect_speed
			if self.attack1rect.y + self.attack1rect.height > 635:
				self.state = 4
				self.surf.fill((0,0,0,0))
				self.frame = 0
				party = [Particle('circle', self.attack1rect.x + random.randint(0,self.attack1rect.width),  self.attack1rect.y + self.attack1rect.height + random.randint(-3,3), 14 + random.randint(-2,2), 14 + random.randint(-2,2), random.randint(-5, 5), random.randint(-12,-6), 0, 0.3, (28,20,29), 0.02) for x in range(50)]

		if self.current_attack == 2:

			self.attack2rects[0].y = self.attack2rects[0].y + self.attack2rect_speed
			if self.attack2rects[0].y > 320 and len(self.attack2rects) > 1:
				self.attack2rects[1].y = self.attack2rects[1].y + self.attack2rect_speed
			if self.attack2rects[0].y + self.attack2rects[0].height > 640:
				fallen = self.attack2rects.pop(0)
				party = [Particle('circle', fallen.x + random.randint(0,fallen.width),  fallen.y + fallen.height, 8 + random.randint(-2,2), 8 + random.randint(-3,3), random.randint(-3, 3), random.randint(-10,-5), 0, 0.3, (28,20,29), 0.02) for x in range(15)]

			if len(self.attack2rects) == 0:
				self.state = 4
				self.surf.fill((0,0,0,0))
				self.frame = 0

		return party
		

	def getObstacles(self):
		if self.current_attack == 1:
			return [Obstacle(self.attack1surf, self.attack1rect)]
		if self.current_attack == 2:
			ret = []
			for rect in self.attack2rects:
				surf = pygame.Surface((rect.width, rect.height))
				surf.fill((28, 20, 29))
				if rect.y > 0:
					ret.append(Obstacle(surf, rect))
			return ret

class bossBot(bossPiece):

	def getPart(self):
		self.width, self.height = 48, 64
		self.scalable_width, self.scalable_height = 48, 64
		self.idle_sheet = pygame.image.load('assets/boss/boss_body_bot_idle_sheet.png').convert_alpha()
		self.idle_sheet = pygame.transform.scale(self.idle_sheet, (self.width * (self.idle_sheet.get_width()/48), self.height))
		self.reform_sheet = pygame.image.load('assets/boss/boss_body_bot_reform_sheet.png').convert_alpha()
		self.reform_sheet = pygame.transform.scale(self.reform_sheet, (self.width * (self.reform_sheet.get_width()/48), self.height))
		self.reform_speed = 6

		self.pos = [180, 520]

		self.attack1surf = pygame.Surface((self.width*1.5, self.height*1.5))
		self.attack1surf.fill((35,24,36))
		self.attack1rect = pygame.Rect((0,0),(self.width*1.5, self.height*1.5))
		self.attack1rect_speed = 3

		self.attack23rect_l = None
		self.attack23rect_r = None
		self.attack23rect_speed = 1
	
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

	def reset_pos(self):
		self.pos = [180, 520]
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)
		self.surf.fill((0,0,0,0))


	def attack_init(self, attack, player_pos):
		if attack == 1:
			self.attack1rect.x = player_pos[0] + random.randint(-20,20)
			self.attack1rect.y = 0 - self.attack1rect.height
			
			if self.attack1rect.x < 0:
				self.attack1rect.x = 0
			elif self.attack1rect.x > 360 - self.attack1rect.width:
				self.attack1rect.x = 360-self.attack1rect.width
			
			self.current_attack = 1

		elif attack == 2:
			w, h = self.width * 1.25, self.height/2 * 1.25
			self.attack23rect_l = pygame.Rect(0 - w, 630 - h, w, h)
			self.attack23rect_r = pygame.Rect(360, 630 - 2 * h - 5, w, h)
			self.current_attack = 2

		elif attack == 3:
			w, h = self.width * 1.25, self.height/2 * 1.25 
			self.attack23rect_l = pygame.Rect(0 - w, 630 - 2 *h-5, w, h)
			self.attack23rect_r = pygame.Rect(360, 630 - h, w, h)
			self.current_attack = 3

		self.state = 3

	def attack_render_intro(self, surface):
		if self.current_attack == 1:
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

		if self.current_attack == 2 or self.current_attack == 3:
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
				if self.current_attack == 3:
					temp_rect_bot = pygame.Rect(360 - temp_rect.x - temp_rect.width, temp_rect.y, self.width * 0.75, self.height *0.75 * 0.5)
					temp_rect_top = pygame.Rect(temp_rect.x, temp_rect.y+(self.height)/2+ 2, self.width * 0.75, self.height * 0.75 * 0.5 - 1)
				else:
					temp_rect_bot = pygame.Rect(temp_rect.x, temp_rect.y, self.width * 0.75, self.height *0.75 * 0.5)
					temp_rect_top = pygame.Rect(360 - temp_rect.x - temp_rect_bot.width, temp_rect.y+(self.height)/2+ 2, self.width * 0.75, self.height * 0.75 * 0.5 - 1)

				pygame.draw.rect(surface, (35,24,36), temp_rect_top)
				pygame.draw.rect(surface, (35,24,36), temp_rect_bot)
				old_pos = self.pos[0]
				self.pos[0] = self.pos[0] + 10
				if self.pos[0] > 360:
					self.state = 2
					self.retreat_val = 0

		else:
			pass

	def attack_update(self, delta, keys):
		if self.current_attack == 1:
			self.attack1rect.y = self.attack1rect.y + self.attack1rect_speed
			if self.attack1rect.y + self.attack1rect.height > 635:
				self.state = 4
				self.frame = 0
				self.surf.fill((0,0,0,0))
				return [Particle('circle', self.attack1rect.x + random.randint(0,self.attack1rect.width),  self.attack1rect.y + self.attack1rect.height, 10 + random.randint(-2,2), 10 + random.randint(-2,2), random.randint(-3, 3), random.randint(-10,-5), 0, 0.3, (28,20,29), 0.02) for x in range(20)]

		if self.current_attack == 2 or self.current_attack == 3:
			self.attack23rect_l.x = self.attack23rect_l.x + self.attack23rect_speed
			self.attack23rect_r.x = self.attack23rect_r.x - self.attack23rect_speed

			if self.current_attack == 3: #right
				parts = [Particle('circle', self.attack23rect_r.x + random.randint(0,self.attack23rect_r.width),  self.attack23rect_r.y + self.attack23rect_r.height, 10 + random.randint(-2,2), 4 + random.randint(-2,2), self.attack23rect_speed/3 + random.randint(1, 3), random.randint(-3,-1), 0, 0.3, (28,20,29), 0.03) for x in range(1)]
			else:
				parts = [Particle('circle', self.attack23rect_l.x + random.randint(0,self.attack23rect_l.width),  self.attack23rect_l.y + self.attack23rect_l.height, 10 + random.randint(-2,2), 4 + random.randint(-2,2), -self.attack23rect_speed/3 + random.randint(-3, -1), random.randint(-3,-1), 0, 0.3, (28,20,29), 0.03) for x in range(1)]
			
			if self.attack23rect_l.x > 360:
				self.state = 4
				self.frame = 0
				self.surf.fill((0,0,0,0))

			return parts
				
		return[]

	def attack_render(self, surface):
		if self.current_attack == 1:
			pass
			#pygame.draw.rect(surface, (35,24,36), self.attack1rect)

	def getObstacles(self):
		if self.current_attack == 1:
			return [Obstacle(self.attack1surf, self.attack1rect)]

		if self.current_attack == 2 or self.current_attack == 3:
			surf = pygame.Surface((self.attack23rect_r.width, self.attack23rect_r.height))
			surf.fill((28, 20, 29))
			return [Obstacle(surf, self.attack23rect_r), Obstacle(surf, self.attack23rect_l)]

class bossHead(bossPiece):
	
	def __init__(self):
		self.width, self.height = 188, 180
		self.head_idle_sheet = pygame.image.load('assets/boss/boss_head_idle_sheet.png').convert_alpha()
		self.head_idle_sheet = pygame.transform.scale(self.head_idle_sheet, (self.width * (self.head_idle_sheet.get_width()/188), self.height))
		self.head_left_laser_sheet = pygame.image.load('assets/boss/boss_head_laser_left_sheet.png').convert_alpha()
		self.head_left_laser_sheet =  pygame.transform.scale(self.head_left_laser_sheet, (self.width * (self.head_left_laser_sheet.get_width()/188), self.height))
		self.head_right_laser_sheet = pygame.image.load('assets/boss/boss_head_laser_right_sheet.png').convert_alpha()
		self.head_right_laser_sheet =  pygame.transform.scale(self.head_right_laser_sheet, (self.width * (self.head_right_laser_sheet.get_width()/188), self.height))
		self.laser_sheet = pygame.image.load('assets/boss/boss_horn_laser_sheet.png').convert_alpha()
		self.pos = [180, 150]
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height/2, self.width, self.height)

		self.state = 0 #0-IDLE, 
		self.frame = 0

		self.current_attack = 0
		self.head_laser_charge_speed = 15
		self.head_laser_shoot_speed = 40
		self.horn_laser_render_trigger = False
		self.horn_laser_shoot_trigger = False
		self.horn_laser_pos = [0,0]
		self.horn_laser_surf = pygame.Surface((82,590), pygame.SRCALPHA)
		self.horn_laser_rect_draw = pygame.Rect(0, 0, 82, 590)
		self.horn_laser_rect_hit = pygame.Rect(0,0, 36, 590)\

		self.has_left_lasered = False
		self.has_right_lasered = False

	def update(self, delta, keys):
		self.frame = self.frame + 1
		self.updateRect() 
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
	
	def render(self, surface, offset):
		if self.state == 0:
			new_pos = (self.rect.x+offset[0], self.rect.y+offset[1])
			self.getFrame(self.head_idle_sheet, 10, self.frame)
			surface.blit(self.surf, new_pos)
		elif self.state == 1:
			self.attack_render_intro(surface)
		elif self.state == 2:
			pass
		elif self.state == 3:
			self.attack_render(surface)

	def attack_init(self, attack, player_pos):
		if attack == 1:
			self.horn_laser_pos[0], self.horn_laser_pos[1] = self.rect.x + 5 - self.horn_laser_rect_draw.width/2, self.rect.y+5 
			self.horn_laser_rect_draw.x, self.horn_laser_rect_draw.y = self.horn_laser_pos[0], self.horn_laser_pos[1]
			self.horn_laser_rect_hit.x, self.horn_laser_rect_hit.y = self.horn_laser_pos[0] + 23, self.horn_laser_pos[1]
			self.current_attack == 1
		elif attack == 2:
			self.horn_laser_pos[0], self.horn_laser_pos[1] = self.rect.x + self.width - 5 - self.horn_laser_rect_draw.width/2, self.rect.y+5 
			self.horn_laser_rect_draw.x, self.horn_laser_rect_draw.y = self.horn_laser_pos[0], self.horn_laser_pos[1]
			self.horn_laser_rect_hit.x, self.horn_laser_rect_hit.y = self.horn_laser_pos[0] + 23, self.horn_laser_pos[1]
			self.current_attack == 2

		self.frame = 0
		self.state = 3

	def attack_render_intro(self, surface):
		if self.current_attack == 1: #LEFT LASER
			i = self.getFrame(self.head_left_laser_sheet, self.head_laser_charge_speed, self.frame)
			if i > 1:
				self.horn_laser_render_trigger = True
			if i == 0 and self.horn_laser_render_trigger:
				self.state = 2
				self.horn_laser_render_trigger = False

		elif self.current_attack == 2:
			i = self.getFrame(self.head_right_laser_sheet, self.head_laser_charge_speed, self.frame)
			if i > 1:
				self.horn_laser_render_trigger = True
			if i == 0 and self.horn_laser_render_trigger:
				self.state = 2
				self.horn_laser_render_trigger = False

		surface.blit(self.surf, self.rect)

	def attack_update(self, delta, keys):
		if self.current_attack == 1 or self.current_attack == 2: 
			val = (random.random()) * self.horn_laser_rect_draw.width
			return [Particle('circle', self.horn_laser_pos[0] + val, self.horn_laser_pos[1] + self.horn_laser_rect_draw.height - 20, 4 + random.randint(-2,2), 4 + random.randint(-2,2), (val-self.horn_laser_rect_draw.width/2)/30, random.randint(-2,-1), 0, 0.5, (255,255,255), 0.10) for x in range(20)]
		return []

	def attack_render(self, surface):
		if self.current_attack == 1:
			self.has_left_lasered = True
			ind = self.getLaserFrame(self.laser_sheet, self.head_laser_shoot_speed, self.frame)
			if ind == 0:
				self.horn_laser_rect_hit.width, self.horn_laser_rect_hit.height = 0,0
			else:
				self.horn_laser_rect_hit.width, self.horn_laser_rect_hit.height = 36, 590

			if ind > 1:
				self.horn_laser_shoot_trigger = True
			elif ind == 0 and self.horn_laser_shoot_trigger:
				self.horn_laser_shoot_trigger = False
				self.frame = 0
				self.state = 5

			surface.blit(self.surf, self.rect)

		elif self.current_attack == 2:
			self.has_right_lasered = True
			ind = self.getLaserFrame(self.laser_sheet, self.head_laser_shoot_speed, self.frame)
			if ind == 0:
				self.horn_laser_rect_hit.width, self.horn_laser_rect_hit.height = 0,0
			else:
				self.horn_laser_rect_hit.width, self.horn_laser_rect_hit.height = 36, 590

			if ind > 1:
				self.horn_laser_shoot_trigger = True
			elif ind == 0 and self.horn_laser_shoot_trigger:
				self.horn_laser_shoot_trigger = False
				self.frame = 0
				self.state = 5

			surface.blit(self.surf, self.rect)

	def getLaserFrame(self, sheet, speed, frame):
		num_frames = 3
		index = (frame // speed) % num_frames
		self.horn_laser_surf.blit(sheet, (0,0), (index * self.horn_laser_rect_draw.width, 0, (index+1) * self.horn_laser_rect_draw.width, self.horn_laser_rect_draw.height))
		return index

	def reset(self):
		self.state = 0 #0-IDLE, 
		self.frame = 0
		self.current_attack = 0
		self.pos = [180, 150]
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

	def getObstacles(self):
		if self.current_attack == 1 or self.current_attack == 2:
			return [Obstacle(None, self.horn_laser_rect_hit), Obstacle(self.horn_laser_surf, self.horn_laser_rect_draw, -1)]

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
	def __init__(self, surface, rect, shadow_smallest_size=0.5):
		self.surf = surface
		self.rect = rect
		self.shadow_smallest_size = shadow_smallest_size

	def render(self, surface):
		if self.surf != None:
			surface.blit(self.surf, self.rect)

	def renderShadow(self, surface, offset):
		if self.surf != None:
			shadow_rect = self.getShadow(offset)
			shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height))
			pygame.draw.ellipse(shadow_surf, (20,20,20), (0,0,shadow_rect.width, shadow_rect.height))
			surface.blit(shadow_surf, shadow_rect, special_flags=2)

	def getShadow(self, offset):
		s_width = self.rect.width - self.rect.width * (((1-self.shadow_smallest_size) * (626 - (self.rect.y + self.rect.height))/626))
		return pygame.Rect(self.rect.x + (self.rect.width - s_width)/2, 627 + offset[1], s_width, 11)


#TOMORROW PLAN
#GENERALIZE BLOCK LEAVING TO FUNCTION LIKE ATTACK_UPDATE
#USE PLAYER QUADRANTS TO WEIGHT ATTACKS OR WEIGHT ATTACK LOCATIONS
#MENUS
#SOUND EFFF
