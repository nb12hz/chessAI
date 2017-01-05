# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:20:43 2016

@author: Mitch
"""

import wx
import wx.grid

class ChessFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        
        #Setup board with Black and White coloured squares
        self.boardGrid = wx.grid.Grid(self, -1)
        self.boardGrid.CreateGrid(8,8)
        self.boardGrid.SetCellBackgroundColour(0, 0, 'BLACK')
        self.boardGrid.SetDefaultColSize(50, True)
        self.boardGrid.SetDefaultRowSize(50, True)
        for y in range(8):
            for x in range(8):
                if ((y%2)+x)%2==0:
                    self.boardGrid.SetCellBackgroundColour(y, x, 'WHITE')
                else:
                    self.boardGrid.SetCellBackgroundColour(y, x, 'BLACK')
                    
        #Setup the control panel, which has an input box, last move output, and button
        self.controls = wx.Panel(self)
        self.button = wx.Button(self.controls, label="Move piece")
        self.nextMove = wx.StaticText(self.controls, label="Your move:")
        self.moveInput = wx.TextCtrl(self.controls, size=(100, -1))
        self.lastMove = wx.StaticText(self.controls, label="Last move made:")
        self.moveOutput = wx.StaticText(self.controls, label="")
        
        #Frame sizer
        self.frameSizer = wx.BoxSizer()
        self.frameSizer.Add(self.controls, 1, wx.ALL | wx.EXPAND)
        
        #Content holding/arranging sizer
        self.contentSizer = wx.GridBagSizer(5, 5)
        self.contentSizer.Add(self.boardGrid, (0, 0))
        self.contentSizer.Add(self.nextMove, (1, 1))
        self.contentSizer.Add(self.moveInput, (1, 2))
        self.contentSizer.Add(self.button, (2, 1), (2, 2), flag=wx.EXPAND)
        self.contentSizer.Add(self.lastMove, (3, 1))
        self.contentSizer.Add(self.moveOutput, (3, 2))
        
        #Implement the sizers
        self.controls.SetSizerAndFit(self.contentSizer)
        self.SetSizerAndFit(self.frameSizer)
        
        #Event handler
        self.button.Bind(wx.EVT_BUTTON, self.ButtonPress)
        
    def ButtonPress(self, e):
        files = ['A','B','C','D','E','F','G','H']
        ranks = ['8','7','6','5','4','3','2','1']
        
        rawIn = self.moveInput.GetValue()
        nMove = list(rawIn)
        if (nMove[0] and nMove[2] in files) and (nMove[1] and nMove[3] in ranks):
            self.moveOutput.SetValue(rawIn)
            #Hand nMove to the main program
        
app = wx.App(False)
frame = ChessFrame(None)
frame.Show()
app.MainLoop()