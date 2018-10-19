from math import e

"""
This file contains the specification and functions describing the environment
Every blob characteristic is an exponential function between the min and max
value of this characteristic for x values in the range of 0 and 1.
The relative size is used as the x value for the exponential functions.
"""

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
    """
    Is used to to calculate the x value for
    the following exponential functions.
    """
    return size / BLOB_MAX_SIZE


def calculate_max_speed(size):
    """
    Calculate the max speed of a blob
    """
    x = get_relative_size(size)
    T = 3
    return BLOB_MAX_SPEED * e**(-x * T) + BLOB_MIN_SPEED


def calculate_max_steering(size):
    """
    Calculate the max steering force of a blob
    """
    x = get_relative_size(size)
    T = 9
    return BLOB_MAX_STEERING * e**(-x * T) + BLOB_MIN_STEERING


def calculate_hdot(size):
    """
    Get the health decrease over time of a blob
    """
    x = get_relative_size(size)
    T = 1
    return BLOB_MAX_HDOT * e**(-x * T) + BLOB_MIN_HDOT


def calculate_hdbm(size):
    """
    Get the health decrease by movement of a blob
    """
    x = get_relative_size(size)
    T = 20
    return BLOB_MAX_HDBM - (BLOB_MAX_HDBM * e**(-x * T) + BLOB_MIN_HDBM)


def calculate_reproduction_chance(size):
    """
    Calculate the reproduction change of a blob
    """
    x = 1 - get_relative_size(size)
    T = 6
    return BLOB_REPRODUCTION_RATE * e**(-x * T)
