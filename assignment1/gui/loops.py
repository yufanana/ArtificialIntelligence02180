"""
LoopController class is used to control the game windows displayed.
"""
import os.path
import pygame
import sys
from copy import deepcopy
from game_logic.constants import ALL_COOR
from game_logic.game import Game
from game_logic.helpers import obj_to_subj_coor, setItem
from game_logic.human import HumanPlayer
from game_logic.player import Player, PlayerMeta
from gui.constants import WIDTH, HEIGHT, WHITE, GRAY, BLACK
from gui.gui_helpers import TextButton, drawBoard, highlightMove
from pygame import (
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    KEYDOWN,
    K_LEFT,
    K_RIGHT,
)
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QRadioButton,
    QComboBox,
    QPushButton,
    QFileDialog,
    QGridLayout,
)
from time import strftime


class LoopController:
    """
    Methods consist of MainLoop, MainMenuLoop, LoadPlayerLoop, GameplayLoop,
    GameOverLoop, ReplayLoop, LoadReplayLoop.
    """

    def __init__(self, playerList) -> None:
        self.loopNum = 0
        self.winnerList = list()
        self.replayRecord = list()
        self.playerList = playerList
        self.filePath = ""
        self.playerTypes = {}
        for i in PlayerMeta.playerTypes:
            # key: class name strings, value: class without ()
            self.playerTypes[i.__name__] = i
        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    def mainLoop(self, window: pygame.Surface):
        """
        Controls the flow to enter mainMenuLoop (0), loadPlayerLoop (1),
        gameplayLoop (2), gameOverLoop (3), replayLoop (4), loadReplayLoop (5).
        """

        # First loop to display the main menu
        if self.loopNum == 0:
            pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
            self.filePath = False
            self.replayRecord = []
            self.mainMenuLoop(window)

        elif self.loopNum == 1:
            # from playButton in mainMenuLoop
            # enters loadPlayerLoop to choose player types
            self.loadPlayerLoop()

        elif self.loopNum == 2:
            # from startButton in loadPlayerLoop
            # enters gameplayLoop to play the game
            waitBot = True
            self.winnerList, self.replayRecord = self.gameplayLoop(
                window, self.playerList, waitBot
            )

        elif self.loopNum == 3:
            # from gameplayLoop after a player wins
            self.gameOverLoop(window, self.winnerList, self.replayRecord)

        elif self.loopNum == 4:
            # to view a replay
            pygame.event.set_allowed(
                [QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN]
            )
            pygame.key.set_repeat(100)
            self.replayLoop(window, self.filePath)

        elif self.loopNum == 5:
            # to select a replay file
            self.filePath = self.loadReplayLoop()

    def mainMenuLoop(self, window: pygame.Surface):
        """
        Display the main menu and register events from the buttons.
        """
        window.fill(WHITE)
        titleText = pygame.font.Font(size=int(WIDTH * 0.08)).render(
            "Chinese Checkers", True, BLACK
        )
        titleTextRect = titleText.get_rect()
        titleTextRect.center = (WIDTH * 0.5, HEIGHT * 0.25)
        window.blit(titleText, titleTextRect)
        playButton = TextButton(
            "Play",
            centerx=int(WIDTH * 0.5),
            centery=int(HEIGHT * 0.375),
            width=WIDTH * 0.25,
            height=HEIGHT * 0.125,
            font_size=32,
        )
        loadReplayButton = TextButton(
            "Load replay",
            centerx=int(WIDTH * 0.5),
            centery=int(HEIGHT * 0.625),
            width=WIDTH * 0.25,
            height=HEIGHT * 0.125,
            font_size=32,
        )
        while True:
            ev = pygame.event.wait()
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = ev.type == MOUSEBUTTONDOWN
            if playButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 1
                break
            if loadReplayButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 5
                break

            playButton.draw(window, mouse_pos)
            loadReplayButton.draw(window, mouse_pos)
            pygame.display.update()

    def loadPlayerLoop(self):
        """
        Display a smaller window to select number of players and player types.
        """
        loaded = False

        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        app.aboutToQuit.connect(self.closing)

        Form = QWidget()
        appModifier = 0.75
        appWidth = WIDTH * appModifier
        appHeight = HEIGHT * appModifier
        Form.setWindowTitle("Game Settings")
        Form.resize(appWidth, appHeight)

        box = QWidget(Form)
        box.setGeometry(
            appWidth * 0.0625,
            appHeight * 0.0625,
            appWidth * 0.875,
            appHeight * 0.625,
        )
        grid = QGridLayout(box)

        # Choose number of players
        label_pNum = QLabel(Form)
        label_pNum.setText("No. of Players")

        # 1 player
        rButton_1P = QRadioButton(Form)
        rButton_1P.setText("1")
        rButton_1P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #878787;")
        )
        rButton_1P.toggled.connect(lambda: cBox_p2.setDisabled(True))
        rButton_1P.toggled.connect(lambda: cBox_p3.setDisabled(True))
        rButton_1P.toggled.connect(lambda: setItem(self.playerList, 1, None))
        rButton_1P.toggled.connect(lambda: setItem(self.playerList, 2, None))

        # 2 players
        rButton_2P = QRadioButton(Form)
        rButton_2P.setText("2")
        rButton_2P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #878787;")
        )
        rButton_2P.toggled.connect(lambda: cBox_p2.setDisabled(False))
        rButton_2P.toggled.connect(lambda: cBox_p3.setDisabled(True))
        rButton_2P.toggled.connect(lambda: setItem(self.playerList, 2, None))

        # 3 players
        rButton_3P = QRadioButton(Form)
        rButton_3P.setText("3")
        rButton_3P.setChecked(True)
        rButton_3P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #000000;")
        )
        rButton_3P.toggled.connect(lambda: cBox_p2.setDisabled(False))
        rButton_3P.toggled.connect(lambda: cBox_p3.setDisabled(False))
        rButton_3P.toggled.connect(
            lambda: setItem(
                self.playerList, 2, self.playerTypes[cBox_p3.currentText()]()
            )
        )

        # Choose player types
        label_p1Type = QLabel(Form)
        label_p1Type.setText("Player 1:")
        label_p2Type = QLabel(Form)
        label_p2Type.setText("Player 2:")
        label_p3Type = QLabel(Form)
        label_p3Type.setText("Player 3:")
        cBox_p1 = QComboBox(Form)
        cBox_p2 = QComboBox(Form)
        cBox_p3 = QComboBox(Form)
        cBoxes = (cBox_p1, cBox_p2, cBox_p3)

        # Set initial player types for the 3 combo boxses
        if not loaded:
            for i in range(3):
                grid.addWidget(cBoxes[i], i + 1, 2, 1, 2)
                cBoxes[i].addItems(list(self.playerTypes))
                cBoxes[i].setCurrentIndex(0)
            loaded = True

        # Modify playerList based on the combo box selection
        cBox_p1.currentIndexChanged.connect(
            lambda: setItem(
                self.playerList, 0, self.playerTypes[cBox_p1.currentText()]()
            )
        )
        cBox_p2.currentIndexChanged.connect(
            lambda: setItem(
                self.playerList, 1, self.playerTypes[cBox_p2.currentText()]()
            )
        )
        cBox_p3.currentIndexChanged.connect(
            lambda: setItem(
                self.playerList, 2, self.playerTypes[cBox_p3.currentText()]()
            )
        )
        
        # Add widgets to the grid
        grid.addWidget(label_pNum, 0, 0)
        grid.addWidget(rButton_1P, 0, 1)
        grid.addWidget(rButton_2P, 0, 2)
        grid.addWidget(rButton_3P, 0, 3)
        grid.addWidget(label_p1Type, 1, 0, 1, 2)
        grid.addWidget(label_p2Type, 2, 0, 1, 2)
        grid.addWidget(label_p3Type, 3, 0, 1, 2)

        # Start button
        startButton = QPushButton(Form)
        startButton.setText("Start Game")
        startButton.setGeometry(
            appWidth * 0.625,
            appHeight * 0.8125,
            appWidth * 0.25,
            appHeight * 0.125,
        )
        startButton.clicked.connect(self.startGame)

        # Cancel button
        cancelButton = QPushButton(Form)
        cancelButton.setText("Back to Menu")
        cancelButton.setGeometry(
            appWidth * 0.125,
            appHeight * 0.8125,
            appWidth * 0.25,
            appHeight * 0.125,
        )
        cancelButton.clicked.connect(self.backToMenu)

        Form.show()
        app.exec()

    # helpers for loadPlayerLoop and replayLoop
    def startGame(self):
        '''
        Make main loop enter the gameplay loop.
        '''
        self.loopNum = 2
        QApplication.closeAllWindows()

    # helpers for loadPlayerLoop and replayLoop
    def backToMenu(self):
        '''
        Make main loop enter the main menu.
        '''
        self.loopNum = 0
        QApplication.closeAllWindows()

    def gameplayLoop(
        self,
        window: pygame.Surface,
        playerss: list[Player],
        waitBot: bool = False,
    ):
        """
        Returns:
            [results, replayRecord]
            result : len(n_players-1), list of winning player numbers with
                the 1st winnder at index 0. -1 if draw.
            replayRecord : list of moves in the game.
        """
        playingPlayerIndex = 0
        humanPlayerNum = 0
        returnStuff = [[], []]
        replayRecord = []

        # Check player types, total and set player numbers
        players = deepcopy(playerss)
        while None in players:
            players.remove(None)
        # if len(players) > 3:        # why is this needed?
        #     players = players[:3]
            
        for i in range(len(players)):
            players[i].setPlayerNum(i + 1)

        # 1st line in replayRecord is the number of players
        replayRecord.append(str(len(players)))

        # Generate the game
        g = Game(len(players))
        oneHuman = exactly_one_is_human(players)
        if oneHuman:
            for player in players:
                if isinstance(player, HumanPlayer):
                    humanPlayerNum = player.getPlayerNum()

        # Start the game loop
        highlight = []  # list of start and end coordinates of picked move
        while True:
            playingPlayer = players[playingPlayerIndex]
            # If 100 milliseconds has passed and there is no event, ev will be
            # NOEVENT and the bot player will make a move. Otherwise, the bot
            # player won't move until you move your mouse.

            # if waitBot:
            #     ev.type == KEYDOWN
            #         and ev.key == K_RIGHT
            #     ev = pygame.event.wait()
            # else:
            ev = pygame.event.wait(100)

            # Quit the game if the window is closed
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

            # Draw the board
            window.fill(GRAY)
            if humanPlayerNum != 0:
                drawBoard(g, window, humanPlayerNum)
            else:
                drawBoard(g, window)

            # Highlight the 2 coordinates of the move
            if highlight:
                highlightMove(g, window, highlight)

            backButton = TextButton(
                "Back to Menu",
                width=int(HEIGHT * 0.25),
                height=int(HEIGHT * 0.0833),
                font_size=int(WIDTH * 0.04),
            )

            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = ev.type == MOUSEBUTTONDOWN

            # Return to main menu if the back button is clicked
            if backButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 0
                return ([], [])
            backButton.draw(window, mouse_pos)
            pygame.display.update()

            # Playing player makes a move
            if isinstance(playingPlayer, HumanPlayer):
                # Human player makes a move
                start_coor, end_coor = playingPlayer.pickMove(
                    g, window, humanPlayerNum, highlight
                )
                if (not start_coor) and (not end_coor):
                    # Return to main menu
                    self.loopNum = 0
                    return ([], [])
            else:
                # Bot player makes a move
                start_coor, end_coor = playingPlayer.pickMove(g)
            g.movePiece(start_coor, end_coor)

            if oneHuman:
                highlight = [
                    obj_to_subj_coor(start_coor, humanPlayerNum),
                    obj_to_subj_coor(end_coor, humanPlayerNum),
                ]
            else:
                highlight = [start_coor, end_coor]

            replayRecord.append(str(start_coor) + "to" + str(end_coor))

            # Check if the playing player has won
            winning = g.checkWin(playingPlayer.getPlayerNum())

            if winning and len(players) == 2:
                if humanPlayerNum != 0:
                    drawBoard(g, window, humanPlayerNum)
                else:
                    drawBoard(g, window)
                playingPlayer.has_won = True
                returnStuff[0].append(playingPlayer.getPlayerNum())
                # print('The winner is Player %d' % playingPlayer.getPlayerNum())
                returnStuff[1] = replayRecord

                # Go to the game over loop
                self.loopNum = 3
                # print(returnStuff)
                return returnStuff
            elif winning and len(players) == 3:
                playingPlayer.has_won = True
                returnStuff[0].append(playingPlayer.getPlayerNum())
                players.remove(playingPlayer)
                # TODO: show the message on screen
                # print("The first winner is Player %d" % playingPlayer.getPlayerNum())

            # Switch to the next player
            playingPlayerIndex = (playingPlayerIndex + 1) % len(players)

    def replayLoop(self, window: pygame.Surface, filePath: str = None):
        # Check if a path has been selected
        if not filePath:
            print("File Path is void!")
            self.loopNum = 0

        # Replay the game
        if (not self.replayRecord) and filePath:
            isValidReplay = True
            move_list = []
            with open(filePath) as f:
                text = f.read()
                move_list = text.split("\n")
                playerCount = move_list.pop(0)
                if not eval(playerCount) in (2, 3):
                    self.showNotValidReplay()
                    isValidReplay = False
                else:
                    playerCount = eval(playerCount)
                    for i in range(len(move_list)):
                        move_list[i] = move_list[i].split("to")
                        if len(move_list[i]) != 2:
                            self.showNotValidReplay()
                            isValidReplay = False
                            break
                        else:
                            for j in range(len(move_list[i])):
                                move_list[i][j] = eval(move_list[i][j])
                                if not isinstance(move_list[i][j], tuple):
                                    self.showNotValidReplay()
                                    isValidReplay = False
                                    break

            for i in range(len(move_list)):
                if (
                    move_list[i][0] not in ALL_COOR
                    or move_list[i][1] not in ALL_COOR
                ):
                    self.showNotValidReplay()
                    isValidReplay = False
                    break
            if isValidReplay:
                self.replayRecord = [playerCount] + move_list
        if self.replayRecord:
            if f:
                del f
            if text:
                del text
            playerCount = self.replayRecord.pop(0)
            g = Game(playerCount)
            prevButton = TextButton(
                "<",
                centerx=WIDTH * 0.125,
                centery=HEIGHT * 0.5,
                width=int(WIDTH / 8),
                height=int(HEIGHT / 6),
                font_size=int(WIDTH * 0.04),
            )
            nextButton = TextButton(
                ">",
                centerx=WIDTH * 0.875,
                centery=HEIGHT * 0.5,
                width=int(WIDTH / 8),
                height=int(HEIGHT / 6),
                font_size=int(WIDTH * 0.04),
            )
            backButton = TextButton(
                "Back to Menu",
                width=int(HEIGHT * 0.25),
                height=int(HEIGHT * 0.0833),
                font_size=int(WIDTH * 0.04),
            )
            moveListIndex = -1
            left = False
            right = False
            highlight = []
            window.fill(WHITE)
            hintText = pygame.font.Font(size=int(HEIGHT * 0.05)).render(
                "Use the buttons or the left and right arrow keys to navigate through the game",
                antialias=True,
                color=BLACK,
                wraplength=int(WIDTH * 0.375),
            )
            hintTextRect = hintText.get_rect()
            hintTextRect.topright = (WIDTH, 1)
            window.blit(hintText, hintTextRect)
            while True:
                ev = pygame.event.wait()
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if moveListIndex == -1:
                    prevButton.enabled = False
                else:
                    prevButton.enabled = True
                if moveListIndex == len(move_list) - 1:
                    nextButton.enabled = False
                else:
                    nextButton.enabled = True
                mouse_pos = pygame.mouse.get_pos()
                mouse_left_click = ev.type == MOUSEBUTTONDOWN
                left = (
                    ev.type == KEYDOWN
                    and ev.key == K_LEFT
                    and prevButton.enabled
                )
                right = (
                    ev.type == KEYDOWN
                    and ev.key == K_RIGHT
                    and nextButton.enabled
                )
                if backButton.isClicked(mouse_pos, mouse_left_click):
                    self.loopNum = 0
                    break
                if prevButton.isClicked(mouse_pos, mouse_left_click) or left:
                    moveListIndex -= 1
                    # reverse-move move_list[moveListIndex + 1]
                    g.movePiece(
                        move_list[moveListIndex + 1][1],
                        move_list[moveListIndex + 1][0],
                    )
                    highlight = (
                        move_list[moveListIndex] if moveListIndex >= 0 else []
                    )
                if nextButton.isClicked(mouse_pos, mouse_left_click) or right:
                    moveListIndex += 1
                    # move move_list[moveListIndex]
                    g.movePiece(
                        move_list[moveListIndex][0],
                        move_list[moveListIndex][1],
                    )
                    highlight = move_list[moveListIndex]
                prevButton.draw(window, mouse_pos)
                nextButton.draw(window, mouse_pos)
                backButton.draw(window, mouse_pos)
                drawBoard(g, window)
                if highlight:
                    highlightMove(g, window, highlight)
                pygame.display.update()

    def loadReplayLoop(self):
        """
        Display a smaller window to select a replay file.
        """
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        if not os.path.isdir("./replays"):
            os.mkdir("./replays")
        filePath = QFileDialog.getOpenFileName(dir="./replays", filter="*.txt")[
            0
        ]
        if filePath:
            # print(filePath)
            self.loopNum = 4
            return filePath
        else:
            # print("cancelled")
            self.loopNum = 0
            return False

    def gameOverLoop(
        self, window: pygame.Surface, winnerList: list, replayRecord: list
    ):
        # print(winnerList); print(replayRecord)
        # winner announcement text
        if len(winnerList) == 1:
            winnerString = "Player %d wins" % winnerList[0]
        elif len(winnerList) == 2:
            winnerString = "Player %d wins, then Player %d wins" % (
                winnerList[0],
                winnerList[1],
            )
        else:
            winnerString = "len(winnerList) is %d" % len(winnerList)
        font = pygame.font.SysFont("Arial", int(WIDTH * 0.04))
        text = font.render(winnerString, True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (int(WIDTH * 0.5), int(HEIGHT / 6))
        window.blit(text, textRect)

        # Create buttons
        menuButton = TextButton(
            "Back to menu",
            centerx=int(WIDTH * 0.25),
            centery=int(HEIGHT * 2 / 3),
        )
        exportReplayButton = TextButton(
            "Export replay",
            centerx=int(WIDTH * 0.75),
            centery=int(HEIGHT * 2 / 3),
        )

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = pygame.mouse.get_pressed()[0]
            if menuButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 0
                break
            if exportReplayButton.isClicked(mouse_pos, mouse_left_click):
                curTime = strftime("%Y%m%d-%H%M%S")
                if not os.path.isdir("./replays"):
                    os.mkdir("./replays")
                with open(f"./replays/replay-{curTime}.txt", mode="w+") as f:
                    for i in range(len(replayRecord)):
                        if i < len(replayRecord) - 1:
                            f.write(str(replayRecord[i]) + "\n")
                        else:
                            f.write(str(replayRecord[i]))
                exportReplayButton.text = "Replay exported!"
                exportReplayButton.enabled = False
            menuButton.draw(window, mouse_pos)
            exportReplayButton.draw(window, mouse_pos)
            pygame.display.update()

    def closing(self):
        if self.loopNum == 0 or self.loopNum == 1:
            self.backToMenu()
        elif self.loopNum == 2:
            self.startGame()

    def showNotValidReplay(self):
        print("This is not a valid replay!")
        self.loopNum = 0


def exactly_one_is_human(players: list[Player]):
    """
    Checks through the list of players to see if exactly one of them is human.
    """
    only_one = False
    for player in players:
        if only_one is False and isinstance(player, HumanPlayer):
            only_one = True
        elif only_one is True and isinstance(player, HumanPlayer):
            return False
    return only_one


def trainingLoop(g: Game, players: list[Player], recordReplay: bool = False):
    """
    Not sure what this does. Currently not used.
    """
    playingPlayerIndex = 0
    replayRecord = []
    if recordReplay:
        replayRecord.append(str(len(players)))

    # Ensure no humans are playing
    for player in players:
        assert not isinstance(player, HumanPlayer), (
            "Can't have humans during training! Human at player %d"
            % players.index(player)
            + 1
        )

    for i in range(len(players)):
        players[i].setPlayerNum(i + 1)

    # Main training game loop
    while True:
        playingPlayer = players[playingPlayerIndex]

        # Playing player makes a move
        start_coor, end_coor = playingPlayer.pickMove(g)
        g.movePiece(start_coor, end_coor)

        if recordReplay:
            replayRecord.append(str(start_coor) + " " + str(end_coor))

        winning = g.checkWin(playingPlayer.getPlayerNum())

        if winning and len(players) == 2:
            playingPlayer.has_won = True
            print("The winner is Player %d" % playingPlayer.getPlayerNum())
            print(f"{len(replayRecord)} moves")
            break  # TODO: return stuff?
        elif winning and len(players) == 3:
            playingPlayer.has_won = True
            players.remove(playingPlayer)
            print(
                "The first winner is Player %d" % playingPlayer.getPlayerNum()
            )
        if playingPlayerIndex >= len(players) - 1:
            playingPlayerIndex = 0
        else:
            playingPlayerIndex += 1
