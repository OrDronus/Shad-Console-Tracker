# -*- coding: UTF-8 -*-

from datetime import datetime
import locale
import os

arenaRuns = []

class Craft:
    forest, sword, rune, dragon, shadow, blood, haven, all = range(8)

    def __init__(self, craft):
        if craft.__class__ == str:
            craft = craft.lower()
            if craft == "forestcraft" or craft == "forest":
                self.val = Craft.forest
            elif craft == "swordcraft" or craft == "sword":
                self.val = Craft.sword
            elif craft == "runecraft" or craft == "rune":
                self.val = Craft.rune
            elif craft == "dragoncraft" or craft == "dragon":
                self.val = Craft.dragon
            elif craft == "shadowcraft" or craft == "shadow":
                self.val = Craft.shadow
            elif craft == "bloodcraft" or craft == "blood":
                self.val = Craft.blood
            elif craft == "havencraft" or craft == "haven":
                self.val = Craft.haven
            else:
                raise ValueError("Invalid craft name")
        else:
            if craft > 7:
                raise ValueError("Ivalid craft value")
            self.val = craft

    @staticmethod
    def toStr(value):
        # Names must be in the same order as in class definition
        return ["Forestcraft", "Swordcraft", "Runecraft", "Dragoncraft",
                "Shadowcraft", "Bloodcraft", "Havencraft", "All"][value]

    def __str__(self):
        return Craft.toStr(self.val)

class ArenaRun:
    def __init__(self, date, craft, wins, gold):
        self.date = date
        self.craft = craft
        self.wins = wins
        self.gold = gold

    def __str__(self):
        return self.date.strftime("%x") + " " + str(self.craft) + " " + str(self.wins) + " " + str(self.gold)

def loadRuns(fname):
    res = []
    fd = open(fname, "r")
    for line in fd:
        data = line.split()
        # 0-date, 1-craft, 2-wins, 3-gold
        date = datetime.strptime(data[0], "%d.%m.%Y")
        craft = Craft(int(data[1]))
        wins = int(data[2])
        gold = int(data[3])
        res.append(ArenaRun(date, craft, wins, gold))
    fd.close()  # РџРѕС‡С‚РёС‚Р°С‚СЊ РЅСѓР¶РЅРѕ Р»Рё РІ СЏРІРЅРѕРј РІРёРґРµ Р·Р°РєСЂС‹РІР°С‚СЊ С„Р°Р№Р»С‹
    return res

def saveRuns(fname, arenaRuns):
    fd = open(fname, "w")
    for run in arenaRuns:
        fd.write(run.date.strftime("%d.%m.%Y") + " " + str(run.craft.val) +\
        " " + str(run.wins) + " " + str(run.gold) + "\n")
    fd.close()

def saveRun(fname, run):
    fd = open(fname, "a")
    fd.write(run.date.strftime("%d.%m.%Y") + " " + str(run.craft.val) +\
    " " + str(run.wins) + " " + str(run.gold) + "\n")
    fd.close()

def addNewArenaRun(data):
    # [[date], craft, wins, gold], used as stack, because amount of params can differ
    try:
        date = datetime.strptime(data[0], "%x")
        data.remove(0)
    except ValueError:
        date = datetime.today()
    craft = Craft(data.pop(0))
    wins = int(data.pop(0))
    gold = int(data.pop(0))

    newRun = ArenaRun(date, craft, wins, gold)
    saveRun("data", newRun)
    arenaRuns.append(newRun)

def calcStats():
    stats = {"runs": {}, "avgwins": {}, "winrate": {}, "avggold": {}}
    stats["runs"] = {Craft.all: 0, Craft.forest: 0, Craft.sword: 0, Craft.rune: 0, Craft.dragon: 0,
                    Craft.shadow: 0, Craft.blood: 0, Craft.haven: 0}
    totalWins = {Craft.all: 0, Craft.forest: 0, Craft.sword: 0, Craft.rune: 0, Craft.dragon: 0,
                    Craft.shadow: 0, Craft.blood: 0, Craft.haven: 0}
    totalGold = {Craft.all: 0, Craft.forest: 0, Craft.sword: 0, Craft.rune: 0, Craft.dragon: 0,
                    Craft.shadow: 0, Craft.blood: 0, Craft.haven: 0}
    for run in arenaRuns:
        stats["runs"][Craft.all] += 1
        totalWins[Craft.all] += run.wins
        totalGold[Craft.all] += run.gold
        stats["runs"][run.craft.val] += 1
        totalWins[run.craft.val] += run.wins
        totalGold[run.craft.val] += run.gold
        print("type: {}, val: {}".format(run.wins.__class__, run.wins))
    for i in range(8):
        if stats["runs"][i] == 0:
            continue
        stats["winrate"][i] = float(totalWins[i])/float(stats["runs"][i]*5)
        stats["avgwins"][i] = float(totalWins[i])/float(stats["runs"][i])
        stats["avggold"][i] = float(totalGold[i])/float(stats["runs"][i])
        print("i: {}, wins: {}, runs: {}, avg: {}".format(i, totalWins[i], stats["runs"][i], stats["avgwins"][i]))
    return stats

def printStats():
    stats = calcStats()
    for run in arenaRuns:
        print(run)
    print("\tAvg Gold\tWin Rate\tAvg Wins\n")
    print("Total\t{:.2f}\t\t{:.2%}\t\t{:.2f}".format(stats["avggold"][Craft.all], stats["winrate"][Craft.all], stats["avgwins"][Craft.all]))

locale.setlocale(locale.LC_ALL, '')
print("Date format: " + str(datetime.today().strftime("%x")))
commands = {"new": addNewArenaRun}

arenaRuns = loadRuns("data")
while True:
    try:
        os.system("cls")
    except:
        os.system("clear")
    printStats()
    inputline = raw_input(">").split()
    command = inputline.pop(0).lower()
    if command == "q" or command == "quit":
        break
    try:
        commands[command](inputline)
    except KeyError:
        raw_input("No such command")

# saveStats("data", arenaRuns)
