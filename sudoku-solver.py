import logging
import pygame
from SudokuChooser import SudokuChooser
from sudoku import Sudoku


def createRenderedDigits(myfont,color=(0,0,0)):
    rendDigits=[]
    for i in range(1,10):
        rendDigits.append(myfont.render(str(i), False, color))
    return rendDigits


def renderSudoku(pz,screen,rendDim,puzzleDigits,solvedDigits):
    cX=rendDim[0]
    cY=rendDim[1]
    inPz=pz.getInitialStrPuzzle()
    cPz=pz.getCurrentStrPuzzle()
    for i in range(0,9):
        for j in range(0,9):
            cCellVal=int(cPz[i*9+j])
            inCellVal=int(inPz[i*9+j])
            if cCellVal is not 0:
                if inCellVal is 0:
                    screen.blit(solvedDigits[cCellVal-1],(cX,cY))
                else:
                    screen.blit(puzzleDigits[inCellVal-1],(cX,cY))
            cX+=rendDim[2]
            if (j+1)%3==0:
                cX+=15
        cY+=rendDim[3]
        if (i+1)%3==0:
                cY+=10
        cX=rendDim[0]


# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Sudoku solver")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((500,400))
    
     
    # define a variable to control the main loop
    running = True
     
    bkg_color=pygame.Color(255,255,255,255)
    screen.fill(bkg_color)

    
    pygame.font.init() 
    myfont = pygame.font.SysFont('Comic Sans MS', 25,bold=True)
    puzzleDigits=createRenderedDigits(myfont)
    solvedDigits=createRenderedDigits(myfont,(255,0,0))
    digitWidth,digitHeight=myfont.size('8')

    empty_grid=pygame.image.load("empty-sudoku-grid.gif")
    gridStart=(5,10)
    cellWidth=50
    cellHeight=40
    
    chooser=SudokuChooser('hard')
    p=chooser.getPuzzle()
    isSolved=False
    # main loop
    while running:
        screen.blit(empty_grid,gridStart)
        cX=gridStart[1]+(cellWidth-digitWidth)/2
        cY=gridStart[0]+3+(cellHeight-digitHeight)/2
        rendDim=(cX,cY,cellWidth,cellHeight)
        
        renderSudoku(p,screen,rendDim,puzzleDigits,solvedDigits)

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if isSolved is False:
                        p.solvePuzzle()
                        isSolved=True
                    else:
                        p.reset()
                        isSolved=False
                elif event.key == pygame.K_n:
                    isSolved=False
                    p=chooser.newPuzzle()
        pygame.display.flip()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    logging.basicConfig(filename='sudoku.log',filemode='w',level=logging.INFO,format='%(levelname)s:%(message)s')
    main()
