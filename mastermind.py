from enum import Enum, auto


class Gamemode(Enum):
    DEFAULT = auto()
    THREESILO = auto()


class ball(Enum):
    ROBOT = 1
    ENERMY = -1


class mastermind():
    ignoredSilos = []
    silo = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 1, -1, 0]]

    gameode = Gamemode.DEFAULT
    
    def __init__(self, gamemode=0):
        print("Antagonist created")
        if gamemode == Gamemode.THREESILO:
            self.ignoredSilos = [0, 4]

    # return the number of ball inside
    def countBall(self, column):
        return 3 - [row[column] for row in self.silo].count(0)
    
    def drop(self, column, side=ball.ROBOT):
        for i in range(2, -1, -1):
            if self.silo[i][column] == 0:
                self.silo[i][column] = side
                break

    def update(self, column, number):
        # column = [row[0] for row in self.silo]
        for i in range(0, number):
            self.drop(column, ball.ENERMY)

    def chooseSilo(self, chooseOneBallSilo=False):
        scores = [0, 0, 0, 0, 0]

        if all(s == 3 for s in self.silo):
            return 10

        # let's what to do next
        else:
            for s in range(0, len(self.silo[0])):
                if s in self.ignoredSilos:
                    scores[s] = -255
                    continue
                # print(self.countBall(s))
                column = [row[s] for row in self.silo]

                if self.countBall(s) == 3:
                    scores[s] = -255
                elif self.countBall(s) == 2:
                    scores[s] = column[2] * column[1] * -50 + 200
                elif self.countBall(s) == 1:
                    scores[s] = column[2] * 50

        print(scores)


mastermind = mastermind(gamemode=Gamemode.THREESILO)
mastermind.chooseSilo()
