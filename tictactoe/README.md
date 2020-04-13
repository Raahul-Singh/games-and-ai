To run the game, first install the requirements, as listed in the requirements.txt file.

```
pip install -r requirements.txt
```

To play, run the following command:

```
python tictactoe.py
```
The `Engine class` in the `solvers.py` holds the implemented minimax algorithmns and its variants.
The general overview of the game is:

* The `tictactoe.py` holds the IO class which implements the game UI.
* The `IO.py` holds the custom input classes. 
* PyGame does not support direct user input, hence the custom classes.
* The `Board` class in `tictactoe.py` holds the game board which is stored as a NumPy array.
* The `Player` class interfaces with the board and modifies its own state.
* Each AI `Player` has an `Engine` which decideds its next move.
* Lastly, all interactions are glued together in a `Game` object.

The custom optimizations made to minimax algorithms are as follows:

#### 1) Randomisation 
While getting the list of all possible actions, the list of tuples of possible actions are randomly shuffled.
This prevents a bias that the search algorithm may develop as it would otherwise always check the `top left`
quadrant first in each iteration.
This also diversifies the search space and is akin to random restarts in local search.

#### 2) Use of a Robust Evaluation Heuristic
The Evaluation Heuristic used here directly makes a few assumpions about gameplay:
* In order to win a game, the new move must be near already placed moves, i.e, the move density in a region is directly proportional to its value.
* The player is more likely to win if he plays a move in rows, columns or diagonals where he already has made moves previously.
* Making your opponent lose is just as important as winning the game, i.e, breaking your opponents chain of moves is hihly beneficial in larger boards.

