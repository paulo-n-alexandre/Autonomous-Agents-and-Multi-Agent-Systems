import threading
import util
import time

class Bomb:
    def __init__(self, radius, board, timer, explosion):
        self.radius = radius
        self.owner = None
        self.state = "backpack"
        self.bomb = "bomb"
        self.explosion = explosion
        self.bombermanBoard = board
        self.timer = timer
        self.blocksDestroyed = 0
        self.enemiesKilled = 0
        self.selfKill = False


    def placeBomb(self, row, col, onbomb):
        self.positionsToClean = set()
        self.state = "placed"
        self.position = (row, col)
        self.bombermanBoard.Board[row][col] = onbomb
        threading.Timer(self.timer, self.explode).start()

    def upExplosion(self):
        try:
            for i in range(self.radius+1):
                if self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]] != "indestructible":
                    self.positionsToClean.add(tuple([util.floorToZero(self.position[0]-i), self.position[1]]))
                    if self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]] == "destructible":
                        self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]] = self.explosion
                        self.blocksDestroyed += 1
                        break
                    if self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]] in ("agent1", "agent2", "agent3", "agent4",
                                                                                                             "agent1bomb","agent2bomb","agent3bomb","agent4bomb"):
                        agent = self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]].split("b")[0]
                        self.bombermanBoard.agents[agent].state = "dead"
                        self.bombermanBoard.agents[agent].survival_time = str(round(time.time() -  self.bombermanBoard.agents[agent].start_time ,2))

                        if self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]] in (self.owner.onbomb, self.owner.image):
                            self.selfKill = True
                        else:
                            self.enemiesKilled += 1

                    self.bombermanBoard.Board[util.floorToZero(self.position[0]-i)][self.position[1]] = self.explosion
                else:
                    break
        except:
            pass

    def rightExplosion(self):
        try:
            for i in range(self.radius+1):
                if self.bombermanBoard.Board[self.position[0]][self.position[1]+i] != "indestructible":
                    self.positionsToClean.add(tuple([self.position[0], self.position[1]+i]))
                    if self.bombermanBoard.Board[self.position[0]][self.position[1]+i] == "destructible":
                        self.bombermanBoard.Board[self.position[0]][self.position[1]+i] = self.explosion
                        self.blocksDestroyed += 1
                        break
                    if self.bombermanBoard.Board[self.position[0]][self.position[1]+i] in ("agent1", "agent2", "agent3", "agent4",
                                                                                           "agent1bomb","agent2bomb","agent3bomb","agent4bomb"):
                        agent = self.bombermanBoard.Board[util.floorToZero(self.position[0])][self.position[1]+i].split("b")[0]
                        self.bombermanBoard.agents[agent].state = "dead"
                        self.bombermanBoard.agents[agent].survival_time = str(round(time.time() -  self.bombermanBoard.agents[agent].start_time ,2))

                        if self.bombermanBoard.Board[self.position[0]][self.position[1]+i] in (self.owner.onbomb, self.owner.image):
                            self.selfKill = True
                        else:
                            self.enemiesKilled += 1

                    self.bombermanBoard.Board[self.position[0]][self.position[1]+i] = self.explosion
                else:
                    break
        except:
            pass

    def downExplosion(self):
        try:
            for i in range(self.radius+1):
                if self.bombermanBoard.Board[self.position[0]+i][self.position[1]] != "indestructible":
                    self.positionsToClean.add(tuple([self.position[0]+i, self.position[1]]))
                    if self.bombermanBoard.Board[self.position[0]+i][self.position[1]] == "destructible":
                        self.bombermanBoard.Board[self.position[0]+i][self.position[1]] = self.explosion
                        self.blocksDestroyed += 1
                        break
                    if self.bombermanBoard.Board[self.position[0]+i][self.position[1]] in ("agent1", "agent2", "agent3", "agent4",
                                                                                           "agent1bomb","agent2bomb","agent3bomb","agent4bomb"):
                        agent = self.bombermanBoard.Board[util.floorToZero(self.position[0]+i)][self.position[1]].split("b")[0]
                        self.bombermanBoard.agents[agent].state = "dead"
                        self.bombermanBoard.agents[agent].survival_time = str(round(time.time() -  self.bombermanBoard.agents[agent].start_time ,2))

                        if self.bombermanBoard.Board[self.position[0]+i][self.position[1]] in (self.owner.onbomb, self.owner.image):
                            self.selfKill = True
                        else:
                            self.enemiesKilled += 1
                    self.bombermanBoard.Board[self.position[0]+i][self.position[1]] = self.explosion
                else:
                    break
        except:
            pass

    def leftExplosion(self):
        try:
            for i in range(self.radius+1):
                if self.bombermanBoard.Board[self.position[0]][util.floorToZero(self.position[1]-i)] != "indestructible":
                    self.positionsToClean.add(tuple([self.position[0], util.floorToZero(self.position[1]-i)]))
                    if self.bombermanBoard.Board[self.position[0]][util.floorToZero(self.position[1]-i)] == "destructible":
                        self.bombermanBoard.Board[self.position[0]][util.floorToZero(self.position[1]-i)] = self.explosion
                        self.blocksDestroyed += 1
                        break
                    if self.bombermanBoard.Board[self.position[0]][util.floorToZero(self.position[1]-i)] in ("agent1", "agent2", "agent3", "agent4",
                                                                                                             "agent1bomb","agent2bomb","agent3bomb","agent4bomb"):
                        agent = self.bombermanBoard.Board[util.floorToZero(self.position[0])][self.position[1]-i].split("b")[0]
                        self.bombermanBoard.agents[agent].state = "dead"
                        self.bombermanBoard.agents[agent].survival_time = str(round(time.time() -  self.bombermanBoard.agents[agent].start_time ,2))
                        if self.bombermanBoard.Board[self.position[0]][util.floorToZero(self.position[1]-i)]  in (self.owner.onbomb, self.owner.image):
                            self.selfKill = True
                        else:
                            self.enemiesKilled += 1
                    self.bombermanBoard.Board[self.position[0]][util.floorToZero(self.position[1]-i)] = self.explosion
                else:
                    break
        except:
            pass

    def explode(self):
        if self.bombermanBoard.gameState == "running":
            self.upExplosion()
            self.rightExplosion()
            self.downExplosion()
            self.leftExplosion()
            threading.Timer(self.timer/self.timer, self.cleanExplosion).start()

    def cleanExplosion(self):
        if self.bombermanBoard.gameState == "running":
            self.state = "backpack"
            for positionToClean in self.positionsToClean:
                if self.bombermanBoard.Board[positionToClean[0]][positionToClean[1]] in ("explosion1", "explosion2", "explosion3", "explosion4"):
                    self.bombermanBoard.Board[positionToClean[0]][positionToClean[1]] = None