# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:46:21 2020

@author: USER
"""


import game

board=game.game()
game.create(board)
print("Initial Game")
game.printState(board)
game.decideWhoIsFirst(board)
while not game.isFinished(board):
    print("continue game")
    if game.isHumTurn(board):
        game.inputMove(board)
    else:
        board=game.inputComputer(board)
    game.printState(board)

print("Game Over:")
