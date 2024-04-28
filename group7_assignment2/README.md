# Group 7 Assignment 2

## Table of Contents

<!-- toc -->
- [Folder Directory](#folder-directory)
- [Cloning the Repository](#cloning-the-repository)
- [Installing Python Environment](#installing-python-environment)
- [Running the program](#running-the-program)
<!-- tocstop -->

## Folder Directory

```bash
group7_assignment2
├── belief_engine.ipynb
└── BeliefEngine.py
```

## Cloning the Repository

If you do not have the zipped folder, you can clone the repository.

```bash
git clone https://github.com/yufanana/ArtificialIntelligence02180.git
```

## Installing Python Environment

Change directory into the `group7_assignment2` folder.

```bash
cd group7_assignment2
```

To create a new environment with Anaconda, with Python version 3.12, run:

```bash
conda create -n g7_ai2 python=3.12
```

To activate an environment, run:

```bash
conda activate g7_ai2
```

To install the Python packages, run:

```bash
python -m pip install -r requirements.txt
```

## Running the program

The script [`BeliefEngine.py`](BeliefEngine.py) contains the class definition and implementations for the belief revision agent.

The notebook [`belief_engine.ipynb`](belief_engine.ipynb) is the interface to run commands for expansion, contraction and revision. A few sample commands have been included for reference.
