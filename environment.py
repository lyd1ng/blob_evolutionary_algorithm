from math import e

# Environmant Constants for blobs
BLOB_MAX_SIZE = 100
BLOB_MIN_SIZE = 10
BLOB_MIN_SPEED = 0
BLOB_MAX_SPEED = 1000
BLOB_MIN_STEERING = 0
BLOB_MAX_STEERING = 100
BLOB_MIN_HDOT = 0
BLOB_MAX_HDOT = 0.2
BLOB_MIN_HDBM = 0
BLOB_MAX_HDBM = 0.25
BLOB_REPRODUCTION_RATE = 0.2
BLOB_MUTATION_RATE = 1
BLOB_MUTATION_DECREASE_OVER_TIME = 1.001
BLOB_SIZE_MUTATION_STRENGTH = 5
BLOB_HT_MUTATION_STRENGTH = 0.4

# Environment Constants for food
FOOD_MAX_SIZE = 50


def get_relative_size(size):
    return size / BLOB_MAX_SIZE


def calculate_max_speed(size):
    x = get_relative_size(size)
    T = 3
    return BLOB_MAX_SPEED * e**(-x * T) + BLOB_MIN_SPEED


def calculate_max_steering(size):
    x = get_relative_size(size)
    T = 9
    return BLOB_MAX_STEERING * e**(-x * T) + BLOB_MIN_STEERING


def calculate_hdot(size):
    x = get_relative_size(size)
    T = 1
    return BLOB_MAX_HDOT * e**(-x * T) + BLOB_MIN_HDOT


def calculate_hdbm(size):
    x = get_relative_size(size)
    T = 20
    return BLOB_MAX_HDBM - (BLOB_MAX_HDBM * e**(-x * T) + BLOB_MIN_HDBM)


def calculate_reproduction_chance(size):
    x = 1 - get_relative_size(size)
    T = 6
    return BLOB_REPRODUCTION_RATE * e**(-x * T)
