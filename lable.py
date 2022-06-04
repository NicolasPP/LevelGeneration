import pygame


class Lable:
	def __init__(self, text, x, y, font_size, colour):
		self.text = text
		self.x = x
		self.y = y
		self.lable_surface = self.render_lable(font_size, colour)
		self.rect = self.get_lable_rect()
	def render_lable(self, font_size, colour):
		font = pygame.font.Font(None, font_size)
		return font.render(self.text, True, colour)
	def get_lable_rect(self):
		return self.lable_surface.get_rect(topleft=(self.x, self.y))
	def draw(self, surface):
		pygame.draw.rect(surface, 'Black', self.rect)
		surface.blit(self.lable_surface, self.rect)
	def handle_click(self, pos):
		return self.rect.collidepoint(pos)
	def center(self):
		lable_w = self.lable_surface.get_rect().width
		half_w = lable_w // 2
		self.x -= half_w
		self.rect = self.get_lable_rect()