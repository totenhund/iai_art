import numpy as np
import random
from RGB import RGB
from PIL import Image, ImageDraw
from shape import Shape
import colorsys


# Genetic algorithm
# 1) Choose standard reference
# 2) Create initial population
# 3) Calculate fitness score
# 4) Choose best parents based on fitness score
# 5) Produce child from parents (crossover)
# 6) Random mutation of genes
# 7) Loop until it will produce desirable result

class TrueArt:

    def __init__(self):
        self.width = 512
        self.height = 512
        self.art = Image.new('RGB', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.art)
        self.original = None
        self.pop_size = 100
        self.mut_chance = 0.6
        self.population = []
        self.best_score = 100000000
        self.best_gen = []
        self.pix = []
        self.aim_genes = []
        self.color = []

    # Reference standard
    def create_reference(self):
        input_img = Image.open('3.jpg')
        self.original = input_img.resize((512, 512), Image.ANTIALIAS)
        self.pix = self.original.load()

        for i in range(int(self.width / 2)):
            chromosome = []
            for j in range(int(self.height / 2)):
                chromosome.append(self.pix[2 * j, 2 * i])
            self.aim_genes.append(chromosome)

        for i in range(self.width):
            for j in range(self.height):
                self.color.append(self.pix[j, i])

    # create dna
    def create_dna(self):
        dna = []
        w = 0
        h = 0
        for i in range(int(self.width / 2)):
            chromosome = []
            for j in range(int(self.height / 2)):
                points = [(w, h + 4), (w, h), (w + 4, h + 4)]
                rgb = RGB.generate_color(self.color)
                shape = Shape(rgb, points)
                chromosome.append(shape)
                w += 2
            dna.append(chromosome)
            w = 0
            h += 2
        return dna

    # create population
    def create_population(self):
        for i in range(self.pop_size):
            self.population.append(self.create_dna())

    # Compare with the original population genes with reference standard genes
    def calc_fitness(self, population):
        score = 0
        for i in range(len(population)):
            for j in range(len(population[i])):
                score += RGB.compare_rgb(self.aim_genes[i][j], population[i][j].color)
        return score

    # Choose parent with best fitness score for crossover
    def select_dna(self):
        fighter1 = self.population[random.randint(0, self.pop_size - 1)]
        fighter2 = self.population[random.randint(0, self.pop_size - 1)]

        score1 = self.calc_fitness(fighter1)
        score2 = self.calc_fitness(fighter2)

        if score1 < score2:
            return fighter1
        else:
            return fighter2

    # Create children from best populations
    def breed_crossover(self):
        parent1 = self.select_dna()
        parent2 = self.select_dna()
        child = parent2

        for i in range(int(self.width / 2)):
            for j in range(int(self.height / 2)):
                if RGB.compare_rgb(self.aim_genes[i][j], parent1[i][j].color) < 45:
                    child[i][j].color = parent1[i][j].color
                self.random_mutation(child)
        return child

    # Perform mutation
    def random_mutation(self, child):
        chances = []
        times = 10 * self.mut_chance
        for i in range(10):
            if i < times:
                chances.append(1)
            else:
                chances.append(i)
        j = random.randint(0, 9)

        if chances[j] == 1:
            for i in range(20):
                pixel = random.randint(0, int(self.width / 2) - 1)
                child[pixel][pixel].color = self.aim_genes[pixel][pixel]

    # Iterate generations
    def produce_generations(self):
        for i in range(100):
            gen = self.breed_crossover()
            score = self.calc_fitness(gen)
            if score < self.best_score:
                self.best_gen = gen
                self.best_score = score
                print(score)

    # Produce IAI art
    def draw_art(self):
        self.produce_generations()
        canvas = Image.new('HSV', (self.width, self.height), color=(30, 25, 100))
        result = self.best_gen
        for i in range(self.width // 2 - 1):
            for j in range(self.height // 2 - 1):
                paint = ImageDraw.Draw(canvas)
                points = result[i][j].coords
                color = result[i][j].color
                hsv = colorsys.rgb_to_hsv(color[0] / 255, color[1] / 255, color[2] / 255)
                hsv_int = []
                for el in list(hsv):
                    hsv_int.append(int(el * 100))

                paint.polygon(((points[0]), (points[1]), (points[2])), fill=tuple(hsv_int))

        canvas = canvas.convert('RGB')
        canvas.save('2.png')


# creation of class instance
if __name__ == '__main__':
    art = TrueArt()
    art.create_reference()
    art.create_population()
    art.draw_art()
