# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:41:13 2016

@author: Nick
"""

from __future__ import print_function
import copy
import sys

class minimax:
    def __init__(self, Max_Depth, board, pawnMoved, movedTwo, whiteKS, whiteQS, blackKS, blackQS, whiteKing, blackKing):
        self.gameState = [0 for i in range(11)]        
        self.Max_Depth = Max_Depth        
        self.gameState[0] = board
        self.gameState[1] = pawnMoved
        self.gameState[2] = movedTwo
        self.gameState[3] = whiteKS
        self.gameState[4] = whiteQS
        self.gameState[5] = blackKS
        self.gameState[6] = blackQS
        self.gameState[7] = whiteKing
        self.gameState[8] = blackKing
        
    """This is the defintion of out AI functions
    All moves are made using a sepereate set of variables"""
    #The main decision function, returns the best move for the AI
    def minimaxFunction(self):
        bestMove=[]
        bestScore = -sys.maxint-1
        
        for x in range(8):
            for y in range(8):
                #spot is currently occupied by AI's piece
                if (self.gameState[0])[y][x]!='' and (self.gameState[0])[y][x].islower()==True:
                    #for newX in range(8):
                        #for newY in range(8):
                    moves = self.possibleLegalMoves((self.gameState[0])[y][x],x,y)
                    for i in range(len(moves)):
                        newX=(moves[i])[0]
                        newY=(moves[i])[1]
                        if self.isLegalMotion(self.gameState,x,y,newX,newY):

                                    newGameState = self.quickerCopy(self.gameState)
                                    if self.isValidMove(newGameState,x,y,newX,newY):
                                        #makemove
                                        self.movePiece(newGameState,x,y,newX,newY)
                                        #check for pawn promotion
                                        if newY==0:
                                            if ((newGameState[0])[newY][newX])[0]=='p':
                                                ((newGameState[0])[newY][newX])='q'
                                        if self.isCheck(newGameState,False)==False:
                                            score = self.minPlay(1,newGameState,False,bestScore)
                                            if score>bestScore:
                                                bestScore = score
                                                bestMove = [x,y,newX,newY]
                      
        print ((self.gameState[0])[bestMove[1]][bestMove[0]])
        print (self.isAttacked(self.gameState,True,bestMove[2],bestMove[3]))
        return bestMove
    
    #The evaluation function for the AI's turn
    def maxPlay(self, depth, gameState, isWhite, currentMin):
        #Check if game is over or it's reached max depth
        if depth>=self.Max_Depth and self.isCheck(gameState,False)==False and depth<(self.Max_Depth+10):
            return self.evaluateGame(gameState, isWhite)
        elif self.isCheckmate(gameState, isWhite):
            return -sys.maxint -1
            
        maxScore = -sys.maxint -1
        
        for x in range(8):
            for y in range(8):
                #spot is currently occupied by AI's piece
                if (gameState[0])[y][x]!='' and (gameState[0])[y][x].islower()==True:
                    moves = self.possibleLegalMoves((self.gameState[0])[y][x],x,y)
                    for i in range(len(moves)):
                        newX=(moves[i])[0]
                        newY=(moves[i])[1]
                        if maxScore>currentMin:
                            return maxScore
                        if self.isLegalMotion(gameState,x,y,newX,newY):

                                    newGameState = self.quickerCopy(gameState)
                                    if self.isValidMove(newGameState,x,y,newX,newY):
                                        #makemove
                                        self.movePiece(newGameState,x,y,newX,newY)
                                        #check for pawn promotion
                                        if newY==0:
                                            if ((newGameState[0])[newY][newX])[0]=='p':
                                                ((newGameState[0])[newY][newX])='q'
                                        if self.isCheck(newGameState,False)==False:
                                            score = self.minPlay(depth+1,newGameState,isWhite, maxScore)
                                            if score>maxScore:
                                                maxScore = score
                                        
        return maxScore
        
    #The evaluation function for the Opponents turn
    def minPlay(self, depth, gameState, isWhite, currentMax):
        #Check if game is over or it's reached max depth
        if depth>=self.Max_Depth and self.isCheck(gameState,True)==False and depth<(self.Max_Depth+10):
            return self.evaluateGame(gameState, isWhite)
        elif self.isCheckmate(gameState, isWhite):
            return sys.maxint
            
        minScore = sys.maxint
        
        for x in range(8):
            for y in range(8):
                #spot is currently occupied by Opponents piece
                if (gameState[0])[y][x]!='' and (gameState[0])[y][x].isupper()==True:
                    moves = self.possibleLegalMoves((self.gameState[0])[y][x],x,y)
                    for i in range(len(moves)):
                        newX=(moves[i])[0]
                        newY=(moves[i])[1]
                        if minScore<currentMax:
                                return minScore
                        if self.isLegalMotion(gameState,x,y,newX,newY):
                                
                                    newGameState = self.quickerCopy(gameState)
                                    if self.isValidMove(newGameState,x,y,newX,newY):
                                        #makemove
                                        self.movePiece(newGameState,x,y,newX,newY)
                                        #Check for pawn promotion
                                        if newY==0:
                                            if ((newGameState[0])[newY][newX])[0]=='P':
                                               ((newGameState[0])[newY][newX])='Q'
                                        if self.isCheck(newGameState,True)==False:
                                            score = self.maxPlay(depth+1,newGameState,isWhite,minScore)
                                            if score<minScore:
                                                minScore = score
        
        return minScore
        
        
    def evaluateGame(self, gameState, isWhite):
        materialScore = 0
        centerControl = 0
        rookPenalty = 0
        queenProtected = 0
        pawnPromoted = 0
        
        for x in range(8):
            for y in range(8):
                if (gameState[0])[y][x]!='':
                    #catch empty spot
                    if (gameState[0])[y][x]=='k':
                        materialScore+=200
                    elif (gameState[0])[y][x]=='K':
                        materialScore-=200
                    elif (gameState[0])[y][x]=='q':
                        materialScore+=60
                        if self.isAttacked(gameState,False,x,y):
                            queenProtected+=5
                    elif (gameState[0])[y][x]=='Q':
                        materialScore-=50
                        if self.isAttacked(gameState,True,x,y):
                            queenProtected-=5
                    elif (gameState[0])[y][x]=='r':
                        materialScore+=5
                        if y==0 and x==0 and gameState[6]==False and gameState[8]==False:
                            rookPenalty -= 0.1
                        elif y==0 and x==7 and gameState[5]==False and gameState[8]==False:
                            rookPenalty -= 0.1
                    elif (gameState[0])[y][x]=='R':
                        materialScore-=5
                        if y==7 and x==0 and gameState[4]==False and gameState[7]==False:
                            rookPenalty += 0.1
                        elif y==7 and x==7 and gameState[3]==False and gameState[7]==False:
                            rookPenalty += 0.1
                    elif (gameState[0])[y][x]=='b':
                        materialScore+=3
                        if (x>=2 or x<=5):
                            centerControl+=0.5
                    elif (gameState[0])[y][x]=='B':
                        materialScore-=3
                        if (x>=2 or x<=5) and y<7:
                            centerControl-=0.5
                    elif (gameState[0])[y][x]=='n':
                        materialScore+=3
                        if (x>=2 or x<=5) and y>0:
                            centerControl+=1
                    elif (gameState[0])[y][x]=='N':
                        materialScore-=3
                        if (x>=2 or x<=5) and y<7:
                            centerControl-=1
                    elif ((gameState[0])[y][x])[0]=='p':
                        materialScore+=1
                        if (x>=2 or x<=5) and y>1:
                            centerControl+=0.5
                        if y==5:
                            pawnPromoted+=1
                        elif y==6:
                            pawnPromoted+=2
                    elif ((gameState[0])[y][x])[0]=='P':
                        materialScore-=1
                        if (x>=2 or x<=5) and y<6:
                            centerControl-=0.5
                        if y==5:
                            pawnPromoted-=1
                        elif y==6:
                            pawnPromoted-=2
                            
        return (materialScore+centerControl+rookPenalty+queenProtected+pawnPromoted)
    
    #Move the piece in the given coordinates to the target coordinates  
    def movePiece(self, gameState, startX, startY, endX, endY):        
        if ((gameState[0])[startY][startX]!=''):
            (gameState[0])[endY][endX]=(gameState[0])[startY][startX]
            (gameState[0])[startY][startX] = ''
            
    """Define the motion of all the pieces, without modifying the game state in any way"""
    def isLegalMotion(self, gameState, startX, startY, endX, endY):
        valid = True
        
        #Get current and target piece type
        piece = ((gameState[0])[startY][startX])[0]
        if (gameState[0])[endY][endX] != '':
            targetPiece = ((gameState[0])[endY][endX])[0]
        else:
            targetPiece = ''
        
        #No piece to move
        if piece=='':
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

        elif (startX==endX) and (startY==endY):
            valid=False
            return valid
            
        #Move the king
        elif piece=='k'or piece=='K':
            if abs(endX-startX)<=1 and abs(endY-startY)<=1:
                if piece=='k':
                    if self.isAttacked(gameState,False,endX,endY)==False:
                        return valid
                    else:
                        valid=False
                        return valid
                else:
                    if self.isAttacked(gameState,True,endX,endY)==False:
                        return valid
                    else:
                        valid=False
                        return valid
                return valid
                    
            elif abs(endX-startX)==2 and endY==startY and piece=='k':
                #King has been moved
                if gameState[8]==True or self.isAttacked(gameState,False,startX,startY)==True:
                    valid=False
                    return valid
                #Moving Queen Side and neither has been moved
                elif startX>endX and gameState[6]==False and (gameState[0])[0][0]=='r':
                    #Check if empty between them and not attacked
                    for i in range(1,4):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState,False,i,startY)==True:
                            valid = False
                            return valid
                        
                #Moving King Side and neither has been moved    
                elif endX>startX and gameState[5]==False and (gameState[0])[0][7]=='r':
                    #Check if empty between them and not attacked
                    for i in range(5,7):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState, False,i,startY)==True:
                            valid = False 
                            return valid
                        
            elif abs(endX-startX)==2 and endY==startY and piece=='K':
                #King has been moved
                if gameState[7]==True or self.isAttacked(gameState,True,startX,startY)==True:
                    valid=False
                    return valid
                #Moving Queen Side and neither has been moved
                elif startX>endX and gameState[4]==False and (gameState[0])[7][0]=='R':
                    #Check if empty between them and not attacked
                    for i in range(1,4):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState, True,i,startY)==True:
                            valid = False
                            return valid
                    
                #Moving King Side and neither has been moved    
                elif endX>startX and (gameState[3])==False and (gameState[0])[7][7]=='R':
                    #Check if empty between them and not attacked
                    for i in range(5,7):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState,True,i,startY)==True:
                            valid = False 
                            return valid

            else:
                valid=False
                return valid

        #Move the Rook
        elif piece=='r' or piece=='R':
            #make sure it moves in a line
            if (startX==endX and startY!=endY):
                if endY>startY:
                    for i in range(startY+1,endY):
                        if (gameState[0])[i][startX]!='':
                            valid = False 
                            return valid
                else:
                    for i in range(startY-1,endY,-1):
                        if (gameState[0])[i][startX]!='':
                            valid = False
                            return valid
                    
            #make sure it moves in a line
            elif (startY==endY and startX!=endX):
                if endX>startX:
                    for i in range(startX+1,endX):
                        if (gameState[0])[startY][i]!='':
                            valid = False
                            return valid
                    return valid
                else:
                    for i in range(startX-1,endX,-1):
                        if (gameState[0])[startY][i]!='':
                            valid = False
                            return valid
                    return valid
                    
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
                        if (gameState[0])[startY-1-i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Left and down
                elif startX>endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Right and Up
                elif startX<endX and startY>endY:
                    for i in range(difference):
                        if (gameState[0])[startY-1-i][startX+1+i]!='':
                            valid=False
                            return valid
                            
                #Right and Down
                elif startX<endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX+1+i]!='':
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
                        if (gameState[0])[startY-1-i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Left and down
                elif startX>endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Right and Up
                elif startX<endX and startY>endY:
                    for i in range(difference):
                        if (gameState[0])[startY-1-i][startX+1+i]!='':
                            valid=False
                            return valid
                            
                #Right and Down
                elif startX<endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX+1+i]!='':
                            valid=False
                            return valid
                            
                return valid
            #Moving like a Rook
            elif (startX==endX and startY!=endY) or (startY==endY and startX!=endX):
                #make sure it moves in a line
                if (startX==endX and startY!=endY):
                    if endY>startY:
                        for i in range(startY+1,endY):
                            if (gameState[0])[i][startX]!='':
                                valid = False
                                return valid
                        return valid
                    else:
                        for i in range(startY-1,endY,-1):
                            if (gameState[0])[i][startX]!='':
                                valid = False
                                return valid
                        return valid
                #make sure it moves in a line
                elif (startY==endY and startX!=endX):
                    if endX>startX:
                        for i in range(startX+1,endX):
                            if (gameState[0])[startY][i]!='':
                                valid = False
                                return valid
                        return valid
                    else:
                        for i in range(startX-1,endX,-1):
                            if (gameState[0])[startY][i]!='':
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
                        if (gameState[0])[endY][endX]!='' and (gameState[0])[endY][endX].isupper():
                            return valid
                        #En Passant capture
                        elif (gameState[0])[endY][endX]=='' and (gameState[0])[startY][endX].isupper() and len((gameState[0])[startY][endX])>=2:
                            if (gameState[2])[int(((gameState[0])[startY][endX])[1])+7]==True:
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
                        if (gameState[1])[int(((gameState[0])[startY][startX])[1])-1]!=True and (gameState[0])[startY+1][startX]=='' and (gameState[0])[endY][endX]=='':                    
                            return valid
                        else:
                            valid = False
                            return valid
                    #Forward 1 spot
                    elif (endY-startY)==1:
                        #The spot is empty in front
                        if (gameState[0])[endY][endX]=='':
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
                    
            #White Pieces
            else:
                #Capturing
                if abs(startX-endX)==1:
                    #Moving forward one spot
                    if (startY-endY)==1:
                        #if the spot is occupied by opponent
                        if (gameState[0])[endY][endX]!='' and (gameState[0])[endY][endX].islower():
                            return valid
                        #En Passant capture
                        elif (gameState[0])[endY][endX]=='' and (gameState[0])[startY][endX].isupper() and len((gameState[0])[startY][endX])>=2:
                            if (gameState[2])[int(((gameState[0])[startY][endX])[1])-1]==True:
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
                        if (gameState[1])[int(((gameState[0])[startY][startX])[1])+7]!=True and (gameState[0])[startY-1][startX]=='' and (gameState[0])[endY][endX]=='':
                            return valid
                        else:
                            valid = False
                            return valid
                    #Forward 1 spot
                    elif (startY-endY)==1:
                        #The spot is empty in front
                        if (gameState[0])[endY][endX]=='':
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
        
        return valid
        
        
    """Define the rules for movements in chess"""
    def isValidMove(self, gameState, startX, startY, endX, endY):
        
        valid = True
        
        #Get current and target piece type
        piece = ((gameState[0])[startY][startX])[0]
        if (gameState[0])[endY][endX] != '':
            targetPiece = ((gameState[0])[endY][endX])[0]
        else:
            targetPiece = ''
        
        #No piece to move
        if piece=='':
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
        
        elif (startX==endX) and (startY==endY):
            valid=False
            return valid
            
        #Move the king
        elif piece=='k'or piece=='K':
            if abs(endX-startX)<=1 and abs(endY-startY)<=1:
                if (gameState[0])[endY][endX]=='':
                    if piece=='k':
                        if self.isAttacked(gameState,False,endX,endY)==False:
                            gameState[8]=True
                        else:
                            valid=False
                            return valid
                    else:
                        if self.isAttacked(gameState,True,endX,endY)==False:
                            gameState[7]=True
                        else:
                            valid=False
                            return valid
                    return valid
                else:
                    valid = False
                    return valid
                    
            elif abs(endX-startX)==2 and endY==startY and piece=='k':
                #King has been moved
                if gameState[8]==True or self.isAttacked(gameState,False,startX,startY)==True:
                    valid=False
                    return valid
                #Moving Queen Side and neither has been moved
                elif startX>endX and gameState[6]==False and (gameState[0])[0][0]=='r':
                    #Check if empty between them and not attacked
                    for i in range(1,4):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState,False,i,startY)==True:
                            valid = False
                            return valid
                    
                    #Move rook
                    if valid==True:
                        (gameState[0])[0][3]='r'
                        (gameState[0])[0][0]=''
                        
                #Moving King Side and neither has been moved    
                elif endX>startX and gameState[5]==False and (gameState[0])[0][7]=='r':
                    #Check if empty between them and not attacked
                    for i in range(5,7):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState, False,i,startY)==True:
                            valid = False 
                            return valid
                            
                    #Move rook
                    if valid==True:
                        (gameState[0])[0][5]='r'
                        (gameState[0])[0][7]=''
                        
            elif abs(endX-startX)==2 and endY==startY and piece=='K':
                #King has been moved
                if gameState[7]==True or self.isAttacked(gameState,True,startX,startY)==True:
                    valid=False
                    return valid
                #Moving Queen Side and neither has been moved
                elif startX>endX and gameState[4]==False and (gameState[0])[7][0]=='R':
                    #Check if empty between them and not attacked
                    for i in range(1,4):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState, True,i,startY)==True:
                            valid = False
                            return valid
                    
                    #Move rook
                    if valid==True:
                        (gameState[0])[7][3]='R'
                        (gameState[0])[7][0]=''
                #Moving King Side and neither has been moved    
                elif endX>startX and (gameState[3])==False and (gameState[0])[7][7]=='R':
                    #Check if empty between them and not attacked
                    for i in range(5,7):
                        if (gameState[0])[startY][i]!='' or self.isAttacked(gameState,True,i,startY)==True:
                            valid = False 
                            return valid
                            
                    #Move rook
                    if valid==True:
                        (gameState[0])[7][5]='R'
                        (gameState[0])[7][7]=''
            else:
                valid=False
                return valid
                
        #Move the Rook
        elif piece=='r' or piece=='R':
            #make sure it moves in a line
            if (startX==endX and startY!=endY):
                if endY>startY:
                    for i in range(startY+1,endY):
                        if (gameState[0])[i][startX]!='':
                            valid = False 
                            return valid
                else:
                    for i in range(startY-1,endY,-1):
                        if (gameState[0])[i][startX]!='':
                            valid = False
                            return valid
                
                #Set that the Rook was moved for castling
                if valid == True and startY==0 and startX==0:
                    gameState[6]=True
                elif valid==True and startY==0 and startX==7:
                    gameState[5]=True
                elif valid==True and startY==7 and startX==0:
                    gameState[4]=True
                elif valid==True and startY==7 and startX==7:
                    gameState[3]=True
                    
            #make sure it moves in a line
            elif (startY==endY and startX!=endX):
                if endX>startX:
                    for i in range(startX+1,endX):
                        if (gameState[0])[startY][i]!='':
                            valid = False
                            return valid
                    return valid
                else:
                    for i in range(startX-1,endX,-1):
                        if (gameState[0])[startY][i]!='':
                            valid = False
                            return valid
                    return valid
                
                #Set that the Rook was moved for castling
                if valid == True and startY==0 and startX==0:
                    gameState[6]=True
                elif valid==True and startY==0 and startX==7:
                    gameState[5]=True
                elif valid==True and startY==7 and startX==0:
                    gameState[4]=True
                elif valid==True and startY==7 and startX==7:
                    (gameState[3])=True
                    
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
                        if (gameState[0])[startY-1-i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Left and down
                elif startX>endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Right and Up
                elif startX<endX and startY>endY:
                    for i in range(difference):
                        if (gameState[0])[startY-1-i][startX+1+i]!='':
                            valid=False
                            return valid
                            
                #Right and Down
                elif startX<endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX+1+i]!='':
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
                        if (gameState[0])[startY-1-i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Left and down
                elif startX>endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX-1-i]!='':
                            valid=False
                            return valid
                            
                #Right and Up
                elif startX<endX and startY>endY:
                    for i in range(difference):
                        if (gameState[0])[startY-1-i][startX+1+i]!='':
                            valid=False
                            return valid
                            
                #Right and Down
                elif startX<endX and startY<endY:
                    for i in range(difference):
                        if (gameState[0])[startY+1+i][startX+1+i]!='':
                            valid=False
                            return valid
                            
                return valid
            #Moving like a Rook
            elif (startX==endX and startY!=endY) or (startY==endY and startX!=endX):
                #make sure it moves in a line
                if (startX==endX and startY!=endY):
                    if endY>startY:
                        for i in range(startY+1,endY):
                            if (gameState[0])[i][startX]!='':
                                valid = False
                                return valid
                        return valid
                    else:
                        for i in range(startY-1,endY,-1):
                            if (gameState[0])[i][startX]!='':
                                valid = False
                                return valid
                        return valid
                #make sure it moves in a line
                elif (startY==endY and startX!=endX):
                    if endX>startX:
                        for i in range(startX+1,endX):
                            if (gameState[0])[startY][i]!='':
                                valid = False
                                return valid
                        return valid
                    else:
                        for i in range(startX-1,endX,-1):
                            if (gameState[0])[startY][i]!='':
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
                        if (gameState[0])[endY][endX]!='' and (gameState[0])[endY][endX].isupper():
                            (gameState[1])[int(((gameState[0])[startY][startX])[1])-1]=True
                            return valid
                        #En Passant capture
                        elif (gameState[0])[endY][endX]=='' and (gameState[0])[startY][endX].isupper() and len((gameState[0])[startY][endX])>=2:
                            if (gameState[2])[int(((gameState[0])[startY][endX])[1])+7]==True:
                                (gameState[1])[int(((gameState[0])[startY][startX])[1])-1]=True
                                (gameState[0])[startY][endX] = ''
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
                        if (gameState[1])[int(((gameState[0])[startY][startX])[1])-1]!=True and (gameState[0])[startY+1][startX]=='' and (gameState[0])[endY][endX]=='':
                            (gameState[1])[int(((gameState[0])[startY][startX])[1])-1]=True
                            (gameState[2])[int(((gameState[0])[startY][startX])[1])-1]=True                      
                            return valid
                        else:
                            valid = False
                            return valid
                    #Forward 1 spot
                    elif (endY-startY)==1:
                        #The spot is empty in front
                        if (gameState[0])[endY][endX]=='':
                            (gameState[1])[int(((gameState[0])[startY][startX])[1])-1]=True
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
                    
            #White Pieces
            else:
                #Capturing
                if abs(startX-endX)==1:
                    #Moving forward one spot
                    if (startY-endY)==1:
                        #if the spot is occupied by opponent
                        if (gameState[0])[endY][endX]!='' and (gameState[0])[endY][endX].islower():
                            (gameState[1])[int(((gameState[0])[startY][startX])[1])+7]=True
                            return valid
                        #En Passant capture
                        elif (gameState[0])[endY][endX]=='' and (gameState[0])[startY][endX].isupper() and len((gameState[0])[startY][endX])>=2:
                            if (gameState[2])[int(((gameState[0])[startY][endX])[1])-1]==True:
                                (gameState[1])[int(((gameState[0])[startY][startX])[1])+7]=True
                                (gameState[0])[startY][endX] = ''
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
                        if (gameState[1])[int(((gameState[0])[startY][startX])[1])+7]!=True and (gameState[0])[startY-1][startX]=='' and (gameState[0])[endY][endX]=='':
                            (gameState[1])[int(((gameState[0])[startY][startX])[1])+7]=True
                            (gameState[2])[int(((gameState[0])[startY][startX])[1])+7]=True
                            return valid
                        else:
                            valid = False
                            return valid
                    #Forward 1 spot
                    elif (startY-endY)==1:
                        #The spot is empty in front
                        if (gameState[0])[endY][endX]=='':
                            (gameState[1])[int(((gameState[0])[startY][startX])[1])+7]=True
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
        
        return valid
    
            
    def isAttacked(self, gameState, isWhite,x,y):
	attack = False
	
	#Attacked by black
	if isWhite==True:
		#Straight lines
		if x>0 and x<7:
			#left
			for i in range(x-1,-1,-1):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
							
			#right
			for i in range(x+1,8):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
		elif x==0:
			for i in range(1,8):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
		elif x==7:
			for i in range(6,-1,-1):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
		
		if y>0 and y<7:
			#up
			for i in range(y-1,-1,-1):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
							
			#down
			for i in range(y+1,8):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
		elif y==0:
			for i in range(1,8):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
		elif y==7:
			for i in range(6,-1,-1):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='r' or piece=='q':
						attack=True
						return attack
					else:
						break
		
		#Diagonals
		for i in range(1,8):
			#Down and right
			if y+i<8 and x+i<8:
				if (gameState[0])[y+i][x+i]!='':
					piece=(gameState[0])[y+i][x+i]
					if piece=='b' or piece=='q':
						attack=True
						return attack
					else:
						break
			else:
				break
								
		for i in range(1,8):
			#Up and right
			if y-i>=0 and x+i<8:
				if (gameState[0])[y-i][x+i]!='':
					piece=(gameState[0])[y-i][x+i]
					if piece=='b' or piece=='q':
						attack=True
						return attack
					else:
						break	
			else:
				break
				
		for i in range(1,8):
			#Down and left
			if y+i<8 and x-i>=0:
				if (gameState[0])[y+i][x-i]!='':
					piece=(gameState[0])[y+i][x-i]
					if piece=='b' or piece=='q':
						attack=True
						return attack
					else:
						break
			else:
				break
				
		for i in range(1,8):
			#Up and left
			if y-i>=0 and x-i>=0:
				if (gameState[0])[y-i][x-i]!='':
					piece=(gameState[0])[y-i][x-i]
					if piece=='b' or piece=='q':
						attack=True
						return attack
					else:
						break
			else:
				break
		
		#Like a Knight
		#x+1, y+2
		if x+1<8 and y+2<8:
			if (gameState[0])[y+2][x+1]=='n':
				attack=True
				return attack
		#x-1, y+2
		if x-1>=0 and y+2<8:
			if (gameState[0])[y+2][x-1]=='n':
				attack=True
				return attack
		#x+1, y-2
		if x+1<8 and y-2>=0:
			if (gameState[0])[y-2][x+1]=='n':
				attack=True
				return attack
		#x-1, y-2
		if x-1>=0 and y-2>=0:
			if (gameState[0])[y-2][x-1]=='n':
				attack=True
				return attack
		#x+2, y+1
		if x+2<8 and y+1<8:
			if (gameState[0])[y+1][x+2]=='n':
				attack=True
				return attack
		#x+2, y-1
		if x+2<8 and y-1>=0:
			if (gameState[0])[y-1][x+2]=='n':
				attack=True
				return attack
		#x-2, y+1
		if x-2>=0 and y+1<8:
			if (gameState[0])[y+1][x-2]=='n':
				attack=True
				return attack
		#x-2, y-1
		if x-2>=0 and y-1>=0:
			if (gameState[0])[y-1][x-2]=='n':
				attack=True
				return attack
			
		#Pawn Attacks
		if y-1>=0:
			if x+1<8:
				if (gameState[0])[y-1][x+1] !='' and ((gameState[0])[y-1][x+1])[0]=='p':
					attack=True
					return attack
			if x-1>=0:
				if (gameState[0])[y-1][x-1] !='' and ((gameState[0])[y-1][x-1])[0]=='p':
					attack=True
					return attack
					
		#King attacks
		if y+1<8:
			if x+1<8:
				if (gameState[0])[y+1][x+1]=='k':
					attack=True
					return attack
			if x-1>=0:
				if (gameState[0])[y+1][x-1]=='k':
					attack=True
					return attack
			if (gameState[0])[y+1][x]=='k':
					attack=True
					return attack
		if y-1>=0:
			if x+1<8:
				if (gameState[0])[y-1][x+1]=='k':
					attack=True
					return attack
			if x-1>=0:
				if (gameState[0])[y-1][x-1]=='k':
					attack=True
					return attack
			if (gameState[0])[y-1][x]=='k':
					attack=True
					return attack
		if x+1<8:
			if (gameState[0])[y][x+1]=='k':
				attack=True
				return attack
		if x-1>=0:
			if (gameState[0])[y][x-1]=='k':
				attack=True
				return attack
					
	#Attacked by White
	else:
		#Straight lines
		if x>0 and x<7:
			#left
			for i in range(x-1,-1,-1):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
			#right
			for i in range(x+1,8):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
		elif x==0:
			for i in range(1,8):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
		elif x==7:
			for i in range(6,-1,-1):
				if (gameState[0])[y][i]!='':
					piece=(gameState[0])[y][i]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
		
		if y>0 and y<7:
			#up
			for i in range(y-1,-1,-1):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
							
			#down
			for i in range(y+1,8):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
		elif y==0:
			for i in range(1,8):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
		elif y==7:
			for i in range(6,-1,-1):
				if (gameState[0])[i][x]!='':
					piece=(gameState[0])[i][x]
					if piece=='R' or piece=='Q':
						attack=True
						return attack
					else:
						break
		
		#Diagonals
		for i in range(1,8):
			#Down and right
			if y+i<8 and x+i<8:
				if (gameState[0])[y+i][x+i]!='':
					piece=(gameState[0])[y+i][x+i]
					if piece=='B' or piece=='Q':
						attack=True
						return attack
					else:
						break							
			else:
				break
								
		for i in range(1,8):
			#Up and right
			if y-i>=0 and x+i<8:
				if (gameState[0])[y-i][x+i]!='':
					piece=(gameState[0])[y-i][x+i]
					if piece=='B' or piece=='Q':
						attack=True
						return attack
					else:
						break	
			else:
				break
				
		for i in range(1,8):
			#Down and left
			if y+i<8 and x-i>=0:
				if (gameState[0])[y+i][x-i]!='':
					piece=(gameState[0])[y+i][x-i]
					if piece=='B' or piece=='Q':
						attack=True
						return attack
					else:
						break
			else:
				break
				
		for i in range(1,8):
			#Up and left
			if y-i>=0 and x-i>=0:
				if (gameState[0])[y-i][x-i]!='':
					piece=(gameState[0])[y-i][x-i]
					if piece=='B' or piece=='Q':
						attack=True
						return attack
					else:
						break
			else:
				break
		
		#Like a Knight
		#x+1, y+2
		if x+1<8 and y+2<8:
			if (gameState[0])[y+2][x+1]=='N':
				attack=True
				return attack
		#x-1, y+2
		if x-1>=0 and y+2<8:
			if (gameState[0])[y+2][x-1]=='N':
				attack=True
				return attack
		#x+1, y-2
		if x+1<8 and y-2>=0:
			if (gameState[0])[y-2][x+1]=='N':
				attack=True
				return attack
		#x-1, y-2
		if x-1>=0 and y-2>=0:
			if (gameState[0])[y-2][x-1]=='N':
				attack=True
				return attack
		#x+2, y+1
		if x+2<8 and y+1<8:
			if (gameState[0])[y+1][x+2]=='N':
				attack=True
				return attack
		#x+2, y-1
		if x+2<8 and y-1>=0:
			if (gameState[0])[y-1][x+2]=='N':
				attack=True
				return attack
		#x-2, y+1
		if x-2>=0 and y+1<8:
			if (gameState[0])[y+1][x-2]=='N':
				attack=True
				return attack
		#x-2, y-1
		if x-2>=0 and y-1>=0:
			if (gameState[0])[y-1][x-2]=='N':
				attack=True
				return attack
			
		#Pawn Attacks
		if y+1<8:
			if x+1<8:
				if (gameState[0])[y+1][x+1]!='' and ((gameState[0])[y+1][x+1])[0]=='P':
					attack=True
					return attack
			if x-1>=0:
				if (gameState[0])[y+1][x-1]!='' and ((gameState[0])[y+1][x-1])[0]=='P':
					attack=True
					return attack
     
		#King attacks
		if y+1<8:
			if x+1<8:
				if (gameState[0])[y+1][x+1]=='K':
					attack=True
					return attack
			if x-1>=0:
				if (gameState[0])[y+1][x-1]=='K':
					attack=True
					return attack
			if (gameState[0])[y+1][x]=='K':
					attack=True
					return attack
		if y-1>=0:
			if x+1<8:
				if (gameState[0])[y-1][x+1]=='K':
					attack=True
					return attack
			if x-1>=0:
				if (gameState[0])[y-1][x-1]=='K':
					attack=True
					return attack
			if (gameState[0])[y-1][x]=='K':
					attack=True
					return attack
		if x+1<8:
			if (gameState[0])[y][x+1]=='K':
				attack=True
				return attack
		if x-1>=0:
			if (gameState[0])[y][x-1]=='K':
				attack=True
				return attack
		
	return attack
        
    """Check if the king is in check"""
    def isCheck(self, gameState, isWhite):  
        #Black King, check if space is attacked by white
        if isWhite==False:
            for y in range(8):
                for x in range(8):
                    if (gameState[0])[y][x]=='k':
                        return self.isAttacked(gameState,False,x,y)
            
            
        #White Queen, check if space is attacked by Black
        else:
            for y in range(7,-1,-1):
                for x in range(8):
                    if (gameState[0])[y][x]=='K':
                        return self.isAttacked(gameState,True,x,y)
        
        return True
            
    
    def isCheckmate(self, gameState, isWhite):

        #Is a king actually in check?
        if self.isCheck(gameState, False)==False and self.isCheck(gameState, True)==False:
            return False
               
        #Find Black King
        if isWhite==False:
            for x in range(8):
                for y in range(8):
                    if gameState[0][y][x]=='k':
                        currentY=y
                        currentX=x
        #Find White King
        else:
            for x in range(8):
                for y in range(8):
                    if gameState[0][y][x]=='K':
                        currentY=y
                        currentX=x
        #Check through all 8 possible moves for the King
        for i in range(currentY - 1, currentY+2):
            for j in range(currentX - 1, currentX+2):
                if i>=0 and i<=7:
                    if j>=0 and j<=7:
                        if isWhite==False:
                            if (self.isAttacked(gameState, False,j,i)==False) and (gameState[0][i][j] in ['r','n','b','q','p'])==False:
                                return False
                        else:
                            if (self.isAttacked(gameState, True,j,i)==False) and (gameState[0][i][j] in ['R','N','B','Q','P'])==False:
                                return False
        
        #Check every possible move for White
        if(isWhite):
            for sY in range(8):
                for sX in range(8):
                    if gameState[0][sY][sX].isupper():
                        for eY in range(8):
                            for eX in range(8):
                                if self.isLegalMotion(gameState,sX, sY, eX, eY)==True:
                                    tempBoard = copy.deepcopy(gameState[0])
                                    tempPawns = copy.deepcopy(gameState[1])
                                    tempTwo = copy.deepcopy(gameState[2])
                                    
                                    WkingMoved = gameState[7]
                                    WkingSide = gameState[3]
                                    WqueenSide = gameState[4]
                                    BkingMoved = gameState[8]
                                    BkingSide = gameState[5]
                                    BqueenSide = gameState[6]
                                    
                                    if self.isValidMove(gameState,sX,sY,eX,eY):
                                        
                                        if self.isCheck(gameState,isWhite)==True:
                                            gameState[0]=copy.deepcopy(tempBoard)
                                            gameState[1]=copy.deepcopy(tempPawns)
                                            gameState[2]=copy.deepcopy(tempTwo)
                                            gameState[7]=WkingMoved
                                            gameState[3]=WkingSide
                                            gameState[4]=WqueenSide
                                            gameState[8]=BkingMoved
                                            gameState[5]=BkingSide
                                            gameState[6]=BqueenSide
                                            return True
                                        else:
                                            gameState[0]=copy.deepcopy(tempBoard)
                                            gameState[1]=copy.deepcopy(tempPawns)
                                            gameState[2]=copy.deepcopy(tempTwo)
                                            gameState[7]=WkingMoved
                                            gameState[3]=WkingSide
                                            gameState[4]=WqueenSide
                                            gameState[8]=BkingMoved
                                            gameState[5]=BkingSide
                                            gameState[6]=BqueenSide
                                            return False
        #Check every possible move for Black
        else:
            for sY in range(8):
                for sX in range(8):
                    if gameState[0][sY][sX].islower():
                        for eY in range(8):
                            for eX in range(8):
                                if self.isLegalMotion(gameState,sX, sY, eX, eY)==True:
                                    tempBoard = copy.deepcopy(gameState[0])
                                    tempPawns = copy.deepcopy(gameState[1])
                                    tempTwo = copy.deepcopy(gameState[2])
                                    
                                    WkingMoved = gameState[7]
                                    WkingSide = gameState[3]
                                    WqueenSide = gameState[4]
                                    BkingMoved = gameState[8]
                                    BkingSide = gameState[5]
                                    BqueenSide = gameState[6]
                                    
                                    if self.isValidMove(gameState,sX,sY,eX,eY):
                                        
                                        if self.isCheck(gameState,isWhite)==True:
                                            gameState[0]=copy.deepcopy(tempBoard)
                                            gameState[1]=copy.deepcopy(tempPawns)
                                            gameState[2]=copy.deepcopy(tempTwo)
                                            gameState[7]=WkingMoved
                                            gameState[3]=WkingSide
                                            gameState[4]=WqueenSide
                                            gameState[8]=BkingMoved
                                            gameState[5]=BkingSide
                                            gameState[6]=BqueenSide
                                            return True
                                        else:
                                            gameState[0]=copy.deepcopy(tempBoard)
                                            gameState[1]=copy.deepcopy(tempPawns)
                                            gameState[2]=copy.deepcopy(tempTwo)
                                            gameState[7]=WkingMoved
                                            gameState[3]=WkingSide
                                            gameState[4]=WqueenSide
                                            gameState[8]=BkingMoved
                                            gameState[5]=BkingSide
                                            gameState[6]=BqueenSide
                                            return False
        
        return False

    def quickerCopy(self,gameState):
        temp = [0 for i in range(9)]
        temp[0] = [row[:] for row in (gameState[0])]
        temp[1] = (gameState[1])[:]
        temp[2] = (gameState[2])[:]
        temp[3] = (gameState[3])
        temp[4] = (gameState[4])
        temp[5] = (gameState[5])
        temp[6] = (gameState[6])
        temp[7] = (gameState[7])
        temp[8] = (gameState[8])
        
        return temp
        
    def possibleLegalMoves(self, piece, x, y):
        moves = []
        
        if piece=='':
            return moves
        elif piece=='R' or piece=='r':
            for i in range(x-1,-1,-1):
                moves.append([i,y]) 
            for i in range(x+1,8):
                moves.append([i,y])
            for i in range(y-1,-1,-1):
                moves.append([x,i]) 
            for i in range(x+1,8):
                moves.append([x,i])
            return moves
        elif piece=='B' or piece=='b':
            for i in range(1,8):
                #Down and right
                if y+i<8 and x+i<8:
                    moves.append([x+i,y+i])
            for i in range(1,8):
                #Up and right
                if y-i>=0 and x+i<8:
                    moves.append([x+i,y-i])
            for i in range(1,8):
                #Down and left
                if y+i<8 and x-i>=0:
                    moves.append([x-i,y+i])
            for i in range(1,8):
                #Up and left
                if y-i>=0 and x-i>=0:
                    moves.append([x-i,y-i])
            return moves
        elif piece=='N' or piece=='n':
            if x+1<8 and y+2<8:
                moves.append([x+1,y+2])
            if x-1>=0 and y+2<8:
                moves.append([x-1,y+2])
            if x+1<8 and y-2>=0:
                moves.append([x+1,y-2])
            if x-1>=0 and y-2>=0:
                moves.append([x-1,y-2])
            if x+2<8 and y+1<8:
                moves.append([x+2,y+1])
            if x+2<8 and y-1>=0:
                moves.append([x+2,y-1])
            if x-2>=0 and y+1<8:
                moves.append([x-2,y+1])
            if x-2>=0 and y-1>=0:
                moves.append([x-2,y-1])
            return moves
        elif piece=='Q' or piece=='q':
            #Horizontal/Vertical Moves
            for i in range(x-1,-1,-1):
                moves.append([i,y]) 
            for i in range(x+1,8):
                moves.append([i,y])
            for i in range(y-1,-1,-1):
                moves.append([x,i]) 
            for i in range(x+1,8):
                moves.append([x,i])
                
            #Diagonal moves
            for i in range(1,8):
                #Down and right
                if y+i<8 and x+i<8:
                    moves.append([x+i,y+i])
            for i in range(1,8):
                #Up and right
                if y-i>=0 and x+i<8:
                    moves.append([x+i,y-i])
            for i in range(1,8):
                #Down and left
                if y+i<8 and x-i>=0:
                    moves.append([x-i,y+i])
            for i in range(1,8):
                #Up and left
                if y-i>=0 and x-i>=0:
                    moves.append([x-i,y-i])
                    
            return moves
        elif piece=='K' or piece=='k':
            if y+1<8:
                if x+1<8:
                    moves.append([x+1,y+1])
                if x-1>=0:
                    moves.append([x-1,y+1])
                moves.append([x,y+1])
            if y-1>=0:
                if x+1<8:
                    moves.append([x+1,y-1])
                if x-1>=0:
                    moves.append([x-1,y-1])
                moves.append([x,y-1])
            if x+1<8:
                moves.append([x+1,y])
            if x-1>=0:
                moves.append([x-1,y])
        elif piece[0]=='P':
            if y-1>=0:
                if x+1<8:
                    moves.append([x+1,y-1])
                if x-1>=0:
                    moves.append([x-1,y-1])
                moves.append([x,y-1])
            if y==6:
                moves.append([x,y-2])
            return moves
        elif piece[0]=='p':
            if y+1<8:
                if x+1<8:
                    moves.append([x+1,y+1])
                if x-1>=0:
                    moves.append([x-1,y+1])
                moves.append([x,y+1])
            if y==1:
                moves.append([x,y+2])
        return moves