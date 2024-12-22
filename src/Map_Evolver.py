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
        """
        Randomly change some tiles in the map, and return the mutated map
        """
        mutated_map = map.getmap().copy()
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < self.mutation_rate:
                    mutated_map[y][x] = random.choice(list(IMAGES.keys()))
        return RPGMAP(self.width, self.height, mutated_map)

    def crossover(self, map1: RPGMAP, map2: RPGMAP):
        """
        for each row in the map, randomly choose a column to break the map into two parts
        """
        
        break_points = [random.randint(0, self.width) for _ in range(self.height)]
        child_map = []
        for y in range(self.height):
            child_map.append(map1.getmap()[y][:break_points[y]] + map2.getmap()[y][break_points[y]:])
        return RPGMAP(self.width, self.height, child_map)

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


