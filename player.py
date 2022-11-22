import pygame
import numpy as np
import os
import random 
class Player:

	def __init__(self, gwidth, gheight):
		self.game_width, self.game_height = gwidth, gheight
		self.width, self.height = 48,48
		self.pos = [60, 630]
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(self.pos[0]-self.width/2, self.pos[1]-self.height, self.width, self.height)

		self.run_speed = 2.3
		self.state = 0 #0=GROUNDED, 1=AIR_1, 2=AIR_2
		self.button_state = False
		self.button_timer = 0

		self.idle_state = False
		self.idle_timer = 0

		self.quadrant_x = 0
		self.quadrant_y = 0

		#air1 stuff
		self.air1_apex = False
		self.air1_ascend_speed = 12
		self.air1_descend_speed = 0
		self.air1_gravity = 0.5
		self.air1_terminal = 20

		#air2 stuff
		self.air2_apex = False
		self.air2_fast_fall = False
		self.air2_original_height = 0
		self.air2_ascend_speed = 5
		self.air2_slow_fall_speed = 3 
		self.air2_descend_speed = 0
		self.air2_dest_fall_speed = 15
		self.air2_gravity = 0.5
		self.air2_terminal = 20

		#image stuff
		self.idle_image = pygame.image.load('assets/player/player_ground_idle.png').convert_alpha()
		self.idle_image = pygame.transform.scale(self.idle_image, (self.width, self.height))
		self.walk_right_sheet = pygame.image.load('assets/player/player_walk_right_sheet.png').convert_alpha()
		self.walk_right_sheet = pygame.transform.scale(self.walk_right_sheet, (self.width * (self.walk_right_sheet.get_width()/32), self.height))
		self.walk_left_sheet = pygame.image.load('assets/player/player_walk_left_sheet.png').convert_alpha()
		self.walk_left_sheet = pygame.transform.scale(self.walk_left_sheet, (self.width * (self.walk_left_sheet.get_width()/32), self.height))

		self.frame = 0
		self.walk_animation_speed = 5

	def update(self, delta, keys):
		
		if self.state == 0: #GROUNDED
			if keys[pygame.K_SPACE]: #if they are pressing space
				backwards = 1 #walk back
				#self.button_state = True #they are now pressing
				if self.button_state == False: #if this is a new press 
					self.idle_state = True
					self.idle_timer = pygame.time.get_ticks()

					self.button_state = True
					if self.didJump(pygame.time.get_ticks(), 200): #if they jumped
						self.state = 1 #change to jump state
						self.idle_state = False

					else: #if they didn't
						self.button_timer = pygame.time.get_ticks() #set timer at press time
				
				else: #if not new press
					self.button_state = True
	
			else:
				backwards = -1 #walk forwards
				if self.button_state == True: #if button was released
					self.idle_state = True
					self.idle_timer = pygame.time.get_ticks()
					self.button_state = False
					#self.button_timer = 0

			if not self.isIdle(pygame.time.get_ticks(), 200):
				self.pos[0] = self.pos[0] + (self.run_speed * delta * 60)*(-1 * backwards)
			

		if self.state == 1: #AIR_1

			if not self.air1_apex and not self.pos[1] < 300:
				if self.pos[1] < 330: #if nearing jump apex
					self.pos[1] = self.pos[1] + (self.air1_ascend_speed * delta * 60 * -1 * 0.5) #slow ascent
				else:
					self.pos[1] = self.pos[1] + (self.air1_ascend_speed * delta * 60 * -1) #ascent at normal pace
				
				if self.pos[1] < 300:
					self.air1_apex = True
			else: #if already ascended
				self.air1_descend_speed = self.air1_descend_speed + self.air1_gravity
				if self.air1_descend_speed > self.air1_terminal:
					self.air1_descend_speed = self.air1_terminal
				self.pos[1] = self.pos[1] + (self.air1_descend_speed * delta * 60) #they fall
				
				if keys[pygame.K_SPACE]: #if button pressed
					self.state = 2 
					self.air1_apex = False
					self.air1_descend_speed = 0
					self.button_state = True
					self.air2_original_height = self.pos[1]

			if self.groundCheck(): #if we are now grounded
				self.air1_apex = False #reset air1 stuff
				self.air1_descend_speed = 0 #reset air descent speed

		if self.state == 2: #AIR_2
			
			if not self.air2_apex and not (self.air2_original_height - self.pos[1]) > 100:
				self.pos[1] = self.pos[1] + (self.air2_ascend_speed * delta * 60 * -1) #ascend
				if (self.air2_original_height - self.pos[1]) > 100: #if we finished jump
					self.air2_apex = True #set jump flag

			else:
				if not self.air2_fast_fall:
					if keys[pygame.K_SPACE]: #if they are pressing
						self.button_state = True
						self.air2_descend_speed = self.air2_descend_speed - 1 #slow descent with wings
						if self.air2_descend_speed < self.air2_slow_fall_speed:
							self.air2_descend_speed = self.air2_slow_fall_speed
						self.pos[1] = self.pos[1] + (self.air2_descend_speed * delta * 60) #slow fall
						

					else: 
						self.air2_descend_speed = self.air2_descend_speed + self.air2_gravity
						if self.air2_descend_speed > self.air2_terminal:
							self.air2_descend_speed = self.air2_terminal
						self.button_state = False
						self.pos[1] = self.pos[1] + (self.air2_descend_speed * delta * 60) #normal fall

				else:
					self.pos[1] = self.pos[1] + (self.air2_fast_fall_speed * delta * 60) #fast fall

			if self.groundCheck(): #if we are now grounded
				self.air2_apex = False
				self.air2_fast_fall = False #reset air2 stuff
				self.air2_original_height = 0
				self.air2_descend_speed = 0

		self.frame = self.frame + 1
		self.edgeCheck()
		self.updateRect() #update rect after moving and stuff
		self.getQuad()		

	def render(self, surface):
		self.surf.fill((0,0,0,0))
		if self.state == 0:
			if self.idle_state:
				surface.blit(self.idle_image, self.rect)
			else:
				if self.button_state == True: #if going left
					self.getFrame(self.walk_left_sheet, self.walk_animation_speed, self.frame)
				else:
					self.getFrame(self.walk_right_sheet, self.walk_animation_speed, self.frame)
				surface.blit(self.surf, self.rect)
		else:
			pygame.draw.rect(surface, (30,255,150), self.rect)

	def updateRect(self):
		self.rect.x = self.pos[0]-self.width/2
		self.rect.y = self.pos[1]-self.height

	def edgeCheck(self):
		if (self.pos[0] - self.width/2) < 0:
			self.pos[0] = self.width/2

		if self.pos[0] + self.width/2 > self.game_width:
			self.pos[0] = self.game_width - self.width/2

	def getQuad(self):
		self.quadrant_x = (self.pos[0] - self.game_width/2) // (self.game_width/8)
		self.quadrant_y = (self.game_height - self.pos[1]) // (self.game_height/4)

	def didJump(self, nT, timer):
		delta = nT - self.button_timer #change in time since last press
		if delta < timer: #if second press is fast enough
			return True
		else:
			return False

	def isIdle(self, nT, timer):
		delta = nT - self.idle_timer
		if delta < timer:
			return True
		else:
			self.idle_state = False
			return False

	def groundCheck(self):
		if self.pos[1] > 630:
			self.pos[1] = 630
			self.state = 0
			self.idle_state = True
			self.idle_timer = pygame.time.get_ticks()
			return True

	def getFrame(self, sheet, speed, frame):
		num_frames = sheet.get_width()/self.width
		index = frame % (num_frames * speed) // num_frames
		self.surf.blit(sheet, (0,0), (index * self.width, 0, (index+1) * self.width, self.height))

		print(index)

		

#STATES
#- grounded
#- air1
#- air2


#GROUNDED
#- 