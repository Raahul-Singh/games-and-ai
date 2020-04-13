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

#### 1) Exploitation vs Exploration tradeoff
For any game playing search agent, there is always a tradeoff between exploiting its already searched neighbourhood and exploring futher. This is characterised by the `field of view` of the search agent, which is the radius from its current state upto which the agent will explore its neighbourhood.
By being exploitation heavy, the player may miss out on more valuable stases further away from its current `field of view`, but can depend on the utility of the states neearby, and is usually faster in making decisions.
On the other hand, an agent which explores more, runs the risk of taking a longer time and not finding any particularly useful new state.
A game of tictactoe is denoted by a tuple (a, b) where `a` represents the length of the board side, and `b` denotes the win score or the number of contigous squares required to win the game. Thus a traditional tictactoe game would be (3, 3).
Further, in tictactoe, the `field of view` of the agent is the spacial distance form its current square that the player is willing to explore.
In tictactoe, a player is more likely to win if he makes a move in a region where he already has made moves previously.
With larger games, where the winning score is smaller, eg., side 7 and wins core 3 this means that the game will finish in much less number of moves than the total nmber of possible states in the game.
Exploration in this scenario will take the agent spacially away from its current move. This would lead to suboptimal and downright poor gameplaying.
Thus, tictactoe is a game where the player is more likely to win if he exploits his neighbourhood.
I have implemented this by calculating the distance of the possible moves at any given state from the last played move by the player. By setting the `field of view` to be equal to the win score, only those states are considered that are at a distance less than or equal to the required win score from the last played move.
This has several useful implications:
* The agent is forced to find the best move near the last played move. 
* This ensures fast searches for winning configurations.
* It reduces the number of moves required to win the game.
* It makes up for sub optimal players as the AI would prioritise winning the game based on its own previous moves first. This is a big intuitive step up from a traditional minimax algorithm.
* There is a hard limit on the number of states to be considered per move.
, * Performance wise this produces near unfathomable speedups. For example, in vanilla minimax, for the third move of a (7, 3) game would need to consider 47! moves. This implementation would by contrast only need, around 23! moves. This is an order of 10^(37) less moves, while ensuring optimal play.
Further, this works extremely well when using alpha beta pruning and depth limiting heuristics as described below, ensuring optimal play.
Since the number of states generated depend on the winning score and not the board size, the efficiency of this approach grows by the order factorial of the square of the board side divided by the factorial of the (win score + 1) square. 
* Due to this massive speedup, it enabled the agent to use a larger depth limit while searching, which further increases its performance.

#### 2) Use of a Robust Evaluation Heuristic
The Evaluation Heuristic used here directly makes a few assumpions about gameplay:
* In order to win a game, the new move must be near already placed moves, i.e, the move density in a region is directly proportional to its value.
* The player is more likely to win if he plays a move in rows, columns or diagonals where he already has made moves previously.
* Making your opponent lose is just as important as winning the game, i.e, breaking your opponents chain of moves is highly beneficial in larger boards.

#### 3) Randomisation 
While getting the list of all possible actions, the list of tuples of possible actions are randomly shuffled.
This prevents a bias that the search algorithm may develop as it would otherwise always check the `top left`
quadrant first in each iteration.
This also diversifies the search space and is akin to random restarts in local search.

Further, by keeping a track of the previous moves, the goal test is done in order O(win score), again exploiting the locality of moves in tictactoe.

Thus, a combination of `limiting Field of View`, a heuristic that exploits the `locality of previous moves`, `randomisation of search moves` and a clever implementation of `goal test` allows this program to play near optimally and with a near constant speed irrespective of the board size.
