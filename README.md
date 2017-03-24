# py_ms

py_ms is a CLI-based Minesweeper and solver written in Python.

Additionally, there is Docker support and unit tests utilizing unittest.

## Prerequisites

> Suggest using built-in means like `brew`, `apt-get` or `pip` to avoid human error.

* Python 2.7.x - https://www.python.org/downloads/release/python-2713/
* (optional) Docker - https://docs.docker.com/engine/getstarted/

## Running py_ms

From the repo directory:

    python ./Minesweeper.py

## Solver

An automatic way to solve Minesweeper. The current thought process is the following:

1. Identify all safe moves and mines based on immediate neighbors
2. Identify all safe moves based on known mines
3. Identify all safe moves by using neighbors' info
4. Identify least risky move
5. Blind click if no other options are found

The pass rate is a little above 90% (100,000 iterations) currently.
