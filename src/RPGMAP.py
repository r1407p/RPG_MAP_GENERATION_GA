import pygame
from src.utils import TILE_SIZE, IMAGES

class RPGMAP(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[str(0) for x in range(width)] for y in range(height)]
        self.objects = []

    def setmap(self, map):
        self.map = map
    
    def getmap(self):
        return self.map
    
    def generate_map_image(self):
        

        map_image = pygame.Surface((self.width * TILE_SIZE, self.height * TILE_SIZE))

        for y in range(self.height):
            for x in range(self.width):
                image = IMAGES[self.map[y][x]]
                map_image.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

        return map_image

    def store_map_image(self, path):
        map_image = self.generate_map_image()
        pygame.image.save(map_image, path)
        
        
if __name__ == "__main__":
    from src.utils import MAP_WIDTH, MAP_HEIGHT

    rpg_map = RPGMAP(MAP_WIDTH, MAP_HEIGHT)
    default_map_path = 'data/default.map'

    with open(default_map_path, 'r') as f:
        raw_map = f.readlines()

    map_ = []
    for line in raw_map:
        map_.append([x for x in line.strip()])

    rpg_map.setmap(map_)
    
    print(rpg_map.generate_map_image())
    rpg_map.store_map_image('data/default.png')