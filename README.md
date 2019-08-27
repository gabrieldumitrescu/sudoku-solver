# sudoku-solver
An application that shows sudoku puzzles in graphical form and can solve them.
# Getting Started
The application is written in python3 using pygame for the graphical interface.

### Prerequisites
Requires a recent version of python3. Installation procedure depends on OS and architecture.

After installing python it needs ```pygame``` library. Installing it is as simple as running ```pip install pygame```, but I
recommend doing that in a virtual environment. For that, after cloning the repository or downloading the file to a directory,
named for example sudoku-solver and changing to that directory you can run:
```
python3 -m venv .
source bin/activate
pip install pygame
```
### Installing
Does not need installation other than the prerequisite pygame library. I comes as a .py file that can be executed as is.

## Running
If pygame is globaly installed it can be run with just:
```
python3 sudoku-solver.py
```
If installed in a virtual environment, first the venv must be activated by doing:
```
source bin/activate
```
and then running sudoku-solver.py

The sudoku-solver.sh does both steps automaticaly and also deactivates the venv after leaving the application.

The application shows a random sudoku puzzle.
To show a different puzzle press ```n``` key.
To show current sudoku solution press ```s```.
The puzzles are chosen from one of five categories 1 to 5 in increasing difficulty.
By default it chooses puzzles from the 'hard' category, from file puzzles4.txt.
To choose a different category, modify line 69 in sudoku-chooser.py with one of:
'easiest', 'easy', 'normal', 'hard', or 'hardest'
For example:
```
chooser=SudokuChooser('easiest')
```

## Author
 * **Gabriel Dumitrescu** - *Initial work* -
 
## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements
 *  Pygame library - https://www.pygame.org
