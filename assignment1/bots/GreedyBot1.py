import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class GreedyBot1(Player):
    """
    Choose the move that moves a piece to the topmost cell.
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Choose the forward move with the greatest y value. If there are no
        forward moves, choose a sideway move randomly.

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
            # If there are moves
            if moves[coor] != []:
                forwardMoves[coor] = []
                sidewaysMoves[coor] = []

            # Check y-coordinate of destination
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

        # If there are no forward moves, move sideways randomly.
        if len(forwardMoves) == 0:
            start_coor = random.choice(list(sidewaysMoves))
            end_coor = random.choice(sidewaysMoves[start_coor])
            return [
                subj_to_obj_coor(start_coor, self.playerNum),
                subj_to_obj_coor(end_coor, self.playerNum),
            ]

        # Choose the furthest destination (biggest y value in dest),
        # then backmost piece (smallest y value in coor)
        biggestDestY = -8
        smallestStartY = 8
        for coor in forwardMoves:
            for i in range(len(forwardMoves[coor])):
                dest = forwardMoves[coor][i]
                # Find forward move with biggest y dest value
                if dest[1] > biggestDestY:
                    (start_coor, end_coor) = (coor, dest)
                    biggestDestY = dest[1]
                    smallestStartY = coor[1]

                elif dest[1] == biggestDestY:
                    startY = coor[1]

                    # If tiebreakers,
                    # choose forward move with smallest y start value
                    if startY < smallestStartY:
                        (start_coor, end_coor) = (coor, dest)
                        biggestDestY = dest[1]
                        smallestStartY = coor[1]
                    elif startY == smallestStartY:
                        start_coor, end_coor = random.choice(
                            [[start_coor, end_coor], [coor, dest]],
                        )
                        biggestDestY = end_coor[1]
                        smallestStartY = start_coor[1]
        return [
            subj_to_obj_coor(start_coor, self.playerNum),
            subj_to_obj_coor(end_coor, self.playerNum),
        ]
