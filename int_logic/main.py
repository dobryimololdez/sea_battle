from random import randint
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class BoardExcptn(Exception):
    pass

class BoardOutException(BoardExcptn):
    def __str__(self):
        return "Выстрел за предел доски"

class ShotSameSlot(BoardExcptn):
    def __str__(self):
        return "Выстрел в клетку куда уже сделан ход"

class WrongShipException(BoardExcptn):
    pass

class Ship:
    def __init__(self, length, front, position, l):
        self.length = length
        self.front = front
        self.position = position
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.front.x
            cur_y = self.front.y

            if self.position == 0:
                cur_x += i
            elif self.position == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, hide=False, size = 6):
        self.size = size
        self.hide = hide

        self.count = 0

        self.field = [["O"] * size for _ in range(size) ]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += " | 1 | 2 | 3 | 4 | 5 | 6 | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hide:
            res = res.replace("1", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, 1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise WrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "6"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise ShotSameSlot()
        self.busy.append(d)

        for ship in self.ships:
            if d in ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        self.field[d.x][d.y] = "."
        print("Мимо")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    def ask(self):
        raise NotImplementedError()
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExcptn as e:
                print(e)

class AI(Player):

    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class Human(Player):

    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) !=2:
                print("Введите 2 координаты! ")
                continue
            x, y = cords
            if not(x.isdigit()) or not(y.isdigit()):
                print("Нужно ввести именно числа! ")
                continue
            x, y = int(x), int(y)
            return Dot(x-1, y-1)

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = Human(pl, co)

    def try_board(self):
        length = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in length:
            while True:
                attempts +=1
                if attempts > 2500:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), randint(0,1), 2, 2)
                try:
                    board.add_ship(Ship)
                    break
                except WrongShipException:
                    pass
        board.begin()
        return board
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("------Приветствие------")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.Human.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-"*20)
            if num / 2 == 0:
                print("Ходит пользователь!")
                repeat = self.Human.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл")
                break
            if self.Human.board.count == 7:
                print("-" * 20)
                print("Комп выиграл")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()




g = Game()
g.start()

