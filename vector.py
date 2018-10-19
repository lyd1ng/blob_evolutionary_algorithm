import math


class vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_int_tupel(self):
        return (int(self.x), int(self.y))

    @staticmethod
    def add(v1, v2):
        return vector2(v1.x + v2.x, v1.y + v2.y)

    @staticmethod
    def sub(v1, v2):
        return vector2(v1.x - v2.x, v1.y - v2.y)

    @staticmethod
    def div(v1, f):
        return vector2(v1.x / f, v1.y / f)

    @staticmethod
    def mul(v1, f):
        return vector2(v1.x * f, v1.y * f)

    @staticmethod
    def normalize(v1):
        length = math.sqrt(v1.x**2 + v1.y**2)
        return vector2(v1.x / length, v1.y / length)

    @staticmethod
    def set_magnitude(v1, magnitude):
        norm_v1 = vector2.normalize(v1)
        return vector2.mul(norm_v1, magnitude)

    @staticmethod
    def limit(v1, magnitude):
        if (vector2.abs(v1) > magnitude):
            return vector2.set_magnitude(v1, magnitude)
        return v1

    @staticmethod
    def abs(v1):
        return math.sqrt(v1.x**2 + v1.y**2)

    @staticmethod
    def polar(r, alpha):
        return vector2(r*math.cos(alpha), r*math.sin(alpha))

