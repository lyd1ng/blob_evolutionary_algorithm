from pygame import Rect
from pygame.draw import rect as draw_rect


class food:
    def __init__(self, position, size):
        self.position = position
        self.rectangle = Rect(0, 0, size, size)
        self.rectangle.center = (self.position.x, self.position.y)
        self.size = size

    def draw(self, screen):
        draw_rect(screen, (0, 168, 73), self.rectangle, 0)
