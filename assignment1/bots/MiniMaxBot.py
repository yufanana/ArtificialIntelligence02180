import random
import numpy as np
from game_logic.player import Player
from game_logic.game import Game
from game_logic.constants import END_COOR
from game_logic.helpers import subj_to_obj_coor, obj_to_subj_coor

MAX_DEPTH = 3
POS_DEV_WEIGHT = 2
STD_DEV_WEIGHT = [0.8, 0.8]
X_STD_DEV_WEIGHT = [0.1, 0.1]
Y_STD_DEV_WEIGHT = [1.1, 1.1]
OPT_X = [2.666, -2.73]
OPT_Y = [-5.133, -2.467]
y_rotations = 0.6



class MiniMaxBot(Player):
    def __init__(self):
        super().__init__()
        """ x_avg = 0
        y_avg = 0
        pieces = 0
        boardState = g.getBoardState(self.playerNum)
        for coor in boardState:
            if boardState[coor] == self.playerNum:
                x_avg += coor[0]
                y_avg += coor[1]
                pieces += 1
        x_avg /= pieces
        y_avg /= pieces
        OPT_X = -x_avg
        OPT_Y = -y_avg
 """    
    def utility(self, g: Game, depth: int, playerNum = 2):
        """
        Returns:
            A number between -1 and 1 that represents the utility of the game state for the current player.
        """

        if depth > 1:
            return 0
        
        # Update the optimal x and y coordinates excuding the positions where pieces are already placed
        x_avg = 0
        y_avg = 0
        pieces = 0
        for coor in END_COOR[playerNum]:
            # If the end position is already occupied by the player's piece, we don't want to consider it for the optimal position calculation
            subj_coord = obj_to_subj_coor(coor, playerNum)
            boardState = g.getBoardState(playerNum)
            if not boardState[subj_coord] == playerNum:
                x_avg += coor[0]
                y_avg += coor[1]
                pieces += 1
        x_avg /= pieces
        y_avg /= pieces
        OPT_X[depth] = -x_avg
        OPT_Y[depth] = -y_avg
        #print(f"OPT_X[{depth}]: {OPT_X[depth]}, OPT_Y[{depth}]: {OPT_Y[depth]}")
        
        ############################################################
        #Calulate utility part for the current player
        x_avg = 0
        y_avg = 0
        pieces = 0
        x = []
        y = []
        boardState = g.getBoardState(playerNum)
        for coor in boardState:
            if boardState[coor] == playerNum:
                x.append(coor[0])
                y.append(coor[1])
                x_avg += coor[0]
                y_avg += coor[1]
                pieces += 1
        std_dev_x = np.std(x)
        std_dev_y = np.std(([num * y_rotations for num in y])+ x)
        x_avg /= pieces
        y_avg /= pieces
        # print(f"x_avg: {x_avg}, y_avg: {y_avg}")

        #Calulate utility part for opponent
        opponent_util = - self.utility(g, depth + 1, self.changePlayer(playerNum))
        return opponent_util + ((x_avg - OPT_X[depth]) + (y_avg - OPT_Y[depth])) - STD_DEV_WEIGHT[depth]*(X_STD_DEV_WEIGHT[depth]*std_dev_x + Y_STD_DEV_WEIGHT[depth]*std_dev_y)

    def min_value(self, g: Game, depth, alpha, beta, playerNum):
        if depth >= MAX_DEPTH:
            return self.utility(g, 0), None
        # Check if the game is over (we are in a leaf) and return the utility of the final state
        for player in g.playerList:
            if g.checkWin(player.playerNum):
                return self.utility(g, 0), None
        depth += 1
        v = 100
        move = None
        # For each possible move, get the maximum value
        moves = g.allMovesDict(playerNum)
        for c in moves:
            for m in moves[c]:
                if m[1] < c[1]:
                    continue
                g.movePiece(subj_to_obj_coor(c, playerNum),
                            subj_to_obj_coor(m, playerNum)) # We move the piece
                v2, a2 = self.max_value(g, depth, alpha, beta, self.changePlayer(playerNum))
                if v2 < v:
                    v = v2
                    move = (c, m)
                    beta = min(beta, v)
                g.movePiece(subj_to_obj_coor(m, playerNum),
                             subj_to_obj_coor(c, playerNum)) # We reset the last move
                if v <= alpha:
                    return v, move
        return v, move
    
    def max_value(self, g: Game, depth, alpha, beta, playerNum):
        if depth >= MAX_DEPTH:
            return self.utility(g, 0), None
        for player in g.playerList:
            if g.checkWin(player.playerNum):
                return self.utility(g, 0), None
        depth += 1
        v = -100
        move = None

        # For each possible move, get the minimum value
        moves = g.allMovesDict(playerNum)
        for c in moves:
            for m in moves[c]:
                if m[1] < c[1]:
                    continue
                g.movePiece(subj_to_obj_coor(c, playerNum),
                            subj_to_obj_coor(m, playerNum)) # We move the piece
                v2, a2 = self.min_value(g, depth, alpha, beta, self.changePlayer(playerNum)) # We move the piece and call min_value
                # If we get a higher value, we update the value and the "best move"
                if v2 > v:
                    v = v2
                    move = (c, m)
                    alpha = max(alpha, v)
                g.movePiece(subj_to_obj_coor(m, playerNum),
                             subj_to_obj_coor(c, playerNum)) # We reset the last move
                if v >= beta:
                    return v, move
        return v, move
    
    def minimax_search(self, g: Game):
        """
        Find the best move for the current player based on the minimax algrithm.
        Returns:
            [start_coor, end_coor] : in subjective coordinates"""
        v, move = self.max_value(g, 0, -100, 100, self.playerNum)
        return move


    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"playerNum: {self.playerNum}")
        moves = g.allMovesDict(self.playerNum)
        # print(f"moves: {[subj_to_obj_coor(move, self.playerNum) for move in moves]}")

        # For each coor (piece), check if it has moves.
        # If it has any, add the piece to start_coords list
        start_coords = []
        for coor in moves:
            if moves[coor] != []:
                start_coords.append(coor)

        # Update the optimal x and y coordinates excuding the positions where pieces are already placed
        x_avg = 0
        y_avg = 0
        pieces = 0
        for coor in END_COOR[self.playerNum]:
            # If the end position is already occupied by the player's piece, we don't want to consider it for the optimal position calculation
            if not g.getBoardState(self.playerNum)[obj_to_subj_coor(coor, self.playerNum)] == self.playerNum:
                x_avg += coor[0]
                y_avg += coor[1]
                pieces += 1
        x_avg /= pieces
        y_avg /= pieces
        OPT_X[0] = -x_avg
        OPT_Y[0] = -y_avg
        #print(f"OPT_X[0]: {OPT_X[0]}, OPT_Y: {OPT_Y[0]}")
        
        # Choose a start_coor
        start_coord, end_coord = self.minimax_search(g)
        
        

        return [
            subj_to_obj_coor(start_coord, self.playerNum),
            subj_to_obj_coor(end_coord, self.playerNum),
        ]
    
    def changePlayer(self, playerNum: int):
        """
        Changes the player's turn.
        """
        if playerNum == self.playerNum:
            return 1
        else:
            return self.playerNum
