import logging
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor
from copy import deepcopy

logging.basicConfig(level=logging.INFO)


def alphaBetaSearch(game: Game, depth: int):
    def minValue(game: Game, depth: int, alpha: int, beta: int):
        nonlocal nodeCount
        # print(f"minValue: {game.playerNum}, depth: {depth}")
        # tabDepth = (3 - depth)*"\t"
        if game.isOver() or depth == 0:
            nodeCount += 1
            return game.eval()
        v = float("inf")
        for startCoor, endCoors in game.allMovesDict(game.playerNum).items():
            logging.debug(f"startCoor: {startCoor}")
            for endCoor in endCoors:
                if endCoor[1] < startCoor[1]:  # do not go backwards
                    logging.debug(f"\tskipping move: {startCoor} -> {endCoor}")
                    continue
                # print(f"{tabDepth}Evaluating move: {startCoor} -> {endCoor}")
                new_game = deepcopy(game)
                new_game.movePiece(startCoor, endCoor)
                v = min(v, maxValue(new_game, depth - 1, alpha, beta))
                nodeCount += 1
                # print(f"nodeCount: {nodeCount}")
                if v <= alpha:
                    return v
                beta = min(beta, v)
        return v

    def maxValue(game: Game, depth: int, alpha: int, beta: int):
        nonlocal nodeCount
        # print(f"maxValue: {game.playerNum}, depth: {depth}")
        # tabDepth = (3 - depth)*"\t"
        if game.isOver() or depth == 0:
            nodeCount += 1
            return game.eval()
        v = float("-inf")
        for startCoor, endCoors in game.allMovesDict(game.playerNum).items():
            logging.debug(f"startCoor: {startCoor}")
            for endCoor in endCoors:
                if endCoor[1] < startCoor[1]:  # do not go backwards
                    logging.debug(f"\tskipping move: {startCoor} -> {endCoor}")
                    continue
                # print(f"{tabDepth}Evaluating move: {startCoor} -> {endCoor}")
                new_game = deepcopy(game)
                new_game.movePiece(startCoor, endCoor)
                v = max(v, minValue(new_game, depth - 1, alpha, beta))
                nodeCount += 1
                # print(f"nodeCount: {nodeCount}")
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        return v

    bestMove = (None, None)
    alpha = float("-inf")
    beta = float("inf")
    v = float("-inf")
    nodeCount = 0
    for startCoor, endCoors in game.allMovesDict(game.playerNum).items():
        for endCoor in endCoors:
            new_game = deepcopy(game)
            new_game.movePiece(startCoor, endCoor)
            logging.debug(f"\nEvaluating move: {startCoor} -> {endCoor}")
            v = max(v, minValue(new_game, depth - 1, alpha, beta))
            if v > alpha:
                alpha = v
                bestMove = (startCoor, endCoor)
    print(f"[AdversarialBot] final nodeCount: {nodeCount}")
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

        print("[AdversarialBot] Computing...")
        bestMove = alphaBetaSearch(g, 3)
        print(f"[AdversarialBot] bestMove: {bestMove}\n")

        return [
            subj_to_obj_coor(bestMove[0], self.playerNum),
            subj_to_obj_coor(bestMove[1], self.playerNum),
        ]
