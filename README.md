# Map Evolver

## Overview
This project generates RPG-style maps using a genetic algorithm. The maps are evolved over several generations to optimize specific fitness criteria, such as tile connections, penalties for undesirable neighboring tiles, and central features.

## Features
- Generates maps using a genetic algorithm.
- Evaluates map fitness based on tile connections and penalties for undesirable tile arrangements.
- Supports mutation and crossover operations for generating new map populations.
- Saves generated maps as image files.
- Allows customization of algorithm parameters like mutation rate, population size, and number of generations.

## Requirements
- Python 3.x
- Required libraries:
  - `pygame`
  - `tqdm`

Install the dependencies using:
```bash
pip install pygame tqdm
```
# Usage
## Running the Script
To generate maps, run the main script:
```
python main.py
```
This will generate 10 maps and save them in the output/ directory.

### Customization
Modify the following parameters in src/utils.py to customize the map generation:

# Example configuration
MAP_WIDTH = 40
MAP_HEIGHT = 40
POPULATION_SIZE = 200
GENERATIONS = 200
MUTATION_RATE = 0.1
SELECTION_SIZE = 3

# Outputs
Generated maps are saved as .png files in the output/ directory. Intermediate maps are saved every 50 generations for progress tracking.

# Code Structure
- main.py: Entry point for the program. Initializes the MapEvolver and saves the best maps.
- src/Map_Evolver.py: Implements the genetic algorithm for evolving maps.
- src/RPGMAP.py: Represents individual maps and provides utilities for rendering and saving them.
- src/utils.py: Contains constants and configuration parameters.
# Fitness Function
The fitness function evaluates maps based on:

- Connections: Groups of connected tiles are rewarded, with higher scores for larger groups.
- Penalties: Negative scores are assigned for undesirable neighboring tiles based on a penalty weight matrix.
- Central Features: Bonus points are awarded for specific tiles located near the map's center.