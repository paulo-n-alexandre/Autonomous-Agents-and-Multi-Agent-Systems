
# configs
BOARD_HEIGHT = 11
BOARD_WIDTH = 17
CELL_SIZE = 80
CELL_SPACING = 0
MARGIN = 0
BACKGROUND_IMAGE = "grass"
BOMB_RADIUS = 2
BOMB_TIMER = 7
THINK_TIME = 0.75
SEARCH_THRESHOLD = 10
DESTRUC_PROB = 0.3


def floorToZero(int):
    if int < 0:
        return 0
    return int


def checkMargins(position):
    if 0 <= position[0] < BOARD_HEIGHT and 0 <= position[1] < BOARD_WIDTH:
        return True
    else:
        return False


def checkLeft(position, board, agentCheck=False, destructibleCheck=False):
    if agentCheck:
        if checkMargins((position[0], position[1] - 1)):
            return board[position[0]][position[1] - 1] in (None, "agent1", "agent2", "agent3", "agent4")
        return False
    if destructibleCheck:
        if checkMargins((position[0], position[1] - 1)):
            return board[position[0]][position[1] - 1] in (None, "destructible")
        return False
    if checkMargins((position[0], position[1] - 1)):
        return board[position[0]][position[1] - 1] == None
    return False


def checkRight(position, board, agentCheck=False, destructibleCheck = False):
    if agentCheck:
        if checkMargins((position[0], position[1] + 1)):
            return board[position[0]][position[1] + 1] in (None, "agent1", "agent2", "agent3", "agent4")
        return False
    if destructibleCheck:
        if checkMargins((position[0], position[1] + 1)):
            return board[position[0]][position[1] + 1] in (None, "destructible")
        return False
    if checkMargins((position[0], position[1]+1)):
        return board[position[0]][position[1] + 1] == None
    return False


def checkUp(position, board, agentCheck = False, destructibleCheck = False):
    if agentCheck:
        if checkMargins((position[0] - 1, position[1])):
            return board[position[0] - 1][position[1]] in (None, "agent1", "agent2", "agent3", "agent4")
        return False
    if destructibleCheck:
        if checkMargins((position[0] - 1, position[1])):
            return board[position[0] - 1][position[1]] in (None, "destructible")
        return False
    if checkMargins((position[0] - 1, position[1])):
        return board[position[0] - 1][position[1]] == None
    return False


def checkDown(position, board, agentCheck = False, destructibleCheck = False):
    if agentCheck:
        if checkMargins((position[0] + 1, position[1])):
            return board[position[0] + 1][position[1]] in (None, "agent1", "agent2", "agent3", "agent4")
    if destructibleCheck:
        if checkMargins((position[0] + 1, position[1])):
            return board[position[0] + 1][position[1]] in (None, "destructible")
        return False
    if checkMargins((position[0] + 1, position[1])):
        return board[position[0] + 1][position[1]] == None
    return False


def checkDupesInList(list):
    list_as_set = set(list)
    return len(list) == len(list_as_set)


def relativeSafeFromBomb(bombPosition):
    return (bombPosition[0] != 0 and bombPosition[1] != 0) \
            or bombPosition[0] > BOMB_RADIUS \
            or bombPosition[1] > BOMB_RADIUS \
            or bombPosition[0] < -BOMB_RADIUS \
            or bombPosition[1] < -BOMB_RADIUS

def safeFromDanger(board, position):
    danger = ("explosion1", "explosion2", "explosion3", "explosion4", "bomb", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb")
    blocked = []
    for i in range(1, BOMB_RADIUS+1):
        #check left
        if checkMargins((position[0], position[1] - i)) and board[position[0]][position[1] - i] in danger and "left" not in blocked:
            return False
        elif checkMargins((position[0], position[1] - i)) and board[position[0]][position[1] - i] in ("destructible", "indestructible"):
            blocked.append("left")

        #check right
        if checkMargins((position[0], position[1]+i)) and board[position[0]][position[1] + i] in danger and "right" not in blocked:
            return False
        elif checkMargins((position[0], position[1]+i)) and board[position[0]][position[1] + i] in ("destructible", "indestructible"):
            blocked.append("right")

        #check up
        if checkMargins((position[0] - i, position[1])) and board[position[0] - i][position[1]] in danger and "up" not in blocked:
            return False
        elif checkMargins((position[0] - i, position[1])) and board[position[0] - i][position[1]] in ("destructible", "indestructible"):
            blocked.append("up")

        #check down
        if checkMargins((position[0] + i, position[1])) and board[position[0] + i][position[1]] in danger and "down" not in blocked:
            return False
        elif checkMargins((position[0] + i, position[1])) and board[position[0] + i][position[1]] in ("destructible", "indestructible"):
            blocked.append("down")
    return True

def bombKills(board, targetPosition, position, radius):
    if targetPosition[0] == 0:
        if board[position[0]][position[1] + targetPosition[1] // 2] == "indestructible":
            return False
        return - radius <= targetPosition[1] <= radius
    if targetPosition[1] == 0:
        if board[position[0] + targetPosition[0] // 2][position[1]] == "indestructible":
            return False
        return - radius <= targetPosition[0] <= radius



def simulateAction(currentPosition, move):
    if move == "moveLeft()":
        return (currentPosition[0], currentPosition[1]-1)
    elif move == "moveRight()":
        return (currentPosition[0], currentPosition[1]+1)
    elif move == "moveUp()":
        return (currentPosition[0]-1, currentPosition[1])
    elif move == "moveDown()":
        return (currentPosition[0]+1, currentPosition[1])
    else:
        return currentPosition


def simulateRelativePosition(targetPosition, move):
    if move == "moveLeft()":
        return (targetPosition[0], targetPosition[1]+1)
    if move == "moveRight()":
        return (targetPosition[0], targetPosition[1]-1)
    if move == "moveUp()":
        return (targetPosition[0]+1, targetPosition[1])
    if move == "moveDown()":
        return (targetPosition[0]-1, targetPosition[1])


def printBoard(board, height, width):
    for i in range(height):
        line = ""
        for j in range(width):
            line += " " + str(board[i][j]).ljust(15)
        print(line)


def moveToCenter(position, possibleActions):
    distances = {}
    for action in possibleActions:
        simulatedPosition = simulateAction(position, action)
        distances[action] =  pow(simulatedPosition[0] - BOARD_HEIGHT//2, 2) + pow(simulatedPosition[1] - BOARD_WIDTH//2, 2)
    return [action for action in distances if distances[action] == distances[min(distances, key=distances.get)]]

