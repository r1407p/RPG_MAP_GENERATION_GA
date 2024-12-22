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
            def bfs(x, y, tile):
                stack = [(x, y)]
                reward = 0

                while stack:
                    cx, cy = stack.pop()

                    if cx < 0 or cx >= self.width or cy < 0 or cy >= self.height or temp_map[cy][cx] == 'x':
                        continue
                    if temp_map[cy][cx] != tile:
                        continue

                    temp_map[cy][cx] = 'x'  # Mark as visited
                    reward += 1

                    # Add neighbors to the stack
                    stack.append((cx + 1, cy))
                    stack.append((cx - 1, cy))
                    stack.append((cx, cy + 1))
                    stack.append((cx, cy - 1))

                if tile == '1':
                    reward /= 2
                return reward

            connections = []
            for x in range(self.width):
                for y in range(self.height):
                    if temp_map[y][x] != 'x':
                        connections.append(bfs(x, y, temp_map[y][x]))
            return connections
        connections_num = connections(map_data)
        connections_scores = [x ** 1.5 for x in connections_num]

        score = sum(connections_scores)

        penalties = 0
        nearby_tiles = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        corner_tiles = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        """
        0: mountain
        1: river
        2: grass
        3: rock
        4: riverstone
        desirce seperation:, mountain, rock, grass, river, riverstone
        """
        penalties_weight = [
            [0, 4, 2, 1, 3],
            [4, 0, 2, 3, 1],
            [2, 2, 0, 1, 1],
            [1, 3, 1, 0, 2],
            [3, 1, 1, 2, 0],
        ]
        for x in range(self.width):
            for y in range(self.height):
                for dx, dy in nearby_tiles:
                    if x + dx >= 0 and x + dx < self.width and y + dy >= 0 and y + dy < self.height:
                        x1, y1 = x, y
                        x2, y2 = x + dx, y + dy
                        tile1 = int(map_data[y1][x1])
                        tile2 = int(map_data[y2][x2])
                        penalties -= 2 * penalties_weight[tile1][tile2]**3

                for dx, dy in corner_tiles:
                    if x + dx >= 0 and x + dx < self.width and y + dy >= 0 and y + dy < self.height:
                        x1, y1 = x, y
                        x2, y2 = x + dx, y + dy
                        tile1 = int(map_data[y1][x1])
                        tile2 = int(map_data[y2][x2])
                        penalties -= penalties_weight[tile1][tile2]**3

                center_x = self.width // 2
                center_y = self.height // 2
                center_tile = int(map_data[center_y][center_x])
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

                tile = int(map_data[y][x])
                
                if tile == center_tile and distance < min(self.width, self.height) / 10:
                    score += 1000

        score += penalties
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
            # mutation_rate = self.init_mutation_rate * (1 - generation / self.generations) # linearly decrease the mutation rate
            max_mutation_rate = self.init_mutation_rate
            min_mutation_rate = self.init_mutation_rate / 10
            mutation_rate = max_mutation_rate - (max_mutation_rate - min_mutation_rate) * generation / self.generations

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


