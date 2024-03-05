import random
import numpy as np
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


def distance_to_line(line: np.ndarray, p: list[tuple]):
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


def side_of_line(line: np.ndarray, p: list[tuple]):
    """
    Compute the side of the line that the points are on.

    Args:
        line : (3,1) equation of line in homogenous form (l.T @ p = 0)
        p : list of tuple coordinates

    Returns:
        side : np.array of side of the line (15,)
    """
    p = np.array(p).T  # (2,15)
    ph = np.vstack((p, np.ones(p.shape[1])))  # (3,15)
    side = line.T @ ph
    side = side.reshape(-1)
    return side


def check_forward_moves(moves: dict, piece: tuple):
    """
    Check if there are any forward moves for the piece.

    Args:
        moves : dict of moves
        piece : tuple of piece coordinates

    Returns:
        forward_moves : list of forward moves
    """
    forward_moves = []
    for dest in moves[piece]:
        if dest[1] > piece[1]:  # Compare y-coordinates
            forward_moves.append(dest)
    return forward_moves


class LadderBot(Player):
    """
    Bot that favours bringing pieces along the centerline
    of the board, and favour skips.
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        1. Select piece furthest from centerline, or bottom-most piece
        2. For selected piece, find forward moves, else move sideways.
        3. From forward moves, find largest skip, else move closest to centerline.

        Returns:
            [start_coor, end_coor] : in objective coordinates
        """

        # Find all pieces
        pieces_obj = g.pieces[self.playerNum]
        pieces = [p.getCoor() for p in pieces_obj]  # contains coordinates
        moves = g.allMovesDict(self.playerNum)

        ################ STAGE 1: Selecting a piece ################
        # Find the piece that is the furthest from the v-centerline
        centerline = np.array(
            [[2, 1, 0]],
        ).T  # vertical centerline: y=-2x, 0=2x+y
        d = distance_to_line(centerline, pieces)
        max_hor_idx = np.argmax(d)
        far_piece = pieces[max_hor_idx]

        # Enforce max y-distance between pieces
        max_gap = 7.0
        min_y_piece = min(pieces, key=lambda x: x[1])
        max_y_piece = max(pieces, key=lambda x: x[1])
        if max_y_piece[1] - min_y_piece[1] > max_gap:
            print("LadderBot: Max gap exceeded")
            # Move the further back piece
            sorted_pieces = sorted(pieces, key=lambda x: x[1])
            for piece in sorted_pieces:
                # Find the bottom-most piece that has moves
                if piece in moves:
                    far_piece = piece
                    forward_moves = check_forward_moves(moves, far_piece)
                    if forward_moves == []:  # No forward moves
                        continue
                    print(f"LadderBot: moving last piece, {far_piece}")
                    break

        start_coor = far_piece

        ################ STAGE 2: Selecting a move ################
        # Check for forward moves
        forward_moves = check_forward_moves(moves, far_piece)

        # If there are no forward moves, move sideways randomly. End.
        if forward_moves == []:
            end_coor = random.choice(moves[start_coor])
            return [
                subj_to_obj_coor(start_coor, self.playerNum),
                subj_to_obj_coor(end_coor, self.playerNum),
            ]

        # Choose moves with greatest dist travelled
        d = np.linalg.norm(
            np.array(far_piece) - np.array(forward_moves),
            axis=1,
        )
        if any(d > np.sqrt(2)):  # skips found
            # Choose largest skip
            max_d_idx = np.argmax(d)
            end_coor = forward_moves[max_d_idx]
        else:
            # Choose dest closest to the centerline
            d = distance_to_line(centerline, forward_moves)
            min_d_idx = np.argmin(d)
            end_coor = forward_moves[min_d_idx]

        return [
            subj_to_obj_coor(start_coor, self.playerNum),
            subj_to_obj_coor(end_coor, self.playerNum),
        ]
