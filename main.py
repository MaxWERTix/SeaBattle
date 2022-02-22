import typer
import random
import time
import pickle
from WinPics import WinPicList


def player_symbol(pair):
    if pair == [0, 0]:
        return " "
    if pair == [0, 1]:
        return "*"
    if pair == [1, 0]:
        return "O"
    if pair == [1, 1]:
        return "X"


def opp_symbol(pair):
    if pair == [0, 0]:
        return " "
    if pair == [0, 1]:
        return "*"
    if pair == [1, 0]:
        return " "
    if pair == [1, 1]:
        return "X"


def show_player_field(n, k, field):
    print("   ", sep='', end='')
    for i in range(n):
        letter = chr(ord('A') + i)
        print(letter, " ", sep='', end='')
    print("\n", sep='', end='')
    for j in range(k):
        print(j + 1, sep='', end='')
        if j + 1 < 10:
            print(" ", sep='', end='')
        for i in range(n):
            print("|", sep='', end='')
            print(player_symbol(field[i][j]), sep='', end='')
        print("|\n", sep='', end='')


def show_opp_field(n, k, field):
    print("   ", sep='', end='')
    for i in range(n):
        letter = chr(ord('A') + i)
        print(letter, " ", sep='', end='')
    print("\n", sep='', end='')
    for j in range(k):
        print(j + 1, sep='', end='')
        if j + 1 < 10:
            print(" ", sep='', end='')
        for i in range(n):
            print("|", sep='', end='')
            print(opp_symbol(field[i][j]), sep='', end='')
        print("|\n", sep='', end='')


def show_field(n, k, opp_field, player_field):
    print("***", sep='', end='')
    for i in range(n):
        print("**", sep='', end='')
    print("\n", sep='', end='')
    for i in range(int((2 * n - 8) / 2)):
        print("*", sep='', end='')
    print("Opp", "'", "s Field", sep='', end='')
    for i in range(int((2 * n - 8) / 2)):
        print("*", sep='', end='')
    print("\n", sep='', end='')
    print("***", sep='', end='')
    for i in range(n):
        print("**", sep='', end='')
    print("\n", sep='', end='')

    show_opp_field(n, k, opp_field)

    print("***", sep='', end='')
    for i in range(n):
        print("**", sep='', end='')
    print("\n", sep='', end='')
    for i in range(int((2 * n - 8) / 2)):
        print("*", sep='', end='')
    print("Your Field ", sep='', end='')
    for i in range(int((2 * n - 8) / 2)):
        print("*", sep='', end='')
    print("\n", sep='', end='')
    print("***", sep='', end='')
    for i in range(n):
        print("**", sep='', end='')
    print("\n", sep='', end='')

    show_player_field(n, k, player_field)


def check_cell(n, k, x, y, field):
    if not (0 <= x < n and 0 <= y < k):
        return 0

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if 0 <= x + i < n and 0 <= y + j < k and field[x + i][y + j][0] == 1:
                return 0
    return 1


def auto_fill(n, k, field):
    FourDeckCount = round(n * k / 100)
    ThreeDeckCount = round(2 * n * k / 100)
    TwoDeckCount = round(3 * n * k / 100)
    OneDeckCount = round(4 * n * k / 100)
    DeckCount = [OneDeckCount, TwoDeckCount, ThreeDeckCount, FourDeckCount]
    for DeckCounter in [3, 2, 1, 0]:
        for i in range(DeckCount[DeckCounter]):

            PlaceIsntOk = 1
            while PlaceIsntOk:
                x = random.randint(0, n - 1)
                y = random.randint(0, k - 1)
                rot = random.randint(0, 1)
                PlaceIsntOk = 1
                if rot:
                    for p in range(DeckCounter + 1):
                        PlaceIsntOk += check_cell(n, k, x + p, y, field)
                else:
                    for p in range(DeckCounter + 1):
                        PlaceIsntOk += check_cell(n, k, x, y + p, field)

                if PlaceIsntOk == DeckCounter + 2:
                    if rot:
                        for p in range(DeckCounter + 1):
                            field[x + p][y] = [1, 0]
                    else:
                        for p in range(DeckCounter + 1):
                            field[x][y + p] = [1, 0]
                    PlaceIsntOk = 0


def is_destroyed(n, k, x, y, field):

    counter = 1
    while x + counter < n and field[x + counter][y][0] == 1:
        if field[x + counter][y][1] == 0:
            return 0
        counter += 1

    counter = 1
    while x - counter >= 0 and field[x - counter][y][0] == 1:
        if field[x - counter][y][1] == 0:
            return 0
        counter += 1

    counter = 1
    while y + counter < k and field[x][y + counter][0] == 1:
        if field[x][y + counter][1] == 0:
            return 0
        counter += 1

    counter = 1
    while y - counter >= 0 and field[x][y - counter][0] == 1:
        if field[x][y - counter][1] == 0:
            return 0
        counter += 1

    return 1


def is_win(n, k, field):
    for i in range(n):
        for j in range(k):
            if field[i][j] == [1, 0]:
                return 0
    return 1


def opp_fire(n, k, other_field, field):

    show_field(n, k, other_field, field)

    x = 0
    y = 0
    CellIsntFree = 1
    while CellIsntFree:
        x_r = random.randint(0, n - 1)
        y_r = random.randint(0, k - 1)
        if field[x_r][y_r][1] == 0:
            field[x_r][y_r][1] = 1
            x = x_r
            y = y_r
            CellIsntFree = 0

    print("Your opponent shot at the cell ", chr(ord('A') + x), y + 1, ".\n", sep='', end='')
    time.sleep(3)
    if field[x][y][0]:
        if is_win(n, k, field):
            print("Unfortunately, you lost. You'll be lucky next time!\n", sep='', end='')
            time.sleep(3)
            return 1
        else:
            print("Hit! The opponent makes an additional move.\n", sep='', end='')
            time.sleep(3)
            return opp_fire(n, k, other_field, field)
    else:
        print("Miss! The move passes to you.\n", sep='', end='')
        time.sleep(3)
        return 0


def player_fire(n, k, field, other_field):

    show_field(n, k, field, other_field)

    print("Your turn:\n", sep='', end='')
    input_str = input()

    if input_str == "end":
        return 1

    if input_str.split()[0] == "save":
        name = "autosave.pickle"
        if len(input_str.split()) > 1:
            name = input_str.split()[1] + ".pickle"
        f = open(name, 'wb')
        pickle.dump([field, other_field], f)
        f.close()
        print("Saving was successful.\n")
        time.sleep(2)
        return player_fire(n, k, field, other_field)

    if input_str.split()[0] == "load":
        name = "autosave.pickle"
        if len(input_str.split()) > 1:
            name = input_str.split()[1] + ".pickle"
        try:
            f = open(name, 'rb')
            fields = pickle.load(f)
            field = fields[0]
            other_field = fields[1]
            f.close()
            return player_fire(n, k, field, other_field)
        except OSError:
            print("There is no save with this name.\n")
            time.sleep(5)
            return player_fire(n, k, field, other_field)

    if not(ord('A') <= ord(input_str[0]) < ord('A') + n and ord('1') <= ord(input_str[1]) <= ord('9')):
        print("Wrong Move. Your turn should consist of two symbols: Letters from A to ", chr(ord('A') + n - 1),
              " and numbers from 1 to ", k, ". Try again:\n", sep='', end='')
        time.sleep(5)
        return player_fire(n, k, field, other_field)

    x = ord(input_str[0]) - ord('A')
    y = int(input_str[1])
    if len(input_str) > 2:
        if not(ord('0') <= ord(input_str[2]) <= ord('9') and y * 10 + int(input_str[2]) <= k):
            print("Wrong Move. Your turn should consist of two symbols: Letters from A to ", chr(ord('A') + n - 1),
                  " and numbers from 1 to ", k, ". Try again:\n", sep='', end='')
            time.sleep(5)
            return player_fire(n, k, field, other_field)
        else:
            y = y * 10 + int(input_str[2])
    y -= 1

    if field[x][y][1] == 1:
        print("You have already shot at this cell. Try again:\n", sep='', end='')
        return player_fire(n, k, field, other_field)

    field[x][y][1] = 1

    f = open("autosave.pickle", 'wb')
    pickle.dump([field, other_field], f)
    f.close()

    if field[x][y][0]:
        if is_win(n, k, field):
            print("Congratulations! You won!\n", sep='', end='')
            time.sleep(3)
            print(random.choice(WinPicList))
            return 1
        else:
            if is_destroyed(n, k, x, y, field):
                print("Destroyed! You can make an additional move.\n", sep='', end='')
                time.sleep(3)
                return player_fire(n, k, field, other_field)
            else:
                print("Hit! You can make an additional move.\n", sep='', end='')
                time.sleep(3)
                return player_fire(n, k, field, other_field)
    else:
        print("Miss! The move goes to the opponent.\n", sep='', end='')
        time.sleep(3)
        return 0


def main(n: int, k: int):
    if n > 26 or k > 26:
        print("The size of the playing field cannot exceed 26")
        return

    if n < 5 or k < 5:
        print("the size of the playing field cannot be less than 5")
        return

    PlayerField = []

    for i in range(n):
        SupList = []
        for j in range(k):
            SupList.append([0, 0])
        PlayerField.append(SupList)

    OppField = []

    for i in range(n):
        SupList = []
        for j in range(k):
            SupList.append([0, 0])
        OppField.append(SupList)

    auto_fill(n, k, PlayerField)
    auto_fill(n, k, OppField)

    GameInProgress = 1

    while GameInProgress:
        if opp_fire(n, k, OppField, PlayerField):
            GameInProgress = 0
        else:
            if player_fire(n, k, OppField, PlayerField):
                GameInProgress = 0


if __name__ == "__main__":
    typer.run(main)
