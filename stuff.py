from datetime import datetime
import locale
import tkinter
import webbrowser

# class Craft:
#     crafts = []
#     forest, sword, rune, dragon, shadow, blood, haven, all = range(8)
#
#     def __init__(self, craft):
#         if craft.__class__ == str:
#             craft = craft.lower()
#             if craft == "forestcraft" or craft == "forest":
#                 self.val = Craft.forest
#             elif craft == "swordcraft" or craft == "sword":
#                 self.val = Craft.sword
#             elif craft == "runecraft" or craft == "rune":
#                 self.val = Craft.rune
#             elif craft == "dragoncraft" or craft == "dragon":
#                 self.val = Craft.dragon
#             elif craft == "shadowcraft" or craft == "shadow":
#                 self.val = Craft.shadow
#             elif craft == "bloodcraft" or craft == "blood":
#                 self.val = Craft.blood
#             elif craft == "havencraft" or craft == "haven":
#                 self.val = Craft.haven
#             else:
#                 raise ValueError("invalid craft name: {}".format(craft))
#         else:
#             if craft > 6:
#                 raise ValueError("invalid craft value: {}".format(craft))
#             self.val = craft
#
#     @staticmethod
#     def init():
#         for i in range(8):
#             Craft.crafts.append(Craft(i))
#
#     @staticmethod
#     def toStr(value):
#         # Names must be in the same order as in class definition
#         return ["Forestcraft", "Swordcraft", "Runecraft", "Dragoncraft",
#                 "Shadowcraft", "Bloodcraft", "Havencraft", "All"][value]
#
#     def __str__(self):
#         return Craft.toStr(self.val)
#
# Craft.init()

class Craft:
    class _Craft:
        def __init__(self, val, name):
            self.val = val
            self.name = name

        def __str__(self):
            return "{}: {}".format(self.name, self.val)
    forest = _Craft(0, "Forestcraft")
    sword = _Craft(1, "Swordcraft")
    _crafts = [forest, sword]
    def __new__(cls, val):
        if val.__class__ == str:
            if val == "forest":
                return Craft.forest
            elif val == "sword":
                return Craft.sword
            else:
                raise ValueError("Invalid craft value: {}".format(val))
        else:
            return Craft._crafts[val]

a = Craft("forest")
b = Craft(0)
print(a is b)
print(a.__class__)

class Thing:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

    def foo(self):
        return -self.val2

    def __str__(self):
        return "{};{}".format(self.val1, self.val2)

a = Thing(5, 3)
lst = [Thing(21,12), Thing(51,9), Thing(32,10), Thing(11,2)]
lst.sort(key=lambda x: x.val1)
for thing in lst[:3]:
    print(thing, " ", end="")
date = None
print("{}".format(date.strftime("%d.%m.%Y") if date else "n"))

# class Craft:
#     _forest = {"val": 0, "name": "Forestcraft"}
#     _sword = {"val": 1, "name": "Swordcraft"}
#     _crafts = [_forest, _sword]
#
#     def __init__(self, val):
#         if val.__class__ == str:
#             if val == "forest":
#                 self.__dict__ = Craft._forest
#             elif val == "sword":
#                 self.__dict__ = Craft._sword
#             else:
#                 raise ValueError("Invalid craft value: {}".format(val))
#         else:
#             self.__dict__ = Craft._crafts[val]
#
#     def forest():
#         return Craft(0)
#
#     def __str__(self):
#         return "{}: {}".format(self.name, self.val)
#
# a = Craft.forest()
# b = Craft("forest")
# print(a is b)
#
# class Single:
#     _instance = None
#     def __new__(cls, val):
#         if Single._instance is None:
#             Single._instance = object.__new__(cls)
#         Single._instance.val = val
#         return Single._instance
#
#     def foo(self, num):
#         return self.val + num
#
# a = Single(6)
# b = Single(8)
# print(a is b)


# class ArenaStats:
#
#     def __init__(self):
#         self.runs = 0
#         self.totalWins = 0
#         self.avgWins = 0
#         self.winrate = 0
#         self.avgGold = 0
#         self.totalGold = 0
#
# string = ("This "
#         "is "
#         "multi "
#         "line")
#
# tk = tkinter.Tk()
# tk.withdraw()
#
# input("Copy the link and press any button")
# url = tk.clipboard_get()
# print(url)
# input("Press any button to check clipboar again")
# print(tk.clipboard_get())
# input("Press again to get the link back")
# tk.clipboard_clear()
# tk.clipboard_append(url)
# newUrl = tk.clipboard_get()
# print("URL from clipboard: {}".format(newUrl))
# webbrowser.open(tk.clipboard_get())
# tk.destroy()
