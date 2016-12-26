# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:41:13 2016

@author: Nick
"""

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
        #attackedByWhite
        self.gameState[9] = [[False for i in range(8)] for j in range(8)]
        #attackedByBlack
        self.gameState[10] = [[False for i in range(8)] for j in range(8)]
        
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
                    for newX in range(8):
                        for newY in range(8):
                            if self.isLegalMotion(self.gameState,x,y,newX,newY):
                                newGameState = copy.deepcopy(self.gameState)
                                if self.isValidMove(newGameState,x,y,newX,newY):
                                    #makemove
                                    self.movePiece(newGameState,x,y,newX,newY)
                                    if self.isCheck(newGameState,False)==False:
                                        score = self.minPlay(1,newGameState,False,bestScore)
                                        if score>bestScore:
                                            bestScore = score
                                            bestMove = [x,y,newX,newY]
                                        
        return bestMove
    
    #The evaluation function for the AI's turn
    def maxPlay(self, depth, gameState, isWhite, currentMin):
        #Check if game is over or it's reached max depth
        if depth==self.Max_Depth or self.isCheckmate():
            return self.evaluateGame(gameState, isWhite)
            
        maxScore = -sys.maxint -1
        
        for x in range(8):
            for y in range(8):
                #spot is currently occupied by AI's piece
                if (gameState[0])[y][x]!='' and (gameState[0])[y][x].islower()==True:
                    for newX in range(8):
                        for newY in range(8):
                            if maxScore>currentMin:
                                return maxScore
                            if self.isLegalMotion(gameState,x,y,newX,newY):
                                newGameState = copy.deepcopy(gameState)
                                if self.isValidMove(newGameState,x,y,newX,newY):
                                    #makemove
                                    self.movePiece(newGameState,x,y,newX,newY)
                                    if self.isCheck(newGameState,False)==False:
                                        score = self.minPlay(depth+1,newGameState,isWhite, maxScore)
                                        if score>maxScore:
                                            maxScore = score
                                        
        return maxScore
        
    #The evaluation function for the Opponents turn
    def minPlay(self, depth, gameState, isWhite, currentMax):
        #Check if game is over or it's reached max depth
        if depth==self.Max_Depth or self.isCheckmate():
            return self.evaluateGame(gameState, isWhite)
            
        minScore = sys.maxint
        
        for x in range(8):
            for y in range(8):
                #spot is currently occupied by Opponents piece
                if (gameState[0])[y][x]!='' and (gameState[0])[y][x].isupper()==True:
                    for newX in range(8):
                        for newY in range(8):
                            if minScore<currentMax:
                                return minScore
                            if self.isLegalMotion(gameState,x,y,newX,newY):
                                newGameState = copy.deepcopy(gameState)
                                if self.isValidMove(newGameState,x,y,newX,newY):
                                    #makemove
                                    self.movePiece(newGameState,x,y,newX,newY)
                                    if self.isCheck(newGameState,False)==False:
                                        score = self.maxPlay(depth+1,newGameState,isWhite,minScore)
                                        if score<minScore:
                                            minScore = score
        
        return minScore
        
        
    def evaluateGame(self, gameState, isWhite):
        materialScore = 0
        centerControl = 0
        for x in range(8):
            for y in range(8):
                if (gameState[0])[y][x]!='':
                    #catch empty spot
                    if (gameState[0])[y][x]=='k':
                        materialScore+=200
                    elif (gameState[0])[y][x]=='K':
                        materialScore-=200
                    elif (gameState[0])[y][x]=='q':
                        materialScore+=9
                    elif (gameState[0])[y][x]=='Q':
                        materialScore-=9
                    elif (gameState[0])[y][x]=='r':
                        materialScore+=5
                    elif (gameState[0])[y][x]=='R':
                        materialScore-=5
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
                        if (x>=2 or x<=5) and y>0:
                            centerControl+=0.5
                    elif ((gameState[0])[y][x])[0]=='P':
                        materialScore-=1
                        if (x>=2 or x<=5) and y<7:
                            centerControl-=0.5
                            
        return (materialScore+centerControl)
    
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
                if gameState[8]==True:
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
                if gameState[7]==True:
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
                    if (endY-startY)==-1:
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
                if gameState[8]==True:
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
                if gameState[7]==True:
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
                    if (endY-startY)==-1:
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
    
    """Update the currently under attack arrays"""
    def updateAttacked(self, gameState):      
        #Clear attacked by White array
        (gameState[9]) = [[False for i in range(8)] for j in range(8)]
        #Clear attacked by Black array
        (gameState[10]) = [[False for i in range(8)] for j in range(8)]
        
        for y in range(8):
            for x in range(8):
                #Update attacked by white
                if (gameState[0])[y][x]!='' and (gameState[0])[y][x].isupper():
                    #Update squares for pawn attacks
                    if len((gameState[0])[y][x])==2:
                        if (x+1)<8 and (y-1)>=0:
                            (gameState[9])[y-1][x+1]=True
                        if (x-1)>=0 and (y-1)>=0:
                            (gameState[9])[y-1][x-1]=True
                            
                    for newX in range(8):
                        for newY in range(8):
                            if len((gameState[0])[y][x])<=1 and self.isLegalMotion(gameState,x,y,newX,newY)==True:
                                (gameState[9])[newY][newX]=True
                                
                #Update attacked by black
                elif (gameState[0])[y][x]!='' and (gameState[0])[y][x].islower():
                    #Update squares for pawn attacks
                    if len((gameState[0])[y][x])==2:
                        if (x+1)<8 and (y+1)<8:
                            (gameState[10])[y+1][x+1]=True
                        if (x-1)>=0 and (y+1)<8:
                            (gameState[10])[y+1][x-1]=True
                            
                    for newX in range(8):
                        for newY in range(8):
                            if  len((gameState[0])[y][x])<=1 and self.isLegalMotion(gameState,x,y,newX,newY)==True:
                                (gameState[10])[newY][newX]=True                
                    
    """Check if the current square is under attack"""
    def isAttacked(self, gameState, isWhite, currentX, currentY):
        #Test if white is attacking this square
        if isWhite==False:
            return (gameState[9])[currentY][currentX]
            
        #Test if black is attacking this square
        else:
            return (gameState[10])[currentY][currentX]
        
    """Check if the king is in check"""
    def isCheck(self, gameState, isWhite):  
        #Black King, check if space is attacked by white
        if isWhite==False:
            for x in range(8):
                for y in range(8):
                    if (gameState[0])[y][x]=='k':
                        currentY=y
                        currentX=x
                        return (gameState[9])[currentY][currentX]
            
            
        #White Queen, check if space is attacked by Black
        else:
            for x in range(8):
                for y in range(8):
                    if (gameState[0])[y][x]=='K':
                        currentY=y
                        currentX=x
                        return (gameState[10])[currentY][currentX]
        
        return True
            
    
    def isCheckmate(self):
        return False