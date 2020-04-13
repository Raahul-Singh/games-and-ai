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

The custom optimization made to minimax algorithm: 
