# Assignment 1

Our group has chosen **Chinese Checkers** as our game.

The GUI is adapted from [henrychess's repository](https://github.com/henrychess/pygame-chinese-checkers/). The code has been reorganised to have 3 main packages: `bots`,`game_logic`,`gui`. Our group intends to put most of work as new scripts and bots into the `bots` package.

## Table of Contents

<!-- toc -->

- [Folder Directory](#folder-directory)
- [Cloning the Repository](#cloning-the-repository)
- [Installing Python Environment](#installing-python-environment)
  - [With Anaconda](#with-anaconda)
  - [With venv](#with-venv)
  - [With virtualenv](#with-virtualenv)
- [Running the program](#running-the-program)
- [Development](#development)

<!-- tocstop -->

## Folder Directory

```bash
assignment1
├── bots
│   ├── __init__.py
│   ├── BotTemplate.py
│   ├── GreedyBot0.py
│   ├── GreedyBot1.py
│   ├── GreedyBot2.py
│   └── RandomBot.py
├── game_logic
│   ├── __init__.py
│   ├── constants.py
│   ├── game.py
│   ├── helpers.py
│   ├── human.py
│   ├── piece.py
│   └── player.py
├── gui
│   ├── __init__.py
│   ├── constants.py
│   ├── gui_helpers.py
│   └── loops.py
├── assets
│   ├── bots_development.md
│   └── game_selection.md
├── replays
│   ├── 2player_replay.txt
│   └── 3player_replay.txt
├── LICENSE
├── pyproject.toml
├── README.md
├── main.py
├── requirements.txt
└── display_coordinates.py

```

## Cloning the Repository

For external viewers/examiners,

```bash
git clone https://github.com/yufanana/ArtificialIntelligence02180.git
```

For developers, follow [this tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to add SSH keys to your GitHub.

Run this command to clone.

```bash
git clone git@github.com:yufanana/ArtificialIntelligence02180.git
```

## Installing Python Environment

### With Anaconda

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

### With venv

```bash
cd ArtificialIntelligence02180/assignment1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### With virtualenv

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

To create new custom bots, refer to [bots_development](assets/bots_development.md) for instructions on how to create your own custom bots.

### Configurations

 - The configurations for the game set up can be modified in the [`config.yaml`](config/config0.yaml) files inside the [`config`](config) folder.
- To use a different config for a game, modify the `config_name` hydra parameter inside above `main()` in [`main.py`](main.py)
- The string to represent the player type should be exactly the class name. </br>
e.g. `Human` and not `human`, `GreedyBot0` and not `Greedybot`.
