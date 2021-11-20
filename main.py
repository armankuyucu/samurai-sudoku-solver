import time
import concurrent.futures
import threading

# Global variable set to 0
backtracks = 0

topLeftSudokuString = []
topRightSudokuString = []
bottomLeftSudokuString = []
bottomRightSudokuString = []
centerSudokuString = []

start = time.perf_counter()

# reads the text file
with open('sudoku.txt', 'r') as f:
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


# finds the next empty cell
def findNextEmptyCell(grid):
    for x in range(0, 9):
        for y in range(0, 9):
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
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            [e != centerSudoku[i - 6][x] for x in range(9)])
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all([e != centerSudoku[x][j - 6] for x in range(9)])
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


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where topRightSudoku and centerSudoku intersects
def isValidTopRight(grid, i, j, e):
    if 6 <= i <= 8 and 0 <= j <= 2:
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(e != centerSudoku[i - 6][x] for x in range(9))
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(e != centerSudoku[x][j + 6] for x in range(9))
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


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where bottomLeftSudoku and centerSudoku intersects
def isValidBottomLeft(grid, i, j, e):
    if 0 <= i <= 2 and 6 <= j <= 8:
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(e != centerSudoku[i + 6][x] for x in range(9))
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all(e != centerSudoku[x][j - 6] for x in range(9))
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


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for where bottomRightSudoku and centerSudoku intersects
def isValidBottomRight(grid, i, j, e):
    if 0 <= i <= 2 and 0 <= j <= 2:
        intersectRowOk = all([e != grid[i][x] for x in range(9)]) and all(
            [e != centerSudoku[i + 6][x] for x in range(9)]
            and [e != bottomLeftSudoku[i][x + 6] for x in range(2)])
        if intersectRowOk:
            intersectColumnOk = all(
                [e != grid[x][j] for x in range(9)]) and all([e != centerSudoku[x][j + 6] for x in range(9)])
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


# Checks whether a value is valid by checking rows, columns and 3X3 sectors
# and some additional controls for 4 intersect sectors
def isValidCenter(grid, i, j, e):
    # Top Left Intersect
    if 0 <= i <= 2 and 0 <= j <= 2:
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


def solveSudoku(grid, i=0, j=0):

    # finds the next empty cell
    i, j = findNextEmptyCell(grid)

    if i == -1:  # it means that there are no empty cells left
        return True

    if grid == topLeftSudoku:

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidTopLeft(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == topRightSudoku:

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidTopRight(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == bottomLeftSudoku:

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidBottomLeft(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == bottomRightSudoku:

        for e in range(1, 10):
            # Try different values in i, j location
            if isValidBottomRight(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    elif grid == centerSudoku:
        # if 0 <= i <= 2 and 0 <= j <= 2:
        for i in range(0, 3):
            for j in range(0, 3):
                centerSudoku[i][j] = topLeftSudoku[i + 6][j + 6]

        # elif 0 <= i <= 2 and 6 <= j <= 8:
        for i in range(0, 3):
            for j in range(6, 9):
                centerSudoku[i][j] = topRightSudoku[i + 6][j - 6]

        # elif 6 <= i <= 8 and 0 <= j <= 2:
        for i in range(6, 9):
            for j in range(0, 3):
                centerSudoku[i][j] = bottomLeftSudoku[i - 6][j + 6]

        # elif 6 <= i <= 8 and 6 <= j <= 8:
        for i in range(6, 9):
            for j in range(6, 9):
                centerSudoku[i][j] = bottomRightSudoku[i - 6][j - 6]

        # finds the next empty cell
        i, j = findNextEmptyCell(grid)

        for e in range(1, 10):
            # Try different values in i, j location
            if isValid(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku(grid, i, j):
                    return True

                # Undo the current cell for backtracking
                grid[i][j] = 0

    return False


# def solveSudokuCenter(grid):
#     for i in range(0,3):
#         for j in range(0,3):
#             centerSudoku[i][j] = topLeftSudoku[i+6][j+6]
#
#     for i in range(0,3):
#         for j in range(6,9):
#             centerSudoku[i][j] = topRightSudoku[i+6][j-6]
#
#     for i in range(6,9):
#         for j in range(0,3):
#             centerSudoku[i][j] = bottomLeftSudoku[i-6][j+6]
#
#     for i in range(6,9):
#         for j in range(6,9):
#             centerSudoku[i][j] = bottomRightSudoku[i-6][j-6]
#
#     return solveSudoku(grid)


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


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     f1 = executor.submit(solveSudoku, topLeftSudoku)
#     #print(f1.result())
#
#     f2 = executor.submit(solveSudoku, topRightSudoku)
#     #print(f2.result())
#
#     f4 = executor.submit(solveSudoku, bottomLeftSudoku)
#     #print(f4.result())
#
#     f5 = executor.submit(solveSudoku, bottomRightSudoku)
#     #print(f5.result())
#
#     if f1.done() and f2.done():
#         finish = time.perf_counter()
#         print(f'f1 fone in {finish - start} second(s)')
#         f3 = executor.submit(solveSudokuCenter, centerSudoku)
#         print(f3.result())

t1 = threading.Thread(target=solveSudoku, args=(topLeftSudoku,))
t1.start()
t1.join()

t2 = threading.Thread(target=solveSudoku, args=(topRightSudoku,))
t2.start()
t2.join()

t3 = threading.Thread(target=solveSudoku, args=(bottomLeftSudoku,))
t3.start()
t3.join()

t4 = threading.Thread(target=solveSudoku, args=(bottomRightSudoku,))
t4.start()
t4.join()

t5 = threading.Thread(target=solveSudoku, args=(centerSudoku,))
t5.start()
t5.join()

print('*' * 50)
printResult('topLeftSudoku', topLeftSudoku)

printResult('topRightSudoku', topRightSudoku)

printResult('centerSudoku', centerSudoku)

printResult('bottomLeftSudoku', bottomLeftSudoku)
printResult('bottomRightSudoku', bottomRightSudoku)

# print('\n------ topLeftSudoku ------\n')
# backtracks = 0
# #printSudoku(topLeftSudoku)
# print(solveSudoku(topLeftSudoku))
# printSudoku(topLeftSudoku)
# print('Backtracks = ', backtracks)
#
# print('\n------ topRightSudoku ------\n')
# backtracks = 0
# #printSudoku(topRightSudoku)
# print(solveSudoku(topRightSudoku))
# printSudoku(topRightSudoku)
# print('Backtracks = ', backtracks)
#
# print('\n------ centerSudoku ------\n')
# backtracks = 0
# #printSudoku(centerSudoku)
# print(solveSudoku(centerSudoku))
# printSudoku(centerSudoku)
# print('Backtracks = ', backtracks)
#
# print('\n------ bottomLeftSudoku ------\n')
# backtracks = 0
# #printSudoku(bottomLeftSudoku)
# print(solveSudoku(bottomLeftSudoku))
# printSudoku(bottomLeftSudoku)
# print('Backtracks = ', backtracks)
#
# print('\n------ bottomRightSudoku ------\n')
# backtracks = 0
# #printSudoku(bottomRightSudoku)
# print(solveSudoku(bottomRightSudoku))
# printSudoku(bottomRightSudoku)
# print('Backtracks = ', backtracks)

finish = time.perf_counter()

print(f'Finished in {finish - start} second(s)')
