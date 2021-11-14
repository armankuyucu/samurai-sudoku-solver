# Global variable set to 0
backtracks = 0

topLeftSudokuString = []
topRightSudokuString = []
bottomLeftSudokuString = []
bottomRightSudokuString = []
centerSudokuString = []

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


# finds the next empty square
def findNextEmptyCell(grid):
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


# Checks whether a value is valid by checking rows, columns and sectors
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


def solveSudoku(grid, i=0, j=0):
    global backtracks

    # find the next empty cell
    i, j = findNextEmptyCell(grid)

    if i == -1:  # it means that there are no empty cells left
        return True

    for e in range(1, 10):
        # Try different values in i, j location
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True

            # Undo the current cell for backtracking
            backtracks += 1
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


# input  = [[0,0,0,0,0,0,0,0,0],
#          [0,0,1,0,5,0,7,0,0],
#          [0,5,0,8,9,7,0,6,0],
#          [0,0,7,0,0,0,6,0,0],
#          [0,0,0,0,3,0,0,0,0],
#          [1,2,0,4,0,5,0,8,3],
#          [0,0,3,0,4,0,5,0,0],
#          [7,0,0,0,0,0,0,0,1],
#          [8,0,0,9,0,1,0,0,6]]

# print('------')
# backtracks = 0
# printSudoku(input)
# print(solveSudoku(input))
# printSudoku(input)
# print ('Backtracks = ', backtracks)

print('\n------ topLeftSudoku ------\n')
backtracks = 0
printSudoku(topLeftSudoku)
print(solveSudoku(topLeftSudoku))
printSudoku(topLeftSudoku)
print('Backtracks = ', backtracks)

print('\n------ topRightSudoku ------\n')
backtracks = 0
printSudoku(topRightSudoku)
print(solveSudoku(topRightSudoku))
printSudoku(topRightSudoku)
print('Backtracks = ', backtracks)

print('\n------ bottomLeftSudoku ------\n')
backtracks = 0
printSudoku(bottomLeftSudoku)
print(solveSudoku(bottomLeftSudoku))
printSudoku(bottomLeftSudoku)
print('Backtracks = ', backtracks)

print('\n------ bottomRightSudoku ------\n')
backtracks = 0
printSudoku(bottomRightSudoku)
print(solveSudoku(bottomRightSudoku))
printSudoku(bottomRightSudoku)
print('Backtracks = ', backtracks)

print('\n------ centerSudoku ------\n')
backtracks = 0
printSudoku(centerSudoku)
print(solveSudoku(centerSudoku))
printSudoku(centerSudoku)
print('Backtracks = ', backtracks)
