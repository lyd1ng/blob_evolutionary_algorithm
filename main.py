import pygame
import random
from math import e as E
from blob import blob
from blob import blob_init
from blob import BLOB_DEATH_EVENT
from blob import BLOB_REPRODUCTION_EVENT
from blob import BLOB_ATE_EVENT
from food import food
from vector import vector2
from environment import BLOB_MUTATION_RATE
from environment import BLOB_MUTATION_DECREASE_OVER_TIME
from environment import BLOB_MIN_SIZE
from environment import BLOB_MAX_SIZE
from environment import BLOB_SIZE_MUTATION_STRENGTH
from environment import BLOB_HT_MUTATION_STRENGTH
from environment import FOOD_MAX_SIZE

"""
Events to controll the environment
"""
FEED_EVENT = pygame.USEREVENT + 0
MUTATION_DECREASE_EVENT = pygame.USEREVENT + 1


# Create a random piece of food
def create_food(foods):
    posx = random.randint(0, maxX)
    posy = random.randint(0, maxY)
    size = FOOD_MAX_SIZE * E**(-random.random() * 2)
    # size = 10
    foods.append(food(vector2(posx, posy), size))


# Create a random blob
def create_blob(blobs):
    posx = random.randint(0, maxX)
    posy = random.randint(0, maxY)
    size = random.randint(BLOB_MIN_SIZE, BLOB_MAX_SIZE)
    threshold = random.random()
    blobs.append(blob(vector2(posx, posy), [size, threshold]))


# Create a blob generation
def create_blob_generation(blobs, amount):
    for i in range(0, amount):
        create_blob(blobs)


if __name__ == "__main__":
    pygame.init()
    blob_init()
    # Font to render environment informations
    font = pygame.font.SysFont("DejaVuSansMono", 20)

    maxX = 1366
    maxY = 768
    """
    Initialise the screen with maxX and maxY as dimension
    and initialise the clock. The clock is used to throw
    environment events.
    """
    screen = pygame.display.set_mode((maxX, maxY))
    clock = pygame.time.Clock()
    running = True

    # Set the feeding timer
    pygame.time.set_timer(FEED_EVENT, 150)

    # Set the second passed timer
    pygame.time.set_timer(MUTATION_DECREASE_EVENT, 1000)

    """
    The blobs and foods arrays containing every object of the ecosystem
    """
    blobs = []
    foods = []
    for i in range(0, 80):
        create_food(foods)
    create_blob_generation(blobs, 10)

    while(running):
        clock.tick(500)
        timing_factor = clock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == FEED_EVENT:
                create_food(foods)
            if event.type == MUTATION_DECREASE_EVENT:
                BLOB_MUTATION_RATE /= BLOB_MUTATION_DECREASE_OVER_TIME
            if event.type == BLOB_DEATH_EVENT:
                blobs.remove(event.blob)
            if event.type == BLOB_ATE_EVENT:
                try:
                    foods.remove(event.food)
                    event.blob.health += event.food.size / event.blob.size
                    if event.blob.health > 1.0:
                        event.blob.health = 1.0
                except(Exception):
                    pass
            if event.type == BLOB_REPRODUCTION_EVENT:
                cloned_dna = event.blob.dna
                if random.random() < BLOB_MUTATION_RATE:
                    cloned_dna[0] += int((1 - random.random() * 2) * BLOB_SIZE_MUTATION_STRENGTH)
                    # Ensure logical borders
                    if cloned_dna[0] < BLOB_MIN_SIZE:
                        cloned_dna[0] = BLOB_MIN_SIZE
                    if cloned_dna[0] > BLOB_MAX_SIZE:
                        cloned_dna[0] = BLOB_MAX_SIZE
                    cloned_dna[1] += (1 - random.random() * 2) * BLOB_HT_MUTATION_STRENGTH
                    # Ensure logical borders
                    if cloned_dna[1] < 0:
                        cloned_dna[1] = 0
                    if cloned_dna[1] > 1:
                        cloned_dna[1] = 1
                # Add the blob with the half of the parent health.
                blobs.append(blob(event.blob.position, cloned_dna, event.blob.health / 2))

        # Update all blobs (no need to update food)
        for b in blobs:
            b.update(foods, timing_factor)

        # Draw
        screen.fill((0, 0, 0))
        for f in foods:
            f.draw(screen)
        for b in blobs:
            b.draw(screen)
        # Render the mutation rate
        info_surface = font.render(str(BLOB_MUTATION_RATE), False, (255, 255, 255))
        screen.blit(info_surface, (10, 10))
        pygame.display.flip()
