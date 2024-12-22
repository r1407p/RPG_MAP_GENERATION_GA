from src.Map_Evolver import MapEvolver
from src.RPGMAP import RPGMAP
import os 
from src.utils import MAP_WIDTH, MAP_HEIGHT, POPULATION_SIZE, GENERATIONS, MUTATION_RATE, SELECTION_SIZE
from src.utils import GENERATIONS

def main():
    output_dir = f'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(10):
        print(f"Start generating map {i+1}")
        map_evolver = MapEvolver(MAP_WIDTH, MAP_HEIGHT, POPULATION_SIZE, GENERATIONS, MUTATION_RATE, SELECTION_SIZE)
        best_map = map_evolver.evolve()
        best_map.store_map_image(os.path.join(output_dir, f'map_{i}.png'))
        print(f"Map {i+1} generated")

if __name__ == "__main__":
    main()