import random


class VariationEngine:

    def __init__(self, seed=None):

        self.random = random.Random(seed)

    def vary(self, target, variation):

        minimum = max(0.0, target - variation)
        maximum = min(1.0, target + variation)

        return round(
            self.random.uniform(minimum, maximum),
            3,
        )

    def generate(self, dna):

        return {

            "softness": self.vary(*dna.softness),
            "contrast": self.vary(*dna.contrast),
            "rhythm": self.vary(*dna.rhythm),
            "geometry": self.vary(*dna.geometry),
            "elegance": self.vary(*dna.elegance),

        }