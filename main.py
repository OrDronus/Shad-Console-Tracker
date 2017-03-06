# -*- coding: UTF-8 -*-

# Комментарий на русском для проверки
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
                raise ValueError("invalid craft name: {}".format(craft))
        else:
            if craft > 6:
                raise ValueError("invalid craft value: {}".format(craft))
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

class UserError(Exception):
    def __init__(self, message):
        self.message = message

    def show(self):
        print(self.message)
        input("Press any key to continue")

# class InvalidFileDataError(UserError):
#     def __init__(self, filename, datatype):
#         self.file = filename
#         self.data = datatype

def loadRuns(fname):
    res = []
    # Возможные исключения: FileNotFoundError, ValueError
    try:
        with open(fname, "r") as fd:
            for line in fd:
                data = line.split()
                if len(data) == 0:
                    continue
                # 0-date, 1-craft, 2-wins, 3-gold
                date = datetime.strptime(data[0], "%d.%m.%Y")
                craft = Craft(data[1])
                wins = int(data[2])
                gold = int(data[3])
                res.append(ArenaRun(date, craft, wins, gold))
    except ValueError:
        raise UserError("\"{}\" file, that contains arena runs, has"
        " Invalid data, check it's contents or delete it.".format(fname))
    except FileNotFoundError:
        pass    # File will be created, when saving new arena run
    return res

def saveRuns(fname, arenaRuns):
    with open(fname, "w") as fd:
        for run in arenaRuns:
            fd.write(run.date.strftime("%d.%m.%Y") + " " + str(run.craft) +\
            " " + str(run.wins) + " " + str(run.gold) + "\n")

def saveRun(fname, run):
    with open(fname, "a") as fd:
        fd.write(run.date.strftime("%d.%m.%Y") + " " + str(run.craft) +\
        " " + str(run.wins) + " " + str(run.gold) + "\n")

def addNewArenaRun(data):
    # [[date], craft, wins, gold], used as stack, because amount of params can differ
    try:
        try:
            date = datetime.strptime(data[0], "%x")
            data.pop(0)
        except ValueError:
            date = datetime.today()
        craft = Craft(data.pop(0))
        wins = int(data.pop(0))
        gold = int(data.pop(0))

        newRun = ArenaRun(date, craft, wins, gold)
        saveRun("data", newRun)
        arenaRuns.append(newRun)
    except IndexError:
        raise UserError("Not enough command parameters")
    except ValueError as err:
        raise UserError("Invalid command parameters: \"{}\"".format(err))
    except OSError as err:
        raise UserError("Could not save new arena run: \"{}\"".format(err))

class ArenaStats:

    def __init__(self):
        self.runs = 0
        self.totalWins = 0
        self.avgWins = 0
        self.winrate = 0
        self.avgGold = 0
        self.totalGold = 0

def calcStats():
    statsArray = []
    for i in range(8):
        statsArray.append(ArenaStats())
    for run in arenaRuns:
        statsArray[7].runs += 1
        statsArray[7].totalWins += run.wins
        statsArray[7].totalGold += run.gold
        statsArray[run.craft.val].runs += 1
        statsArray[run.craft.val].totalWins += run.wins
        statsArray[run.craft.val].totalGold += run.gold

    for stats in statsArray:
        if stats.runs == 0:
            continue
        stats.winrate = stats.totalWins/(stats.runs*5)
        stats.avgWins = stats.totalWins/stats.runs
        stats.avgGold = stats.totalGold/stats.runs

    return statsArray

def printTable(table, space):
    rows = len(table)
    if rows == 0:
        return
    cols = len(table[0])
    maxColWidth = [0] * cols
    for i in range(rows):
        for j in range(cols):
            if len(table[i][j]) > maxColWidth[j]:
                maxColWidth[j] = len(table[i][j])
    for i in range(rows):
        for j in range(cols):
            pad = maxColWidth[j] - len(table[i][j]) + space
            print(table[i][j] + " " * pad, end="")
        print()

def printStats():
    statsArray = calcStats()
    table = []
    table.extend([["Craft", "Avg Wins", "Winrate", "Avg Gold", "Runs"],
                ["", "", "", "", ""]])
    statsAll = statsArray[Craft.all]
    table.extend([[Craft.toStr(Craft.all), "{:.2f}".format(statsAll.avgWins),
                "{:.2%}".format(statsAll.winrate),
                "{:.2f}".format(statsAll.avgGold),
                str(statsAll.runs)],
                ["", "", "", "", ""]])
    for i in range(7):
        stats = statsArray[i]
        if stats.runs == 0:
            continue
        table.append([Craft.toStr(i), "{:.2f}".format(stats.avgWins),
                    "{:.2%}".format(stats.winrate),
                    "{:.2f}".format(stats.avgGold),
                    str(stats.runs)])
    printTable(table, 4)

def clearScreen():
    try:
        os.system("cls")
    except:
        os.system("clear")

locale.setlocale(locale.LC_ALL, '')
commands = {"arena": addNewArenaRun}

try:
    arenaRuns = loadRuns("data")
except UserError as err:
    err.show()

while True:
    clearScreen()
    printStats()
    print()
    try:
        inputline = input(">").split()
        cname = inputline.pop(0).lower()
        if cname == "q" or cname == "quit":
            break
        command = commands[cname]
    except KeyError:
        input("No such command\nPress any key to continue")
    except IndexError:
        pass
    else:
        try:
            command(inputline)
        except UserError as err:
            err.show()


# saveStats("data", arenaRuns)
