import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface,rect):
        surface.blit(self.map_surface, rect)

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            # print(len(row))
            for tile in row:
                # if tile == '0':
                #     self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                # el
                if tile == '0':
                    tiles.append(Tile('Tile_01.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '1':
                    tiles.append(Tile('Tile_02.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('Tile_03.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '3':
                    tiles.append(Tile('Tile_04.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('Tile_05.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('Tile_06.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '6':
                    tiles.append(Tile('Tile_07.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '7':
                    tiles.append(Tile('Tile_08.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '8':
                    tiles.append(Tile('Tile_09.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile != '-1': 
                    tiles.append(Tile(str('Tile_'+str(int(tile)+1)+'.png'), x * self.tile_size, y * self.tile_size, self.spritesheet))
                    # Move to next tile in current row
                # print(x)
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        print(x)
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
