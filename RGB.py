from math import sqrt
import random


class RGB:

    # generate random rgb color from existing colors
    @staticmethod
    def generate_color(colors):
        # r = random.randint(0, 255)
        # g = random.randint(0, 255)
        # b = random.randint(0, 255)
        i = random.randint(0, len(colors) - 1)
        rgb = colors[i]
        return rgb

    # compare rgb, smaller D - more accurate color
    @staticmethod
    def compare_rgb(original, current):
        r = abs(original[0] - current[0])
        g = abs(original[1] - current[1])
        b = abs(original[2] - current[2])
        score = (sqrt(r ** 2 + g ** 2) + sqrt(g ** 2 + b ** 2) + sqrt(b ** 2 + r ** 2)) / 3
        return score.real
