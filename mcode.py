from random import randint

class GamePole:
    POLE = None
    def __new__(cls, *args, **kwargs):
        if cls.POLE is None:
            cls.POLE = super().__new__(cls)
        return cls.POLE
        
    def __init__(self, n, m, total_mines):
        self.n = n 
        self.m = m
        self.total_mines = total_mines

        self.__pole_cells = [[Cell() for j in range(n)] for i in range(m)]
    @property
    def pole(self):
        return self.__pole_cells
    
    def init_pole(self):
        indx = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        mines = self.total_mines
        while mines > 0:
            indx1 = randint(0, self.m-1)
            indx2 = randint(0, self.n-1)
            if not self.pole[indx1][indx2].is_mine:          # если нет мины ставим 
                self.pole[indx1][indx2].is_mine = True
            mines -= 1
        
        for i in range(self.m):
            for j in range(self.n):
                if not self.pole[i][j].is_mine:
                    count = sum([1 if self.pole[i+x][j+y].is_mine else 0 for x, y in indx if 0<= i+x < self.m and 0 <= j+y < self.n]) 
                    self.pole[i][j].number = count
        # сделать мины для поля!
    
    def open_cell(self, i, j):
        if 0 <= i < self.m and 0 <= j < self.n:
            self.pole[i][j].is_open = True
            return
        raise IndexError('некорректные индексы i, j клетки игрового поля')

    def show_pole(self):
        for stroka in self.pole:
            for mine in stroka:
                if mine.is_open:
                    print('B', end=' ') if mine.is_mine else print(mine.number, end=' ')
                else:
                    print('#', end=' ')
            print()
                

class DesCell:
    def __set_name__(self, owner, name):
        self.name = '__' + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.name == '__number':
            if 0 <= value <= 8:
                instance.__dict__[self.name] = value
            else:
                raise ValueError("недопустимое значение атрибута")
        if self.name in ['__is_mine', '__is_open']:
            if not(isinstance(value, bool)):
                raise ValueError("недопустимое значение атрибута")
            instance.__dict__[self.name] = value
        

class Cell:
    is_mine = DesCell()
    number = DesCell()
    is_open = DesCell()
    def __init__(self):
        self.is_mine = False
        self.number = 0
        self.is_open = False
    
    def __bool__(self):
        return not(self.is_open)

pole = GamePole(4, 4, 2)
pole.init_pole()
pole.show_pole()
