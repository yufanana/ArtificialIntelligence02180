# Assignment 1

Our group has chosen game Chinese Checkers as our game.

The GUI is adapted from [henrychess's repository](https://github.com/henrychess/pygame-chinese-checkers/). The code has been reorganised to have 3 main packages: `bots`,`game_logic`,`gui`. Our group intends to put most of work as new scripts and bots into the `bots` package.

**File directory**

```bash
assignment1
│
│   bots_instructions.md
│   display_coordinates.py
│   game_selection.md
│   LICENSE
│   main.py
│   pyproject.toml
│   README.md
│   requirements.txt
│
├───assets
│
├───bots
│   │   __init__.py
│   │   BotTemplate.py
│   │   GreedyBot0.py
│   │   GreedyBot1.py
│   │   GreedyBot2.py
│   │   RandomBot.py
│
├───game_logic
│   │   __init__.py
│   │   constants.py
│   │   game.py
│   │   helpers.py
│   │   human.py
│   │   piece.py
│   │   player.py
│
├───gui
│   │   __init__.py
│   │   constants.py
│   │   gui_helpers.py
│   │   loops.py
│
└───replays
        2player_replay.txt
        3player_replay.txt
```

## Cloning the Repository

To add SSH keys to your GitHub, follow [this tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# View public key
more C:\Users\<username>\.ssh\id_ed25519.pub
```

For developers,

```bash
git clone git@github.com:yufanana/ArtificialIntelligence02180.git
```

For external viewers/examiners,

```bash
git clone https://github.com/yufanana/ArtificialIntelligence02180.git
```

## Installing with Anaconda

To create a new environment, with Python version 3.12, run:

```bash
conda create -n g7_ai1 python=3.12
```

To activate an environment, run:

```bash
conda activate g7_ai1
```

To install the Python packages, run:

```bash
python -m pip install -r requirements.txt
```

## Installing with virtualenv

```bash
cd ArtificialIntelligence02180/assignment1

pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows,

```bash
cd ArtificialIntelligence02180/assignment1

pip install virtualenv
virtualenv .venv
.venv/Scripts activate
pip install -r requirements.txt
```

## Running the program

First, open a terminal and change to the directory containing `assignment1`.

The command on Linux/Mac should look like this:

```bash
# Linux/Mac
cd ~/ArtificialIntelligence02180/assignment1

# Windows
cd \ArtificialIntelligence02180\assignment1
```

To start the game, run:

```bash
conda activate g7_ai1
python main.py
```

The game will then prompt you to select players after clicking `Play`.

If you want to close the window, you can quit the game by clicking the X button on the top of the window or go to the terminal and press `Ctrl + C` or `cmd + C`.

## Development

To create new custom bots, refer to [bots_development](bots_development.md) for instructions on how to create your own custom bots.
