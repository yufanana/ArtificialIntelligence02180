import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class RandomBot(Player):
    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """returns [start_coor, end_coor]"""
        moves = g.allMovesDict(self.playerNum)

        start_coords = []
        for coor in moves:
            if moves[coor] != []:
                start_coords.append(coor)

        # Choose a start_coor
        start_coord = random.choice(start_coords)
        end_coord = random.choice(moves[coor])
        return [
            subj_to_obj_coor(start_coord, self.playerNum),
            subj_to_obj_coor(end_coord, self.playerNum),
        ]
