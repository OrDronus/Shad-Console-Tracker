from datetime import datetime
import locale
import tkinter

class ArenaStats:

    def __init__(self):
        self.runs = 0
        self.totalWins = 0
        self.avgWins = 0
        self.winrate = 0
        self.avgGold = 0
        self.totalGold = 0

arr = []

for i in range(8):
    arr.append(ArenaStats())

stats = arr[3]

stats.runs = 5

print(arr[3].runs)
