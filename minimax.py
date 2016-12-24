# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:41:13 2016

@author: Nick
"""

import copy
import sys
    
class minimax:
    def __init__(self, board, pawnMoved, movedTwo, whiteKS, whiteQS, blackKS, blackQS, whiteKing, blackKing):
        self.board = board
        self.pawnMoved = pawnMoved
        self.movedTwo = movedTwo
        self.whiteKS = whiteKS
        self.whiteQS = whiteQS
        self.blackKS = blackKS
        self.blackQS = blackQS
        self.whiteKing = whiteKing
        self.blackKing = blackKing
        self.attackedByWhite = [[False for i in range(8)] for j in range(8)]
        self.attackedByBlack = [[False for i in range(8)] for j in range(8)]
        
    """This is the defintion of out AI functions
    All moves are made using a sepereate set of variables"""
    #The main decision function
    def minimax(self):
        
        return 0
    
    #The evaluation function for the AI's turn
    def maxPlay(self):
            #Check if game is over
        if self.isCheckmate():
            return self.evaluateGame()
            
        maxScore = -sys.maxint -1
        
        return maxScore
        
    #The evaluation function for the Opponents turn
    def minPlay(self):
        #Check if game is over
        if self.isCheckmate():
            return self.evaluateGame()
            
        minScore = sys.maxint
        
        
        return minScore
        
    def getAvailableMoves(self):
        
        return 0
        
    def evaluateGame(self):
        
        return 0
    
    #Move the piece in the given coordinates to the target coordinates  
    def movePiece(self, board, startX, startY, endX, endY):        
        if (board[startY][startX]!=''):
            board[endY][endX]=board[startY][startX]
            board[startY][startX] = ''
            
    """Define the rules for movements in chess"""
    def isValidMove(self, board, startX, startY, endX, endY, pawnMoved, movedTwo, whiteKS, whiteQS, blackKS, blackQS, whiteKing, blackKing):
        
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
            if abs(endX-startX)<=1 and abs(endY-startY)<=1:
                if board[endY][endX]=='':
                    if piece=='k':
                        if self.isAttacked(False,endX,endY)==False:
                            blackKing=True
                        else:
                            valid=False
                    else:
                        if self.isAttacked(True,endX,endY)==False:
                            whiteKing=True
                        else:
                            valid=False
                    return valid
                else:
                    valid = False
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
                        if board[startY][i]!='' or self.isAttacked(False,i,startY)==True:
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
                        if board[startY][i]!='' or self.isAttacked(False,i,startY)==True:
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
                        if board[startY][i]!='' or self.isAttacked(True,i,startY)==True:
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
                        if board[startY][i]!='' or self.isAttacked(True,i,startY)==True:
                            valid = False 
                            return valid
                            
                    #Move rook
                    if valid==True:
                        board[7][5]='R'
                        board[7][7]=''
            else:
                valid=False
                
        #Move the Rook
        elif piece=='r' or piece=='R':
            #make sure it moves in a line
            if (startX==endX and startY!=endY):
                if endY>startY:
                    for i in range(startY+1,endY):
                        if board[i][startX]!='':
                            valid = False                
                else:
                    for i in range(startY-1,endY,-1):
                        if board[i][startX]!='':
                            valid = False
                
                #Set that the Rook was moved for castling
                if valid == True and startY==0 and startX==0:
                    blackQS=True
                elif valid==True and startY==0 and startX==7:
                    blackQS=True
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
                else:
                    for i in range(startX-1,endX,-1):
                        if board[startY][i]!='':
                            valid = False
                    return valid
                
                #Set that the Rook was moved for castling
                if valid == True and startY==0 and startX==0:
                    blackQS=True
                elif valid==True and startY==0 and startX==7:
                    blackQS=True
                elif valid==True and startY==7 and startX==0:
                    whiteQS=True
                elif valid==True and startY==7 and startX==7:
                    whiteKS=True
                    
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
                        if pawnMoved[int((board[startY][startX])[1])-1]!=True and board[startY+1][startX+1]=='' and board[endY][endX]=='':
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
                        if pawnMoved[int((board[startY][startX])[1])+7]!=True and board[startY-1][startX-1]=='' and board[endY][endX]=='':
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
        
        #Not caught by any case, invalid move
        else:
            valid=False
        
        return valid
    
    """Update the currently under attack arrays"""
    def updateAttacked(self, board):
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
                            if len(board[y][x])<=1 and self.isValidMove(x,y,newX,newY)==True:
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
                            if  len(board[y][x])<=1 and self.isValidMove(x,y,newX,newY)==True:
                                attackedByBlack[newY][newX]=True                
                    
    """Check if the current square is under attack"""
    def isAttacked(isWhite, currentX, currentY, attackedByWhite, attackedByBlack):
        #Test if white is attacking this square
        if isWhite==False:
            return attackedByWhite[currentY][currentX]
            
        #Test if black is attacking this square
        else:
            return attackedByBlack[currentY][currentX]
        
    """Check if the king is in check"""
    def isCheck(isWhite, board, attackedByBlack, attackedByWhite):  
        #Black King, check if space is attacked by white
        if isWhite==False:
            for x in range(8):
                for y in range(8):
                    if board[y][x]=='k':
                        currentY=y
                        currentX=x
                        
            return attackedByWhite[currentY][currentX]
            
        #White Queen, check if space is attacked by Black
        else:
            for x in range(8):
                for y in range(8):
                    if board[y][x]=='K':
                        currentY=y
                        currentX=x
                        
            return attackedByBlack[currentY][currentX]