import pygame

TILE_SIZE = 64
MAP_WIDTH = 46
MAP_HEIGHT = 46

POPULATION_SIZE = 50
GENERATIONS = 1000
MUTATION_RATE = 0.01

IMAGES_PATH = {
    '0': 'data/mountain.png',
    '1': 'data/river.png',
    '2': 'data/grass.png',
    '3': 'data/rock.png',
    '4': 'data/riverstone.png',
}

IMAGES = {
    '0': pygame.image.load(IMAGES_PATH['0']),
    '1': pygame.image.load(IMAGES_PATH['1']),
    '2': pygame.image.load(IMAGES_PATH['2']),
    '3': pygame.image.load(IMAGES_PATH['3']),
    '4': pygame.image.load(IMAGES_PATH['4']),        
}


