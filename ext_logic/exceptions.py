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





