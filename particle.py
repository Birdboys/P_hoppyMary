import pygame
import os
import random
import numpy as np

class Particle():

	particle_id = 0
	def __init__(self, shape, x, y, width, height, vel_x, vel_y, acc_x, acc_y, color, scale_factor):
		self.shape = shape
		self.width = width
		self.og_width = width
		self.height = height
		self.og_height = height
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.acc_y = acc_y
		self.acc_x = acc_x
		self.color = color
		self.scale_factor = scale_factor
		self.rect = pygame.Rect(x, y, width, height)
		self.particle_id = Particle.particle_id
		Particle.particle_id = Particle.particle_id + 1

	def update(self):
		self.vel_x = self.vel_x + self.acc_x
		self.vel_y = self.vel_y + self.acc_y

		self.rect.x, self.rect.y = self.rect.x+self.vel_x, self.rect.y+self.vel_y

		self.width = self.width - self.og_width * self.scale_factor
		self.height = self.height - self.og_height * self.scale_factor

	def render(self, surface):
		if self.shape == 'rect':
			pygame.draw.rect(surface, self.color, self.rect)
		if self.shape == 'circle':
			pygame.draw.circle(surface, self.color, (self.rect.x, self.rect.y), self.width)
