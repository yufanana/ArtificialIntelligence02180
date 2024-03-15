import random
import numpy as np
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class Groupbot(Player):
    """Always finds a move that jumps through the maximum distance (dest[1] - coor[1]), if not it reduces distance between pieces"""

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Choose a forward move with the greatest distance travelled. If there
        are no forward moves, choose a sideway move randomly.

        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        moves = g.allMovesDict(self.playerNum)
        # state = g.boardState(self.playerNum)

        forwardMoves = dict()
        sidewaysMoves = dict()
        (start_coor, end_coor) = ((), ())

        # Split moves into forward and sideways
        for coor in moves:
            if moves[coor] != []:
                forwardMoves[coor] = []
                sidewaysMoves[coor] = []
            else:
                continue
            for dest in moves[coor]:
                if dest[1] > coor[1]:
                    forwardMoves[coor].append(dest)
                if dest[1] == coor[1]:
                    sidewaysMoves[coor].append(dest)

        # Remove empty keys
        for coor in list(forwardMoves):
            if forwardMoves[coor] == []:
                del forwardMoves[coor]
        for coor in list(sidewaysMoves):
            if sidewaysMoves[coor] == []:
                del sidewaysMoves[coor]

        # If forward is empty, move sideways
        if len(forwardMoves) == 0:
            start_coor = random.choice(list(sidewaysMoves))
            end_coor = random.choice(sidewaysMoves[start_coor])
            return [
                subj_to_obj_coor(start_coor, self.playerNum),
                subj_to_obj_coor(end_coor, self.playerNum),
            ]

        # Find forward with the max distance travelled
        max_dist = 0
        pieces_obj = g.pieces[self.playerNum]
        pieces_in_play = [p.getCoor() for p in pieces_obj]
        std_dev = np.std([coor[0] for coor in pieces_in_play])
        print(f"stdev: {std_dev}")
        for coor in forwardMoves:
            for dest in forwardMoves[coor]:
                dist = dest[1] - coor[1]
                if dist > max_dist:
                    max_dist = dist
                    (start_coor, end_coor) = (coor, dest)
                elif dist == max_dist:
                    if end_coor[1] < start_coor[1]:  # do not go backwards
                        continue
                    else:
                        # Prefers to move the piece to reduce pieces stdev
                        if (
                            np.std([dest[1] for dest in forwardMoves[coor]])
                            < std_dev
                        ):
                            max_dist = dist
                            (start_coor, end_coor) = (coor, dest)
        return [
            subj_to_obj_coor(start_coor, self.playerNum),
            subj_to_obj_coor(end_coor, self.playerNum),
        ]
