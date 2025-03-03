# SlitherlinkLPSolver
A Slitherlink puzzle solver powered by Linear Programming, featuring an interactive interface for easy use. This tool efficiently finds valid loop solutions by formulating the puzzle as a constraint satisfaction problem and solving it with mathematical optimization.

## Installation
- Ensure you have Python 3.7+ installed. 
- Make sure you have installed **gurobipy** and **tk** package.

## Usage

### Run the application

```sh
python src.py
```

### Choose size of the puzzle
- Enter the number of row and collumn of your puzzle

  ![Interface](https://github.com/minhtran0901/SlitherlinkLPSolver/blob/main/Interface.png)

### Example Screenshots:
- Example Puzzle from the website https://www.puzzle-loop.com/:
  
  ![puzzle_loop](https://github.com/minhtran0901/SlitherlinkLPSolver/blob/main/7x7%20Slitherlink.jpg)

- You need to enter the values of all the cells in the puzzle:
   
  ![puzzle_loop](https://github.com/minhtran0901/SlitherlinkLPSolver/blob/main/Puzzle.png)
    
  - Solved Puzzle will be display in terminal after you click **"Solve"**:

  ![Solved puzzle](https://github.com/minhtran0901/SlitherlinkLPSolver/blob/main/result.png)



## Note
- Nonogram rules: Find the rules here (https://en.wikipedia.org/wiki/Slitherlink)
- Read Slitherlink.pdf to understand the math
