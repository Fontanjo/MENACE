import numpy as np
from utils import hash_to_board

# Tokens to choose next move
BLUE   = (0, 0)
RED    = (0, 1)
ORANGE = (0, 2)
GREEN  = (1, 0)
ROSE   = (1, 1)
PURPLE = (1, 2)
YELLOW = (2, 0)
GREY   = (2, 1)
BLACK  = (2, 2)

BEADS = [BLUE, RED, ORANGE, GREEN, ROSE, PURPLE, YELLOW, GREY, BLACK]


INITIAL_BEADS = 5

def get_initial_beads(hs, nb_of_each):
	standard_board = hash_to_board(hs, 0)
	bds = []
	for bd in BEADS:
		if standard_board[bd] == 0:
			for _ in range(nb_of_each):
				bds.append(bd)

	return bds

def choose_menace_move(hs, variant, dict_of_beads):
	if hs not in dict_of_beads or dict_of_beads[hs] == []:
		dict_of_beads[hs] = get_initial_beads(hs, INITIAL_BEADS)

	# Get possible moves (weighted)
	possible_moves = dict_of_beads[hs]
	# Choose one
	move = possible_moves[np.random.choice(len(possible_moves))]

	return move

# Add new beads
def add_beads(dict_of_beads, moves):
	for hash_val, _, bead in moves:
		dict_of_beads[hash_val].append(bead)

# Remove beads
def remove_beads(dict_of_beads, moves):
	for hash_val, _, bead in moves:
		dict_of_beads[hash_val].remove(bead)