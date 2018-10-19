import math
import pygame
from random import random
from vector import vector2
from environment import calculate_max_speed
from environment import calculate_max_steering
from environment import calculate_hdot
from environment import calculate_hdbm
from environment import calculate_reproduction_chance


"""
This event will signal a death of a blob and trigger a creation
of food at the same position
"""
BLOB_DEATH_EVENT = pygame.USEREVENT + 2
"""
This event will trigger a creation of a new blob with similar dna
the dna will be mutated and added as an event attribute
"""
BLOB_REPRODUCTION_EVENT = pygame.USEREVENT + 3
"""
This event will thrown if a blob ate a piece of food
"""
BLOB_ATE_EVENT = pygame.USEREVENT + 4

# A font to render blob health
FONT = None


def blob_init():
    """
    This function loads the font to use. The blob module contains
    an own font object cause I didnt know a loggical place to store the
    font module for main.py and blob.py to use it.
    As a result this function has to be invoked before a blob is rendered.
    """
    global FONT
    FONT = pygame.font.SysFont("DejaVuSansMono", 15)


class blob:
    """
    This class represents the blobs.
    It contains the states needed for physical simulation,
    as well as subject properties.
    """
    def __init__(self, position, dna, health=1):
        self.position = position
        self.velocity = vector2(0, 0)
        self.health = health
        self.dna = dna
        self.size = dna[0]
        self.health_threshold = dna[1]
        self.max_speed = calculate_max_speed(self.size)
        self.max_steering = calculate_max_steering(self.size)
        # Health decrease over time
        self.hdot = calculate_hdot(self.size)
        # Health decrease by movement
        self.hdbm = calculate_hdbm(self.size)
        # Blobs become adults after eating the first food
        self.is_adult = False
        # A surface to render the health on
        self.health_surface = FONT.render(str(self.health), False, (255, 255, 255))

    def seek(self, food):
        """
        This function calculates the velocity by the formulars of
        steering behaviour (look at daniel shiffmans youtube account for
        more informations)
        """
        desired = vector2(0, 0)
        if food is None:
            # If the object is not seekin any food slow down until full stop
            desired = vector2.mul(self.velocity, -1)
        else:
            desired = vector2.sub(food.position, self.position)
            desired = vector2.set_magnitude(desired, self.max_speed)
        steering = vector2.sub(desired, self.velocity)
        steering = vector2.limit(steering, self.max_steering)
        self.velocity = vector2.add(self.velocity, steering)
        self.velocity = vector2.limit(self.velocity, self.max_speed)

    def throw_events(self, timing_factor, nearest_food):
        """
        This function throws events to interact with the environment
        """
        # Throw a death event to remove this blob from the simulation
        if self.health <= 0:
            print(self.health)
            death_event = pygame.event.Event(BLOB_DEATH_EVENT, blob=self)
            pygame.event.post(death_event)

        # Throw a reproduction event to add a new related blob
        if random() < self.health * calculate_reproduction_chance(self.size):
            if self.is_adult:
                repr_event = pygame.event.Event(BLOB_REPRODUCTION_EVENT, blob=self)
                pygame.event.post(repr_event)

        # Throw a ate event to remove the food from the environment
        if nearest_food is not None:
            if vector2.abs(vector2.sub(self.position, nearest_food.position)) < self.size:
                self.is_adult = True
                ate_event = pygame.event.Event(BLOB_ATE_EVENT, blob=self, food=nearest_food)
                pygame.event.post(ate_event)

    def update(self, foods, timing_factor):
        """
        This function will be invoked on every frame and takes care of the
        whole blob behaviour
        """
        nearest_food = None
        if self.health <= self.health_threshold:
            # Find the newest eatable piece of food
            smallest_distance = math.inf
            for food in foods:
                distance_to_food = vector2.abs(vector2.sub(food.position, self.position))
                if distance_to_food < smallest_distance and food.size < self.size:
                    smallest_distance = distance_to_food
                    nearest_food = food
        # Seek the nearest food
        self.seek(nearest_food)
        # Move
        self.position = vector2.add(self.position,
        vector2.mul(self.velocity, timing_factor))
        # Decrease health by momevement speed
        relative_speed = vector2.abs(self.velocity) / self.max_speed
        self.health -= self.hdbm * relative_speed * timing_factor
        # Decrease health over time
        self.health -= self.hdot * timing_factor
        self.throw_events(timing_factor, nearest_food)
        # Update health font surface
        self.health_surface = FONT.render(str(self.health), False, (255, 255, 255))

    def draw(self, screen):
        """
        Render the blob and health surface.
        """
        pygame.draw.circle(screen, (255, 0, 0),
                self.position.as_int_tupel(), self.size, self.size // 10)
        screen.blit(self.health_surface, (self.position.x, self.position.y))
