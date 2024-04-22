# if all of them equal to 1, wait
def chooseSilo(silo, chooseOneBallSilo=False, position=2):
    scores = [0, 0, 0, 0, 0]
    highest_score = 0

    # if they're all 3, stop !
    if all(s == 3 for s in silo):
        return 10
    # let's what to do next
    else:
        for s in range(0, 5):
            # choose the 2-ball silo or the 0-ball silo
            if silo[s] == 2:
                scores[s] = 150
            elif silo[s] == 0:
                scores[s] = 100
            elif silo[s] == 1:
                scores[s] = 50
            else:
                scores[s] = 0

            # choose the closest one
            scores[s] -= abs(position - s) * 5

            if s == 0:
                continue

            if scores[s] > scores[highest_score]:
                highest_score = s

    if scores[highest_score] in range(40, 51) and not chooseOneBallSilo:
        return 9
    return highest_score

# print(chooseSilo([0,2,3,1,1], False))
