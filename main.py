# -*- coding: UTF-8 -*-

# Комментарий на русском для проверки
from datetime import datetime
import locale
import os
import traceback

locale.setlocale(locale.LC_ALL, '')

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

def clearScreen():
    try:
        os.system("cls")
    except:
        os.system("clear")

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

class ArenaStats:

    def __init__(self, craft):
        self.craft = craft
        self.runs = 0
        self.totalWins = 0
        self.avgWins = 0
        self.winrate = 0
        self.avgGold = 0
        self.totalGold = 0

class Deck:
    def __init__(self, craft, name):
        self.craft = craft
        self.name = name
        self.rRuns = 0
        self.uRuns = 0
        self.rWins = 0
        self.uWins = 0
        self.rWinrate = 0
        self.uWinrate = 0
        self.tWinrate = 0

    def resetStats(self):
        self.rRuns = 0
        self.uRuns = 0
        self.rWins = 0
        self.uWins = 0
        self.rWinrate = 0
        self.uWinrate = 0
        self.tWinrate = 0

    def __str__(self):
        return "{}[{}]".format(self.name, self.craft)

class Game:
    def __init__(self, date, deck, ranked, win):
        self.date = date
        self.deck = deck
        self.ranked = ranked
        self.win = win

    def __str__(self):
        return "{} {} {}".format(self.date.strftime("%x"), self.deck,
        {True: "Ranked", False: "Unranked"}[self.ranked],
        {True: "Win", False: "Loss"}[self.win])

class UserError(Exception):
    def __init__(self, message):
        self.message = message

    def show(self):
        print(self.message)
        input("Press any key to continue")

class Printer:
    stats, list = range(2)  # What to show
    arena, decks, games, onedeck = range(4)  # Types of data
    ranked, unranked, both = range(3)   # When showing games
    none, winrate, played = range(3)    # When showing stats

    def __init__(self, tracker):
        self.tracker = tracker
        self.sortedDecks = []
        self.sortedArenas = []

        self.deck = None
        self.show = Printer.stats
        self.data = Printer.arena
        self.games = Printer.both
        self.maxDate = None
        self.minDate = None
        self.sort = Printer.none

    def printArenaStats(self):
        print("Arena Stats\n")
        if not self.tracker.arenaRuns:
            print("You haven't completed any arena runs")
            return
        table = []
        table.extend([["Craft", "Avg Wins", "Winrate", "Avg Gold", "Runs"],
                    ["", "", "", "", ""]])
        statsAll = self.sortedArenas[Craft.all]
        table.extend([[Craft.toStr(Craft.all), "{:.2f}".format(statsAll.avgWins),
                    "{:.2%}".format(statsAll.winrate),
                    "{:.2f}".format(statsAll.avgGold),
                    str(statsAll.runs)],
                    ["", "", "", "", ""]])
        for i in range(7):
            stats = self.sortedArenas[i]
            if stats.runs == 0:
                continue
            table.append([Craft.toStr(stats.craft), "{:.2f}".format(stats.avgWins),
                        "{:.2%}".format(stats.winrate),
                        "{:.2f}".format(stats.avgGold),
                        str(stats.runs)])
        printTable(table, 4)

    def printGamesStats(self):
        if self.data == Printer.decks:
            print("Deck List\n")
            if not self.tracker.decks:
                print("You don't have any decks yet")
                return
        else:
            print("Games Stats\n")
            if not self.tracker.games:
                print("You haven't played any games yet")
                return

        table = []
        table.extend([["Name", "Craft", "Winrate", "Runs"],
                    ["", "", "", ""]])
        for deck in self.sortedDecks:
            if self.data != Printer.decks and deck.uRuns + deck.rRuns == 0:
                continue
            table.append([deck.name, str(deck.craft), "{:.2%}".format(deck.tWinrate),
                        str(deck.rRuns + deck.uRuns)])
        printTable(table, 4)

    def printOneDeckStats(self):
        if not self.deck:
            print("You don't have any deck selcted")
            return
        print("Name: {} Craft: {}\n".format(self.deck.name, self.deck.craft))
        table = [["", "Unranked", "Ranked", "Total"],
                    ["Runs", str(self.deck.uRuns), str(self.deck.rRuns),
                        str(self.deck.uRuns + self.deck.rRuns)],
                    ["Winrate", "{:2%}".format(self.deck.uWinrate),
                        "{:2%}".format(self.deck.rWinrate), "{:2%}".format(self.deck.tWinrate)]]
        printTable(table, 4)

    def printArenaList(self):
        print("Arenas List\n")
        if not self.tracker.arenaRuns:
            print("You haven't completed any arena runs")
            return
        for arena in self.tracker.arenaRuns:
            print(arena)

    def printGamesList(self):
        print("Games List\n")
        if not self.tracker.games:
            print("You haven't played any games")
            return
        for game in self.tracker.games:
            if self.games == Printer.both:
                print(game)
            elif self.games == Printer.ranked and game.ranked:
                print(game)
            elif self.games == Printer.unranked and not game.ranked:
                print(game)

    def printStuff(self):
        if self.data == Printer.decks:
            self.printGamesStats()
        elif self.data == Printer.arena:
            if self.show == Printer.list: self.printArenaList()
            else: self.printArenaStats()
        elif self.data == Printer.games:
            if self.show == Printer.list: self.printGamesList()
            else: self.printGamesStats()
        else:
            self.printOneDeckStats()

    def sortArenaStats(self):
        if self.sort == Printer.none:
            self.sortedArenas = self.tracker.arenaStats
        else:
            if self.sort == Printer.winrate:
                key = lambda x: x.winrate
            else:
                key = lambda x: x.runs
            self.sortedArenas = self.tracker.arenaStats[:7]
            self.sortedArenas.sort(key=key, reverse=True)
            self.sortedArenas.append(self.tracker.arenaStats[7])

    def sortGamesStats(self):
        self.sortedDecks = self.tracker.decks
        if self.sort == Printer.none:
            return
        else:
            if self.sort == Printer.winrate:
                key = {Printer.ranked: lambda x: x.rWinrate,
                       Printer.unranked: lambda x: x.uWinrate,
                       Printer.both: lambda x: x.tWinrate}[self.games]
            else:
                key = {Printer.ranked: lambda x: x.rRuns,
                       Printer.unranked: lambda x: x.uRuns,
                       Printer.both: lambda x: x.rRuns + x.uRuns}[self.games]
            self.sortedDecks.sort(key=key, reverse=True)

class DeckTracker:
    def __init__(self, farena="data/arena", fdecks="data/decks",
                fgames="data/games", fconf="data/conf"):
        self.arenasFile = farena
        self.decksFile = fdecks
        self.gamesFile = fgames
        self.confFile = fconf

        self.arenaRuns = []
        self.arenaStats = []
        self.loadRuns()
        self.calcArenaStats()
        self.decks = []
        self.loadDecks()
        self.games = []
        self.loadGames()
        self.calcGamesStats()

        self.printer = Printer(self)
        self.loadConf()
        self.printer.sortArenaStats()
        self.printer.sortGamesStats()

    def saveRun(self, run):
        with open(self.arenasFile, "a") as fd:
            fd.write("{} {} {} {}\n".format(run.date.strftime("%d.%m.%Y"), run.craft,
            run.wins, run.gold))

    def saveDeck(self, deck):
        with open(self.decksFile, "a") as fd:
            fd.write("{} {}\n".format(deck.craft, deck.name))

    def saveGame(self, game):
        with open(self.gamesFile, "a") as fd:
            fd.write("{} {} {} {}\n".format(game.date.strftime("%d.%m.%Y"),
            self.decks.index(game.deck), game.ranked, game.win))

    def saveConf(self):
        # show, data, games, minDate, maxDate, sort, deck
        with open(self.confFile, "w") as fd:
            if self.printer.deck:
                deckid = self.decks.index(self.printer.deck)
            else:
                deckid = -1
            minDate = self.printer.minDate
            maxDate = self.printer.maxDate
            fd.write("{} {} {} {} {} {} {}\n".format(self.printer.show,
                self.printer.data, self.printer.games,
                minDate.strftime("%d.%m.%Y") if minDate else "n",
                maxDate.strftime("%d.%m.%Y") if maxDate else "n",
                self.printer.sort, deckid))

    def loadRuns(self):
        # Возможные исключения: FileNotFoundError, ValueError
        # 0-date, 1-craft, 2-wins, 3-gold
        try:
            with open(self.arenasFile, "r") as fd:
                for line in fd:
                    data = line.split()
                    if len(data) == 0:
                        continue
                    date = datetime.strptime(data[0], "%d.%m.%Y")
                    craft = Craft(data[1])
                    wins = int(data[2])
                    gold = int(data[3])
                    self.arenaRuns.append(ArenaRun(date, craft, wins, gold))
        except ValueError:
            raise UserError("\"{}\" file, that contains arena runs, has"
            " Invalid data, check it's contents or delete it.".format(self.arenasFile))
        except FileNotFoundError:
            pass    # File will be created, when saving new arena run

    def loadDecks(self):
        # 0-craft, 1-name
        try:
            with open(self.decksFile, "r") as fd:
                for line in fd:
                    data = line.split(maxsplit=1)
                    if len(data) == 0:
                        continue
                    craft = Craft(data[0])
                    name = data[1].strip()
                    self.decks.append(Deck(craft, name))
        except ValueError:
            raise UserError("\"{}\" file, that contains decks, has"
            " Invalid data, check it's contents or delete it.".format(self.decksFile))
        except FileNotFoundError:
            pass    # File will be created, when saving new deck

    def loadGames(self):
        # 0-date, 1-deck, 2-ranked, 3-win
        try:
            with open(self.gamesFile, "r") as fd:
                for line in fd:
                    data = line.split()
                    if len(data) == 0:
                        continue
                    date = datetime.strptime(data[0], "%d.%m.%Y")
                    deck = self.decks[int(data[1])]
                    ranked = data[2] == "True"
                    win = data[3] == "True"
                    self.games.append(Game(date, deck, ranked, win))
        except ValueError:
            raise UserError("\"{}\" file, that contains games, has"
            " Invalid data, check it's contents or delete it.".format(self.gamesFile))
        except FileNotFoundError:
            pass    # File will be created, when saving new game

    def loadConf(self):
        # show, data, games, minDate, maxDate, sort, deck
        try:
            with open(self.confFile, "r") as fd:
                data = fd.readline().split()
                self.printer.show = int(data[0])
                self.printer.data = int(data[1])
                self.printer.games = int(data[2])
                if data[3] == "n":
                    self.printer.minDate = None
                else:
                    self.printer.minDate = datetime.strptime(data[3], "%d.%m.%Y")
                if data[4] == "n":
                    self.printer.maxDate = None
                else:
                    self.printer.maxDate = datetime.strptime(data[4], "%d.%m.%Y")
                self.printer.sort = int(data[5])
                deckid = int(data[6])
                if deckid == -1:
                    self.printer.deck = None
                else:
                    self.printer.deck = self.decks[deckid]
        except (ValueError, IndexError):
            raise UserError("\"{}\" file, that contains configuration, has"
            " Invalid data, check it's contents or delete it.".format(self.gamesFile))
        except FileNotFoundError:
            pass    # File will be created, when saving new conf

    def addNewArenaRun(self, params):
        # [[date], craft, wins, gold], used as stack, because amount of params can differ
        try:
            data = params.lower().split()
            try:
                date = datetime.strptime(data[0], "%x")
                del data[0]
            except ValueError:
                date = datetime.today()
            craft = Craft(data.pop(0))
            wins = int(data.pop(0))
            gold = int(data.pop(0))

            newRun = ArenaRun(date, craft, wins, gold)
            self.saveRun(newRun)
            self.arenaRuns.append(newRun)
            self.calcArenaStats()
            self.printer.sortArenaStats()
        except IndexError:
            raise UserError("Not enough command parameters")
        except ValueError as err:
            raise UserError("Invalid command parameters: \"{}\"".format(err))
        except OSError as err:
            raise UserError("Could not save new arena run: \"{}\"".format(err))

    def addNewDeck(self, params):
        # 0-craft, 1-name
        try:
            data = params.split(maxsplit=1)
            craft = Craft(data[0])
            name = data[1].strip()

            newDeck = Deck(craft, name)
            self.saveDeck(newDeck)
            self.decks.append(newDeck)
            self.printer.sortGamesStats()
        except IndexError:
            raise UserError("Not enough command parameters")
        except ValueError as err:
            raise UserError("Invalid command parameters: \"{}\"".format(err))
        except OSError as err:
            raise UserError("Could not save new deck: \"{}\"".format(err))

    def selectDeck(self, words):
        res = []
        for deck in self.decks:
            deckName = deck.name.lower()
            match = True
            for word in words:
                if word not in deckName:
                    match = False
                    break
            if match:
                res.append(deck)
        if not res:
            raise UserError("There is no deck with that name")
        if len(res) > 1:
            # If there is only one deck with the same amount of words in the name as
            # search que, it will be selected
            sameLen = None
            for deck in res:
                if len(deck.name.split()) <= len(words):
                    if sameLen:
                        sameLen = None
                        break
                    sameLen = deck
            if sameLen:
                return sameLen
            # Last resort- selecting a deck manually
            print()
            for i in range(len(res)):
                print("{}) {}".format(i+1, res[i]))
            print("Select a deck from the list")
            while True:
                try:
                    return res[int(input(">"))-1]
                except ValueError:
                    print("Please enter a number")
                except KeyError:
                    print("There is no such deck")
        else:
            return res[0]

    def addNewGame(self, params):
        # [date], [ranked], deck, win
        try:
            data = params.lower().split()
            try:
                date = datetime.strptime(data[0], "%x")
                del data[0]
            except ValueError:
                date = datetime.today()
            ranked = False
            if data[0] == "ranked":
                ranked = True
                del data[0]
            deck = self.selectDeck(data[:len(data)-1])
            val = data[len(data)-1]
            if val == "win" or val == "won":
                win = True
            elif val == "loss" or val == "lost":
                win = False
            else:
                raise UserError("Match result is not specified")
            newGame = Game(date, deck, ranked, win)
            self.saveGame(newGame)
            self.games.append(newGame)
            self.calcGamesStats()
            self.printer.sortGamesStats()
        except IndexError as err:
            traceback.print_exc()
            raise UserError("Not enough command parameters")
        except ValueError as err:
            traceback.print_exc()
            raise UserError("Invalid command parameters: \"{}\"".format(err))
        except OSError as err:
            raise UserError("Could not save new game: \"{}\"".format(err))

    def deleteArenaRun(self, params):
        raise UserError("Operation is not supported yet")

    def deleteDeck(self, params):
        raise UserError("Operation is not supported yet")

    def deleteGame(self, params):
        raise UserError("Operation is not supported yet")

    def calcArenaStats(self):
        # 0-6: crafts, 7-all/total
        self.arenaStats.clear()
        for i in range(8):
            self.arenaStats.append(ArenaStats(i))
        for run in self.arenaRuns:
            self.arenaStats[7].runs += 1
            self.arenaStats[7].totalWins += run.wins
            self.arenaStats[7].totalGold += run.gold
            self.arenaStats[run.craft.val].runs += 1
            self.arenaStats[run.craft.val].totalWins += run.wins
            self.arenaStats[run.craft.val].totalGold += run.gold
        for stats in self.arenaStats:
            if stats.runs == 0:
                continue
            stats.winrate = stats.totalWins/(stats.runs*5)
            stats.avgWins = stats.totalWins/stats.runs
            stats.avgGold = stats.totalGold/stats.runs

    def calcGamesStats(self):
        for deck in self.decks:
            deck.resetStats()
        for game in self.games:
            if game.ranked:
                game.deck.rRuns += 1
                if game.win:
                    game.deck.rWins += 1
            else:
                game.deck.uRuns += 1
                if game.win:
                    game.deck.uWins += 1
        for deck in self.decks:
            if deck.rRuns:
                deck.rWinrate = deck.rWins/deck.rRuns
            if deck.uRuns:
                deck.uWinrate = deck.uWins/deck.uRuns
            if deck.rRuns or deck.uRuns:
                deck.tWinrate = (deck.rWins + deck.uWins)/(deck.rRuns + deck.uRuns)

    def newCommand(self, params):
        try:
            data = params.split(maxsplit=1)
            { "arena": self.addNewArenaRun, "deck": self.addNewDeck,
              "game": self.addNewGame }[data[0]](data[1])
        except KeyError:
            raise UserError("Invalid parameter: {}".format(data[0]))

    def deleteCommand(self, params):
        try:
            data = params.split(maxsplit=1)
            { "arena": self.deleteArenaRun, "deck": self.deleteDeck,
              "game": self.deleteGame }[data[0]](data[1])
        except KeyError:
            raise UserError("Invalid parameter: {}".format(data[0]))

    def showCommand(self, params):
        data = params.lower().split()
        if data[0] == "deck":
            self.printer.deck = self.selectDeck(data[1:])
            self.printer.data = Printer.onedeck
        else:
            for param in data:
                if param == "arena":
                    self.printer.data = Printer.arena
                elif param == "games":
                    self.printer.data = Printer.games
                elif param == "decks":
                    self.printer.data = Printer.decks
                elif param == "stats":
                    self.printer.show = Printer.stats
                elif param == "list":
                    self.printer.show = Printer.list
                elif param == "ranked":
                    self.printer.games = Printer.ranked
                    self.printer.sortGamesStats()
                elif param == "unranked":
                    self.printer.games = Printer.unranked
                    self.printer.sortGamesStats()
                elif param == "both":
                    self.printer.games = Printer.both
                    self.printer.sortGamesStats()
                else:
                    raise UserError("Unknown parameter: {}".format(param))
            self.saveConf()

    def sortCommand(self, params):
        try:
            data = params.lower().strip()
            self.printer.sort = {"none": Printer.none, "winrate": Printer.winrate,
                                "played": Printer.played}[data]
            self.printer.sortArenaStats()
            self.printer.sortGamesStats()
            self.saveConf()
        except KeyError as err:
            raise UserError("Unknown parameter: {}".format(err))

    def run(self):
        commands = {"new": self.newCommand, "delete": self.deleteCommand,
                    "show": self.showCommand, "sort": self.sortCommand}
        while True:
            clearScreen()
            self.printer.printStuff()
            print()
            try:
                inputline = input(">").split(maxsplit=1)
                action = inputline[0].lower()
                if action == "q" or action == "quit":
                    break
                if len(inputline) > 1:
                    params = inputline[1]
                else:
                    params = ""
                command = commands[action]
            except KeyError:
                input("No such command\nPress any key to continue")
            except IndexError:
                pass
            else:
                try:
                    command(params)
                except UserError as err:
                    err.show()

DeckTracker().run()

# def test1():
#     track = DeckTracker("test/arena", fdecks="test/decks", fgames="test/games")
#     track.printer.data = Printer.decks
#     track.printer.printStuff()
#     print(track.selectDeck(["daria"]))
