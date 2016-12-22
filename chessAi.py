# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:37:05 2016

@author: Nick Blais and Mitchell Blais
@student number: 5245741 and 
"""

from __future__ import print_function
import wx
import math

board, pawnMoved

"""Basic UI and movement functions"""
#Setup the peices on the board
def intializeBoard():
    global board, pawnMoved
    board = ['r','n','b','q','k','b','n','r'],['p1','p2','p3','p4','p5','p6','p7','p8'],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['P1','P2','P3','P4','P5','P6','P7','P8'],['R','N','B','Q','K','B','N','R']
    pawnMoved = [False for i in range(16)]

#Move the piece in the given coordinates to the target coordinates  
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
    global board, pawnMoved
    valid = True
    
    #Get current and target piece type
    piece = (board[startY][startX])[0]
    if board[endY][endX] != '':
        targetPiece = (board[endY][endX])[0]
    else:
        targetPiece = ''
    
    #No piece to move
    if piece=='':
        valid = False
       
    #If the piece is friendly
    elif targetPiece!='' and piece.isupper() and targetPiece.isupper():
        valid=False
        
    #If the piece is friendly   
    elif targetPiece!='' and piece.islower() and targetPiece.islower():
        valid=False
    
    #Move the king
    elif piece=='k'or piece=='K':
        if abs(endX-startX)<=1 or abs(endY-startY)<=1:
            if (board[startY][startX]==''):
                return valid
            else:
                valid = False
                return valid
    
    #Move the Rook
    elif piece=='r' or piece=='R':
        #make sure it moves in a line
        if (startX==endX and startY!=endY):
            if endY>startY:
                for i in range(startY+1,endY):
                    if board[i][startX]!='':
                        valid = False
                return valid
            else:
                for i in range(startY-1,endY,-1):
                    if board[i][startX]!='':
                        valid = False
                return valid
        #make sure it moves in a line
        elif (startY==endY and startX!=endX):
            if endX>startX:
                for i in range(startX+1,endX):
                    if board[startY][i]!='':
                        valid = False
                return valid
            else:
                for i in range(startX-1,endX,-1):
                    if board[startY][i]!='':
                        valid = False
                return valid
        else:
            valid=False
    
    #Move the knight
    elif piece=='n'or piece=='N':
        if (abs(startX-endX)==2 and abs(startY-endY)==1) or (abs(startY-endY)==2 and abs(startX-endX)==1):
            return valid
        else:
            valid = False
    
    #Move the bishop
    elif piece=='b'or piece=='B':
        #Check that the move is diagonal
        if (abs(startX-endX)==abs(startY-endY) and startX!=endX and startY!=endY):
            difference = abs(startX-endX)-1
            
            #Left and up
            if startX>endX and startY>endY:
                for i in range(difference):
                    if board[startY-1-i][startX-1-i]!='':
                        valid=False
                        return valid
                        
            #Left and down
            elif startX>endX and startY<endY:
                for i in range(difference):
                    if board[startY+1+i][startX-1-i]!='':
                        valid=False
                        return valid
                        
            #Right and Up
            elif startX<endX and startY>endY:
                for i in range(difference):
                    if board[startY-1-i][startX+1+i]!='':
                        valid=False
                        return valid
                        
            #Right and Down
            elif startX<endX and startY<endY:
                for i in range(difference):
                    if board[startY+1+i][startX+1+i]!='':
                        valid=False
                        return valid
                        
            return valid
        else:
            valid = False
    
    #Move the Queen    
    elif piece=='q'or piece=='Q':
        #moving like a Bishop
        if (abs(startX-endX)==abs(startY-endY) and startX!=endX and startY!=endY):
            difference = abs(startX-endX)-1
            
            #Left and up
            if startX>endX and startY>endY:
                for i in range(difference):
                    if board[startY-1-i][startX-1-i]!='':
                        valid=False
                        return valid
                        
            #Left and down
            elif startX>endX and startY<endY:
                for i in range(difference):
                    if board[startY+1+i][startX-1-i]!='':
                        valid=False
                        return valid
                        
            #Right and Up
            elif startX<endX and startY>endY:
                for i in range(difference):
                    if board[startY-1-i][startX+1+i]!='':
                        valid=False
                        return valid
                        
            #Right and Down
            elif startX<endX and startY<endY:
                for i in range(difference):
                    if board[startY+1+i][startX+1+i]!='':
                        valid=False
                        return valid
                        
            return valid
        #Moving like a Rook
        elif (startX==endX and startY!=endY) or (startY==endY and startX!=endX):
            #make sure it moves in a line
            if (startX==endX and startY!=endY):
                if endY>startY:
                    for i in range(startY+1,endY):
                        if board[i][startX]!='':
                            valid = False
                    return valid
                else:
                    for i in range(startY-1,endY,-1):
                        if board[i][startX]!='':
                            valid = False
                    return valid
            #make sure it moves in a line
            elif (startY==endY and startX!=endX):
                if endX>startX:
                    for i in range(startX+1,endX):
                        if board[startY][i]!='':
                            valid = False
                    return valid
                else:
                    for i in range(startX-1,endX,-1):
                        if board[startY][i]!='':
                            valid = False
                    return valid
        else:
            valid = False
    
    #Move pawns
    elif piece=='p'or piece=='P':
        #Black Pieces
        if piece=='p':
            #Capturing
            if abs(startX-endX)==1:
                #Moving forward one spot
                if (endY-startY)==1:
                    #if the spot is occupied by opponent
                    if board[endY][endx]!='' and board[endY][endx].isupper():
                        return valid
                    #Empty or friendly in the spot
                    else:
                        valid = False
                        return valid
                #Invalid move (ie 2 forward or backwards)
                else:
                    valid = False
                    return valid
                    
            #Moving straight forward
            elif startX==endX:
                #Moving forward 2 spots
                if (endY-startY)==2:
                    #Make sure it hasn't moved yet
                    if pawnMoved[(board[startY][startX])[1]-1]==True:
                        return valid
                    else:
                        valid = False
                        return valid
                #Forward 1 spot
                elif (endY-startY)==1:
                    #The spot is empty in front
                    if board[startY][startX]=='':
                        return valid
                    #Spot is occupied
                    else:
                        valid=False
                        return valid
            else:
                valid=False
                return valid
                
        #White Pieces
        else:
            #Capturing
            if abs(startX-endX)==1:
                #Moving forward one spot
                if (endY-startY)==-1:
                    #if the spot is occupied by opponent
                    if board[endY][endx]!='' and board[endY][endx].islower():
                        return valid
                    #Empty or friendly in the spot
                    else:
                        valid = False
                        return valid
                #Invalid move (ie 2 forward or backwards)
                else:
                    valid = False
                    return valid
                    
            #Moving straight forward       
            elif startX==endX:
                #Moving forward 2 spots
                if (endY-startY)==-2:
                    #Make sure it hasn't moved yet
                    if pawnMoved[(board[startY][startX])[1]+7]==True:
                        return valid
                    else:
                        valid = False
                        return valid
                elif (endY-startY)==-1:
                    
                    
                
    else:
        valid=False
    
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