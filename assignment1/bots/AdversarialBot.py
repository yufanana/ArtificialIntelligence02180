import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


def alphaBetaSearch(game: Game, depth: int):
    def minValue(game: Game, depth: int, alpha: int, beta: int):
        if game.isOver() or depth == 0:
            return game.eval()
        v = float("inf")
        for move in game.allMovesDict(game.playerNum):
            new_game = game.copy()
            new_game.move(move)
            v = min(v, maxValue(new_game, depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def maxValue(game: Game, depth: int, alpha: int, beta: int):
        if game.isOver() or depth == 0:
            return game.eval()
        v = float("-inf")
        for move in game.allMovesDict(game.playerNum):
            new_game = game.copy()
            new_game.move(move)
            v = max(v, minValue(new_game, depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    bestMove = None
    alpha = float("-inf")
    beta = float("inf")
    v = float("-inf")
    for move in game.allMovesDict(game.playerNum):
        new_game = game.copy()
        new_game.move(move)
        v = max(v, minValue(new_game, depth - 1, alpha, beta))
        if v > alpha:
            alpha = v
            bestMove = move
    return bestMove


class AdversarialBot(Player):
    """
    <Description of bot>
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        pieces = g.pieces[self.playerNum]
        print(pieces)
        print(len(pieces))

        moves = g.allMovesDict(self.playerNum)

        start_coords = []
        for coor in moves:
            if moves[coor] != []:
                start_coords.append(coor)

        # Choose a random start_coor
        start_coord = random.choice(start_coords)
        end_coord = random.choice(moves[start_coord])

        return [
            subj_to_obj_coor(start_coord, self.playerNum),
            subj_to_obj_coor(end_coord, self.playerNum),
        ]
