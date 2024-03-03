import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class LadderBot(Player):
    """
    Bot that favours bringing pieces along the centerline
    of the board, and favour skips.
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        # centerline: y = -2x, 0 = 2x + y
        # line = np.array([[2, 1, 0]]).T

        # d = abs(line.T @ p) / (abs(p[2]) * np.sqrt(line[0] ** 2 + line[1] ** 2))

        # Find all pieces
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
