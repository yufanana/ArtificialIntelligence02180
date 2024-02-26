import sys
import math

from pygame.locals import *
from game_logic.game import Game
from game_logic.player import Player
from gui.literals import *
from gui.gui_helpers import *

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def pickMove(
        self,
        g: Game,
        window: pygame.Surface,
        humanPlayerNum: int = 0,
        highlight=None,
    ):
        pieceSet: set[Piece] = g.pieces[self.playerNum]
        validmoves = []
        clicking = False
        selected_piece_coor = ()
        prev_selected_piece_coor = ()
        # pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        while True:
            ev = pygame.event.wait()
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            # wait for a click,
            # if mouse hovers on a piece, highlight it
            mouse_pos = pygame.mouse.get_pos()
            clicking = ev.type == MOUSEBUTTONDOWN
            
            if highlight:
                pygame.draw.circle(
                    window,
                    (117, 10, 199),
                    abs_coors(g.centerCoor, highlight[0], g.unitLength),
                    g.circleRadius,
                    g.lineWidth + 2,
                )
                pygame.draw.circle(
                    window,
                    (117, 10, 199),
                    abs_coors(g.centerCoor, highlight[1], g.unitLength),
                    g.circleRadius,
                    g.lineWidth + 2,
                )

            backButton = TextButton(
                "Back to Menu",
                width=int(HEIGHT * 0.25),
                height=int(HEIGHT * 0.0833),
                font_size=int(WIDTH * 0.04),
            )
            if backButton.isClicked(mouse_pos, clicking):
                return (False, False)
            backButton.draw(window, mouse_pos)

            for piece in pieceSet:
                coor = (
                    obj_to_subj_coor(piece.getCoor(), self.playerNum)
                    if humanPlayerNum != 0
                    else piece.getCoor()
                )
                absCoor = abs_coors(g.centerCoor, coor, g.unitLength)
                if (
                    math.dist(mouse_pos, absCoor) <= g.circleRadius
                    and piece.mouse_hovering == False
                ):
                    # change the piece's color
                    pygame.draw.circle(
                        window,
                        brighten_color(
                            PLAYER_COLORS[piece.getPlayerNum() - 1], 0.75
                        ),
                        absCoor,
                        g.circleRadius - 2,
                    )
                    piece.mouse_hovering = True
                elif (
                    math.dist(mouse_pos, absCoor) > g.circleRadius
                    and piece.mouse_hovering == True
                    and tuple(window.get_at(ints(absCoor))) != WHITE
                ):
                    # draw a circle of the original color
                    pygame.draw.circle(
                        window,
                        PLAYER_COLORS[piece.getPlayerNum() - 1],
                        absCoor,
                        g.circleRadius - 2,
                    )
                    piece.mouse_hovering = False
                # when a piece is selected, and you click any of the valid destinations,
                # you will move that piece to the destination
                if selected_piece_coor == piece.getCoor() and validmoves != []:
                    for d in validmoves:
                        destCoor = (
                            abs_coors(
                                g.centerCoor,
                                obj_to_subj_coor(d, self.playerNum),
                                g.unitLength,
                            )
                            if humanPlayerNum != 0
                            else abs_coors(g.centerCoor, d, g.unitLength)
                        )
                        if math.dist(mouse_pos, destCoor) <= g.circleRadius:
                            if clicking:
                                return [selected_piece_coor, d]
                            # draw a gray circle
                            else:
                                pygame.draw.circle(
                                    window,
                                    LIGHT_GRAY,
                                    destCoor,
                                    g.circleRadius - 2,
                                )
                        elif math.dist(mouse_pos, destCoor) > g.circleRadius:
                            # draw a white circle
                            pygame.draw.circle(
                                window, WHITE, destCoor, g.circleRadius - 2
                            )
                # clicking the piece
                if (
                    math.dist(mouse_pos, absCoor) <= g.circleRadius
                    and clicking == True
                ):
                    selected_piece_coor = piece.getCoor()
                    if (
                        prev_selected_piece_coor != ()
                        and selected_piece_coor != prev_selected_piece_coor
                    ):
                        if humanPlayerNum != 0:
                            g.drawBoard(window, self.playerNum)
                        else:
                            g.drawBoard(window)
                    prev_selected_piece_coor = selected_piece_coor
                    # draw a semi-transparent gray circle outside the piece
                    pygame.draw.circle(
                        window,
                        (161, 166, 196, 50),
                        absCoor,
                        g.circleRadius,
                        g.lineWidth + 1,
                    )
                    # draw semi-transparent circles around all coordinates in getValidMoves()
                    validmoves = g.getValidMoves(
                        selected_piece_coor, self.playerNum
                    )
                for c in validmoves:
                    c2 = (
                        obj_to_subj_coor(c, self.playerNum)
                        if humanPlayerNum != 0
                        else c
                    )
                    pygame.draw.circle(
                        window,
                        (161, 166, 196),
                        abs_coors(g.centerCoor, c2, g.unitLength),
                        g.circleRadius,
                        g.lineWidth + 2,
                    )

            pygame.display.update()
            # return [start_coor, end_coor]
