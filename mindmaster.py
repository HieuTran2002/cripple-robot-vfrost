from enum import Enum, auto


class Gamemode(Enum):
    DEFAULT = auto()
    THREESILO = auto()


class mastermind():
    silos_self_count = [0, 0, 0, 0, 0]
    silos_scan = [0] * 5

    def __init__(self, gamemode=Gamemode.DEFAULT):
        self.gameMode = gamemode

    def drop(self, column):
        
        self.silos_self_count[column] += 1
        if len(self.silos_self_count) > 3:
            self.silos_self_count = 3
    def all_ball(self):
        return sum(self.silos_self_count)
