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
        
        #Setup board font, readonly, colours, alignment and labels
        self.boardGrid = wx.grid.Grid(self, -1)
        self.boardGrid.CreateGrid(8,8)
        self.boardGrid.SetDefaultColSize(50, True)
        self.boardGrid.SetDefaultRowSize(50, True)
        for y in range(8):
            for x in range(8):
                self.boardGrid.SetReadOnly(x, y, True)
                if ((y%2)+x)%2==0:
                    self.boardGrid.SetCellBackgroundColour(y, x, 'WHITE')
                else:
                    self.boardGrid.SetCellBackgroundColour(y, x, 'GREY')
        newFont = self.boardGrid.GetDefaultCellFont()
        newFont.SetPointSize(25)
        self.boardGrid.SetDefaultCellFont(newFont)
        self.boardGrid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.boardGrid.SetRowLabelValue(0, '8')
        self.boardGrid.SetRowLabelValue(1, '7')
        self.boardGrid.SetRowLabelValue(2, '6')
        self.boardGrid.SetRowLabelValue(3, '5')
        self.boardGrid.SetRowLabelValue(4, '4')
        self.boardGrid.SetRowLabelValue(5, '3')
        self.boardGrid.SetRowLabelValue(6, '2')
        self.boardGrid.SetRowLabelValue(7, '1')
        
        #Place pieces
        self.boardGrid.SetCellValue(0, 0, u'\u265C')
        self.boardGrid.SetCellValue(0, 7, u'\u265C')
        self.boardGrid.SetCellValue(0, 1, u'\u265E')
        self.boardGrid.SetCellValue(0, 6, u'\u265E')
        self.boardGrid.SetCellValue(0, 2, u'\u265D')
        self.boardGrid.SetCellValue(0, 5, u'\u265D')
        self.boardGrid.SetCellValue(0, 3, u'\u265B')
        self.boardGrid.SetCellValue(0, 4, u'\u265A')
        for i in range(8):
            self.boardGrid.SetCellValue(1, i, u'\u265F')
            self.boardGrid.SetCellValue(6, i, u'\u2659')
        self.boardGrid.SetCellValue(7, 0, u'\u2656')
        self.boardGrid.SetCellValue(7, 7, u'\u2656')
        self.boardGrid.SetCellValue(7, 1, u'\u2658')
        self.boardGrid.SetCellValue(7, 6, u'\u2658')
        self.boardGrid.SetCellValue(7, 2, u'\u2657')
        self.boardGrid.SetCellValue(7, 5, u'\u2657')
        self.boardGrid.SetCellValue(7, 3, u'\u2655')
        self.boardGrid.SetCellValue(7, 4, u'\u2654')
                    
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
        self.contentSizer.Add(self.lastMove, (4, 1))
        self.contentSizer.Add(self.moveOutput, (4, 2))
        
        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.contentSizer, 1, wx.ALL | wx.EXPAND, 5)
        
        #Implement the sizers
        self.controls.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.frameSizer)
        
        #Event handler
        self.button.Bind(wx.EVT_BUTTON, self.ButtonPress)
        
    def ButtonPress(self, e):
        self.moveOutput.SetValue("Move Recorded")
        files = ['A','B','C','D','E','F','G','H']
        ranks = ['8','7','6','5','4','3','2','1']
        
        rawIn = self.moveInput.GetValue()
        nMove = list(rawIn)
        if (nMove[0] and nMove[2] in files) and (nMove[1] and nMove[3] in ranks):
            self.moveOutput.SetValue(rawIn)
            #Hand nMove to the main program
            self.boardGrid.SetCellValue(files[nMove[2]], ranks[nMove[3]], self.boardGrid.GetCellValue(files[nMove[0]], ranks[nMove[1]]))
            self.boardGrid.SetCellValue(files[nMove[0]], ranks[nMove[1]], "")
        else:
            self.moveOutput.SetValue("Invalid Move")
        
app = wx.App(False)
frame = ChessFrame(None)
frame.Show()
app.MainLoop()