from datetime import datetime
import locale

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

table = [["Name", "Quantity", "Stuff"],
        ["", "", ""],
        ["Bob", "30", "Abracadabra"],
        ["Nicolas Cage", "56", "idunno"],
        ["Arthur", "57", "yeah, stuff"]]

printTable(table, 3)
