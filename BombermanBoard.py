import threading
from game2dboard import Board
from numpy.random import choice
import util
import time

class BombermanBoard:
    def __init__(self, height, width, cell_size, cell_spacing, margin, background_image, destructibleProbability, debugMode=False):
        if debugMode:
            self.Board = []
            for i in range(height):
                self.Board.append([])
                for k in range(width):
                    self.Board[i].append(None)
        else:
            self.Board = Board(height, width)
            self.Board.cell_size = cell_size
            self.Board.cell_spacing = cell_spacing
            self.Board.margin = margin
            self.Board.background_image = background_image
        self.height = height
        self.width = width
        self.destructibleProbability = destructibleProbability
        self.startingWidth = 0
        self.startingHeight = 0
        self.spawnIndestructibleBlocks()
        self.spawnDestructibleBlocks()
        self.gameState = "running"
        self.agents = {}

    def spawnIndestructibleBlocks(self):
        #setup indestructible block
        for i in range(self.height):
            for k in range(self.width):
                if i%2==1 and k%2==1:
                    self.Board[i][k] = "indestructible"

    def spawnDestructibleBlocks(self):
        #setup destrucible block
        for i in range(self.height):
            for k in range(self.width):
                if self.Board[i][k] != "indestructible":
                    if choice([False, True], 1, p=[1-self.destructibleProbability, self.destructibleProbability])[0]:
                        #spawn protection
                        if not (i == 0 and k == 1 or
                                i == 1 and k == 0 or
                                i == self.height-1 and k == 1 or
                                i == self.height-2 and k == 0 or
                                i == 0 and k == self.width-2 or i == 1 and k == self.width-1 or
                                i == self.height-1 and k == self.width-2 or
                                i == self.height-2 and k == self.width-1):
                            self.Board[i][k] = "destructible"

    def initAgents(self, agents):
        for agent in agents:
            self.agents[agent.image] = agent
            self.Board[agent.position[0]][agent.position[1]] = agent.image

    def updateGameState(self):
        agentsAlive = []
        for i in range(self.height):
            for k in range(self.width):
                if self.Board[i][k] in ["agent1", "agent2", "agent3", "agent4"]:
                    agentsAlive.append(self.Board[i][k])
                if self.Board[i][k] in ["agent1bomb", "agent2bomb", "agent3bomb", "agent4bomb"]:
                    agentsAlive.append(self.Board[i][k].split("bomb")[0])

        if len(agentsAlive) == 1:
            self.agents[agentsAlive[0]].gameState = "Game Over"
            self.gameState = "Game Over"
            return agentsAlive[0]
        elif len(agentsAlive) == 0:
            self.gameState = "Game Over"
            return "Draw!"

    def dropBorder(self):
        if self.gameState == "running":
            for i in range(self.startingWidth, self.width - self.startingWidth):
                if self.Board[self.startingHeight][i] == "agent1" or self.Board[self.height - self.startingHeight - 1][i] == "agent1" :
                    self.agents["agent1"].state = "dead"
                    self.agents["agent1"].survival_time = str(round(time.time()- self.agents["agent1"].start_time,2))
                    self.agents["agent1"].diedToBorder = True
                if self.Board[self.startingHeight][i] == "agent2" or self.Board[self.height - self.startingHeight - 1][i] == "agent2" :
                    self.agents["agent2"].state = "dead"
                    self.agents["agent2"].survival_time = str(round(time.time()- self.agents["agent2"].start_time,2))
                    self.agents["agent2"].diedToBorder = True
                if self.Board[self.startingHeight][i] == "agent3" or self.Board[self.height - self.startingHeight - 1][i] == "agent3" :
                    self.agents["agent3"].state = "dead"
                    self.agents["agent3"].survival_time = str(round(time.time()- self.agents["agent3"].start_time,2))
                    self.agents["agent3"].diedToBorder = True
                if self.Board[self.startingHeight][i] == "agent4" or self.Board[self.height - self.startingHeight - 1][i] == "agent4" :
                    self.agents["agent4"].state = "dead"
                    self.agents["agent4"].survival_time = str(round(time.time()- self.agents["agent4"].start_time,2))
                    self.agents["agent4"].diedToBorder = True
                self.Board[self.startingHeight][i] = "indestructible"
                self.Board[self.height - self.startingHeight - 1][i] = "indestructible"
            for i in range(self.startingHeight, self.height - self.startingHeight):
                if self.Board[i][self.startingWidth] == "agent1" or self.Board[i][self.width - self.startingWidth - 1] == "agent1" :
                    self.agents["agent1"].state = "dead"
                    self.agents["agent1"].survival_time = str(round(time.time()- self.agents["agent1"].start_time,2))
                    self.agents["agent1"].diedToBorder = True
                if self.Board[i][self.startingWidth] == "agent2" or self.Board[i][self.width - self.startingWidth - 1] == "agent2" :
                    self.agents["agent2"].state = "dead"
                    self.agents["agent2"].survival_time = str(round(time.time()- self.agents["agent2"].start_time,2))
                    self.agents["agent2"].diedToBorder = True
                if self.Board[i][self.startingWidth] == "agent3" or self.Board[i][self.width - self.startingWidth - 1] == "agent3" :
                    self.agents["agent3"].state = "dead"
                    self.agents["agent3"].survival_time = str(round(time.time()- self.agents["agent3"].start_time,2))
                    self.agents["agent3"].diedToBorder = True
                if self.Board[i][self.startingWidth] == "agent4" or self.Board[i][self.width - self.startingWidth - 1] == "agent4" :
                    self.agents["agent4"].state = "dead"
                    self.agents["agent4"].survival_time = str(round(time.time()- self.agents["agent4"].start_time,2))
                    self.agents["agent4"].diedToBorder = True
                self.Board[i][self.startingWidth] = "indestructible"
                self.Board[i][self.width - self.startingWidth - 1] = "indestructible"
            self.startingWidth += 1
            self.startingHeight += 1
            threading.Timer(10, self.dropBorder).start()





