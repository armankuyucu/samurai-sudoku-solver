import time
import threading
from tkinter import *

# Global variable set to 0
backtracks = 0


topLeftSudoku = []
topRightSudoku = []
bottomLeftSudoku = []
bottomRightSudoku = []
centerSudoku = []


thread1Steps = []
thread2Steps = []
thread3Steps = []
thread4Steps = []
thread5Steps = []
thread6Steps = []
thread7Steps = []
thread8Steps = []
thread9Steps = []
thread10Steps = []

# creating a RLock
lock = threading.RLock()


# reads the text file
def readFromTxt():
    with open('testSudokuHard.txt', 'r') as f:
        global topLeftSudoku
        global topRightSudoku
        global bottomLeftSudoku
        global bottomRightSudoku
        global centerSudoku

        topLeftSudokuString = []
        topRightSudokuString = []
        bottomLeftSudokuString = []
        bottomRightSudokuString = []
        centerSudokuString = []

        f_contentsList = f.readlines()

        for i in range(0, 9):
            topLeftSudokuString.append(f_contentsList[i][:9])

        for i in range(0, 6):
            topRightSudokuString.append(f_contentsList[i][9:18])
        for i in range(6, 9):
            topRightSudokuString.append(f_contentsList[i][12:21])

        for i in range(12, 21):
            bottomLeftSudokuString.append(f_contentsList[i][0:9])

        for i in range(12, 15):
            bottomRightSudokuString.append(f_contentsList[i][12:21])
        for i in range(15, 21):
            bottomRightSudokuString.append(f_contentsList[i][9:18])

        for i in range(6, 9):
            centerSudokuString.append(f_contentsList[i][6:15])
        for i in range(9, 12):
            centerSudokuString.append(f_contentsList[i][:])
        for i in range(12, 15):
            centerSudokuString.append(f_contentsList[i][6:15])

        # uses list comprehension to convert a list into 2D a list
        topLeftSudoku = [[topLeftSudokuString[0][j] for j in range(0, 9)]
                         for topLeftSudokuString[0] in topLeftSudokuString]

        topRightSudoku = [[topRightSudokuString[0][j] for j in range(0, 9)]
                          for topRightSudokuString[0] in topRightSudokuString]

        bottomLeftSudoku = [[bottomLeftSudokuString[0][j] for j in range(0, 9)]
                            for bottomLeftSudokuString[0] in bottomLeftSudokuString]

        bottomRightSudoku = [[bottomRightSudokuString[0][j] for j in range(0, 9)]
                             for bottomRightSudokuString[0] in bottomRightSudokuString]

        centerSudoku = [[centerSudokuString[0][j] for j in range(0, 9)]
                        for centerSudokuString[0] in centerSudokuString]

        # replaces * with 0
        for i in range(0, 9):
            for j in range(0, 9):
                topLeftSudoku[i][j] = topLeftSudoku[i][j].replace("*", "0")
                topRightSudoku[i][j] = topRightSudoku[i][j].replace("*", "0")
                bottomLeftSudoku[i][j] = bottomLeftSudoku[i][j].replace("*", "0")
                bottomRightSudoku[i][j] = bottomRightSudoku[i][j].replace("*", "0")
                centerSudoku[i][j] = centerSudoku[i][j].replace("*", "0")

        # convert string to int
        topLeftSudoku = [list(map(int, i)) for i in topLeftSudoku]
        topRightSudoku = [list(map(int, i)) for i in topRightSudoku]
        bottomLeftSudoku = [list(map(int, i)) for i in bottomLeftSudoku]
        bottomRightSudoku = [list(map(int, i)) for i in bottomRightSudoku]
        centerSudoku = [list(map(int, i)) for i in centerSudoku]


readFromTxt()


# finds the next empty cell
def findNextEmptyCell(grid):
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def findNextEmptyCellReversed(grid):
    for x in reversed(range(0, 9)):
        for y in reversed(range(0, 9)):
            if grid[x][y] == 0:
                return x, y
    return -1, -1



# Checks whether a value is valid by checking rows, columns and 3X3 sectors
def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of
            # the section or sub-grid containing the i,j cell
            secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where topLeftSudoku and centerSudoku intersects
def isValidTopLeft(grid, i, j, e):
    if 6 <= i <= 8 and 6 <= j <= 8:
        lock.acquire()
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            [e != centerSudoku[i - 6][x] for x in range(9)]) and all(
            [e != topRightSudoku[i][x] for x in range(3)])

        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(
                [e != centerSudoku[x][j - 6] for x in range(9)]) and all(
                [e != bottomLeftSudoku[x][j] for x in range(3)])

            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            lock.release()
                            return False
                lock.release()
                return True
            lock.release()
            return False
        lock.release()
        return False

    else:
        return isValid(grid, i, j, e)


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where topRightSudoku and centerSudoku intersects
def isValidTopRight(grid, i, j, e):
    if (6 <= i <= 8) and (0 <= j <= 2):
        lock.acquire()
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            [e != centerSudoku[i - 6][x] for x in range(9)]) and all(
            [e != topLeftSudoku[i][x + 6] for x in range(3)])
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(
                [e != centerSudoku[x][j + 6] for x in range(9)]) and all(
                [e != bottomRightSudoku[x][j]] for x in range(3))
            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            lock.release()
                            return False
                lock.release()
                return True
            lock.release()
            return False
        lock.release()
        return False

    else:
        return isValid(grid, i, j, e)


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where bottomLeftSudoku and centerSudoku intersects
def isValidBottomLeft(grid, i, j, e):
    if 0 <= i <= 2 and 6 <= j <= 8:
        lock.acquire()
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            [e != centerSudoku[i + 6][x] for x in range(9)]) and all(
            [e != bottomRightSudoku[i][x] for x in range(3)])
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(
                [e != centerSudoku[x][j - 6] for x in range(9)]) and all(
                [e != topLeftSudoku[x + 6][j] for x in range(3)])

            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            lock.release()
                            return False
                lock.release()
                return True
            lock.release()
            return False
        lock.release()
        return False

    else:
        return isValid(grid, i, j, e)


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where bottomRightSudoku and centerSudoku intersects
def isValidBottomRight(grid, i, j, e):
    if 0 <= i <= 2 and 0 <= j <= 2:
        lock.acquire()
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            [e != centerSudoku[i + 6][x] for x in range(9)]) and all(
            [e != bottomLeftSudoku[i][x + 6] for x in range(3)])
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(
                [e != centerSudoku[x][j + 6] for x in range(9)]) and all(
                [e != topRightSudoku[x + 6][j] for x in range(3)])
            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            lock.release()
                            return False
                lock.release()
                return True
            lock.release()
            return False
        lock.release()
        return False

    else:
        return isValid(grid, i, j, e)


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for 4 intersect sectors
def isValidCenter(grid, i, j, e):
    # Top Left Intersect
    if 0 <= i <= 2 and 0 <= j <= 2:
        # print('Top Left' + 'i: ' + str(i) + 'j: ' + str(j))
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            e != topLeftSudoku[i + 6][x] for x in range(9))
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(e != topLeftSudoku[x][j + 6] for x in range(9))
            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

    # Top Right Intersect
    elif 0 <= i <= 2 and 6 <= j <= 8:
        # print('Top Right' + 'i: ' + str(i) + 'j: ' + str(j))

        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            e != topRightSudoku[i + 6][x] for x in range(9))
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(e != topRightSudoku[x][j - 6] for x in range(9))
            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

    # Bottom Left Intersect
    elif 6 <= i <= 8 and 0 <= j <= 2:
        # print('Bottom Left' + 'i: ' + str(i) + 'j: ' + str(j))

        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            e != bottomLeftSudoku[i - 6][x] for x in range(9))
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(e != bottomLeftSudoku[x][j + 6] for x in range(9))
            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

    # Bottom Right Intersect
    elif 6 <= i <= 8 and 6 <= j <= 8:
        # print('Bottom Right' + 'i: ' + str(i) + 'j: ' + str(j))

        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            e != bottomRightSudoku[i - 6][x] for x in range(9))
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(e != bottomRightSudoku[x][j - 6] for x in range(9))
            if intersectColumnOk:
                # finding the top left x,y co-ordinates of
                # the section or sub-grid containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

    else:
        return isValid(grid, i, j, e)


firstTime = True


# Finds definite values using constraints
def solveSudokuConstraints(grid, i=0, j=0):
    if grid == topLeftSudoku:
        topLeftCounter = 0
        solution = 0
        for e in range(1, 10):
            if isValidTopLeft(grid, i, j, e):
                topLeftCounter += 1
                solution = e
        if topLeftCounter == 1:
            topLeftSudoku[i][j] = solution
            if 6 <= i <= 8 and 6 <= j <= 8:
                centerSudoku[i - 6][j - 6] = solution
            print(f'topLeft Constraints i: {i} j: {j} solution: {solution}')
        # print('topLeftCounter ', topLeftCounter)

    if grid == topRightSudoku:
        topRightCounter = 0
        solution = 0
        for e in range(1, 10):
            if isValidTopRight(grid, i, j, e):
                topRightCounter += 1
                solution = e
        if topRightCounter == 1:
            topRightSudoku[i][j] = solution
            print(f'topRight Constraints i: {i} j: {j} solution: {solution}')
            if 6 <= i <= 8 and 0 <= j <= 2:
                centerSudoku[i - 6][j + 6] = solution
        # print('topRightCounter ', topRightCounter)

    if grid == bottomLeftSudoku:
        bottomLeftCounter = 0
        solution = 0
        for e in range(1, 10):
            if isValidBottomLeft(grid, i, j, e):
                bottomLeftCounter += 1
                solution = e
        if bottomLeftCounter == 1:
            bottomLeftSudoku[i][j] = solution
            if 0 <= i <= 2 and 6 <= j <= 8:
                centerSudoku[i + 6][j - 6] = solution
            print(f'bottomLeft Constraints i: {i} j: {j} solution: {solution}')
        # print('bottomLeftCounter ', bottomLeftCounter)

    if grid == bottomRightSudoku:
        bottomRightCounter = 0
        solution = 0
        for e in range(1, 10):
            if isValidBottomRight(grid, i, j, e):
                bottomRightCounter += 1
                solution = e
        if bottomRightCounter == 1:
            bottomRightSudoku[i][j] = solution
            if 0 <= i <= 2 and 0 <= j <= 2:
                centerSudoku[i + 6][j + 6] = solution
            print(f'bottomRight Constraints i: {i} j: {j} solution: {solution}')
        # print('bottomRightCounter ', bottomRightCounter)

    if grid == centerSudoku:
        centerCounter = 0
        solution = 0
        for e in range(1, 10):
            if isValidCenter(grid, i, j, e):
                centerCounter += 1
                solution = e
        if centerCounter == 1:
            centerSudoku[i][j] = solution
            # Top Left
            if 0 <= i <= 2 and 0 <= j <= 2:
                topLeftSudoku[i + 6][j + 6] = solution
            # Top Right
            elif 0 <= i <= 2 and 6 <= j <= 8:
                topRightSudoku[i + 6][j - 6] = solution
            # Bottom Left
            elif 6 <= i <= 8 and 0 <= j <= 2:
                bottomLeftSudoku[i - 6][j + 6] = solution
            # Bottom Right
            elif 6 <= i <= 8 and 6 <= j <= 8:
                bottomRightSudoku[i - 6][j - 6] = solution

            print(f'Center Constraints i: {i} j: {j} solution: {solution}')
        # print('centerCounter ', centerCounter)


def solveSudokuConstraintsHelper():
    for i in range(9):
        for j in range(9):
            if centerSudoku[i][j] == 0:
                solveSudokuConstraints(centerSudoku, i, j)

    for i in range(9):
        for j in range(9):
            if topLeftSudoku[i][j] == 0:
                solveSudokuConstraints(topLeftSudoku, i, j)

    for i in range(9):
        for j in range(9):
            if topRightSudoku[i][j] == 0:
                solveSudokuConstraints(topRightSudoku, i, j)

    for i in range(9):
        for j in range(9):
            if bottomLeftSudoku[i][j] == 0:
                solveSudokuConstraints(bottomLeftSudoku, i, j)

    for i in range(9):
        for j in range(9):
            if bottomRightSudoku[i][j] == 0:
                solveSudokuConstraints(bottomRightSudoku, i, j)


def solveSudoku(grid, number, i=0, j=0):
    if grid == topLeftSudoku:
        # finds the next empty cell
        if number == 1:
            i, j = findNextEmptyCell(grid)
        else:
            i, j = findNextEmptyCellReversed(grid)  # starts reversed

        if i == -1:  # it means that there are no empty cells left
            return True

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidTopLeft(grid, i, j, e):
                grid[i][j] = e
                if number == 1:
                    thread1Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))
                elif number == 6:
                    thread6Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))
                if solveSudoku(grid, number, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == topRightSudoku:
        # finds the next empty cell
        if number == 2:
            i, j = findNextEmptyCell(grid)
        else:
            i, j = findNextEmptyCellReversed(grid)  # starts reversed

        if i == -1:  # it means that there are no empty cells left
            return True

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidTopRight(grid, i, j, e):
                grid[i][j] = e

                if number == 2:
                    thread2Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))
                elif number == 7:
                    thread7Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))

                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == bottomLeftSudoku:
        # finds the next empty cell
        if number == 3:
            i, j = findNextEmptyCell(grid)
        else:
            i, j = findNextEmptyCellReversed(grid)  # starts reversed

        if i == -1:  # it means that there are no empty cells left
            return True

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidBottomLeft(grid, i, j, e):
                grid[i][j] = e

                if number == 3:
                    thread3Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))
                elif number == 8:
                    thread8Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))

                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == bottomRightSudoku:
        # finds the next empty cell
        if number == 4:
            i, j = findNextEmptyCell(grid)
        else:
            i, j = findNextEmptyCellReversed(grid)  # starts reversed
        if i == -1:  # it means that there are no empty cells left
            return True

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidBottomRight(grid, i, j, e):
                grid[i][j] = e

                if number == 4:
                    thread4Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))
                elif number == 9:
                    thread9Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))

                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == centerSudoku:
        global firstTime

        if firstTime:
            # if 0 <= i <= 2 and 0 <= j <= 2:
            for i in range(0, 3):
                for j in range(0, 3):
                    centerSudoku[i][j] = topLeftSudoku[i + 6][j + 6]

            # if 0 <= i <= 2 and 6 <= j <= 8:
            for i in range(0, 3):
                for j in range(6, 9):
                    centerSudoku[i][j] = topRightSudoku[i + 6][j - 6]

            # if 6 <= i <= 8 and 0 <= j <= 2:
            for i in range(6, 9):
                for j in range(0, 3):
                    centerSudoku[i][j] = bottomLeftSudoku[i - 6][j + 6]

            # if 6 <= i <= 8 and 6 <= j <= 8:
            for i in range(6, 9):
                for j in range(6, 9):
                    centerSudoku[i][j] = bottomRightSudoku[i - 6][j - 6]

            firstTime = False

        # finds the next empty cell
        if number == 5:
            i, j = findNextEmptyCell(grid)
        else:
            i, j = findNextEmptyCellReversed(grid)  # starts reversed
        if i == -1:  # it means that there are no empty cells left
            return True
        # print('test ' + 'i: ' + str(i) + ' j: ' + str(j))

        for e in range(1, 10):
            # Try different values in i, j location
            if isValid(grid, i, j, e):
                grid[i][j] = e

                if number == 5:
                    thread5Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))
                elif number == 10:
                    thread10Steps.append('i: ' + str(i) + '  j: ' + str(j) + '  e: ' + str(e))

                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    return False


def printSudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print(' ')
        print(row[0:3], ' ', row[3:6], ' ', row[6:9])
        numrow += 1
    return


def printResult(name, grid):
    print(f'\n------   {name} ------\n')
    printSudoku(grid)


# def gui():
#     window = Tk()  # instantiate an instance of a window
#     # window.geometry("800x800")
#     window.title("Samurai Sudoku")
#     window.configure(bg="white")
#
#     tenThreadsButton = Button(window,
#                               text="solve using 10 threads",
#                               command=lambda: solve(10),
#                               font=("Comic Sans", 25),
#                               padx=25,
#                               pady=25)
#
#     fiveThreadsButton = Button(window,
#                                text="solve using 5 threads",
#                                command=lambda: solve(5),
#                                font=("Comic Sans", 25),
#                                padx=25,
#                                pady=25)
#
#     tenThreadsButton.grid(row=0, column=1)
#     fiveThreadsButton.grid(row=0, column=0)
#     window.mainloop()


def sudokuGui():
    window = Tk()  # instantiate an instance of a window
    # window.geometry("800x800")
    window.title("Samurai Sudoku")
    window.configure(bg="white")

    solve(5)
    solve(10)

    # tenThreadsButton.grid_forget()
    # fiveThreadsButton.grid_forget()
    # Bottom Right
    guiSectors(4, 4, bottomRightSudoku, window)
    # Bottom Left
    guiSectors(4, 0, bottomLeftSudoku, window)
    # Center
    guiSectors(2, 2, centerSudoku, window)
    # Top Right
    guiSectors(0, 4, topRightSudoku, window)
    # Top Left
    guiSectors(0, 0, topLeftSudoku, window)

    window.mainloop()


def graphGui():
    pass


def guiSectors(sectorRow, sectorCol, grid, window):
    for f in range(3):
        for g in range(3):
            frame = Frame(window)
            frame.grid(row=f + sectorRow, column=g + sectorCol)
            frame.config(highlightthickness=1, highlightbackground="blue")

            for i in range(3):
                for j in range(3):
                    e = Entry(frame, width=2, fg='black',
                              font=('Arial', 25, 'bold'),
                              justify='center',
                              )
                    e.grid(row=i, column=j)
                    e.insert(END, grid[i + 3 * f][j + 3 * g])


def writeToTxt(threadNumber):
    with open('thread1.txt', 'w') as thread1FileObject:
        for steps in thread1Steps:
            thread1FileObject.write(steps + '\n')
    with open('thread2.txt', 'w') as thread2FileObject:
        for steps in thread2Steps:
            thread2FileObject.write(steps + '\n')
    with open('thread3.txt', 'w') as thread3FileObject:
        for steps in thread3Steps:
            thread3FileObject.write(steps + '\n')
    with open('thread4.txt', 'w') as thread4FileObject:
        for steps in thread4Steps:
            thread4FileObject.write(steps + '\n')
    with open('thread5.txt', 'w') as thread5FileObject:
        for steps in thread5Steps:
            thread5FileObject.write(steps + '\n')

    if threadNumber == 10:
        with open('thread6.txt', 'w') as thread6FileObject:
            for steps in thread6Steps:
                thread6FileObject.write(steps + '\n')
        with open('thread7.txt', 'w') as thread7FileObject:
            for steps in thread7Steps:
                thread7FileObject.write(steps + '\n')
        with open('thread8.txt', 'w') as thread8FileObject:
            for steps in thread8Steps:
                thread8FileObject.write(steps + '\n')
        with open('thread9.txt', 'w') as thread9FileObject:
            for steps in thread9Steps:
                thread9FileObject.write(steps + '\n')
        with open('thread10.txt', 'w') as thread10FileObject:
            for steps in thread1Steps:
                thread10FileObject.write(steps + '\n')


def solve(threadNumber):

    if threadNumber == 5:
        start = time.perf_counter()

        for c in range(10):
            solveSudokuConstraintsHelper()


        t1 = threading.Thread(target=solveSudoku, args=(topLeftSudoku, 1))
        t2 = threading.Thread(target=solveSudoku, args=(topRightSudoku, 2))
        t3 = threading.Thread(target=solveSudoku, args=(bottomLeftSudoku, 3))
        t4 = threading.Thread(target=solveSudoku, args=(bottomRightSudoku, 4))
        t5 = threading.Thread(target=solveSudoku, args=(centerSudoku, 5))


        # Top Left Sudoku
        t1.start()
        t1.join()

        # Top Right Sudoku
        t2.start()
        t2.join()

        # Bottom Left Sudoku
        t3.start()
        t3.join()

        # Bottom Right Sudoku
        t4.start()
        t4.join()

        # Center Sudoku
        t5.start()
        t5.join()


        writeToTxt(5)
        print('*' * 50)
        print('-- 5 Threads --')
        printResult('topLeftSudoku', topLeftSudoku)
        printResult('topRightSudoku', topRightSudoku)
        printResult('centerSudoku', centerSudoku)
        printResult('bottomLeftSudoku', bottomLeftSudoku)
        printResult('bottomRightSudoku', bottomRightSudoku)

        finish = time.perf_counter()
        print(f'Finished in {finish - start} second(s)\n')
        # graphGui(finish-start)

    elif threadNumber == 10:
        readFromTxt()

        startTenThreads = time.perf_counter()

        for c in range(10):
            solveSudokuConstraintsHelper()


        t1 = threading.Thread(target=solveSudoku, args=(topLeftSudoku, 1))
        t6 = threading.Thread(target=solveSudoku, args=(topLeftSudoku, 6))

        t2 = threading.Thread(target=solveSudoku, args=(topRightSudoku, 2))
        t7 = threading.Thread(target=solveSudoku, args=(topRightSudoku, 7))

        t3 = threading.Thread(target=solveSudoku, args=(bottomLeftSudoku, 3))
        t8 = threading.Thread(target=solveSudoku, args=(bottomLeftSudoku, 8))

        t4 = threading.Thread(target=solveSudoku, args=(bottomRightSudoku, 4))
        t9 = threading.Thread(target=solveSudoku, args=(bottomRightSudoku, 9))

        t5 = threading.Thread(target=solveSudoku, args=(centerSudoku, 5))
        t10 = threading.Thread(target=solveSudoku, args=(centerSudoku, 10))


        # Top Left Sudoku
        t1.start()
        t6.start()

        t1.join()
        t6.join()

        # Top Right Sudoku
        t2.start()
        t7.start()

        t2.join()
        t7.join()

        # Bottom Left Sudoku
        t3.start()
        t8.start()

        t3.join()
        t8.join()

        # Bottom Right Sudoku
        t4.start()
        t9.start()

        t4.join()
        t9.join()

        # Center Sudoku
        t5.start()
        t10.start()

        t5.join()
        t10.join()

        print('*' * 50)
        print('-- 10 Threads --')
        printResult('topLeftSudoku', topLeftSudoku)
        printResult('topRightSudoku', topRightSudoku)
        printResult('centerSudoku', centerSudoku)
        printResult('bottomLeftSudoku', bottomLeftSudoku)
        printResult('bottomRightSudoku', bottomRightSudoku)

        finishTenThreads = time.perf_counter()
        print(f'Finished in {finishTenThreads - startTenThreads} second(s)\n')
        writeToTxt(10)
        # graphGui(finish-startTenThreads)


sudokuGui()
graphGui()


# def solveFiveThreads():
#     start = time.perf_counter()
#
#     for c in range(10):
#         solveSudokuConstraintsHelper()
#
#     print('*' * 50)
#
#     printResult('topLeftSudoku', topLeftSudoku)
#     printResult('topRightSudoku', topRightSudoku)
#     printResult('centerSudoku', centerSudoku)
#     printResult('bottomLeftSudoku', bottomLeftSudoku)
#     printResult('bottomRightSudoku', bottomRightSudoku)
#     print('*' * 50)
#
#     # Top Left Sudoku
#     t1.start()
#     t1.join()
#
#     # Top Right Sudoku
#     t2.start()
#     t2.join()
#
#     # Bottom Left Sudoku
#     t3.start()
#     t3.join()
#
#     # Bottom Right Sudoku
#     t4.start()
#     t4.join()
#
#     # Center Sudoku
#     t5.start()
#     t5.join()
#
#     printResult('topLeftSudoku', topLeftSudoku)
#     printResult('topRightSudoku', topRightSudoku)
#     printResult('centerSudoku', centerSudoku)
#     printResult('bottomLeftSudoku', bottomLeftSudoku)
#     printResult('bottomRightSudoku', bottomRightSudoku)
#     sudokuGui()
#
#     with open('thread1.txt', 'w') as thread1FileObject:
#         for steps in thread1Steps:
#             thread1FileObject.write(steps + '\n')
#     finish = time.perf_counter()
#
#     print(f'Finished in {finish - start} second(s)')


# # Controls if the e value causes the other sudoku to be unsolvable
# def solveSudokuImplications(grid, i, j):
#
#     if grid == topLeftSudoku:
#         topLeftCounter = 0
#         for e in range(1,10):
#             if isValidTopLeft(grid,i,j,e):
#                 topLeftCounter += 1
#         if topLeftCounter >= 1:
#             return True
#         else:
#             return False
#
#     if grid == topRightSudoku:
#         topRightCounter = 0
#         for e in range(1,10):
#             if isValidTopRight(grid,i,j,e):
#                 topRightCounter += 1
#         if topRightCounter >= 1:
#             return True
#         else:
#             return False
#
#     if grid == bottomLeftSudoku:
#         bottomLeftCounter = 0
#         for e in range(1,10):
#             if isValidBottomLeft(grid,i,j,e):
#                 bottomLeftCounter += 1
#         if bottomLeftCounter >= 1:
#             return True
#         else:
#             return False
#
#     if grid == bottomRightSudoku:
#         bottomRightCounter = 0
#         for e in range(1,10):
#             if isValidBottomRight(grid,i,j,e):
#                 bottomRightCounter += 1
#         if bottomRightCounter >= 1:
#             return True
#         else:
#             return False


# def checkOtherSudoku(grid, i, j, e):
#
#     if grid == topLeftSudoku:
#         topRightCounter = 0
#
#         for c in range(0, 3):
#             if topRightSudoku[6][c] == 0:
#
#                 for e in range(1, 10):
#                     if isValidTopRight(grid, i, c, e, ):
#                         topRightCounter += 1
#
#                 if topRightCounter > 0:
#                     return True
#                 else:
#                     return False
#             else:
#                 return True
#
#     return True
