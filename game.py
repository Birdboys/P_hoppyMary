import pygame
import os
import random
from state import *
from player import *
from boss import *

class Game:

	SPAWN_OBSTACLE = pygame.USEREVENT+1
	pygame.display.set_caption("Hoppy Mary")
	BACKGROUND_COLOR = (100,100,100)
	FPS = 60
	clock = pygame.time.Clock()	

	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.music.set_volume(0.3)
		self.WIDTH, self.HEIGHT = 360, 640
		self.WIN = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
		self.game_canvas = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

		self.playing = True
		self.running = True
		self.state_stack = [testState(self)]
		self.prev_state = None

		self.player = Player(360, 640)
		self.boss = Boss(360, 640)

		self.tracks = {'fight':'assets/music/fight_track.mp3'}
		pygame.mixer.music.load(self.tracks['fight'])
		pygame.mixer.music.play(-1)

	def update(self, events, delta, keys):
		self.state_stack[-1].update(events, delta, keys)

	def render(self, events):
		self.state_stack[-1].render(self.game_canvas)
		self.WIN.blit(self.game_canvas,(0,0))
		pygame.display.update()

	def game_loop(self):
		delta = Game.clock.tick(Game.FPS)/1000
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		self.update(events, delta, keys)
		self.render(self.WIN)
