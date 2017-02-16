class Player():

    def __init__(self, name):
        self.__name = name

    def read_position(self):
        position = input('{}, where to shoot? '.format(self.__name))
        while not (position[0].isalpha() and position[1].isnumeric()
                   and 'A' <= position[0].upper() <= 'J' and 1 <= int(position[1]) <= 10):
            position = input('Enter valid coordinates (e.g. \'D3\') ')
        position = position.upper()
        position = (int(position[1]) - 1, ord(position[0]) - ord('A'))
        return position

    def win(self):
        print('{} WINS!!!'.format(self.__name))


class Field():

    def __init__(self):
        self.__ships = Field.__generate_field()
        self.__hit = set()

    @staticmethod
    def __generate_field():

        from random import randint

        def adj_tiles(ship):
            '''
            Generates the adjacent tiles of the tiles from the list.
            '''
            for tile in ship:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if tile[0] + i < 0 or tile[1] + j < 0 \
                                or tile[0] + i > 9 or tile[1] + j > 9:
                            continue
                        yield (tile[0] + i, tile[1] + j)

        field = []
        for i in range(10):
            field += [[]]
            for j in range(10):
                field[i] += [Ship(0)]
        for length in range(4, 0, -1):
            for count in range(5 - length):
                while True:
                    i = randint(0, 9)
                    j = randint(0, 9)
                    dir = randint(1, 2)
                    tiles = []
                    if dir == 1:
                        horizontal = False
                        for x in range(length):
                            tiles.append((i + x, j))
                        if tiles[-1][0] > 9:
                            continue
                    else:
                        horizontal = True
                        for x in range(length):
                            tiles.append((i, j + x))
                        if tiles[-1][1] > 9:
                            continue
                    for tile in adj_tiles(tiles):
                        if len(field[tile[0]][tile[1]]) > 0:
                            break
                    else:
                        break
                sh = Ship(length)
                sh.horizontal = horizontal
                sh.bow = (i, j)
                for tile in tiles:
                    field[tile[0]][tile[1]] = sh
        return field

    def shoot_at(self, tile):
        if len(self.__ships[tile[0]][tile[1]]) > 0:
            hit = self.__ships[tile[0]][tile[1]].shoot_at(tile)
            self.__hit.add((tile, True))
            if hit:
                return 'destroyed'
            return True
        else:
            self.__hit.add((tile, False))
            return False

    def field_without_ships(self):
        #field = '  1 2 3 4 5 6 7 8 9 10'
        field = ''
        for i in range(10):
         #   field += '\n' + chr(i + ord('A')) + ' '
            for j in range(10):
                if ((i, j), True) in self.__hit:
                    field += 'X'
                elif ((i, j), False) in self.__hit:
                    field += '0'
                else:
                    field += ' '
            field += '\n'
        return field

    def field_with_ships(self):
        #field = '  1 2 3 4 5 6 7 8 9 10'
        field = ''
        for i in range(10):
         #   field += '\n' + chr(i + ord('A')) + ' '
            for j in range(10):
                if ((i, j), True) in self.__hit:
                    field += 'X'
                elif len(self.__ships[i][j]) > 0:
                    field += '*'
                elif ((i, j), False) in self.__hit:
                    field += '0'
                else:
                    field += ' '
            field += '\n'
        return field


class Game():

    def __init__(self):
        self.__field = [Field(), Field()]
        name1 = input('Enter the name of the first player: ')
        name2 = input('Enter the name of the second player: ')
        self.__players = [Player(name1), Player(name2)]
        self.__current_player = 0
        self.__destroyed = [0, 0]

    def field_with_ships(self, player):
        return self.__field[player].field_with_ships()

    def field_without_ships(self, player):
        return self.__field[player].field_without_ships()

    def read_position(self, player):
        return self.__players[player].read_position()

    def play(self):
        while self.__destroyed[1 - self.__current_player] != 10:
            print(self.field_with_ships(self.__current_player),
                  self.field_without_ships(1 - self.__current_player), sep='\n\n')
            hit = self.__field[self.__current_player].shoot_at(self.read_position(self.__current_player))
            if hit:
                print('BOOM! Nice shot!')
            elif hit == 'destroyed':
                print('Wheee! Enemy ship destroyed!')
                self.__destroyed[1 - self.__current_player] += 1
            else:
                print('Sorry! Good luck next time! :(')
                self.__current_player = 1 - self.__current_player
        self.__players[self.__current_player].win()



class Ship():

    def __init__(self, length):
        self.__length = length
        self.horizontal = True
        self.bow = (0, 0)
        self.__hit = [False] * length

    def __len__(self):
        return self.__length

    def shoot_at(self, tile):
        start = self.bow
        if self.horizontal:
            for i in range(self.__length):
                if tile == (start[0], start[1] + i):
                    self.__hit[i] = True
                    break
        else:
            for i in range(self.__length):
                if tile == (start[0] + i, start[1]):
                    self.__hit[i] = True
                    break
        for tile in self.__hit:
            if tile == True:
                break
        else:
            return True
