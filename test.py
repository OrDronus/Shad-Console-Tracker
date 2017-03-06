from datetime import datetime
import locale
import tkinter
import webbrowser

class ArenaStats:

    def __init__(self):
        self.runs = 0
        self.totalWins = 0
        self.avgWins = 0
        self.winrate = 0
        self.avgGold = 0
        self.totalGold = 0

string = ("This "
        "is "
        "multi "
        "line")

tk = tkinter.Tk()
tk.withdraw()

input("Copy the link and press any button")
url = tk.clipboard_get()
print(url)
input("Press any button to check clipboar again")
print(tk.clipboard_get())
input("Press again to get the link back")
tk.clipboard_clear()
tk.clipboard_append(url)
newUrl = tk.clipboard_get()
print("URL from clipboard: {}".format(newUrl))
webbrowser.open(tk.clipboard_get())
tk.destroy()
