class HitException(Exception):
    pass


class Player():

    def __init__(self, name):
        self.name = name

    def read_position(self):
        position = input('{}, where to shoot? '.format(self.name))
        while not (position[0].isalpha() and position[1].isnumeric()
                   and 'A' <= position[0].upper() <= 'J' and 1 <= int(position[1:]) <= 10):
            position = input('Enter valid coordinates (e.g. \'D3\') ')
        position = position.upper()
        position = (int(position[1:]) - 1, ord(position[0]) - ord('A'))
        return position


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
                        yield (tile[0] + i, tile[1] + j)

        field = [[Ship(0)] * 10 for i in range(10)]
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
                        try:
                            if len(field[tile[0]][tile[1]]) > 0:
                                break
                        except IndexError:
                            continue
                    else:
                        break
                sh = Ship(length)
                sh.horizontal = horizontal
                sh.bow = (i, j)
                for tile in tiles:
                    field[tile[0]][tile[1]] = sh
        return field

    def shoot_at(self, tile):
        if tile in self.__hit:
            raise HitException('No way')
        hit = self.__ships[tile[0]][tile[1]].shoot_at(tile)
        self.__hit.add(tile)
        return hit

    def field_without_ships(self):
        field = '  A B C D E F G H I J'
        for i in range(10):
            field += '\n' + str(i + 1) + ' ' if i != 9 else '\n' + str(i + 1)
            for j in range(10):
                if (i, j) in self.__hit and len(self.__ships[i][j]) > 0:
                    field += 'X'
                elif (i, j) in self.__hit:
                    field += '0'
                else:
                    field += ' '
                field += ' '
        return field

    def field_with_ships(self):
        field = '  A B C D E F G H I J'
        for i in range(10):
            field += '\n' + str(i + 1) + ' ' if i != 9 else '\n' + str(i + 1)
            for j in range(10):
                if (i, j) in self.__hit and len(self.__ships[i][j]) > 0:
                    field += 'X'
                elif len(self.__ships[i][j]) > 0:
                    field += '*'
                elif (i, j) in self.__hit:
                    field += '0'
                else:
                    field += ' '
                field += ' '
        return field


class Game():

    def __init__(self):
        name1 = input('Enter the name of the first player: ')
        name2 = input('Enter the name of the second player: ')
        print('Press Enter to continue')
        Game.__clear('')
        self.__field = [Field(), Field()]
        self.__players = [Player(name1), Player(name2)]
        self.__destroyed = [0, 0]

    @staticmethod
    def __clear(message):

        import os
        import subprocess
        import platform

        input()
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux':
            if subprocess.getoutput('clear') == 0:
                os.system('clear')
            else:
                print('\n' * 100)
        else:
            if subprocess.getoutput('echo $TERM') != '':
                os.system('clear')
        print(message)

    def field_with_ships(self, player):
        return self.__field[player].field_with_ships()

    def field_without_ships(self, player):
        return self.__field[player].field_without_ships()

    def read_position(self, player):
        return self.__players[player].read_position()

    def play(self):
        current_player = 0
        while self.__destroyed[1 - current_player] != 10:
            try:
                print(self.field_with_ships(current_player),
                      self.field_without_ships(1 - current_player), sep='\n\n')
                hit = self.__field[1 - current_player].shoot_at(self.read_position(current_player))
                if hit == 1:
                    print('Wheee! Enemy ship destroyed!')
                    self.__destroyed[1 - current_player] += 1
                elif hit == 0:
                    print('BOOM! Nice shot!')
                else:
                    print('Sorry! Good luck next time! :(\n')
                    current_player = 1 - current_player
                    Game.__clear('{}\'s turn'.format(self.__players[current_player].name))
                    input('Press Enter when ready')
            except KeyboardInterrupt:
                q = input('Wanna quit? Y/N ')
                if q == 'Y':
                    quit()
                else:
                    continue
            except HitException:
                print('You\'ve shot at this tile already.')
                continue
        print('{} WINS!!!'.format(self.__players[current_player].name))



class Ship():

    def __init__(self, length):
        self.__length = length
        self.__hit = [False] * length
        self.bow = (-1, -1)
        self.horizontal = False

    def __len__(self):
        return self.__length

    def shoot_at(self, tile):
        start = self.bow
        if start == (-1, -1):
            return 2
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
        if self.__hit == [True] * self.__length:
            return 1
        else:
            return 0
