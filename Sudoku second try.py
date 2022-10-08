# -*- coding: utf-8 -*-

import numpy as np
import copy

"""
Created on Tue Nov 16 14:31:28 2021

@author: Oliver
"""

class partialSudoku:
    def __init__(self, inputSudoku, sl, parent = None, missingDict = {}, newValueX = 0, newValueY = 0):
        """initialiser, also "logically solves" sudoku as far as possible (fills in blanks without guessing)"""
        
        self.parent = parent
        
        self.sudoku = np.zeros([9, 9], int)
        self.sl = sl                        #square length, just incase larger / smaller sudokus are used
        self.missingDict = missingDict      #stores the possible values of every square in the sudoku
        self.valid = True
                    
        if(len(missingDict) == 0):
            for i in range(0, 81):
                missingDict[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                 
            #print(missingDict)                
            
            #sets sudoku values given to what they already were to update the dictionary
            for y in range(0, self.sl**2):
                for x in range(0, self.sl**2):
                    if(inputSudoku[y, x] != 0):
                        if(not self.setValue(inputSudoku[y, x], y, x)):
                            print("unsolvable")
                            self.valid = False
                            return None
            
            
        else:
            #print("dictionary given, setting ",newValueX,", ",newValueY," to ",inputSudoku[newValueY, newValueX]," and solving")
            #print(missingDict)
            self.sudoku = inputSudoku.copy()
            self.sudoku[newValueY, newValueX] = 0
            if(not self.setValue(inputSudoku[newValueY, newValueX], newValueY, newValueX)):
                print("unsolvable")
                self.valid = False
                return None
            
        #print(missingDict)
        print("partially solved")
        
    
    def setValue(self, value, y, x):
        """writes value into the sudoku and removes the same value from relevent lists in the dictionary"""
        #print("setting ",x,", ",y," to ",value)
        #print("set ",x,", ",y," to value ",value)
        self.missingDict[self.dictIndexD(y, x)] = []    #setting the dictionary to empty so it doesnt clash with itself
        
        for i in range(0, self.sl**2):
            if(
            not self.removeListValue(y, i, value) or                              #removes value from lists in row
            not self.removeListValue(i, x, value) or                              #removes value from lists in collumn
            not self.removeListValue(((y//self.sl)*self.sl) + (i//self.sl), ((x//self.sl)*self.sl) + (i%self.sl), value)  #removes value from lists in block
            ):
                return False #if any of the removeListValues return false, dont dont bother with the rest of the sudoku
            
        self.sudoku[y, x] = value
        self.missingDict[self.dictIndexD(y, x)] = [value]
        return True
            
            
            
    def removeListValue(self, y, x, value):
        """removes a value from a given square,
        also fills in values where it can and returns false if the sudoku is invalid"""
        
        lisst = self.missingDict[self.dictIndexD(y, x)] #ease of refference
                    
        if(not self.contains(lisst, value)):        #already removed from list
            return True
        elif(len(lisst) == 1):      #no possible values in space, no solutions to sudoku
            #print(x,", ",y," has list ",lisst," and it is being removed leaving no possibilities")
            return False
        elif(len(lisst) == 2):      #only 2 possible values and one is removed, must be the value
            #print("only 2 values in space ",x,", ",y," and one is being removed")
            if(lisst[0] == value):
                return self.setValue(self.missingDict[self.dictIndexD(y, x)][1], y, x)
            else:
                return self.setValue(self.missingDict[self.dictIndexD(y, x)][0], y, x)
        
        for i in range(0, len(lisst)):  #removes value from the squares list
            if(lisst[i] == value):
                del self.missingDict[self.dictIndexD(y, x)][i]
                break
                
        return True
        
    def generateFrontier(self):
        block = self.sl**2              #block with least empty spaces
        value = self.sl**2              #value that corresponds to the lowest number found
        lowest = (self.sl**2) + 1       #lowest number found
        current = 0                     #current number being checked
        
        for i in range(0, self.sl**2):   #finds block with the least 0's
            current = self.getOs(self.getBlock(i, self.sudoku))
            if(current < lowest):
                lowest = current
                block = i
        
                
        #print(block)
        
        possibilityCount = np.zeros((self.sl**2) + 1, int)    #counts how many squares numbers 1-9 number can fit in
        for y in range(0, self.sl):
            for x in range(0, self.sl):
                if(len( self.missingDict[self.dictIndex(block//self.sl, block%self.sl, y, x)] ) != 1):    ##filled in block
                    #print("x: ",x," y: ",y,", ",self.missingDict[self.dictIndex(block//self.sl, block%self.sl, y, x)])
                    for possibility in self.missingDict[self.dictIndex(block//self.sl, block%self.sl, y, x)]:
                        possibilityCount[possibility] += 1
            
        value = 0
        lowest = (self.sl**2) + 1
        #print(possibilityCount)
        
        for i in range(1, (self.sl**2)+1):      #finds the number that can fit in the least squares thats not already assigned
            if(possibilityCount[i] < lowest and possibilityCount[i] != 0):
                lowest = possibilityCount[i]
                value = i
                #if(possibilityCount[i] == 1):
                    #print("this should not happen")        does sometimes happen, easy position to fill in
                    #print("block: ",block," value: ",value)
            
        
        children = []               #makes children for each square the value can be placed in
        for y in range(0, self.sl):
            for x in range(0, self.sl):
                #print(self.missingDict[self.dictIndex(block//self.sl, block%self.sl, y, x)])
                if(value in self.missingDict[self.dictIndex(block//self.sl, block%self.sl, y, x)]):
                    #print("child generated")
                    tempSudoku = self.sudoku.copy()
                    tempSudoku[(block//self.sl)*self.sl + y, (block%self.sl)*self.sl + x] = value
                    newChild = partialSudoku(tempSudoku.copy(), self.sl, self, copy.deepcopy(self.missingDict), (block%self.sl)*self.sl + x, (block//self.sl)*self.sl + y)
                    if(newChild.valid):
                        children.append(newChild)
                    #else:
                        #print("child generated was invalid")
                        
        return children
        
    def aiSolve(self):
        
        print(self.sudoku)
        
        complete = True                 #checks if the sudoku is full (a solution)
        for y in range(0, self.sl**2):
            for x in range(0, self.sl**2):
                if(self.sudoku[y, x]==0):
                    complete = False
                    
        if(complete):
            print("solution found")
            return self.sudoku
        
        children = self.generateFrontier()
        #print(len(children)," to explore")
        
        for child in children: #recursively calls for each child generated, filling in more spaces and logically solving until complete or invalid
            potentialSolution = child.aiSolve()
            if( type(potentialSolution) != str):
                print("returning solution")
                return potentialSolution
        
        return "no solution"
    
        
    def getBlock(self, blockID, sudoku):
        """gets a block (3x3) from the sudoku, clocks numbered 0-8, horisontally then vertically"""
        
        block = np.zeros((self.sl, self.sl), dtype = int)
        modY = (blockID//self.sl)*self.sl
        modX = (blockID%self.sl)*self.sl
        for y in range( 0, self.sl):
            for x in range( 0, self.sl):
                block[y, x] = sudoku[modY + y, modX + x]
        return block
    
    def getMissingNumbers(self, block):
        """gets missing numbers given a 3x3 block"""
        
        missing = []
        for i in range(1, (self.sl*self.sl) + 1):
            missing.append(i)
        
        #print("should be 1-9 ",missing)
        
        for y in range(0, self.sl):
            for x in range(0, self.sl):
                for i in range(0, len(missing)):
                    if(missing[i] == block[y, x]):
                        #print("removing ",missing[i]," as its in ",x,", ",y)
                        del missing[i]
                        #print(missing)
                        break
        return missing
    
    def getOs(self, block):
        """gets number of missing numbers (0's) in a given block"""
        
        retValue = 0
        for y in range(0, self.sl):
            for x in range(0, self.sl):
                if(block[y, x] == 0):
                    retValue+= 1
        if(retValue == 0):
            retValue = (self.sl**2)+1 #should help with some logical stuff, filled boxes are usually ignored
        return retValue

    
    def contains(self, lisst, value):       #when i forgot you could use keyword "in"
        for v in lisst:
            if(value == v):
                return True
        return False
    
    #some shortcut functions to reduce typing and line length  
    def dictIndexD(self, yDD, xDD):
        return (yDD* (self.sl**2)) + xDD
    
    def dictIndex(self, yyD, xxD, yD, xD):
        return (yyD* (self.sl**3)) + (yD* (self.sl**2)) + (xxD* (self.sl**1)) + xD
    
hard1 = np.array([[1, 0, 0, 7, 0, 0, 0, 0, 0], 
                    [0, 3, 2, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 6, 0, 0, 0, 0, 0], 
                    [0, 8, 0, 0, 0, 2, 0, 7, 0], 
                    [5, 0, 7, 0, 0, 1, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 3, 6, 1, 0], 
                    [7, 0, 0, 0, 0, 0, 2, 0, 9], 
                    [0, 0, 0, 0, 5, 0, 0, 0, 0], 
                    [3, 0, 0, 0, 0, 4, 0, 0, 5], 
                    ])

veryEasy1 = np.array([[0, 9, 3, 1, 5, 2, 6, 0, 8], 
                        [8, 6, 2, 7, 0, 3, 1, 9, 5], 
                        [1, 5, 7, 9, 8, 6, 3, 2, 4], 
                        [9, 7, 8, 4, 2, 1, 0, 3, 6], 
                        [5, 0, 6, 8, 3, 9, 4, 1, 7], 
                        [3, 4, 1, 5, 6, 7, 2, 8, 9], 
                        [6, 1, 4, 2, 7, 8, 9, 5, 3], 
                        [7, 3, 9, 6, 1, 5, 8, 4, 2], 
                        [2, 8, 5, 3, 9, 4, 7, 6, 1], 
                        ])

hard2 = np.array([[0, 2, 0, 0, 0, 6, 9, 0, 0], 
                 [0, 0, 0, 0, 5, 0, 0, 2, 0], 
                 [6, 0, 0, 3, 0, 0, 0, 0, 0], 
                 [9, 4, 0, 0, 0, 7, 0, 0, 0], 
                 [0, 0, 0, 4, 0, 0, 7, 0, 0], 
                 [0, 3, 0, 2, 0, 0, 0, 8, 0], 
                 [0, 0, 9, 0, 4, 0, 0, 0, 0], 
                 [3, 0, 0, 9, 0, 2, 0, 1, 7], 
                 [0, 0, 8, 0, 0, 0, 0, 0, 2], 
                 ])

sudoku = partialSudoku(hard2, 3)
if(not sudoku.valid):
    print("invalid sudoku")
else:
    print(sudoku.aiSolve())