import logging
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor, obj_to_subj_coor
from copy import deepcopy
from game_logic.constants import END_COOR, START_COOR

logging.basicConfig(level=logging.INFO)

END_PENALTY = 1
START_PENALTY = 5
# 1/(Player_Start_pieces) ~1/x


def alphaBetaSearch(game: Game, depth: int):
    def minValue(game: Game, depth: int, alpha: int, beta: int):
        nonlocal nodeCount
        # print(f"minValue: {game.playerNum}, depth: {depth}")
        # tabDepth = (3 - depth)*"\t"
        if game.isOver() or depth == 0:
            nodeCount += 1
            return game_eval(game)
        v = float("inf")
        for startCoor, endCoors in game.allMovesDict(game.playerNum).items():
            logging.debug(f"startCoor: {startCoor}")
            for endCoor in endCoors:
                if endCoor[1] < startCoor[1]:  # do not go backwards
                    logging.debug(f"\tskipping move: {startCoor} -> {endCoor}")
                    continue
                new_game = deepcopy(game)
                new_game.movePiece(startCoor, endCoor)
                v = min(v, maxValue(new_game, depth - 1, alpha, beta))
                nodeCount += 1
                if v <= alpha:
                    return v
                beta = min(beta, v)
        return v

    def maxValue(game: Game, depth: int, alpha: int, beta: int):
        nonlocal nodeCount
        if game.isOver() or depth == 0:
            nodeCount += 1
            return game_eval(game)
        v = float("-inf")
        for startCoor, endCoors in game.allMovesDict(game.playerNum).items():
            logging.debug(f"startCoor: {startCoor}")
            for endCoor in endCoors:
                if endCoor[1] < startCoor[1]:  # do not go backwards
                    logging.debug(f"\tskipping move: {startCoor} -> {endCoor}")
                    continue
                new_game = deepcopy(game)
                new_game.movePiece(startCoor, endCoor)
                v = max(v, minValue(new_game, depth - 1, alpha, beta))
                nodeCount += 1
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


def furthestEndCell(game: Game, playerNum: int) -> tuple:
    """ "
    Compares the furthest cell based on subjective subjective,
    returns the furthest cell in objective coordinates.
    """
    furthestCell = (0, 0)
    for coord in END_COOR[playerNum]:
        subCoor = obj_to_subj_coor(coord, playerNum)
        # Find empty cells or cells occupied by the
        # current player
        if (
            game.board[coord] is None
            or game.board[coord].getPlayerNum() != playerNum
        ):
            if subCoor[1] > furthestCell[1]:
                furthestCell = coord
    furthestCell = subj_to_obj_coor(furthestCell, playerNum)
    return furthestCell


def countStartPieces(game: Game, playerNum: int) -> int:
    """
    Count how many of the player's pieces are in its start zone.
    """
    count = 0
    for coor in START_COOR[playerNum]:
        if game.board[coor] is None:  # unoccupied cell
            continue
        if game.board[coor].getPlayerNum() == playerNum:
            count += 1
    return count


def startDistances(game: Game, playerNum: int):
    """ """
    cumDistance = 0
    for coor in START_COOR[playerNum]:
        subjCoor = obj_to_subj_coor(coor, playerNum)
        if game.board[coor] is not None:
            pass


def distanceToFurthestCell(game: Game, playerNum: int):
    """
    Computes the cumulative distance of the player's pieces
    to the furthest empty cell in the end zone.
    """
    furthestCell = furthestEndCell(game, playerNum)
    cumDistance = 0
    for piece in game.pieces[playerNum]:
        cumDistance += furthestCell[1] - piece.getCoor()[1]
    return cumDistance


def game_eval(game: Game):
    """
    Returns the evaluation of the game state for the player.
    """
    # BUG: bot is unable to make the last 3 moves to finish the game
    if game.checkWin(game.playerNum):
        return 300

    # Find the furthest empty cell in end zone
    cumEndDist = distanceToFurthestCell(game, game.playerNum)

    # Find the furthest empty cell in opponent's end zone
    opponentNum = 2
    oppoCumEndDist = distanceToFurthestCell(game, opponentNum)

    # Count start pieces
    playerStartPieces = countStartPieces(game, game.playerNum)
    oppoStartPieces = countStartPieces(game, opponentNum)

    oppoPenalty = END_PENALTY * oppoCumEndDist + START_PENALTY * oppoStartPieces
    playerPenalty = END_PENALTY * cumEndDist + START_PENALTY * playerStartPieces
    score = oppoPenalty - playerPenalty
    return score


def game_eval_cluster(game: Game):
    # TODO: convert ladderbot into a heuristic for adversarial eval function
    # goal: cluster in a vertical rectangle along the centerline
    # steps: maximise number of skips --> travelling the greatest distance
    pass


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
