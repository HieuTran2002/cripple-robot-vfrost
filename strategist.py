from enum import Enum, auto


class Gamemode(Enum):
    DEFAULT = auto()
    THREESILO = auto()


class strategist():
    # silos_self_count    = [1, 1, 1, 1, 1]
    # silos_scan          = [1, 1, 1, 2, 1]
    silos_self_count    = [0] * 5
    silos_scan          = [0] * 5

    gameMode = None
    ignoredSilos = []
    focusedSilos = []
    
    def __init__(self, gamemode=Gamemode.DEFAULT):
        self.gameMode = gamemode
        if gamemode == Gamemode.THREESILO:
            self.focusedSilos = [0, 1, 4]

    def drop(self, column):
        self.silos_self_count[column] += 1
        if self.silos_self_count[column] > 3:
            self.silos_self_count[column] = 3
                
    def focusedIsFilled(self):
        for i in self.focusedSilos:
            if self.silos_self_count[i] == 0:
                return False
        return True

    def findEmtpySilo(self):
        for i in range(0, 5):
            if self.silos_scan[i] == 0:
                return i
        else:
            return None

    def autoFocusSilos(self):
        for i in range(0, len(self.focusedSilos)):
            idx = self.focusedSilos[i]
            # check if this silo hasn't been occupied, and switch to other empty silo.
            if self.silos_scan[idx] > 0 and self.silos_self_count[idx] == 0 and self.findEmtpySilo():
                print("before", self.focusedSilos)
                self.focusedSilos[i] = self.findEmtpySilo()
                print("after", self.focusedSilos)

    def makeDecision(self, position=2):
        # self.silos_scan = [1,1,1,1,1]
        # self.silos_self_count = [1,0,1,0,1]
        self.autoFocusSilos()
        isFilled = self.focusedIsFilled()
        scores = [0] * 5
        bestScore = 0
        for i in range(0, 5):

            if self.silos_scan[i] == 2:
                scores[i] += 200

            elif self.silos_scan[i] == 0:
                scores[i] += 100 
                # focus on un-occupied silo 
                if not isFilled and i in self.focusedSilos:
                    print("focus but still empty")
                    scores[i] += 50

            elif self.silos_scan[i] == 1:
                # focus on occupied silo
                if isFilled and i in self.focusedSilos:
                    print("bonus")
                    scores[i] += 100
                scores[i] += 50
            scores[i] -= abs(position - i) * 5 
            if scores[i] > scores[bestScore]:
                bestScore = i
        print("Best", bestScore, scores)
        return bestScore
