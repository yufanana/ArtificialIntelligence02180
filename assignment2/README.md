# Group 7 Assignment 2

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
assignment2
├── TO BE FILLED
│   ├── TO BE FILLED.py
│   └── TO BE FILLED.py
└── TO BE FILLED.py
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

4. Change back to your branch

```bash
git checkout my-branch
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

## Contribution
