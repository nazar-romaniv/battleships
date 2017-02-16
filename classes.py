class Player():

    def __init__(self, name):
        self.name = name

    def read_position(self):
        position = input('Where to shoot? ')
        while not (position[0].isalpha() and 'A' <= position[0].upper() <= 'J' \
                           and position[1].isnumeric() and 1 <= position[1] <= 10):
            position = input('Enter valid coordinates (e.g. \'D6\'')
        position = position.upper()
        position = (int(position[1]), ord(position[0]) - ord('A'))
        self.position = position
        return None
