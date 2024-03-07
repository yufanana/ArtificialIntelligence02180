"""
Game Class to represent the game state and logic.
"""
import copy
from game_logic.helpers import add, checkJump, obj_to_subj_coor, mult
from game_logic.constants import (
    DIRECTIONS,
    END_COOR,
    NEUTRAL_COOR,
    START_COOR,
    ALL_COOR,
)
from game_logic.piece import Piece
from gui.constants import HEIGHT, WIDTH
from typing import List


class Move:
    """
    Class to backtrace the path of a move.
    """

    def __init__(self, coord: tuple):
        self.parent = None
        self.coord = coord
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def getPath(self):
        """
        Recursively add the parent to the path.
        """
        path = [self.coord]
        if self.parent is self:  # reached the root node
            return path
        else:  # recurse
            return self.parent.getPath() + path


class Game:
    def __init__(self, playerCount=3):
        if playerCount in (2, 3):
            self.playerCount = playerCount
        else:
            self.playerCount = 3
        self.playerList = []
        self.pieces: dict[int, set[Piece]] = {1: set(), 2: set(), 3: set()}
        self.board: List[Piece] = self.createBoard(playerCount)
        self.turnCount = 1
        self.playerNames = 0
        self.playerNum = 0

        # Parameters for drawing board
        self.unitLength = int(WIDTH * 0.05)  # unitLength length in pixels
        self.lineWidth = int(self.unitLength * 0.05)  # line width
        self.circleRadius = int(HEIGHT * 0.025)  # board square (circle) radius
        self.centerCoor = (WIDTH / 2, HEIGHT / 2)  # window size is 800*600

    def createBoard(self, playerCount: int):
        """
        Returns a dict of the board. Adds pieces to starting zones.
        """
        Board = {}

        for x, y in ALL_COOR:
            Board[(x, y)] = None

        # Add empty spaces first because a player's start zones overlaps with
        # another player's end zone

        # Add pieces
        for playerNum in range(1, playerCount + 1):
            for p, q in START_COOR[playerNum]:
                Board[(p, q)] = Piece(playerNum, p, q)
                self.pieces[playerNum].add(Board[p, q])

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

        # Try all 6 directions
        for direction in DIRECTIONS:
            destination = add(startPos, direction)
            # Step is out of bounds
            if destination not in self.board:
                continue

            # Single step into open space
            if self.board[destination] is None:
                moves.append(destination)  # walk

            # Single step into occupied space, check for skips
            else:  # self.board[destination] is not None
                destination = add(destination, direction)
                if (
                    destination not in self.board
                    or self.board[destination] is not None
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

    def checkValidStepDest(self, playerNum: int, dest: tuple):
        """
        Check if the destination is valid single step for the player.

        Args:
            playerNum (int): the player number.
            dest (tuple): the objective coordinates of the destination.

        Returns:
            bool: True if the destination is valid.
        """
        if dest not in self.board:  # out of bounds
            return False
        if self.board[dest] is not None:  # occupied cell
            return False
        if (
            dest not in NEUTRAL_COOR  # other player's territory
            and dest not in END_COOR[playerNum]
            and dest not in START_COOR[playerNum]
        ):
            return False
        return True

    def checkValidJumpDest(self, playerNum: int, dest: tuple):
        """
        Check if the destination is valid jump for the player.

        Args:
            playerNum (int): the player number.
            dest (tuple): the objective coordinates of the destination.

        Returns:
            bool: True if the destination is valid.
        """
        if dest not in self.board:  # out of bounds
            return False
        # if (dest not in NEUTRAL_COOR    # other player's territory
        #     and dest not in END_COOR[playerNum]
        #     and dest not in START_COOR[playerNum]
        #     ):
        #     return False
        return True

    def getMovePath(self, playerNum: int, start: tuple, end: tuple):
        """
        Find the path for the move using breadth-first search.

        Args:
            playerNum (int): the player number.
            start (tuple): objective coordinates of the starting cell.
            end (tuple): objective coordinates of the ending cell.

        Returns:
            path (list(tuples)): objective coordinates of cells along the path.
        """
        # print(f"getMovePath({start}, {end})")
        start_m = Move(start)
        start_m.parent = start_m
        path = []

        # Single step
        for dir in DIRECTIONS:
            dest = add(start, dir)
            dest_m = Move(dest)
            if not self.checkValidStepDest(playerNum, dest):
                continue
            start_m.addChild(dest_m)
            # Found end cell, return path
            if dest == end:
                path += dest_m.getPath()
                # print("full step path:", path, "\n")
                return path

        # Jump steps using BFS
        queue = [start_m]
        while queue:
            current = queue.pop(0)
            for dir in DIRECTIONS:
                stepDest = add(current.coord, dir)
                if not self.checkValidJumpDest(playerNum, stepDest):
                    continue
                if self.board[stepDest] is None:  # no piece to skip
                    continue
                jumpDir = mult(dir, 2)
                dest = add(current.coord, jumpDir)
                dest_m = Move(dest)
                if not self.checkValidJumpDest(playerNum, dest):
                    continue
                if dest == current.parent.coord:
                    continue  # prevents endless loops

                dest_m.parent = current
                current.addChild(dest_m)
                if dest == end:
                    path += dest_m.getPath()
                    # print("full jump path:", path, "\n")
                    return path
                queue.append(dest_m)

        # return path
        # Assumes that a path will be found eventually.
        if path == []:
            raise ValueError("No path found")

    def checkWin(self, playerNum: int):
        """
        Check if all of the player's pieces are in their end zone.
        """
        for i in END_COOR[playerNum]:
            # if there are no pieces
            if self.board[i] is None:
                return False
            # if the piece does not belong to the player
            if (
                isinstance(self.board[i], Piece)
                and self.board[i].getPlayerNum() != playerNum
            ):
                return False
        return True

    def isOver(self):
        """
        Check if the game is over.
        """
        for i in range(1, self.playerCount + 1):
            if self.checkWin(i):
                return True
        return False

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
                if self.board[i] is None
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
            state[obj_to_subj_coor(i, playerNum)] = self.board[i] is not None
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
        assert self.board[start] is not None, "startCoord is empty"
        assert self.board[end] is None, "endCoord is occupied"

        # Update piece attribute
        self.board[start].setCoor(end)

        # Change piece's location in g.board
        self.board[end] = self.board[start]
        self.board[start] = None
