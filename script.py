from copy import deepcopy
from random import randint

tile_convert = lambda tile: (ord(tile[0]) - ord('a'), tile[1] - 1)


def read_field(filename: str) -> list:
    '''
    str -> list(list(chr))
    Reads the field from filename and outputs a list of lists of characters, which represent the
    tiles of the field (' ' is an empty tile; '*' is a ship tile; 'X' is a destroyed ship tile).
    '''
    field = []
    for i in range(10):
        field += [[''] * 10]
    with open(filename) as file:
        lines = file.readlines()
        for i in range(10):
            for j in range(10):
                field[i][j] = lines[i][j]
        return field


def has_ship(field, tile):
    '''
    list(list(chr)), (chr, int) -> bool
    Returns True if the tile is a ship tile.
    '''
    tile = tile_convert(tile)
    try:
        if field[tile[0]][tile[1]] == '*':
            return True
        else:
            return False
    except IndexError:
        return False


def ship_size(field, tile):
    '''
    list(list(chr)), (chr, int) -> int, list((chr, int))
    Returns the size of the ship with the leftmost or topmost tile
    and the list of the coordinates of all tiles.

    Precondition: the leftmost or topmost tile of the ship must be selected.
    '''
    tile = tile_convert(tile)
    ship = [tile]
    if has_ship(field, (tile[0], tile[1] + 1)):
        size = 2
        tile = (tile[0], tile[1] + 1)
        ship.append(tile)
        dir = 0
    elif has_ship(field, (tile[0] + 1, tile[1])):
        size = 2
        tile = (tile[0] + 1, tile[1])
        ship.append(tile)
        dir = 1
    else:
        size = 1
    if size == 2:
        while True:
            if dir == 0:
                check_tile = (tile[0], tile[1] + 1)
            elif dir == 1:
                check_tile = (tile[0] + 1, tile[1])
            if has_ship(field, check_tile):
                ship.append(check_tile)
                tile = check_tile
                size += 1
            else:
                break
    return size, ship


def is_valid(field):
    '''
    list(list(chr)) -> bool
    Checks if a starting field is valid.
    '''
    ship_count = [0, 0, 0, 0]
    new_field = deepcopy(field)
    for i in range(10):
        for j in range(10):
            if new_field[i][j] == 'X':
                continue
            if new_field[i][j] == '*':
                ship = ship_size(new_field, (i, j))
                ship_count[ship[0] - 1] += 1
                for tile in adj_tiles(ship):
                    if (tile not in ship[1]) \
                        and (new_field[tile[0]][tile[1]] == '*'):
                        print(ship)
                        print(tile)
                        return False
                    new_field[tile[0]][tile[1]] = 'X'
    if ship_count == [4, 3, 2, 1]:
        return True
    else:
        return False


def adj_tiles(ship):
    '''
    Generates the adjacent tiles of the tiles from the list.
    '''
    for tile in ship[1]:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if tile[0] + i < 0 or tile[1] + j < 0 \
                   or tile[0] + i > 9 or tile[1] + j > 9:
                    continue
                yield (tile[0] + i, tile[1] + j)


def field_to_str(field):
    '''
    Converts a field to a list of strings.
    '''
    lines = []
    for i in range(10):
        line = ''
        for j in range(10):
            line += field[i][j]
        line += '\n'
        lines.append(line)
    return lines


def generate_field():
    '''
    Generates a random game field.
    '''
    field = []
    for i in range(10):
        field += [[' '] * 10]
    for length in range(4, 0, -1):
        print(length)
        for count in range(5 - length):
            print(count)
            while True:
                i = randint(0, 9)
                j = randint(0, 9)
                dir = randint(1, 2)
                tiles = []
                if dir == 1:
                    for x in range(length):
                        tiles.append((i + x, j))
                    if tiles[-1][0] > 9:
                        continue
                else:
                    for x in range(length):
                        tiles.append((i, j + x))
                    if tiles[-1][1] > 9:
                        continue
                ship = (length, tiles)
                for tile in adj_tiles(ship):
                    if field[tile[0]][tile[1]] == '*':
                        break
                else:
                    print(ship)
                    break
            for tile in ship[1]:
                print(tile)
                field[tile[0]][tile[1]] = '*'
    return field
