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
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.position == 0:
                cur_x += 1
            elif self.position == 1:
                cur_x += 1
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots



