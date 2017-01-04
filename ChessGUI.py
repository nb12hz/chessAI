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
        
        #Master Panel
        self.masterPanel = wx.Panel(self)
        
        #Setup board with Black and White coloured squares
        self.boardGrid = wx.grid.Grid(self, self.masterPanel)
        self.boardGrid.CreateGrid(8,8)
        self.boardGrid.SetColSizes(self, 20)
        self.boardGrid.SetRowSizes(self, 20)
        for y in range(8):
            for x in range(8):
                if ((y%2)+x)%2==0:
                    self.boardGrid.SetCellBackgroundColour(self, y, x, wx.WHITE)
                else:
                    self.boardGrid.SetCellBackgroundColour(self, y, x, wx.BLACK)
                    
        #Setup the control panel, which has an input box, last move output, and button
        self.controls = wx.Panel(self, self.masterPanel)
        self.button = wx.Button(self.controls, label="Move piece")
        self.nextMove = wx.StaticText(self.controls, label="Your move:")
        self.moveInput = wx.TextCtrl(self.controls, size=(100, -1))
        self.lastMove = wx.StaticText(self.controls, label="Last move made:")
        self.moveOutput = wx.staticText(self.controls, label="")
        
        #Frame sizer
        self.frameSizer = wx.BoxSizer()
        self.frameSizer.add(self.masterPanel, 1)
        
        #Content holding/arranging sizer
        self.contentSizer = wx.GridBagSizer(3, 6)
        self.contentSizer.Add(self.boardGrid, (0, 0))
        self.contentSizer.Add(self.nextMove, (1, 0))
        self.contentSizer.Add(self.moveInput, (1, 1))
        self.contentSizer.Add(self.button, (1,2))
        self.contentSizer.Add(self.lastMove, (1, 3))
        self.contentSizer.Add(self.moveOutput, (1, 4))
        
        #Implement the sizers
        self.SetSizerAndFit(self.masterPanel)
        
        #Event handler
        self.button.Bind(wx.EVT_Button, self.ButtonPress)
        
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
        