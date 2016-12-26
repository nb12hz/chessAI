# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:37:05 2016

@author: Nick Blais and Mitchell Blais
@student number: 5245741 and 5686779
"""

from __future__ import print_function
import wx
import math
from minimax import minimax
import copy

"""Booleans for kings and rooks, used for castling"""
whiteKS = False
whiteQS = False
blackKS = False
blackQS = False
whiteKing = False
blackKing = False

"""These functions are for the defintion of the chess board
This allows for playing chess without an AI"""
"""Basic UI and movement functions"""
#Setup the peices on the board
def intializeBoard():
    global board
    global pawnMoved
    global movedTwo
    global attackedByWhite
    global attackedByBlack
    
    board = ['r','n','b','q','k','b','n','r'],['p1','p2','p3','p4','p5','p6','p7','p8'],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['','','','','','','',''],['P1','P2','P3','P4','P5','P6','P7','P8'],['R','N','B','Q','K','B','N','R']
    #Black is 0-7, White is 8-15    
    pawnMoved = [False for i in range(16)]
    #Black is 0-7, White is 8-15
    movedTwo = [False for i in range(16)]
    #Intialize attacked by White array
    attackedByWhite = [[False for i in range(8)] for j in range(8)]
    #Intialize attacked by Black array
    attackedByBlack = [[False for i in range(8)] for j in range(8)]
    
#Move the piece in the given coordinates to the target coordinates  
def movePiece(startX, startY, endX, endY):
    global board    
    if (board[startY][startX]!=''):
        board[endY][endX]=board[startY][startX]
        board[startY][startX] = ''

#Method to print out the board     
def displayBoard():
    print(' ','A','B','C','D','E','F','G','H')
    for i in range(8):
        print(8-i, end = " ")
        for j in range(8):
            if board[i][j] == '':
                print('-',end = " ")
            else:
                print((board[i][j])[0],end = " ")
        print("")

"""Define the rules for movements in chess"""
def isValidMove(startX, startY, endX, endY):
    global board, pawnMoved, whiteKing, blackKing
    global blackKS, blackQS, whiteKS, whiteQS
    
    valid = True
    
    #Get current and target piece type
    piece = (board[startY][startX])[0]
    if board[endY][endX] != '':
        targetPiece = (board[endY][endX])[0]
    else:
        targetPiece = ''
    
    #No piece to move
    if piece=='':
        print('No Piece Selected')
        valid = False
        return valid
    
    #Moving piece to current location
    if [startY,startX]==[endY,endX]:
        valid = False
        return valid
       
    #If the piece is friendly
    elif targetPiece!='' and piece.isupper() and targetPiece.isupper():
        valid=False
        return valid
        
    #If the piece is friendly   
    elif targetPiece!='' and piece.islower() and targetPiece.islower():
        valid=False
        return valid
    
    #Move the king
    elif piece=='k'or piece=='K':
        if abs(endX-startX)<=1 and abs(endY-startY)<=1:
            if piece=='k':
                if isAttacked(False,endX,endY)==False:
                    blackKing=True
                    return valid
                else:
                    valid=False
                    return valid
            else:
                if isAttacked(True,endX,endY)==False:
                    whiteKing=True
                    return valid
                else:
                    valid=False
                    return valid
            return valid
                
        elif abs(endX-startX)==2 and endY==startY and piece=='k':
            #King has been moved
            if blackKing==True:
                valid=False
                return valid
            #Moving Queen Side and neither has been moved
            elif startX>endX and blackQS==False and board[0][0]=='r':
                #Check if empty between them and not attacked
                for i in range(1,4):
                    if board[startY][i]!='' or isAttacked(False,i,startY)==True:
                        valid = False
                        return valid
                
                #Move rook
                if valid==True:
                    board[0][3]='r'
                    board[0][0]=''
                    
            #Moving King Side and neither has been moved    
            elif endX>startX and blackKS==False and board[0][7]=='r':
                #Check if empty between them and not attacked
                for i in range(5,7):
                    if board[startY][i]!='' or isAttacked(False,i,startY)==True:
                        valid = False 
                        return valid
                        
                #Move rook
                if valid==True:
                    board[0][5]='r'
                    board[0][7]=''
                    
        elif abs(endX-startX)==2 and endY==startY and piece=='K':
            #King has been moved
            if whiteKing==True:
                valid=False
                return valid
            #Moving Queen Side and neither has been moved
            elif startX>endX and whiteQS==False and board[7][0]=='R':
                #Check if empty between them and not attacked
                for i in range(1,4):
                    if board[startY][i]!='' or isAttacked(True,i,startY)==True:
                        valid = False
                        return valid
                
                #Move rook
                if valid==True:
                    board[7][3]='R'
                    board[7][0]=''
            #Moving King Side and neither has been moved    
            elif endX>startX and whiteKS==False and board[7][7]=='R':
                #Check if empty between them and not attacked
                for i in range(5,7):
                    if board[startY][i]!='' or isAttacked(True,i,startY)==True:
                        valid = False 
                        return valid
                        
                #Move rook
                if valid==True:
                    board[7][5]='R'
                    board[7][7]=''
        else:
            valid=False
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
            
            #Set that the Rook was moved for castling
            if valid == True and startY==0 and startX==0:
                blackQS=True
            elif valid==True and startY==0 and startX==7:
                blackKS=True
            elif valid==True and startY==7 and startX==0:
                whiteQS=True
            elif valid==True and startY==7 and startX==7:
                whiteKS=True
                
        #make sure it moves in a line
        elif (startY==endY and startX!=endX):
            if endX>startX:
                for i in range(startX+1,endX):
                    if board[startY][i]!='':
                        valid = False
                        return valid
                return valid
            else:
                for i in range(startX-1,endX,-1):
                    if board[startY][i]!='':
                        valid = False
                        return valid
                return valid
            
            #Set that the Rook was moved for castling
            if valid == True and startY==0 and startX==0:
                blackQS=True
            elif valid==True and startY==0 and startX==7:
                blackKS=True
            elif valid==True and startY==7 and startX==0:
                whiteQS=True
            elif valid==True and startY==7 and startX==7:
                whiteKS=True
                
        else:
            valid=False
            return valid
    
    #Move the knight
    elif piece=='n'or piece=='N':
        if (abs(startX-endX)==2 and abs(startY-endY)==1) or (abs(startY-endY)==2 and abs(startX-endX)==1):
            return valid
        else:
            valid = False
            return valid
    
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
            return valid
    
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
                    return valid
                else:
                    for i in range(startY-1,endY,-1):
                        if board[i][startX]!='':
                            valid = False
                            return valid
                    return valid
            #make sure it moves in a line
            elif (startY==endY and startX!=endX):
                if endX>startX:
                    for i in range(startX+1,endX):
                        if board[startY][i]!='':
                            valid = False
                            return valid
                    return valid
                else:
                    for i in range(startX-1,endX,-1):
                        if board[startY][i]!='':
                            valid = False
                            return valid
                    return valid
        else:
            valid = False
            return valid
    
    #Move pawns
    elif piece=='p'or piece=='P':
        #Black Pieces
        if piece=='p':
            #Capturing
            if abs(startX-endX)==1:
                #Moving forward one spot
                if (endY-startY)==1:
                    #if the spot is occupied by opponent
                    if board[endY][endX]!='' and board[endY][endX].isupper():
                        pawnMoved[int((board[startY][startX])[1])-1]=True
                        return valid
                    #En Passant capture
                    elif board[endY][endX]=='' and board[startY][endX].isupper() and len(board[startY][endX])>=2:
                        if movedTwo[int((board[startY][endX])[1])+7]==True:
                            pawnMoved[int((board[startY][startX])[1])-1]=True
                            board[startY][endX] = ''
                            return valid
                        else:
                            valid=False
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
                    #Make sure it hasn't moved yet and no pieces in front
                    if pawnMoved[int((board[startY][startX])[1])-1]!=True and board[startY+1][startX]=='' and board[endY][endX]=='':
                        pawnMoved[int((board[startY][startX])[1])-1]=True
                        movedTwo[int((board[startY][startX])[1])-1]=True                      
                        return valid
                    else:
                        valid = False
                        return valid
                #Forward 1 spot
                elif (endY-startY)==1:
                    #The spot is empty in front
                    if board[endY][endX]=='':
                        pawnMoved[int((board[startY][startX])[1])-1]=True
                        return valid
                    #Spot is occupied
                    else:
                        valid=False
                        return valid
                else:
                    valid=False
                    return False
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
                    if board[endY][endX]!='' and board[endY][endX].islower():
                        pawnMoved[int((board[startY][startX])[1])+7]=True
                        return valid
                    #En Passant capture
                    elif board[endY][endX]=='' and board[startY][endX].isupper() and len(board[startY][endX])>=2:
                        if movedTwo[int((board[startY][endX])[1])-1]==True:
                            pawnMoved[int((board[startY][startX])[1])+7]=True
                            board[startY][endX] = ''
                            return valid
                        else:
                            valid=False
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
                if (startY-endY)==2:
                    #Make sure it hasn't moved yet and no pieces in front
                    if pawnMoved[int((board[startY][startX])[1])+7]!=True and board[startY-1][startX]=='' and board[endY][endX]=='':
                        pawnMoved[int((board[startY][startX])[1])+7]=True
                        movedTwo[int((board[startY][startX])[1])+7]=True
                        return valid
                    else:
                        valid = False
                        return valid
                #Forward 1 spot
                elif (startY-endY)==1:
                    #The spot is empty in front
                    if board[endY][endX]=='':
                        pawnMoved[int((board[startY][startX])[1])+7]=True
                        return valid
                    #Spot is occupied
                    else:
                        valid=False
                        return valid
                else:
                    valid=False
                    return valid
            else:
                valid=False
                return valid
    
    #Not caught by any case, invalid move
    else:
        valid=False
    
    return valid

"""Update the currently under attack arrays"""
def updateAttacked():
    global attackedByWhite, attackedByBlack
    
    #Clear attacked by White array
    attackedByWhite = [[False for i in range(8)] for j in range(8)]
    #Clear attacked by Black array
    attackedByBlack = [[False for i in range(8)] for j in range(8)]
    
    for y in range(8):
        for x in range(8):
            #Update attacked by white
            if board[y][x]!='' and board[y][x].isupper():
                #Update squares for pawn attacks
                if len(board[y][x])==2:
                    if (x+1)<8 and (y-1)>=0:
                        attackedByWhite[y-1][x+1]=True
                    if (x-1)>=0 and (y-1)>=0:
                        attackedByWhite[y-1][x-1]=True
                        
                for newX in range(8):
                    for newY in range(8):
                        if len(board[y][x])<=1 and isValidMove(x,y,newX,newY)==True:
                            attackedByWhite[newY][newX]=True
                            
            #Update attacked by black
            elif board[y][x]!='' and board[y][x].islower():
                #Update squares for pawn attacks
                if len(board[y][x])==2:
                    if (x+1)<8 and (y+1)<8:
                        attackedByBlack[y+1][x+1]=True
                    if (x-1)>=0 and (y+1)<8:
                        attackedByBlack[y+1][x-1]=True
                        
                for newX in range(8):
                    for newY in range(8):
                        if  len(board[y][x])<=1 and isValidMove(x,y,newX,newY)==True:
                            attackedByBlack[newY][newX]=True                
                
"""Check if the current square is under attack"""
def isAttacked(isWhite, currentX, currentY):
    global attackedByWhite, attackedByBlack
    #Test if white is attacking this square
    if isWhite==False:
        return attackedByWhite[currentY][currentX]
        
    #Test if black is attacking this square
    else:
        return attackedByBlack[currentY][currentX]
    
"""Check if the king is in check"""
def isCheck(isWhite):
    global attackedByBlack, attackedByWhite
    
    #Black King, check if space is attacked by white
    if isWhite==False:
        for x in range(8):
            for y in range(8):
                if board[y][x]=='k':
                    currentY=y
                    currentX=x
                    
        return attackedByWhite[currentY][currentX]
    #White King, check if space is attacked by Black
    else:
        for x in range(8):
            for y in range(8):
                if board[y][x]=='K':
                    currentY=y
                    currentX=x
                    
        return attackedByBlack[currentY][currentX]

"""Check if the moves puts the player in check"""
def makeMove(isWhite, startX, startY, endX, endY):
    global board, pawnMoved, movedTwo, blackKS, blackQS, whiteKS, whiteQS, blackKing, whiteKing
    
    tempBoard = copy.deepcopy(board)
    tempPawns = copy.deepcopy(pawnMoved)
    tempTwo = copy.deepcopy(movedTwo)
    
    WkingMoved = whiteKing
    WkingSide = whiteKS
    WqueenSide = whiteQS
    BkingMoved = blackKing
    BkingSide = blackKS
    BqueenSide = blackQS
    
    print("Tried ",startX, " ", startY, " ", endX, " ", endY)
    if isValidMove(startX,startY,endX,endY):
        print("Succeeded ",startX, " ", startY, " ", endX, " ", endY)
        movePiece(startX, startY, endX, endY)
        updateAttacked()
    
        if isCheck(isWhite)==True:
            board=copy.deepcopy(tempBoard)
            pawnMoved=copy.deepcopy(tempPawns)
            movedTwo=copy.deepcopy(tempTwo)
            updateAttacked()
            whiteKing=WkingMoved
            whiteKS=WkingSide
            whiteQS=WqueenSide
            blackKing=BkingMoved
            blackKS=BkingSide
            blackQS=BqueenSide
            print("You will be in check")
            return False
        else:
            return True
    
    else:
        print("Not a valid move")
        return False
    
    
"""Check if there is a checkmate"""
def isCheckmate(isWhite):
    global board, pawnMoved, movedTwo, attackedByWhite, attackedByBlack, blackKS, blackQS, whiteKS, whiteQS, blackKing, whiteKing
    
    #Find Black King
    if isWhite==False:
        for x in range(8):
            for y in range(8):
                if board[y][x]=='k':
                    currentY=y
                    currentX=x
    #Find White King
    else:
        for x in range(8):
            for y in range(8):
                if board[y][x]=='K':
                    currentY=y
                    currentX=x
    #Check through all 8 possible moves for the King
    for i in range(currentY - 1, currentY+2):
        for j in range(currentX - 1, currentX+2):
            if i>=0 and i<=7:
                if j>=0 and j<=7:
                    if isWhite==False:
                        if attackedByWhite[i][j]==False:
                            return False
                    else:
                        if attackedByBlack[i][j]==False:
                            return False
                
    #Check every possible move for White
    if(isWhite):
        for sY in range(8):
            for sX in range(8):
                if board[sY][sX].isupper():
                    for eY in range(8):
                        for eX in range(8):
                            tempBoard = copy.deepcopy(board)
                            tempPawns = copy.deepcopy(pawnMoved)
                            tempTwo = copy.deepcopy(movedTwo)
                            
                            WkingMoved = whiteKing
                            WkingSide = whiteKS
                            WqueenSide = whiteQS
                            BkingMoved = blackKing
                            BkingSide = blackKS
                            BqueenSide = blackQS
                            
                            if isValidMove(sX,sY,eX,eY):
                                updateAttacked()
                                
                                if isCheck(isWhite)==True:
                                    board=copy.deepcopy(tempBoard)
                                    pawnMoved=copy.deepcopy(tempPawns)
                                    movedTwo=copy.deepcopy(tempTwo)
                                    updateAttacked()
                                    whiteKing=WkingMoved
                                    whiteKS=WkingSide
                                    whiteQS=WqueenSide
                                    blackKing=BkingMoved
                                    blackKS=BkingSide
                                    blackQS=BqueenSide
                                    return True
                                else:
                                    return False
    #Check every possible move for Black
    else:
        for sY in range(8):
            for sX in range(8):
                if board[sY][sX].islower():
                    for eY in range(8):
                        for eX in range(8):
                            tempBoard = copy.deepcopy(board)
                            tempPawns = copy.deepcopy(pawnMoved)
                            tempTwo = copy.deepcopy(movedTwo)
                            
                            WkingMoved = whiteKing
                            WkingSide = whiteKS
                            WqueenSide = whiteQS
                            BkingMoved = blackKing
                            BkingSide = blackKS
                            BqueenSide = blackQS
                            
                            if isValidMove(sX,sY,eX,eY):
                                updateAttacked()
                                
                                if isCheck(isWhite)==True:
                                    board=copy.deepcopy(tempBoard)
                                    pawnMoved=copy.deepcopy(tempPawns)
                                    movedTwo=copy.deepcopy(tempTwo)
                                    updateAttacked()
                                    whiteKing=WkingMoved
                                    whiteKS=WkingSide
                                    whiteQS=WqueenSide
                                    blackKing=BkingMoved
                                    blackKS=BkingSide
                                    blackQS=BqueenSide
                                    return True
                                else:
                                    return False
    return False

"""Our main function calls"""
intializeBoard()
updateAttacked()
AI = minimax(2,board, pawnMoved, movedTwo, whiteKS, whiteQS, blackKS, blackQS, whiteKing, blackKing)
files = ['A','B','C','D','E','F','G','H']
ranks = ['8','7','6','5','4','3','2','1']

whiteMove=True

while(isCheckmate(whiteMove)!=True):
    displayBoard()
    if(whiteMove):
        print("White's move")
        
        user_input = str(raw_input("Start Position File:"))
        choice = '~'
        while choice=='~':
            if user_input in files:
                choice = files.index(user_input)
                if choice>=0 and choice<8:
                    startX = choice
                    
        user_input = str(input("Start Position Rank:"))
        choice = '~'
        while choice=='~':
            if user_input in ranks:
                choice = ranks.index(user_input)
                if choice>=0 and choice<8:
                    startY = choice
                    
        user_input = str(raw_input("End Position File:"))
        choice = '~'
        while choice=='~':
            if user_input in files:
                choice = files.index(user_input)
                if choice>=0 and choice<8:
                    endX = choice
        
        user_input = str(input("End Position Rank:"))
        choice = '~'
        while choice=='~':
            if user_input in ranks:
                choice = ranks.index(user_input)
                if choice>=0 and choice<8:
                    endY = choice
                
    else: 
        print("Black's move")
        
        moveArray = AI.minimaxFunction()
        
        if len(moveArray)>0:
            print("AI returned move")
            startX = moveArray[0]
            startY = moveArray[1]
            endX = moveArray[2]
            endY = moveArray[3]
    
            #Make the move and check if makes check or not
            if makeMove(whiteMove,startX,startY,endX,endY)==True:
                #Now whites turn
                whiteMove=True
                #Update squares which are attacked
                updateAttacked()
                #Reset White for En Passant
                for i in range(8,16):
                    movedTwo[i]=False
            
    
    
    #If the current peice is the correct one for the turn we are on
    if whiteMove==True and board[startY][startX]!='' and board[startY][startX].isupper():
        #Make sure the target square is not occupied by an ally
        if board[endY][endX].isupper():
            print("Cannot target friendly piece")
        #Make the move and check if makes check or not
        if makeMove(whiteMove,startX,startY,endX,endY)==True:
            #Now blacks turn
            whiteMove=False
            #Update squares which are attacked
            updateAttacked()
            #Reset Black for En Passant
            for i in range(8):
                movedTwo[i]=False
        
                
    elif whiteMove==False and board[startY][startX]!='' and board[startY][startX].islower():
        #Make sure the target square is not occupied by an ally
        if board[endY][endX].islower():
            print("Cannot target friendly piece")
            
            
    if isCheck(whiteMove)==True:
        print("You are in check")


displayBoard()
if(whiteMove):
    print("Black Wins!")
else:
    print("White Wins!")