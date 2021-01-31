# SPDX-FileCopyrightText: 2021 Ricardo Garcia <r@rg3.name>
# SPDX-License-Identifier: CC0-1.0

MathGame: Game to play with additions, substractions and multiplications

Usage: mathgame.py add|sub|mul NUMBER_FROM_1_TO_10

The first argument is the type of operation to play with.

    * add means additions.
    * sub means substractions.
    * mul means multiplications.

The second argument is the largest "table" to use in the questions, and it
should be a number from 1 to 10. For example, to play with additions up to
6+SOMETHING, use:

    mathgame.py add 6

To stop playing the game at any point in time, answer "q" to the question or
press Ctrl+C.
