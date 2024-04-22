from enum import Enum, auto


class Gamemode(Enum):
    DEFAULT = auto()
    THREESILO = auto()


class strategist():
    # silos_self_count  = [1, 1, 1, 1, 1]
    # silos_scan        = [1, 1, 1, 2, 1]
    silos_self_count    = [0] * 5
    silos_scan          = [0] * 5

    gameMode = None
    ignoredSilos = []
    focusedSilos = []
    
    def __init__(self, gamemode=Gamemode.DEFAULT):
        self.gameMode = gamemode

    def drop(self, column):
        self.silos_self_count[column] += 1
        if self.silos_self_count[column] > 3:
            self.silos_self_count[column] = 3
        if self.silos_self_count[column] == 0:
            self.focusedSilos.append(column)

                
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
        tempList = [0, 0, 0, 0, 0]
        daBo = 0

        for i in range(0, 5):
            daBo += self.silos_self_count[i]
            if self.silos_scan[i] > self.silos_self_count[i]:
                tempList[i] = self.silos_scan[i]
            else:
                tempList[i] = self.silos_self_count[i]
        
        # self.autoFocusSilos()
        scores = [0] * 5
        bestScore = position
        for i in range(0, 5):

            if tempList[i] == 2:
                scores[i] += 200

            elif tempList[i] == 0:
                scores[i] += 100
                if len(self.focusedSilos) < 3:
                    scores[i] += 50
                # focus on un-occupied silo

            elif self.silos_self_count[i] == 1 and daBo >= 3 and len(self.focusedSilos) >= 3:
                # focus on occupied silo
                scores[i] += 150

            scores[i] -= abs(position - i) * 5
            if scores[i] > scores[bestScore]:
                bestScore = i
        print("Best", bestScore, scores)
        return bestScore
