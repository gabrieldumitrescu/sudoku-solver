from sudoku import Sudoku
import random

class SudokuChooser:
    def __init__(self,difficulty='easiest'):
        self.difficulty={
            'easiest':'puzzles1.txt',
            'easy':'puzzles2.txt',
            'normal':'puzzles3.txt',
            'hard':'puzzles4.txt',
            'hardest':'puzzles5.txt'}
        if difficulty not in self.difficulty:
            print(f'Difficulty string must be one of:easiest,easy,normal,hard,hardest ({difficulty} given)')
            print(f'Selecting easiest difficulty')
            difficulty='easiest'
        random.seed(3)
        self.puzzleFile=self.difficulty[difficulty]
        self.newPuzzle()

    def getPuzzle(self):
        return self.currentPz

    def newPuzzle(self):
        idx=random.randint(0,10000)
        #print(f'new index chosen {idx}')
        with open(self.puzzleFile,'r') as pzfile:
            strpz=pzfile.readlines()[idx]
            #print(f'Read puzzle:{strpz}')
            self.currentPz=Sudoku(strpz[:-1])
        return self.currentPz
    





