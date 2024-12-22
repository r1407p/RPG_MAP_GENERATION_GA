from src.RPGMAP import RPGMAP
from src.utils import MAP_WIDTH, MAP_HEIGHT, IMAGES
from tqdm import tqdm
import random
from copy import deepcopy
class MapEvolver(object):
    def __init__(self, width, height, 
                 population_size, generations, 
                 mutation_rate, selection_size,
                 elite_rate=0.4):
        self.width = width
        self.height = height
        self.population_size = population_size
        self.generations = generations
        self.init_mutation_rate = mutation_rate
        self.selection_size = selection_size
        self.tiles = list(IMAGES.keys())
        self.elite_rate = elite_rate

        self.population = [RPGMAP(width, height) for _ in range(population_size)]
        self.fitness = [None for _ in range(population_size)]

    def evaluate_fitness(self, map: RPGMAP):
        map_data = map.getmap()
        def connections(map_data):
            temp_map = deepcopy(map_data)
            for x in range(self.width):
                for y in range(self.height):
                    if temp_map[y][x] == '4': # riverstone is considered as river in this case(connection)
                        temp_map[y][x] = '1'
            def dfs(x, y , tile):
                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    return 1
                if temp_map[y][x] != tile:
                    return 0
                temp_map[y][x] = 'x'
                reward = 1 + dfs(x + 1, y, tile) + dfs(x - 1, y, tile) + dfs(x, y + 1, tile) + dfs(x, y - 1, tile)
                if tile == '1':
                    reward /= 2
                return reward

            connections = []
            for x in range(self.width):
                for y in range(self.height):
                    if temp_map[y][x] != 'x':
                        connections.append(dfs(x, y, temp_map[y][x]))
            return connections
        connections_num = connections(map_data)
        connections_scores = [x * x for x in connections_num]

        score = sum(connections_scores)
        return score


    def mutate(self, map: RPGMAP, mtuation_rate: float):
        """
        Randomly change some tiles in the map, and return the mutated map
        """
        mutated_map = map.getmap().copy()
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < mtuation_rate:
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
        for i in range(self.population_size):
            self.fitness[i] = self.evaluate_fitness(self.population[i])

        for generation in tqdm(range(self.generations)):
            mutation_rate = self.init_mutation_rate * (1 - generation / self.generations) # linearly decrease the mutation rate

            new_population = []
            for _ in range(self.population_size):
                parent1 = self.selection()
                parent2 = self.selection()
                child = self.crossover(parent1, parent2)
                child = self.mutate(child, mutation_rate)
                new_population.append(child)

            old_population = self.population
            old_fitness = self.fitness 

            new_population = new_population
            new_fitness = [None for _ in range(self.population_size)]
            
            for i in range(self.population_size):
                new_fitness[i] = self.evaluate_fitness(new_population[i])

            old_population = sorted(zip(old_population, old_fitness), key=lambda x: x[1], reverse=True)
            new_population = sorted(zip(new_population, new_fitness), key=lambda x: x[1], reverse=True)

            population = old_population[:int(self.population_size * self.elite_rate)] + new_population[:int(self.population_size * (1 - self.elite_rate))]
            self.population = [x[0] for x in population]
            self.fitness = [x[1] for x in population]

        return self.get_best_map()

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


