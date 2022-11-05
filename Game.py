from BombermanBoard import *
from Agent import *
from Bomb import *
import util
from tkinter import messagebox
import time
import sys
DEBUG_MODE = True if sys.argv[1] == "1" else False

def main():
    if not DEBUG_MODE:
        bombermanBoard.Board.start_timer(2000)
    for agent in bombermanBoard.agents:
        threading.Timer(1, bombermanBoard.agents[agent].decideAction).start()
    borderThread.start()

def timedFunction():
    #print("Current grid:\n")
    #printBoard(bombermanBoard.Board, bombermanBoard.height, bombermanBoard.width)
    #print("\n")
    gameResult = bombermanBoard.updateGameState()
    #print("Game result=", gameResult)
    if bombermanBoard.gameState == "Game Over":
        borderThread.cancel()
        if not DEBUG_MODE:
            bombermanBoard.Board.stop_timer()
            messagebox.showinfo("Result", str(gameResult).capitalize() + " has won the game!" if gameResult in ("agent1", "agent2", "agent3", "agent4") else gameResult)
        print("Result:", str(gameResult).capitalize() + " has won the game!" if gameResult in ("agent1", "agent2", "agent3", "agent4") else gameResult)
        writeOutputFile(gameResult)
        quit()
    elif DEBUG_MODE:
        threading.Timer(2, timedFunction).start()

def clickFunction(btn, row, col):
    bombermanBoard.Board[row][col] = "indestructible"


def outputToFile(gameState):
    gameDuration = str(round(time.time()-start_time,2))
    result = ""
    if gameState == "Draw!":
        gameState = "draw"
    result += "Game Result=" + gameState + "\n"
    result += "Game Duration=" + gameDuration + "\n"
    for agent in bombermanBoard.agents:
        thisAgent = bombermanBoard.agents[agent]
        result += "Agent Name=" + thisAgent.name + "\n"
        result += "Survival Time=" + gameDuration + "\n" if thisAgent.survival_time == 0 else "Survival Time=" + str(thisAgent.survival_time) + "\n"
        result += "Total Bombs Placed=" + str(thisAgent.n_bombs_placed) + "\n"
        result += "Number of Enemies Killed=" + str(thisAgent.bomb.enemiesKilled) + "\n"
        result += "Self Kill=" + str(thisAgent.bomb.selfKill) + "\n"
        result += "Number of Blocks Destroyed=" + str(thisAgent.bomb.blocksDestroyed) + "\n"
        result += "Died To Border=" + str(thisAgent.diedToBorder) + "\n"
        result += str(len(thisAgent.history))
        result += " Actions:" + "\n"
        for step in thisAgent.history:
            result += "\tTimestamp=" + step["timestamp"] + "|Action=" + step["action"]["name"]
            if step["action"]["name"] == "placeBomb()":
                result += "|Bomb Placed in=" + str(step["action"]["bomb_in"])
            elif step["action"]["name"] in ("moveLeft()", "moveRight()", "moveDown()", "moveUp()"):
                result += "|Old Position=" + str(step["action"]["old_position"])
                result += "|New Position=" + str(step["action"]["new_position"])
            result+="\n"
    return result[:-1]


def writeOutputFile(gameState):
    output = outputToFile(gameState)
    filename = "log_" + str(datetime.datetime.now()).replace(".", "").replace(" ","_").replace(":", "-") + ".log"
    file = open("log/"+ filename, "w")
    file.write(output)
    file.close()


bombermanBoard = BombermanBoard(util.BOARD_HEIGHT, util.BOARD_WIDTH, util.CELL_SIZE, util.CELL_SPACING, util.MARGIN, util.BACKGROUND_IMAGE, DESTRUC_PROB, DEBUG_MODE)
bomb1 = Bomb(util.BOMB_RADIUS, bombermanBoard, util.BOMB_TIMER, "explosion1")
bomb2 = Bomb(util.BOMB_RADIUS, bombermanBoard, util.BOMB_TIMER, "explosion2")
bomb3 = Bomb(util.BOMB_RADIUS, bombermanBoard, util.BOMB_TIMER, "explosion3")
bomb4 = Bomb(util.BOMB_RADIUS, bombermanBoard, util.BOMB_TIMER, "explosion4")

agent1 = RandomAgent("random", "agent1", bomb1, "agent1bomb", (0,0), bombermanBoard)
agent2 = ReactiveAgent("reactive", "agent2", bomb2, "agent2bomb",(util.BOARD_HEIGHT-1,0), bombermanBoard)
agent3 = DeliberativeAgent("deliberative", "agent3", bomb3, "agent3bomb",(0,util.BOARD_WIDTH-1), bombermanBoard)
agent4 = ReflexAgent("reflex", "agent4", bomb4, "agent4bomb",(util.BOARD_HEIGHT-1,util.BOARD_WIDTH-1), bombermanBoard)

bombermanBoard.initAgents([agent1, agent2, agent3, agent4])
borderThread = threading.Timer(30, bombermanBoard.dropBorder)
start_time = time.time()

if DEBUG_MODE:
    threading.Timer(1, main).start()
    threading.Timer(1, timedFunction).start()

else:
    bombermanBoard.Board.on_start = main
    bombermanBoard.Board.on_timer = timedFunction
    bombermanBoard.Board.on_mouse_click = clickFunction
    bombermanBoard.Board.show()



