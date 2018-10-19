from pygame import Rect
from pygame.draw import rect as draw_rect


class food:
    """
    This class represents the food in the environment.
    It contains nothing more than a position and a size
    as well as a rectangle which dimensions depends on size
    """
    def __init__(self, position, size):
        """
        Set the position and size and generate the corret rectangle
        """
        self.position = position
        self.rectangle = Rect(0, 0, size, size)
        self.rectangle.center = (self.position.x, self.position.y)
        self.size = size

    def draw(self, screen):
        """
        Draw a green looking rectangle.
        """
        draw_rect(screen, (0, 168, 73), self.rectangle, 0)
