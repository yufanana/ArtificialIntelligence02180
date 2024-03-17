# Group 7 Assignment 1

Our group has chosen **Chinese Checkers** as our game.

<img src="assets/MMLadder_opening.png" width="400"/>


The GUI is adapted from [henrychess's repository](https://github.com/henrychess/pygame-chinese-checkers/). The group's work is explained in the [Contribution](#contribution) section. Links to the YouTube videos of the game play are available in the [Running the program](#running-the-program) section.

## Table of Contents

<!-- toc -->
- [Folder Directory](#folder-directory)
- [Cloning the Repository](#cloning-the-repository)
- [Installing Python Environment](#installing-python-environment)
- [Running the program](#running-the-program)
- [Development](#development)
- [Contribution](#contribution)
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
│   ├── GroupBot.py
│   ├── LadderBot.py
│   ├── MMCluster.py
│   ├── MMLadder.py
│   └── RandomBot.py
├── config
│   ├── config-ladder-greedy2.yaml
│   ├── config-mmcluster-greedy1.yaml
│   ├── config-mmcluster-greedy2.yaml
│   ├── config-mmcluster-mmladder.yaml
│   └── config-mmladder-greedy2.yaml
├── game_logic
│   ├── __init__.py
│   ├── game.py
│   ├── helpers.py
│   ├── human.py
│   ├── layout.py
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
│   ├── MMCluster_Greedy2.txt
│   ├── MMCluster_MMLadder.txt
│   └── MMLadder_Greedy2.txt
├── README.md
├── main.py
├── requirements.txt
├── LICENSE
├── pyproject.toml
└── display_coordinates.py
```

## Cloning the Repository

If you do not have the zipped folder, you can clone the repository.

```bash
git clone https://github.com/yufanana/ArtificialIntelligence02180.git
```

## Installing Python Environment

Change directory into the `group7_assignment1` folder.

```bash
cd group7_assignment1
```

### With Anaconda (recommended)

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
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### With virtualenv

```bash
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows,

```bash
pip install virtualenv
virtualenv .venv
.venv/Scripts activate
pip install -r requirements.txt
```

## Running the program

### Replay

The group has recorded a few complete game plays to avoid the long computation time for actual game play (~10mins for a full game). The replay mode can be selected at the main menu of the GUI. To toggle autoplay, you may have to double-click on the `Autoplay` button a few times.

If you prefer to watch the recorded game play, the replays can be found in the YouTube links below.

- [MMLadder vs Greedy2](https://youtu.be/ChkEJpHClPY)
- [MMLadder vs MMCluster](https://youtu.be/dTW4lY1AmtY)
- [MMCluster vs Greedy2](https://youtu.be/pVf_NswFP8Q)


### Game Play

The group has developed 2 main minimax bots `MMCluster` and `MMLadder`. To watch the bots play against `GreedyBot2`, the configuration file can be selected by commenting out the relevant lines in [`main.py`](main.py) line 23-26. A full round with one of the minimax bots takes about 10 minutes on our computers.

First, open a terminal and change directory to the root folder of assignment 1 and activate the virtual environment.

```bash
cd group7_assignment1
conda activate g7_ai1
```

Start the game.

```bash
python main.py
```

If you want to close the window, you can quit the game by clicking the X button on the top of the window or pressing `Ctrl + C` or `cmd + C` in the terminal.


## Development

For developers, follow [this tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to add SSH keys to your GitHub.

Run this command to clone.

```bash
git clone git@github.com:yufanana/ArtificialIntelligence02180.git
```

To create new custom bots, refer to [bots_development](assets/bots_development.md) for instructions on how to create your own custom bots.

### Updating your Branch

1. Commit whatever changes you have on your branch.

```bash
git add .
git commit -m "describe your changes"
```

2. Change to the main branch

```bash
git checkout main
```

3. Get the latest updates

```bash
git pull
```

4. Change back to your adversarial branch

```bash
git checkout my-adversarial
```

5. Rebase your branch onto the main branch

```bash
git rebase main
```

6. If there are any conflicts, resolve them in VS Code. Find the files that have been highlighted red with an exclamation mark in the `Folder Explorer`. After you have resolved the conflicts, run

```bash
git rebase --continue
```

7. Done! :)

### Configurations

 - The configurations for the game set up can be modified in the [`config.yaml`](config/config0.yaml) files inside the [`config`](config) folder.
- To use a different config for a game, modify the `config_name` parameter inside `main()` in [`main.py`](main.py)
- The string to represent the player type should be exactly the class name. </br>
e.g. `Human` and not `human`, `GreedyBot0` and not `Greedybot`.

## Contribution

The code has been reorganised to have 3 main packages: `bots`,`game_logic`,`gui`.

Our group has placed most of work as new scripts and bots in the `bots` package,
- `MMLadder.py`
- `MMCluster.py`
- `LadderBot.py`
- `GroupBot.py`

There were improvements in the GUI, with the following new functions implemented.
- `game_logic` package
    - `game.py`: `getMovePath()`, `checkValidStepDest()`
    - `layout.py`: new mirror layout, reduced pieces to 10
- `gui` package
    - `gui_helpers.py`: `drawPath()`, `drawCoordinates()`, `drawPlayerTypes()`, `drawTurnCount()`
    - `loops.py`: modified to work for more than 3 players
- `config` folder
    - Introduced a new way to load player types using yaml files instead of GUI.
