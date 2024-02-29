import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class RandomBot(Player):
    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"playerNum: {self.playerNum}")
        moves = g.allMovesDict(self.playerNum)
        # print(f"moves: {[subj_to_obj_coor(move, self.playerNum) for move in moves]}")

        start_coords = []
        for coor in moves:
            if moves[coor] != []:
                start_coords.append(coor)

        # Choose a random start_coor
        start_coord = random.choice(start_coords)
        print(f"start_coord: {subj_to_obj_coor(start_coord, self.playerNum)}")
        end_coord = random.choice(moves[start_coord])
        print(f"end_coord: {subj_to_obj_coor(end_coord, self.playerNum)}")

        return [
            subj_to_obj_coor(start_coord, self.playerNum),
            subj_to_obj_coor(end_coord, self.playerNum),
        ]
