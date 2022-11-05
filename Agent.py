from copy import copy
import util
import numpy as np
import threading
import datetime
import time
from util import *


class Agent:
    def __init__(self, name, image, bomb, onbomb, position, board):
        self.state = "alive"
        self.name = name
        self.image = image
        self.bomb = bomb
        self.onbomb = onbomb
        self.position = position
        self.bombermanBoard = board
        self.history = []
        self.thinkTime = THINK_TIME
        self.n_bombs_placed = 0
        self.bomb.owner = self
        self.diedToBorder = False
        self.start_time = time.time()
        self.survival_time = 0

    def placeBomb(self):
        if self.bomb.state == "backpack":
            self.bomb.placeBomb(self.position[0], self.position[1], self.onbomb)
            self.n_bombs_placed += 1


    def moveLeft(self):
        if checkMargins((self.position[0], self.position[1]-1)):
            self.move(self.position[0],self.position[1]-1)

    def moveRight(self):
        if checkMargins((self.position[0], self.position[1]+1)):
            self.move(self.position[0],self.position[1]+1)

    def moveUp(self):
        if checkMargins((self.position[0]-1, self.position[1])):
            self.move(self.position[0]-1, self.position[1])

    def moveDown(self):
        if checkMargins((self.position[0]+1, self.position[1])):
            self.move(self.position[0]+1, self.position[1])

    def move(self, newRow, newCol):
        if self.bombermanBoard.Board[newRow][newCol] in ("explosion1", "explosion2", "explosion3", "explosion4"):
            self.state = "dead"
            self.survival_time = str(round(time.time()- self.start_time,2))
        elif self.bombermanBoard.Board[newRow][newCol] == None:
            self.bombermanBoard.Board[newRow][newCol] = self.image
        #elif self.bombermanBoard.Board[newRow][newCol] in ("destructible", "indestructible", "agent1", "agent2", "agent3", "agent4", "bomb"):
        else:
            return
        if self.bombermanBoard.Board[self.position[0]][self.position[1]] == self.onbomb:
            self.bombermanBoard.Board[self.position[0]][self.position[1]] = "bomb"
        elif self.bombermanBoard.Board[self.position[0]][self.position[1]] == self.image:
            self.bombermanBoard.Board[self.position[0]][self.position[1]] = None
        self.position = (newRow, newCol)
        #self.Board[self.position[0]][self.position[1]] = "bomb" if self.Board[self.position[0]][self.position[1]] == self.onbomb else None


    def makeHistory(self, action, old_position):
        step = {}
        step["action"] = {"name": str(action)}
        if action in ("moveLeft()", "moveRight()", "moveDown()", "moveUp()"):
            step["action"]["old_position"] = old_position
            step["action"]["new_position"] = self.position
        elif action == "placeBomb()":
            step["action"]["bomb_in"] = self.position
        step["timestamp"] = str(datetime.datetime.now())
        self.history.append(step)


    def lookForBomb(self, board):
        bombs = ("bomb", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb")
        blocked = []
        if board[self.position[0]][self.position[1]] == self.onbomb: return (0,0)
        for i in range(1, self.bomb.radius+1):
            #check left
            if checkMargins((self.position[0], self.position[1] - i)) and board[self.position[0]][self.position[1] - i] in bombs and "left" not in blocked:
                return (0, -i)
            elif checkMargins((self.position[0], self.position[1] - i)) and board[self.position[0]][self.position[1] - i] in ("destructible", "indestructible"):
                blocked.append("left")

            #check right
            if checkMargins((self.position[0], self.position[1]+i)) and board[self.position[0]][self.position[1] + i] in bombs and "right" not in blocked:
                return (0, i)
            elif checkMargins((self.position[0], self.position[1]+i)) and board[self.position[0]][self.position[1] + i] in ("destructible", "indestructible"):
                blocked.append("right")

            #check up
            if checkMargins((self.position[0] - i, self.position[1])) and board[self.position[0] - i][self.position[1]] in bombs and "up" not in blocked:
                return (-i, 0)
            elif checkMargins((self.position[0] - i, self.position[1])) and board[self.position[0] - i][self.position[1]] in ("destructible", "indestructible"):
                blocked.append("up")

            #check down
            if checkMargins((self.position[0] + i, self.position[1])) and board[self.position[0] + i][self.position[1]] in bombs and "down" not in blocked:
                return (i, 0)
            elif checkMargins((self.position[0] + i, self.position[1])) and board[self.position[0] + i][self.position[1]] in ("destructible", "indestructible"):
                blocked.append("down")
        return None

    def lookForAgent(self, board, enemyAgents):
        blocked = []
        for i in range(1, self.bomb.radius+1):
            #check left
            if checkMargins((self.position[0], self.position[1] - i)) and board[self.position[0]][self.position[1] - i] in enemyAgents and "left" not in blocked:
                return (0, -i)
            elif checkMargins((self.position[0], self.position[1] - i)) and board[self.position[0]][self.position[1] - i] in ("destructible", "indestructible"):
                blocked.append("left")

            #check right
            if checkMargins((self.position[0], self.position[1]+i)) and board[self.position[0]][self.position[1]+i] in ("agent1", "agent3", "agent4") and "right" not in blocked:
                return (0, i)
            elif checkMargins((self.position[0], self.position[1]+i)) and board[self.position[0]][self.position[1] + i] in ("destructible", "indestructible"):
                blocked.append("right")

            #check up
            if checkMargins((self.position[0] - i, self.position[1])) and board[self.position[0]-i][self.position[1]] in ("agent1", "agent3", "agent4") and "up" not in blocked:
                return (-i, 0)
            elif checkMargins((self.position[0] - i, self.position[1])) and board[self.position[0] - i][self.position[1]] in ("destructible", "indestructible"):
                blocked.append("up")

            #check down
            if checkMargins((self.position[0] + i, self.position[1])) and board[self.position[0]+i][self.position[1]] in ("agent1", "agent3", "agent4") and "down" not in blocked:
                return (i, 0)
            elif checkMargins((self.position[0] + i, self.position[1])) and board[self.position[0] + i][self.position[1]] in ("destructible", "indestructible"):
                blocked.append("down")
        return None

    def lookForDestructible(self, board):
        #check left
        if checkMargins((self.position[0], self.position[1] - 1)) and board[self.position[0]][self.position[1] - 1] == "destructible":
            return (0, -1)
        #check right
        if checkMargins((self.position[0], self.position[1]+1)) and board[self.position[0]][self.position[1]+1] == "destructible":
            return (0, 1)
        #check up
        if checkMargins((self.position[0]-1, self.position[1])) and board[util.floorToZero(self.position[0]-1)][self.position[1]] == "destructible":
            return (-1, 0)
        #check down
        if checkMargins((self.position[0]+1, self.position[1])) and board[self.position[0]+1][self.position[1]] == "destructible":
            return (1, 0)
        return None

    def doAction(self, action):
        if action == None:
            return
        else:
            eval("self." + action)

    def randomMove(self):
        return np.random.choice(["moveLeft()", "moveRight()", "moveDown()", "moveUp()"], 1)[0]

    def randomActionFromList(self, possibleActions):
        if len(possibleActions):
            return np.random.choice(moveToCenter(self.position, possibleActions), 1)[0]
        else:
            return None
    def reactToBomb(self, bombPosition, board):
        #react to bomb
        if bombPosition == None:
            return None
        elif bombPosition == (0,0):
            #bomb is on me
            possibleActions = []
            #check if left is free
            if checkLeft(self.position, board):
                possibleActions.append("moveLeft()")
            #check if right is free
            if checkRight(self.position, board):
                possibleActions.append("moveRight()")
            #check if up is free
            if checkUp(self.position, board):
                possibleActions.append("moveUp()")
            #check if down is free
            if checkDown(self.position, board):
                possibleActions.append("moveDown()")
            return self.randomActionFromList(possibleActions)
        elif bombPosition[0] < 0:
            #bomb is above me
            possibleActions = []
            #check if left is free
            if checkLeft(self.position, board):
                possibleActions.append("moveLeft()")
            #check if right is free
            if checkRight(self.position, board):
                possibleActions.append("moveRight()")
            #go in the opposite direction of the bomb
            if len(possibleActions) == 0 and checkDown(self.position, board):
                possibleActions.append("moveDown()")
            action = self.randomActionFromList(possibleActions)
            return action
        elif bombPosition[0] > 0:
            #bomb is below me
            possibleActions = []
            #check if left is free
            if checkLeft(self.position, board):
                possibleActions.append("moveLeft()")
            #check if right is free
            if checkRight(self.position, board):
                possibleActions.append("moveRight()")
            #go in the opposite direction of the bomb
            if len(possibleActions) == 0 and checkUp(self.position, board):
                possibleActions.append("moveUp()")

            action = self.randomActionFromList(possibleActions)
            return action
        elif bombPosition[1] < 0:
            #bomb is on my left
            possibleActions = []
            #check if up is free
            if checkUp(self.position, board):
                possibleActions.append("moveUp()")
            #check if down is free
            if checkDown(self.position, board):
                possibleActions.append("moveDown()")
            #go in the opposite direction of the bomb
            if len(possibleActions) == 0 and checkRight(self.position, board):
                possibleActions.append("moveRight()")
            action = self.randomActionFromList(possibleActions)
            return action
        elif bombPosition[1] > 0:
            #bomb is on my right
            possibleActions = []
            #check if up is free
            if checkUp(self.position, board):
                possibleActions.append("moveUp()")
            #check if down is free
            if checkDown(self.position, board):
                possibleActions.append("moveDown()")
            #go in the opposite direction of the bomb
            if len(possibleActions) == 0 and checkLeft(self.position, board):
                possibleActions.append("moveLeft()")
            action = self.randomActionFromList(possibleActions)
            return action

    def reactToDestructible(self, destructiblePosition):
        return None if destructiblePosition == None or self.bomb.state == "placed" else "placeBomb()"

    def reactToAgent(self, agentPosition):
        return None if agentPosition == None or self.bomb.state == "placed" else "placeBomb()"



class RandomAgent(Agent):
    def decideAction(self):
        if self.state == "alive" and self.bombermanBoard.gameState == "running":
            old_position = self.position
            action = np.random.choice(["moveLeft()", "moveRight()", "moveDown()", "moveUp()", "placeBomb()", None], 1)[0]
            self.doAction(action)
            self.makeHistory(action, old_position)
            threading.Timer(self.thinkTime, self.decideAction).start()


class ReactiveAgent(Agent):
    def decideAction(self):
        if self.state == "alive" and self.bombermanBoard.gameState == "running":
            bombIn = self.lookForBomb(self.bombermanBoard.Board)
            old_position = self.position

            action = self.reactToBomb(bombIn, self.bombermanBoard.Board)
            if action == None:
                #there is no bomb nearby
                enemyAgents = ["agent1", "agent2", "agent3", "agent4", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb"]
                enemyAgents.remove(self.image)
                enemyAgents.remove(self.onbomb)
                agentIn = self.lookForAgent(self.bombermanBoard.Board, enemyAgents)
                action = self.reactToAgent(agentIn)
                if action == None:
                    #there is no enemy agent nearby
                    destructibleIn = self.lookForDestructible(self.bombermanBoard.Board)
                    action = self.reactToDestructible(destructibleIn)
            if action == None:
                #there is no reaction - will do a random movement
                possibleActions = []
                if checkUp(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveUp()")
                if checkDown(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveDown()")
                if checkLeft(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveLeft()")
                if checkRight(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveRight()")
                action = self.randomActionFromList(possibleActions)

            self.doAction(action)
            self.makeHistory(action, old_position)
            threading.Timer(self.thinkTime, self.decideAction).start()

class DeliberativeAgent(Agent):
    plan = []
    beliefs = []
    desires = []
    intention = {}
    def updateBeliefs(self):
        self.beliefs = copy(self.bombermanBoard.Board)

    def succeededIntention(self):
        if list(self.intention.keys())[0] in ("kill enemy", "destroy block"):
            return self.bomb.state == "placed"
        else:
            return self.lookForBomb(self.beliefs) == None

    def impossibleIntention(self):
        if list(self.intention.keys())[0] == "destroy block":
            destructiblePosition = self.intention["destroy block"][1]
            return self.beliefs[destructiblePosition[0]][destructiblePosition[1]] == None
        elif list(self.intention.keys())[0] == "kill enemy":
            enemies = ["agent1", "agent2", "agent3", "agent4", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb" ]
            enemies.remove(self.image)
            enemies.remove(self.onbomb)
            planPosition = self.position
            for action in self.plan[:-1]:
                planPosition = simulateAction(planPosition, action)
            for i in range(BOMB_RADIUS+1):
                positionToCheck = (planPosition[0]+i, planPosition[1])
                if checkMargins(positionToCheck) and self.beliefs[positionToCheck[0]][positionToCheck[1]] in enemies:
                    return False
                positionToCheck = (planPosition[0]-i, planPosition[1])
                if checkMargins(positionToCheck) and self.beliefs[positionToCheck[0]][positionToCheck[1]] in enemies:
                    return False
                positionToCheck = (planPosition[0], planPosition[1]+i)
                if checkMargins(positionToCheck) and self.beliefs[positionToCheck[0]][positionToCheck[1]] in enemies:
                    return False
                positionToCheck = (planPosition[0], planPosition[1]-i)
                if checkMargins(positionToCheck) and self.beliefs[positionToCheck[0]][positionToCheck[1]] in enemies:
                    return False
            #print(self.name, "impossible to kill")
            return True


    def isPlanSound(self, action):
        try:
            if list(self.intention.keys())[0] != "escape bomb":
                return safeFromDanger(self.beliefs, simulateAction(self.position, action))
            return True
        except:
            return safeFromDanger(self.beliefs, simulateAction(self.position, action))


    def searchForAgent(self, pathActions=None):
        enemies = ["agent1", "agent2", "agent3", "agent4", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb" ]
        enemies.remove(self.image)
        enemies.remove(self.onbomb)
        if pathActions is None:
            pathActions = []
            if checkLeft(self.position, self.beliefs, True):
                pathActions.append(["moveLeft()"])
                simulatedPosition = simulateAction(self.position, "moveLeft()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] in enemies:
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if checkRight(self.position, self.beliefs, True):
                pathActions.append(["moveRight()"])
                simulatedPosition = simulateAction(self.position, "moveRight()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] in enemies:
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if checkUp(self.position, self.beliefs, True):
                pathActions.append(["moveUp()"])
                simulatedPosition = simulateAction(self.position, "moveUp()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] in enemies:
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if checkDown(self.position, self.beliefs, True):
                pathActions.append(["moveDown()"])
                simulatedPosition = simulateAction(self.position, "moveDown()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] in enemies:
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if len(pathActions) == 0:
                return None
        newPlans = []
        for plan in pathActions:
            planPosition = self.position
            for action in plan:
                planPosition = simulateAction(planPosition, action)
            possibleActions = []
            if len(plan) > SEARCH_THRESHOLD:
                continue
            if self.beliefs[planPosition[0]][planPosition[1]] in enemies:
                return (planPosition[0] - self.position[0], planPosition[1] - self.position[1]), planPosition
            if checkLeft(planPosition, self.beliefs, True) and plan[-1] != "moveRight()":
                possibleActions.append("moveLeft()")
            if checkRight(planPosition, self.beliefs, True) and plan[-1] != "moveLeft()":
                possibleActions.append("moveRight()")
            if checkUp(planPosition, self.beliefs, True) and plan[-1] != "moveDown()":
                possibleActions.append("moveUp()")
            if checkDown(planPosition, self.beliefs, True) and plan[-1] != "moveUp()":
                possibleActions.append("moveDown()")
            for possibleAction in possibleActions:
                newPlans.append([*plan, possibleAction])
        if len(newPlans) == 0:
            return None
        return self.searchForAgent(newPlans)

    def searchForDestructible(self, pathActions=None):
        if pathActions is None:
            pathActions = []
            if checkLeft(self.position, self.beliefs, destructibleCheck=True):
                pathActions.append(["moveLeft()"])
                simulatedPosition = simulateAction(self.position, "moveLeft()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] == "destructible":
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if checkRight(self.position, self.beliefs, destructibleCheck=True):
                pathActions.append(["moveRight()"])
                simulatedPosition = simulateAction(self.position, "moveRight()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] == "destructible":
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if checkUp(self.position, self.beliefs, destructibleCheck=True):
                pathActions.append(["moveUp()"])
                simulatedPosition = simulateAction(self.position, "moveUp()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] == "destructible":
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if checkDown(self.position, self.beliefs, destructibleCheck=True):
                pathActions.append(["moveDown()"])
                simulatedPosition = simulateAction(self.position, "moveDown()")
                if self.beliefs[simulatedPosition[0]][simulatedPosition[1]] == "destructible":
                    return (self.position[0] - simulatedPosition[0], self.position[1] - simulatedPosition[1]), simulatedPosition
            if len(pathActions) == 0:
                return None
        newPlans = []
        for plan in pathActions:
            planPosition = self.position
            for action in plan:
                planPosition = simulateAction(planPosition, action)
            possibleActions = []
            if len(plan) > SEARCH_THRESHOLD // 2:
                continue
            if self.beliefs[planPosition[0]][planPosition[1]] == "destructible":
                return (planPosition[0] - self.position[0], planPosition[1] - self.position[1]), planPosition
            if checkLeft(planPosition, self.beliefs, destructibleCheck=True) and plan[-1] != "moveRight()":
                possibleActions.append("moveLeft()")
            if checkRight(planPosition, self.beliefs, destructibleCheck=True) and plan[-1] != "moveLeft()":
                possibleActions.append("moveRight()")
            if checkUp(planPosition, self.beliefs, destructibleCheck=True) and plan[-1] != "moveDown()":
                possibleActions.append("moveUp()")
            if checkDown(planPosition, self.beliefs, destructibleCheck=True) and plan[-1] != "moveUp()":
                possibleActions.append("moveDown()")
            for possibleAction in possibleActions:
                newPlans.append([*plan, possibleAction])
        if len(newPlans) == 0:
            return None
        return self.searchForDestructible(newPlans)

    def deliberate(self):
        self.desires = []
        #these are relative positions
        bombPosition = self.lookForBomb(self.beliefs)
        enemyPosition = self.searchForAgent()
        destructiblePosition = self.searchForDestructible()
        self.intention = {}
        if bombPosition:
            self.intention = {"escape bomb": bombPosition}
        elif enemyPosition and self.bomb.state == "backpack":
            self.intention = {"kill enemy": enemyPosition}
        elif destructiblePosition and self.bomb.state == "backpack":
            self.intention = {"destroy block": destructiblePosition}


    def buildPlan(self):
        self.plan = []
        if len(self.intention) == 0:
            return
        intention = list(self.intention.keys())[0]
        if intention == "escape bomb":
            self.plan = self.buildPathEscape(self.intention[intention])
        elif intention == "kill enemy":
            self.plan = self.buildPathBombPlace(self.intention[intention][0], self.bomb.radius)
        elif intention == "destroy block":
            self.plan = self.buildPathBombPlace(self.intention[intention][0], 1)

    def buildPathEscape(self, bombPosition, plansList=None):
        if plansList is None:
            plansList = []
            if checkLeft(self.position, self.beliefs):
                plansList.append(["moveLeft()"])
                if relativeSafeFromBomb(simulateRelativePosition(bombPosition, "moveLeft()")):
                    return ["moveLeft()"]
            if checkRight(self.position, self.beliefs):
                plansList.append(["moveRight()"])
                if relativeSafeFromBomb(simulateRelativePosition(bombPosition, "moveRight()")):
                    return ["moveRight()"]
            if checkDown(self.position, self.beliefs):
                plansList.append(["moveDown()"])
                if relativeSafeFromBomb(simulateRelativePosition(bombPosition, "moveDown()")):
                    return ["moveDown()"]
            if checkUp(self.position, self.beliefs):
                plansList.append(["moveUp()"])
                if relativeSafeFromBomb(simulateRelativePosition(bombPosition, "moveUp()")):
                    return ["moveUp()"]
            if len(plansList) == 0:
                return []
        newPlans = []
        for plan in plansList:
            planPosition = self.position
            planBombPosition = bombPosition
            if len(plan) > self.bomb.radius*2+1:
                continue
            for action in plan:
                planPosition = simulateAction(planPosition, action)
                planBombPosition = simulateRelativePosition(planBombPosition, action)
            possibleActions = []
            if checkLeft(planPosition, self.beliefs) and plan[-1] != "moveRight()":
                possibleActions.append("moveLeft()")
                if relativeSafeFromBomb(simulateRelativePosition(planBombPosition, "moveLeft()")):
                    return [*plan, "moveLeft()"]
            if checkRight(planPosition, self.beliefs)and plan[-1] != "moveLeft()":
                possibleActions.append("moveRight()")
                if relativeSafeFromBomb(simulateRelativePosition(planBombPosition, "moveRight()")):
                    return [*plan, "moveRight()"]
            if checkUp(planPosition, self.beliefs) and plan[-1] != "moveDown()":
                possibleActions.append("moveUp()")
                if relativeSafeFromBomb(simulateRelativePosition(planBombPosition, "moveUp()")):
                    return [*plan, "moveUp()"]
            if checkDown(planPosition, self.beliefs) and plan[-1] != "moveUp()":
                possibleActions.append("moveDown()")
                if relativeSafeFromBomb(simulateRelativePosition(planBombPosition, "moveDown()")):
                    return [*plan, "moveDown()"]
            for possibleAction in possibleActions:
                newPlans.append([*plan, possibleAction])
        if len(newPlans) == 0:
            return newPlans
        return self.buildPathEscape(bombPosition, newPlans)

    def buildPathBombPlace(self, targetPosition, radius, plansList=None):
        if plansList is None:
            plansList = []
            if bombKills(self.beliefs, targetPosition, self.position, radius):
                return ["placeBomb()"]
            if checkLeft(self.position, self.beliefs):
                plansList.append(["moveLeft()"])
            if checkRight(self.position, self.beliefs):
                plansList.append(["moveRight()"])
            if checkDown(self.position, self.beliefs):
                plansList.append(["moveDown()"])
            if checkUp(self.position, self.beliefs):
                plansList.append(["moveUp()"])
            if len(plansList) == 0:
                return []
        newPlans = []
        for plan in plansList:
            planPosition = self.position
            planAgentPosition = targetPosition
            if len(plan) > SEARCH_THRESHOLD:
                continue
            for action in plan:
                planPosition = simulateAction(planPosition, action)
                planAgentPosition = simulateRelativePosition(planAgentPosition, action)
            possibleActions = []
            if bombKills(self.beliefs, planAgentPosition, planPosition, radius):
                return [*plan, "placeBomb()"]
            if checkLeft(planPosition, self.beliefs) and plan[-1] != "moveRight()":
                possibleActions.append("moveLeft()")
            if checkRight(planPosition, self.beliefs) and plan[-1] != "moveLeft()":
                possibleActions.append("moveRight()")
            if checkUp(planPosition, self.beliefs) and plan[-1] != "moveDown()":
                possibleActions.append("moveUp()")
            if checkDown(planPosition, self.beliefs) and plan[-1] != "moveUp()":
                possibleActions.append("moveDown()")
            for possibleAction in possibleActions:
                newPlans.append([*plan, possibleAction])
        if len(newPlans) == 0:
            return newPlans
        return self.buildPathBombPlace(targetPosition, radius, newPlans)

    def reactDecision(self):
        if self.state == "alive" and self.bombermanBoard.gameState == "running":
            bombIn = self.lookForBomb(self.bombermanBoard.Board)
            old_position = self.position

            action = self.reactToBomb(bombIn, self.bombermanBoard.Board)
            if action == None:
                #there is no bomb nearby
                enemyAgents = ["agent1", "agent2", "agent3", "agent4", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb"]
                enemyAgents.remove(self.image)
                enemyAgents.remove(self.onbomb)
                agentIn = self.lookForAgent(self.bombermanBoard.Board, enemyAgents)
                action = self.reactToAgent(agentIn)
                if action == None:
                    #there is no enemy agent nearby
                    destructibleIn = self.lookForDestructible(self.bombermanBoard.Board)
                    action = self.reactToDestructible(destructibleIn)
            if action == None:
                #there is no reaction - will do a random movement
                possibleActions = []
                if checkUp(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveUp()")
                if checkDown(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveDown()")
                if checkLeft(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveLeft()")
                if checkRight(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveRight()")
                action = self.randomActionFromList(possibleActions)
            return action
        return None

    def decideReactiveAction(self, old_position):
        action = self.reactDecision()
        if self.isPlanSound(action):
            self.doAction(action)
            self.makeHistory(action, old_position)
        else:
            action = None
            self.doAction(action)
            self.makeHistory(action, old_position)
    def decideAction(self):
        if self.state == "alive" and self.bombermanBoard.gameState == "running":
            old_position = self.position
            self.updateBeliefs()

            if len(self.plan) != 0 and not self.succeededIntention() and not self.impossibleIntention():
                #print("succeded intention", self.succeededIntention())
                #print("impossible intention", self.impossibleIntention())
                action = self.plan[0]
                #print("my plan", self.plan)
                self.plan = self.plan[1:]
                if self.isPlanSound(action):
                    self.doAction(action)
                    self.makeHistory(action, old_position)
                else:
                    self.decideReactiveAction(old_position)

            else:
                self.deliberate()
                #print(self.name ,"my intention", self.intention)
                self.buildPlan()
                if len(self.plan) == 0:
                    self.decideReactiveAction(old_position)
            threading.Timer(self.thinkTime, self.decideAction).start()


class ReflexAgent(Agent):
    def bombReflex(self, bombPosition, board):
        #react to bomb
        if bombPosition == None:
            return None
        else:
            possibleActions = []
            #check if left is free
            if checkLeft(self.position, board):
                if self.safeLeft(bombPosition):
                    possibleActions.append("moveLeft()")
            #check if right is free
            if checkRight(self.position, board):
                if self.safeRight(bombPosition):
                    possibleActions.append("moveRight()")
            #check if up is free
            if checkUp(self.position, board):
                if self.safeUp(bombPosition):
                    possibleActions.append("moveUp()")
            #check if down is free
            if checkDown(self.position, board):
                if self.safeDown(bombPosition):
                    possibleActions.append("moveDown()")
            safePossibleActions = []
            for action in possibleActions:
                if safeFromDanger(self.bombermanBoard.Board, simulateAction(self.position, action)):
                    safePossibleActions.append(action)
            if len(safePossibleActions) > 0:
                return self.randomActionFromList(safePossibleActions)
            return self.randomActionFromList(possibleActions)



    def safeLeft(self, bombRelativePosition):
        simulatedPosition = simulateAction(self.position, "moveLeft()")
        moves = 1
        while moves <= BOMB_RADIUS+1 - abs(bombRelativePosition[1]):
            if checkUp(simulatedPosition, self.bombermanBoard.Board) or checkDown(simulatedPosition, self.bombermanBoard.Board):
                return True
            if checkLeft(simulatedPosition, self.bombermanBoard.Board):
                moves += 1
                simulatedPosition = simulateAction(simulatedPosition, "moveLeft()")
            else:
                return False
        return True

    def safeRight(self, bombRelativePosition):
        simulatedPosition = simulateAction(self.position, "moveRight()")
        moves = 1
        while moves <= BOMB_RADIUS+1 - abs(bombRelativePosition[1]):
            if checkUp(simulatedPosition, self.bombermanBoard.Board) or checkDown(simulatedPosition, self.bombermanBoard.Board):
                return True
            if checkRight(simulatedPosition, self.bombermanBoard.Board):
                moves += 1
                simulatedPosition = simulateAction(simulatedPosition, "moveRight()")
            else:
                return False
        return True

    def safeUp(self, bombRelativePosition):
        simulatedPosition = simulateAction(self.position, "moveUp()")
        moves = 1
        while moves <= BOMB_RADIUS+1 - abs(bombRelativePosition[0]):
            if checkLeft(simulatedPosition, self.bombermanBoard.Board) or checkRight(simulatedPosition, self.bombermanBoard.Board):
                return True
            if checkUp(simulatedPosition, self.bombermanBoard.Board):
                moves += 1
                simulatedPosition = simulateAction(simulatedPosition, "moveUp()")
            else:
                return False
        return True

    def safeDown(self, bombRelativePosition):
        simulatedPosition = simulateAction(self.position, "moveDown()")
        moves = 1
        while moves <= BOMB_RADIUS+1 - abs(bombRelativePosition[0]):
            if checkLeft(simulatedPosition, self.bombermanBoard.Board) or checkRight(simulatedPosition, self.bombermanBoard.Board):
                return True
            if checkDown(simulatedPosition, self.bombermanBoard.Board):
                moves += 1
                simulatedPosition = simulateAction(simulatedPosition, "moveDown()")
            else:
                return False
        return True

    def decideAction(self):
        if self.state == "alive" and self.bombermanBoard.gameState == "running":
            bombIn = self.lookForBomb(self.bombermanBoard.Board)

            old_position = self.position
            possibleActions = []

            action = self.bombReflex(bombIn, self.bombermanBoard.Board)
            if action == None:
                #there is no bomb nearby
                enemyAgents = ["agent1", "agent2", "agent3", "agent4", "agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb"]
                enemyAgents.remove(self.image)
                enemyAgents.remove(self.onbomb)
                agentIn = self.lookForAgent(self.bombermanBoard.Board, enemyAgents)
                action = self.reactToAgent(agentIn)
                #print("react agent", action)
                if action == None:
                    #there is no enemy agent nearby
                    destructibleIn = self.lookForDestructible(self.bombermanBoard.Board)
                    action = self.reactToDestructible(destructibleIn)
                    #print("destructible react", action)

            if action == None:
                #there is no reaction - will do a random movement
                if checkUp(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveUp()")
                if checkDown(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveDown()")
                if checkLeft(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveLeft()")
                if checkRight(self.position, self.bombermanBoard.Board):
                    possibleActions.append("moveRight()")
                safePossibleActions = []
                for action in possibleActions:
                    if safeFromDanger(self.bombermanBoard.Board, simulateAction(self.position, action)):
                        safePossibleActions.append(action)
                action = self.randomActionFromList(safePossibleActions)
                self.doAction(action)


            else:
                self.doAction(action)
            self.makeHistory(action, old_position)
            threading.Timer(self.thinkTime, self.decideAction).start()




