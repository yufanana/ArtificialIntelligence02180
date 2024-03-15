import logging
import numpy as np
from game_logic.player import Player
from game_logic.game import Game
from game_logic.layout import END_COOR, START_COOR
from game_logic.helpers import subj_to_obj_coor, obj_to_subj_coor
from copy import deepcopy

# Change the logging level here to see debug messages in console if needed
logging.basicConfig(level=logging.INFO)

# Weights for scoring
END_PENALTY = 1
START_PENALTY = 5
SEP_PENALTY = 1
CENTER_PENALTY = 1
# 1/(Player_Start_pieces) ~1/x


class MMLadder(Player):
    """
    Moves pieces based on the minimax algorithm with alpha-beta pruning.
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"[MMLadder] is player {self.playerNum}")
        print("[MMLadder] Computing...")
        bestMove = alphaBetaSearch(g, 3)
        bestMove = [
            subj_to_obj_coor(bestMove[0], self.playerNum),
            subj_to_obj_coor(bestMove[1], self.playerNum),
        ]
        print(f"[MMLadder] bestMove: {bestMove}\n")

        return bestMove


def alphaBetaSearch(game: Game, depth: int):
    """
    Alpha-beta search algorithm to find the best move with the largest utility.
    """

    def minValue(game: Game, depth: int, alpha: int, beta: int):
        """
        Returns the minimum value of the possible game state among the children
        up to the given depth.
        """
        oppoNum = 2
        nonlocal nodeCount
        if game.isOver() or depth == 0:
            nodeCount += 1
            return utility_cluster(game)
        v = float("inf")
        for startCoor, endCoors in game.allMovesDict(oppoNum).items():
            # logging.debug(f"startCoor: {startCoor}")
            for endCoor in endCoors:
                if endCoor[1] < startCoor[1]:  # do not go backwards
                    # logging.debug(f"\tskipping move: {startCoor} -> {endCoor}")
                    continue
                # if endCoor[1] == startCoor[1]:  # do not go sideways
                #     continue
                # Create a new game state and make the move
                new_game = deepcopy(game)
                new_game.movePiece(
                    subj_to_obj_coor(startCoor, oppoNum),
                    subj_to_obj_coor(endCoor, oppoNum),
                )
                v = min(v, maxValue(new_game, depth - 1, alpha, beta))
                nodeCount += 1
                if v <= alpha:  # alpha cut-off
                    return v
                beta = min(beta, v)
        return v

    def maxValue(game: Game, depth: int, alpha: int, beta: int):
        """
        Returns the maximum value of the possible game state among the children
        up to the given depth.
        """
        nonlocal nodeCount
        if game.isOver() or depth == 0:
            nodeCount += 1
            return utility_cluster(game)
            # return utility(game)
        v = float("-inf")
        for startCoor, endCoors in game.allMovesDict(game.playerNum).items():
            # logging.debug(f"startCoor: {startCoor}")
            for endCoor in endCoors:
                if endCoor[1] < startCoor[1]:  # do not go backwards
                    # logging.debug(f"\tskipping move: {startCoor} -> {endCoor}")
                    continue
                # if endCoor[1] == startCoor[1]:  # do not go sideways
                #     continue
                # Create a new game state and make the move
                new_game = deepcopy(game)
                new_game.movePiece(startCoor, endCoor)
                v = max(v, minValue(new_game, depth - 1, alpha, beta))
                nodeCount += 1
                if v >= beta:  # beta cut-off
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
            # logging.debug(f"\nEvaluating move: {startCoor} -> {endCoor}")
            v = max(v, minValue(new_game, depth - 1, alpha, beta))
            if v > alpha:
                alpha = v
                bestMove = (startCoor, endCoor)
    print(f"[MMLadder] final nodeCount: {nodeCount}")
    return bestMove


def furthestEndCell(game: Game, playerNum: int) -> tuple:
    """
    Return the furthest empty cell in the end zone.

    Note:
        Comparison is based on the subjective coordinates.
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


def computeSeparation(game: Game, playerNum: int) -> int:
    """
    Compute the y-separation between the furthest and closest pieces.
    """
    furthestPiece = (4, -8)
    closestPiece = (4, 8)
    for piece in game.pieces[playerNum]:
        subCoor = obj_to_subj_coor(piece.getCoor(), playerNum)
        if subCoor[1] > furthestPiece[1]:
            furthestPiece = piece.getCoor()
        if subCoor[1] < closestPiece[1]:
            closestPiece = piece.getCoor()
    return furthestPiece[1] - closestPiece[1]


def distanceToLine(line: np.ndarray, p: list[tuple]):
    """
    Compute shortest distance d between line l and 2D homogenous point p.

    Args:
        line : (3,1) equation of line in homogenous form (l.T @ p = 0)
        p : list of tuple coordinates

    Returns:
        d : np.array of distances (15,)
    """
    p = np.array(p).T  # (2,15)
    ph = np.vstack((p, np.ones(p.shape[1])))  # (3,15)
    d = abs(line.T @ ph) / (abs(ph[2]) * np.sqrt(line[0] ** 2 + line[1] ** 2))
    d = d.reshape(-1)
    return d


def distanceToCenterline(game: Game, playerNum: int) -> int:
    """
    Return the cumulative distance of the player's pieces to the centerline.
    """
    cumDistance = 0
    centerline = np.array([[2, 1, 0]]).T  # vertical centerline: y=-2x, 0=2x+y
    for piece in game.pieces[playerNum]:
        subCoor = obj_to_subj_coor(piece.getCoor(), playerNum)
        cumDistance += distanceToLine(centerline, [subCoor])
    return cumDistance


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


def utility(game: Game):
    """
    Returns the evaluation of the game state for the player.
    """
    # BUG: bot is unable to make the last 3 moves to finish the game
    if game.checkWin(game.playerNum):
        return 300

    oppoNum = 2

    # Find the cumulative distance to the furthest empty cell in the end zone
    cumEndDist = distanceToFurthestCell(game, game.playerNum)
    oppoCumEndDist = distanceToFurthestCell(game, oppoNum)

    # Count start pieces
    playerStartPieces = countStartPieces(game, game.playerNum)
    oppoStartPieces = countStartPieces(game, oppoNum)

    # Compute scores
    oppoPenalty = END_PENALTY * oppoCumEndDist + START_PENALTY * oppoStartPieces
    playerPenalty = END_PENALTY * cumEndDist + START_PENALTY * playerStartPieces
    score = oppoPenalty - playerPenalty
    return score


def utility_cluster(game: Game):
    """
    Penalises based on y-separation of pieces, distance to centerline, and
    distance to end zone.
    """
    oppoNum = 2

    if game.checkWin(game.playerNum):
        return 300
    if game.checkWin(2):
        return -300

    # Find the cumulative distance to the furthest empty cell in the end zone
    cumEndDist = distanceToFurthestCell(game, game.playerNum)
    oppoCumEndDist = distanceToFurthestCell(game, oppoNum)

    # Find y-distance between furthest and closet piece
    playerSep = computeSeparation(game, game.playerNum)
    oppoSep = computeSeparation(game, oppoNum)

    # Find cumulative distance from centerline
    centerDistance = distanceToCenterline(game, game.playerNum)
    oppoCenterDistance = distanceToCenterline(game, oppoNum)

    # Count start pieces
    playerStartPieces = countStartPieces(game, game.playerNum)
    oppoStartPieces = countStartPieces(game, oppoNum)

    # Compute scores
    playerScore = (
        SEP_PENALTY * playerSep
        + CENTER_PENALTY * centerDistance
        + END_PENALTY * cumEndDist
        + START_PENALTY * playerStartPieces
    )
    oppoScore = (
        SEP_PENALTY * oppoSep
        + CENTER_PENALTY * oppoCenterDistance
        + END_PENALTY * oppoCumEndDist
        + START_PENALTY * oppoStartPieces
    )
    score = oppoScore - playerScore
    return score
