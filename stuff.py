

def userDialog(message):
    print(message)
    while True:
        ans = input("Yes or No?: ").lower()
        if ans == "y" or ans == "yes":
            return True
        elif ans == "n" or ans == "no":
            return False

def clearScreen():
    try:
        os.system("cls")
    except:
        os.system("clear")

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
