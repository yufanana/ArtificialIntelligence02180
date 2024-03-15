import random
import numpy as np
from game_logic.player import Player
from game_logic.game import Game
from game_logic.layout import END_COOR
from game_logic.helpers import subj_to_obj_coor, obj_to_subj_coor

MAX_DEPTH = 3
POS_WEIGHT = 3
STD_DEV_WEIGHT = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
X_WEIGHT = 1
Y_WEIGHT = 1.6
X_STD_DEV_WEIGHT = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
Y_STD_DEV_WEIGHT = [1, 1, 1.1, 1.1, 1.1, 1.1]
OPT_X = [-4,4,0,0,0,0]
OPT_Y = [8,-8,0,0,0,0]
OPPONENT_UTIL_WEIGHT = 0.1
y_rotations = 1
x_rotations = 0.5




class MiniMaxBot(Player):
    def __init__(self):
        super().__init__()
        self.nodesCount = 0

    def getOptimalCoor(self, g: Game, depth: int, playerNum: int):
        # Update the optimal x and y coordinates excuding the positions where pieces are already placed
        x_avg = 0
        y_avg = 0
        pieces = 0
        boardState = g.getBoardState(playerNum)
        for coor in END_COOR[playerNum]:
            # If the end position is already occupied by the player's piece, we don't want to consider it for the optimal position calculation
            subj_coord = obj_to_subj_coor(coor, playerNum)
            if not boardState[subj_coord] == playerNum:
                x_avg += coor[0]
                y_avg += (coor[1] * y_rotations) + (coor[0] * x_rotations)
                pieces += 1
        #if playerNum == self.playerNum and pieces == 0: # If all the pieces are placed, we return 1000, that will be "bad" if we are considering the opponent, good otherwise 
         #   return 1000
        if pieces == 0:
                pieces += 1
        x_avg /= pieces
        y_avg /= pieces
        OPT_X[depth] = x_avg
        OPT_Y[depth] = y_avg
        return OPT_X[depth], OPT_Y[depth]
        #if playerNum == self.playerNum:
        #    print(f"OPT_X[{depth}]: {OPT_X[depth]}, OPT_Y[{depth}]: {OPT_Y[depth]}")
        
    def getAverageCoor(self, g: Game, playerNum: int):
            """
            Returns the average x and y coordinates and x and y std deviation of the pieces of the player."""
            x_avg = 0
            y_avg = 0
            pieces = 0
            x = []
            y = []
            boardState = g.getBoardState(playerNum)
            for coor in boardState:
                #If the piece is the player's and it's not in the end positions, we want to consider it
                if boardState[coor] == playerNum and subj_to_obj_coor(coor, playerNum) not in END_COOR[playerNum]:
                    # I want the average of the objective coordinates of the pieces
                    obj_coord = subj_to_obj_coor(coor, playerNum)
                    x.append(obj_coord[0])
                    y.append(obj_coord[1])
                    x_avg += obj_coord[0]
                    y_avg += (obj_coord[1] * y_rotations) + (obj_coord[0] * x_rotations)
                    pieces += 1
            std_dev_x = np.std(x)
            std_dev_y = np.std(([num * y_rotations for num in y])+ ([num * x_rotations for num in x]))
            if pieces == 0:
                pieces += 1
            x_avg /= pieces
            y_avg /= pieces
            return x_avg, y_avg, std_dev_x, std_dev_y
            #if playerNum == 2:
                #print(f"x_avg: {x_avg}, y_avg: {y_avg}")

    def eval(self, g: Game, playerNum: int, util_depth = 0):
        """
        Returns:
            A number between -1 and 1 that represents the utility of the game state for the current player.
        """
        if util_depth >= len(g.playerList):
            return 0
        
        #Calulate utility part for the current player
        x_avg, y_avg, std_dev_x, std_dev_y = self.getAverageCoor(g, playerNum)

        # Get new otimal coordinates
        OPT_X[util_depth], OPT_Y[util_depth] = self.getOptimalCoor(g, util_depth, playerNum)
        position_util = POS_WEIGHT * np.sqrt( X_WEIGHT * (x_avg - OPT_X[util_depth])**2 + Y_WEIGHT * (y_avg - OPT_Y[util_depth])**2)
        # We want the importance of the std dev to be less when the pieces are closer to the optimal position
        std_util = STD_DEV_WEIGHT[util_depth] * 1/(position_util) * ( ((X_STD_DEV_WEIGHT[util_depth] * std_dev_x) + (Y_STD_DEV_WEIGHT[util_depth] * std_dev_y)))        
        current_player_util =  - (std_util + position_util)
        #Calulate utility part for opponent
        opponent_util = self.eval(g, self.nextPlayer(playerNum, len(g.playerList)), util_depth + 1)
        if util_depth == 0:
            return current_player_util + OPPONENT_UTIL_WEIGHT * opponent_util
        return current_player_util - OPPONENT_UTIL_WEIGHT * opponent_util

    def min_value(self, g: Game, depth, alpha, beta, playerNum):
        self.nodesCount += 1
        if depth >= MAX_DEPTH:
            return self.eval(g, self.playerNum), None
        # Check if the game is over (we are in a leaf) and return the eval of the final state
        for player in g.playerList:
            if g.checkWin(player.playerNum):
                return self.eval(g, self.playerNum), None
        depth += 1
        v = float('inf')
        #move = None
        moves = g.allMovesDict(playerNum) # For each possible move, get the maximum value
        for c in moves:
            for m in moves[c]:
                if m[1] < c[1]:
                    continue                
                g.movePiece(subj_to_obj_coor(c, playerNum), subj_to_obj_coor(m, playerNum)) # We move the piece
                # If the next player is us (MiniMaxBot), we call max_value, otherwise we call min_value
                v2, a2 = self.max_value(g, depth, alpha, beta, self.nextPlayer(playerNum, len(g.playerList)))
                if v2 < v:
                    v = v2
                    move = (c, m)
                    beta = min(beta, v)
                g.movePiece(subj_to_obj_coor(m, playerNum), subj_to_obj_coor(c, playerNum)) # We reset the last move
                if v <= alpha:
                    return v, move
        v = round(v, 2)
        return v, move
    
    def max_value(self, g: Game, depth, alpha, beta, playerNum):
        self.nodesCount += 1
        if depth >= MAX_DEPTH:
            return self.eval(g, self.playerNum), None
        for player in g.playerList:
            if g.checkWin(player.playerNum):
                return self.eval(g, self.playerNum), None
        depth += 1
        v = -float('inf')
        # For each possible move, get the minimum value
        moves = g.allMovesDict(playerNum)
        for c in moves:
            for m in moves[c]:
                if m[1] < c[1]:
                    continue
                # if the move moves a piece form a non-end postion to an end position we choose it and return a very high value
                if self.playerNum == playerNum and subj_to_obj_coor(c, playerNum) not in END_COOR[playerNum] and subj_to_obj_coor(m, playerNum) in END_COOR[playerNum]:
                    return 1000, (c, m)
                
                g.movePiece(subj_to_obj_coor(c, playerNum), subj_to_obj_coor(m, playerNum)) # We move the piece
                v2, a2 = self.min_value(g, depth, alpha, beta, self.nextPlayer(playerNum, len(g.playerList)))
                if v2 > v:
                    v = v2
                    move = (c, m)
                    alpha = max(alpha, v)
                g.movePiece(subj_to_obj_coor(m, playerNum),subj_to_obj_coor(c, playerNum)) # We reset the last move
                if v >= beta:
                    return v, move
        v = round(v, 2)
        return v, move
    
    def minimax_search(self, g: Game):
        """
        Find the best move for the current player based on the minimax algrithm.
        Returns:
            [start_coor, end_coor] : in subjective coordinates"""
        self.nodesCount = 0
        v, move = self.max_value(g, 0, -10000000, 10000000, self.playerNum)
        print(f"[MiniMaxBot] Final node count: {self.nodesCount}\n")
        return move


    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"[MiniMaxBot] is player {self.playerNum}")
        moves = g.allMovesDict(self.playerNum)
        # print(f"moves: {[subj_to_obj_coor(move, self.playerNum) for move in moves]}")

        # For each coor (piece), check if it has moves.
        # If it has any, add the piece to start_coords list
        start_coords = []
        for coor in moves:
            if moves[coor] != []:
                start_coords.append(coor)
        start_coord, end_coord = self.minimax_search(g)
        
        

        return [
            subj_to_obj_coor(start_coord, self.playerNum),
            subj_to_obj_coor(end_coord, self.playerNum),
        ]
    
    """def changePlayer(self, playerNum: int):
        
        #Changes the player's turn.
        
        if playerNum == self.playerNum:
            return 1
        else:
            return self.playerNum
       """ 
    def nextPlayer(self, playerNum: int, allPlayersNum):
        """
        Changes the player's turn.
        """
        if playerNum == allPlayersNum :
            return 1
        else:
            return playerNum + 1
