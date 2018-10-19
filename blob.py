import math
import pygame
from random import random
from vector import vector2
from environment import calculate_max_speed
from environment import calculate_max_steering
from environment import calculate_hdot
from environment import calculate_hdbm
from environment import calculate_reproduction_chance


# This event will signal a death of a blob and trigger a creation
# of food at the same position
BLOB_DEATH_EVENT = pygame.USEREVENT + 2
# This event will trigger a creation of a new blob with similar dna
# the dna will be mutated and added as an event attribute
BLOB_REPRODUCTION_EVENT = pygame.USEREVENT + 3
# This event will thrown if a blob ate a piece of food
BLOB_ATE_EVENT = pygame.USEREVENT + 4

# A font to render blob health
FONT = None


def blob_init():
    global FONT
    FONT = pygame.font.SysFont("DejaVuSansMono", 15)


class blob:
    def __init__(self, position, dna, health=1):
        self.position = position
        self.velocity = vector2(0, 0)
        self.health = health
        self.dna = dna
        self.size = dna[0]
        self.health_threshold = dna[1]
        self.max_speed = calculate_max_speed(self.size)
        self.max_steering = calculate_max_steering(self.size)
        self.hdot = calculate_hdot(self.size)
        self.hdbm = calculate_hdbm(self.size)
        self.is_adult = False
        self.health_surface = FONT.render(str(self.health), False, (255, 255, 255))

    def seek(self, food):
        desired = vector2(0, 0)
        if food is None:
            desired = vector2.mul(self.velocity, -1)
        else:
            desired = vector2.sub(food.position, self.position)
            desired = vector2.set_magnitude(desired, self.max_speed)
        steering = vector2.sub(desired, self.velocity)
        steering = vector2.limit(steering, self.max_steering)
        self.velocity = vector2.add(self.velocity, steering)
        self.velocity = vector2.limit(self.velocity, self.max_speed)

    # Create events on death or reproduction
    def throw_events(self, timing_factor, nearest_food):
        if self.health <= 0:
            print(self.health)
            death_event = pygame.event.Event(BLOB_DEATH_EVENT, blob=self)
            pygame.event.post(death_event)

        if random() < self.health * calculate_reproduction_chance(self.size):
            if self.is_adult:
                repr_event = pygame.event.Event(BLOB_REPRODUCTION_EVENT, blob=self)
                pygame.event.post(repr_event)

        if nearest_food is not None:
            if vector2.abs(vector2.sub(self.position, nearest_food.position)) < self.size:
                self.is_adult = True
                ate_event = pygame.event.Event(BLOB_ATE_EVENT, blob=self, food=nearest_food)
                pygame.event.post(ate_event)

    def update(self, foods, timing_factor):
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
        pygame.draw.circle(screen, (255, 0, 0),
                self.position.as_int_tupel(), self.size, self.size // 10)
        screen.blit(self.health_surface, (self.position.x, self.position.y))
