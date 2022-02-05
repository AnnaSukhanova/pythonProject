class SeaMap:
    def __init__(self):
        self.x = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        self.map = [self.x for i in range(10)]

    def shoot(self, row, col, result):
        if result == 'miss':
            self.map[row][col] = '*'
        elif result == 'hit':
            self.map[row][col] = 'X'
        elif result == 'sink':
            allcoor = list(filter(lambda x: 0 <= x[0] <= 9 and 0 <= x[1] <= 9,
                                  [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1], [row, col + 1],
                                   [row + 1, col + 1], [row + 1, col], [row + 1, col - 1], [row, col - 1]]))
            for i in allcoor:
                if self.map[i[0]][i[1]] == '.':
                    self.map[i[0]][i[1]] = '*'
            self.map[row][col] = 'X'

    def cell(self, row, col):
        return self.map[row][col]


sm = SeaMap()
sm.shoot(2, 0, 'sink')
sm.shoot(6, 9, 'hit')
for row in range(10):
    for col in range(10):
        print(sm.cell(row, col), end='')
    print()
