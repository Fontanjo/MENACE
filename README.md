# MENACE - Python Implementation

Welcome to the Python implementation of MENACE (Matchbox Educable Noughts and Crosses Engine), one of the first demonstrations of artificial intelligence learning (in this case using the famous tic-tac-toe game).

## How MENACE Works

MENACE operates by using matchboxes to represent possible game states, with each matchbox containing marbles of different colors to denote potential moves. At every step, MENACE randomly picks a marble from the corresponding box in order to choose the next move.

Here's a brief overview of how MENACE learns:

- **Winning:** Every time MENACE wins a game, three new marbles (beads) with the same color as the winning move are added to the corresponding matchbox.

- **Draws:** In the case of a draw (a positive outcome in tic-tac-toe), one new marble (bead) with the same color as the moves contributing to the draw is added to the corresponding matchbox.

- **Losing:** When MENACE loses a game, the beads used in the moves leading to the loss are removed from the corresponding matchbox.

Through multiple iterations and learning epochs, MENACE adjusts its strategy based on the bead counts in each matchbox. This adaptive learning process helps MENACE become a progressively more skilled tic-tac-toe player.

For more in-depth information, refer to the original MENACE paper by Donald Michie: [Original MENACE Paper](https://people.csail.mit.edu/brooks/idocs/matchbox.pdf)

## Usage

To run MENACE:

1. Open `main.py`.
2. Specify the number of epochs, the number of games per epoch and the opponent type.
3. Run the file.

MENACE will automatically train and play games according to the specified parameters.

Feel free to contribute or explore further enhancements!

---

*Happy tic-tac-toe learning!*
