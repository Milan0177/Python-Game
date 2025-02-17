# -*- coding: utf-8 -*-
from pygame import Rect
from pygame.sprite import Sprite

from singleton import Singleton
import settings as config



class Camera(Singleton):

	# constructor called on new instance: Camera()
	def __init__(self, lerp=5,width=config.XWIN, height=config.YWIN):
		self.state = Rect(0, 0, width, height)
		self.lerp = lerp
		self.center = height//2
		self.maxheight = self.center

	def reset(self) -> None:
		" Called only when game restarts (after player death)."
		self.state.y = 0
		self.maxheight = self.center
	
	def apply_rect(self,rect:Rect) -> Rect:
		""" Transforms given rect relative to camera position.
		:param rect pygame.Rect: the rect to transform
		"""
		return rect.move((0,-self.state.topleft[1]))
	
	def apply(self, target:Sprite) -> Rect:
		""" Returns new target render position based on current camera position.
		:param target Sprite: a sprite that wants to get its render position.
		"""
		return self.apply_rect(target.rect)
	
	def update(self, target:Rect) -> None:
		""" Scrolls up to maxheight reached by player.
		Should be called each frame.
		:param target pygame.Rect: the target position to follow.
		"""
		# updating maxheight
		if(target.y<self.maxheight):
			self.lastheight = self.maxheight
			self.maxheight = target.y
		# calculate scrolling speed required
		speed = ((self.state.y+self.center)-self.maxheight)/self.lerp
		self.state.y-=speed

