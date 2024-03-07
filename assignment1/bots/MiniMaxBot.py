import numpy as np
from game_logic.player import Player
from game_logic.game import Game
from game_logic.constants import END_COOR
from game_logic.helpers import subj_to_obj_coor, obj_to_subj_coor

MAX_DEPTH = 2
POS_DEV_WEIGHT = 2
STD_DEV_WEIGHT = 0.6
X_STD_DEV_WEIGHT = 0.3
Y_STD_DEV_WEIGHT = 1
OPT_X = 2.5
OPT_Y = 2.6


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

    def utility(self, g: Game):
        """
        Returns:
            A number between -1 and 1 that represents the utility of the game state for the current player.
        """
        x_avg = 0
        y_avg = 0
        pieces = 0
        x = []
        y = []
        boardState = g.getBoardState(self.playerNum)
        for coor in boardState:
            if boardState[coor] == self.playerNum:
                x.append(coor[0])
                y.append(coor[1])
                x_avg += coor[0]
                y_avg += coor[1]
                pieces += 1
        std_dev_x = np.std(x)
        std_dev_y = np.std(y)
        x_avg /= pieces
        y_avg /= pieces
        # print(f"x_avg: {x_avg}, y_avg: {y_avg}")

        return ((x_avg - OPT_X) + (y_avg - OPT_Y)) - STD_DEV_WEIGHT * (
            X_STD_DEV_WEIGHT * std_dev_x + Y_STD_DEV_WEIGHT * std_dev_y
        )

    def min_value(self, g: Game, depth, alpha, beta):
        if depth >= MAX_DEPTH:
            return self.utility(g), None
        # Check if the game is over (we are in a leaf) and return the utility of the final state
        for player in g.playerList:
            if g.checkWin(player.playerNum):
                return self.utility(g), None
        depth += 1
        v = 100
        move = None
        # For each possible move, get the maximum value
        for c in g.allMovesDict(self.playerNum):
            for m in g.allMovesDict(self.playerNum)[c]:
                g.movePiece(
                    subj_to_obj_coor(c, self.playerNum),
                    subj_to_obj_coor(m, self.playerNum),
                )  # We move the piece
                v2, a2 = self.max_value(g, depth, alpha, beta)
                if v2 < v:
                    v = v2
                    move = (c, m)
                    beta = min(beta, v)
                g.movePiece(
                    subj_to_obj_coor(m, self.playerNum),
                    subj_to_obj_coor(c, self.playerNum),
                )  # We reset the last move
                if v <= alpha:
                    return v, move
        return v, move

    def max_value(self, g: Game, depth, alpha, beta):
        if depth >= MAX_DEPTH:
            return self.utility(g), None
        for player in g.playerList:
            if g.checkWin(player.playerNum):
                return self.utility(g), None
        depth += 1
        v = -100
        move = None

        # For each possible move, get the minimum value
        for c in g.allMovesDict(self.playerNum):
            for m in g.allMovesDict(self.playerNum)[c]:
                g.movePiece(
                    subj_to_obj_coor(c, self.playerNum),
                    subj_to_obj_coor(m, self.playerNum),
                )  # We move the piece
                v2, a2 = self.min_value(
                    g, depth, alpha, beta
                )  # We move the piece and call min_value
                # If we get a higher value, we update the value and the "best move"
                if v2 > v:
                    v = v2
                    move = (c, m)
                    alpha = max(alpha, v)
                g.movePiece(
                    subj_to_obj_coor(m, self.playerNum),
                    subj_to_obj_coor(c, self.playerNum),
                )  # We reset the last move
                if v >= beta:
                    return v, move
        return v, move

    def minimax_search(self, g: Game):
        """
        Find the best move for the current player based on the minimax algrithm.
        Returns:
            [start_coor, end_coor] : in subjective coordinates"""
        v, move = self.max_value(g, 0, -100, 100)
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
            if not g.getBoolBoardState(self.playerNum)[
                obj_to_subj_coor(coor, self.playerNum)
            ]:
                x_avg += coor[0]
                y_avg += coor[1]
                pieces += 1
        x_avg /= pieces
        y_avg /= pieces
        OPT_X = -x_avg
        OPT_Y = -y_avg
        print(f"OPT_X: {OPT_X}, OPT_Y: {OPT_Y}")
        # Choose a start_coor
        start_coord, end_coord = self.minimax_search(g)

        return [
            subj_to_obj_coor(start_coord, self.playerNum),
            subj_to_obj_coor(end_coord, self.playerNum),
        ]
