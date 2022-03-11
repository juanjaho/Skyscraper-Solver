import pprint as pp
import copy
from functools import reduce
import itertools
from operator import mul


def highrise(clues):
    t = Tower(clues)
    t.apply()

    for row in t.grid:
        if 0 in row:
            t = guess(t, clues)
            break

    print(t.grid, "goodness")
    return t.grid


def guess(t, clues):
    for i, row in enumerate(t.grid):
        if 0 in row:
            a = i
            break

    temp = t.r[a][:]

    for i in range(len(temp)):
        t.r[a] = [temp[i]]
        try:
            t.runs = 0
            t.apply()
            if t.isSolved(t.grid):

                return t

            for row in t.grid:
                if 0 in row:
                    t = guess(t, clues)
                    break

        except:
            # if t.isSolved(t.grid):
            #     return t

            t = Tower(clues)
            t.apply()

        finally:

            if t.isSolved(t.grid):
                return t

    return t


class Tower:
    def __init__(self, clues):
        self.clueSet = sortClues(clues[:])
        self.r = list(map(getPoss, self.clueSet['r']))
        self.c = list(map(getPoss, self.clueSet['c']))
        self.grid = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [
            0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

        self.cellPoss = []
        self.c = crossCheck(self.c, self.r)
        self.r = crossCheck(self.r, self.c)
        self.runs = 0
        self.apply()

    def apply(self):
        self.runs += 1
        for i in range(len(self.grid)):
            if 0 in self.grid[i]:
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 0:
                        if checkElement(self.r[i][0][j], j, self.r[i]):
                            self.grid[i][j] = self.r[i][0][j]
                            self.r = filterPossible(
                                self.r, i, j, self.grid[i][j])
                            self.c = filterPossible(
                                self.c, j, i, self.grid[i][j])
                            self.c = crossCheck(self.c, self.r)
                            self.r = crossCheck(self.r, self.c)

                        if checkElement(self.c[j][0][i], i, self.c[j]):
                            self.grid[i][j] = self.c[j][0][i]
                            self.r = filterPossible(
                                self.r, i, j, self.grid[i][j])
                            self.c = filterPossible(
                                self.c, j, i, self.grid[i][j])
                            self.c = crossCheck(self.c, self.r)
                            self.r = crossCheck(self.r, self.c)

        if not self.isSolved(self.grid) and self.runs < 100:

            return self.apply()

        return self

    def isSolved(self, grid):
        for row in grid:
            if 0 in row:
                return False

        r = list(map(lambda row: getClue(row), grid[:]))
        c = list(map(lambda col: getClue(col), rotateGrid(grid[:])))

        for i in range(len(r)):

            r[i] = every2(r, i, self.clueSet)
            c[i] = every2(c, i, self.clueSet)

            if not r or not c:
                return False

        return True


def every2(r, i, clueSet):
    for j, e in enumerate(r[i]):
        if not(clueSet["r"][i][j] == 0 or clueSet["r"][i][j] == r[i][j]):
            return False
    return True


def rotateGrid(grid):
    res = []
    for i in range(len(grid)):
        res.append(list(map(lambda e: e[i], grid)))

    return res

#checkElement(self.r[i][0][j], j, self.r[i])
def checkElement(e, i, poss):
    res = []
    for a in poss:
        if e != a[i]:
            return False
    return e


def filterPossible(possible, row, col, element):
    res = []
    for r, p in enumerate(possible):
        run = []
        stats = None
        for a in p:
            if r == row:
                stats = a[col] == element
            else:
                stats = a[col] != element
            if stats:
                run.append(a)
        res.append(run)

    return res


def sortClues(clues):
    c = []
    for i in range(0, len(clues), 7):
        c.append(clues[i:i+7])
    d = {"c": [], "r": []}
    for n in c[0]:
        d['c'].append([n, c[2].pop()])
    for n in c[1]:
        d['r'].append([c[3].pop(), n])

    return d


perms = []
for row in itertools.permutations(range(1, 7 + 1)):
    perms.append(row)


def getClue(a):
    vis = [0, 0]
    sky = [0, 0]
    l = len(a)-1

    for i in range(len(a)):
        if a[i] > sky[0]:
            sky[0] = a[i]
            vis[0] += 1

        if a[l-i] > sky[1]:
            sky[1] = a[l-i]
            vis[1] += 1
    return vis


def getPoss(clue):

    if clue == [0, 0]:
        return perms
    elif clue[0] == 0:
        return list(filter(lambda x: getClue(x)[1] == clue[1], perms))

    elif clue[1] == 0:
        return list(filter(lambda x: getClue(x)[0] == clue[0], perms))

    return list(filter(lambda x: getClue(x) == clue, perms))


def crossCheck(r, c):
    for i in range(7):
        r[i] = list(filter(lambda a: every(a, c, i), r[i]))
    return r


def every(a, c, i):

    for j, e in enumerate(a):
        found = False
        for b in c[j]:
            if b[i] == e:
                found = True
                break
        if not found:
            return False
    return True


clue = [3, 1, 5, 5, 4, 2, 3, 3, 2, 1, 2, 3, 3,
        5, 3, 4, 2, 2, 2, 2, 1, 1, 2, 3, 4, 4, 5, 2]
# clue = [4,2,1,5,3,3,2,3,1,2,2,3,5,4,5,2,4,2,2,2,1,1,2,2,4,4,7,3]
pp.pprint(highrise(clue))
# 3 1 5 5 4 2 3 3 2 1 2 3 3 5 3 4 2 2 2 2 1 1 2 3 4 4 5 2
