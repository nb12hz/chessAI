# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:37:05 2016

@author: Nick Blais and Mitchell Blais
@student number: 5245741 and 
"""

from __future__ import print_function
import wx
import math

board

"""Basic UI and movement functions"""
#Setup the peices on the board
def intializeBoard():
    global board
    board = ['r','n','b','q','k','b','n','r'],['p1','p2','p3','p4','p5','p6','p7','p8'],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['P1','P2','P3','P4','P5','P6','P7','P8'],['R','N','B','Q','K','B','N','R']
    
def movePiece(startX, startY, endX, endY):
    global board    
    if (board[startY][startX]!=''):
        board[endY][endX]=board[startY][startX]
        board[startY][startX] = ''

#Method to print out the board     
def displayBoard():
    for i in range(8):
        for j in range(8):
            if board[i][j] == '':
                print('-',end = " ")
            else:
                print(board[i][j],end = " ")
        print("")

"""Define the rules for movements in chess"""
def isValidMove(startX, startY, endX, endY):
    global board
    valid = True
    
    piece = (board[startY][startX])[0]
    print(piece)
    if piece=='':
        valid = False
    elif piece=='k'or piece=='K':
        if abs(endX-startX)<=1 or abs(endY-startY)<=1:
            return valid
        
    elif piece=='r' or piece=='R':
        if (startX==endX and startY!=endY) or (startY==endY and startX!=endX):
            return valid
        else:
            valid=False
            
    elif piece=='n'or piece=='N':
        if (abs(startX-endX)==2 and abs(startY-endY)==1) or (abs(startY-endY)==2 and abs(startX-endX)==1):
            return valid
        else:
            valid = False
            
    elif piece=='b'or piece=='B':
        if (abs(startX-endX)==abs(startY-endY) and startX!=endX and startY!=endY):
            return valid
        else:
            valid = False
            
    elif piece=='q'or piece=='Q':
        #moving like a bishop
        if (abs(startX-endX)==abs(startY-endY) and startX!=endX and startY!=endY):
            return valid
        elif (startX==endX and startY!=endY) or (startY==endY and startX!=endX):
            return valid
        else:
            valid = False
            
    """elif piece=='p'or piece=='P':
        if peice=='p':
            if
        else piece=='P':"""
    
    return valid
    
"""Our main function calls"""
intializeBoard()

while(True):
    displayBoard()
    
    user_input = str(input("Start Position X:"))
    choice = -1
    while choice==-1:
        if user_input.isdigit():
            choice = int(user_input)
            if choice>=0 and choice<8:
                startX = choice
                
    user_input = str(input("Start Position Y:"))
    choice = -1
    while choice==-1:
        if user_input.isdigit():
            choice = int(user_input)
            if choice>=0 and choice<8:
                startY = choice
                
    user_input = str(input("End Position X:"))
    choice = -1
    while choice==-1:
        if user_input.isdigit():
            choice = int(user_input)
            if choice>=0 and choice<8:
                endX = choice
    
    user_input = str(input("End Position Y:"))
    choice = -1
    while choice==-1:
        if user_input.isdigit():
            choice = int(user_input)
            if choice>=0 and choice<8:
                endY = choice
    
    if isValidMove(startX,startY,endX,endY):        
        movePiece(startX,startY,endX,endY)