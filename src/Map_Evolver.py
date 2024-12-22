from src.RPGMAP import RPGMAP
from src.utils import MAP_WIDTH, MAP_HEIGHT, IMAGES
from tqdm import tqdm
import random

class MapEvolver(object):
    def __init__(self, width, height, 
                 population_size, generations, 
                 mutation_rate, selection_size):
        self.width = width
        self.height = height
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.selection_size = selection_size
        self.tiles = list(IMAGES.keys())

        self.population = [RPGMAP(width, height) for _ in range(population_size)]
        self.fitness = [None for _ in range(population_size)]

    def evaluate_fitness(self):
        pass

    def mutate(self, map: RPGMAP):
        mutated_map = map.getmap().copy()
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < self.mutation_rate:
                    mutated_map[y][x] = random.choice(list(IMAGES.keys()))
        return RPGMAP(self.width, self.height, mutated_map)

    def crossover(self, map1, map2):
        pass
    
    def evolve(self):
        pass

    def selection(self):
        """
        using tournament selection
        """
        samples_idx = random.sample(range(self.population_size), self.selection_size)
        best_idx = max(samples_idx, key=lambda x: self.fitness[x])
        return self.population[best_idx]

    def get_best_map(self):
        best_fitness_index = self.fitness.index(max(self.fitness))
        return self.population[best_fitness_index]


