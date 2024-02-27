"""
Game Class to represent the game state and logic.
"""
import copy
from game_logic.helpers import add, checkJump, obj_to_subj_coor
from game_logic.constants import DIRECTIONS, END_COOR, NEUTRAL_COOR, START_COOR
from game_logic.piece import Piece
from gui.constants import HEIGHT, WIDTH


class Game:
    def __init__(self, playerCount=3):
        if playerCount in (2, 3):
            self.playerCount = playerCount
        else:
            self.playerCount = 3
        self.pieces: dict[int, set[Piece]] = {1: set(), 2: set(), 3: set()}
        self.board = self.createBoard(playerCount)
        # for drawing board
        self.unitLength = int(WIDTH * 0.05)  # unitLength length in pixels
        self.lineWidth = int(self.unitLength * 0.05)  # line width
        self.circleRadius = int(HEIGHT * 0.025)  # board square (circle) radius
        self.centerCoor = (WIDTH / 2, HEIGHT / 2)  # window size is 800*600

    def createBoard(self, playerCount: int):
        """
        Returns a dict of the board. Adds pieces to starting zones.
        """
        Board = {}
        # player 1 end zone
        for p in range(-4, 1):
            for q in range(4, 9):
                if p + q > 4:
                    continue
                else:
                    if (p, q) not in Board:
                        Board[(p, q)] = None
        # player 1 start zone
        for p in range(0, 5):
            for q in range(-8, -3):
                if p + q < -4:
                    continue
                else:
                    Board[(p, q)] = Piece(1, p, q)
                    self.pieces[1].add(Board[p, q])
        # player 2 end zone
        for p in range(4, 9):
            for q in range(-4, 1):
                if p + q > 4:
                    continue
                else:
                    if (p, q) not in Board:
                        Board[(p, q)] = None
        # player 2 start zone
        for p in range(-8, -3):
            for q in range(0, 5):
                if p + q < -4:
                    continue
                else:
                    Board[(p, q)] = Piece(2, p, q)
                    self.pieces[2].add(Board[p, q])
        # player 3 end zone
        for p in range(-4, 1):
            for q in range(-4, 1):
                if p + q > -4:
                    continue
                else:
                    if (p, q) not in Board:
                        Board[(p, q)] = None
        # player 3 start zone
        for p in range(0, 5):
            for q in range(0, 5):
                if p + q < 4:
                    continue
                else:
                    Board[(p, q)] = None if playerCount == 2 else Piece(3, p, q)
                    if playerCount == 3:
                        self.pieces[3].add(Board[p, q])
        # neutral zone
        for p in range(-3, 4):
            for q in range(-3, 4):
                if p + q <= 3 and p + q >= -3:
                    Board[(p, q)] = None
        return Board

    def getValidMoves(self, startPos: tuple, playerNum: int):
        """
        Compute all valid moves for a piece.

        Args:
            startPos (tuple): objective coordinates of the piece.
            playerNum (int): the player number.

        Returns:
            list of tuples: objective coordinates of the dest valid moves.
        """
        moves = []

        # Try all 8 directions
        for direction in DIRECTIONS:
            destination = add(startPos, direction)
            # Step is out of bounds
            if destination not in self.board:
                continue  
            
            # Single step into open space
            if self.board[destination] == None:
                moves.append(destination)  # walk
                
            # Single step into occupied space, check for skips
            else:  # self.board[destination] != None
                destination = add(destination, direction)
                if (
                    destination not in self.board
                    or self.board[destination] != None
                ):
                    continue  # out of bounds or can't jump
                moves.append(destination)
                checkJump(moves, self.board, destination, direction, playerNum)
        
        # You can move past other player's territory, but you can't stay there.
        for i in copy.deepcopy(moves):
            if (
                (i not in START_COOR[playerNum])
                and (i not in END_COOR[playerNum])
                and (i not in NEUTRAL_COOR)
            ):
                while i in moves:
                    moves.remove(i)
        return list(set(moves))

    def checkWin(self, playerNum: int):
        """
        Check if all of the player's pieces are in their end zone.
        """
        for i in END_COOR[playerNum]:
            # if there are no pieces
            if self.board[i] == None:
                return False
            # if the piece does not belong to the player
            if (
                isinstance(self.board[i], Piece)
                and self.board[i].getPlayerNum() != playerNum
            ):
                return False
        return True

    def getBoardState(self, playerNum: int):
        """
        Key: subjective coordinates
        Value: piece's player number,
        or 0 if it's vacant
        """
        state = dict()
        for i in self.board:
            state[obj_to_subj_coor(i, playerNum)] = (
                0
                if self.board[i] == None
                else int(self.board[i].getPlayerNum())
            )
        return state

    def getBoolBoardState(self, playerNum: int):
        """
        Returns a dict of the board in subjective coordinates.

        Key: subjective coordinates
        Value: true if occupied, false if vacant
        """
        state = dict()
        for i in self.board:
            state[obj_to_subj_coor(i, playerNum)] = self.board[i] != None
        return state

    def allMovesDict(self, playerNum: int):
        """
        Returns a dict of all valid moves, in subjective coordinates.

        Key: coordinates of a piece (`tuple`),
        Value: list of destination coordinates.
        """
        moves = dict()
        for p in self.pieces[playerNum]:
            p_moves_list = self.getValidMoves(p.getCoor(), playerNum)
            if p_moves_list == []:
                continue
            p_subj_coor = obj_to_subj_coor(p.getCoor(), playerNum)
            moves[p_subj_coor] = [
                obj_to_subj_coor(i, playerNum) for i in p_moves_list
            ]
        return moves

    def movePiece(self, start: tuple, end: tuple):
        """
        Moves a piece from start coord to end coord.
        """
        assert (
            self.board[start] != None and self.board[end] == None
        ), "Start or end coord is occupied."
        self.board[start].setCoor(end)
        self.board[end] = self.board[start]
        self.board[start] = None
