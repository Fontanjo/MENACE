import numpy as np
from itertools import chain
from tqdm import tqdm
import matplotlib.pyplot as plt
from copy import copy

from players import RandomPlayer, MenacePlayer, MiniMaxPlayer
from utils import hash_board, hash_to_board, variate_matrix, flatten, pretty_print_matrix, pretty_print_matrices
from menace import choose_menace_move, get_initial_beads, add_beads, remove_beads
from tic_tac_toe import win, draw, cross_win, circle_win, full_board

CIRCLE_STRATEGY = "minimax" # "menace" # "random"


# Store list of matrice outside hash function, to avoid regenerating it every time
list_of_h_matrices = None


EPOCHS = 20 # At every epoch the nb of wins/draws/looses are stored
GAMES_PER_EPOCH = 20

NB_RESETS = 1 # Copy strategy to opponent (if menace) and reset ai



# Player 1 uses crosses, player 2 uses circles
# Define constants for readability
EMPTY = 0
CROSS = 1
CIRCLE = 2


def main():
	if CIRCLE_STRATEGY == "random":
		pl = RandomPlayer()
	elif CIRCLE_STRATEGY == "menace":
		pl = MenacePlayer()
	elif CIRCLE_STRATEGY == "minimax":
		pl = MiniMaxPlayer(max_depth=8)
	else:
		print("Given circle_strategy not found, using random")
		pl = RandomPlayer()

	dict_of_beads = {}

	nb_epochs = EPOCHS
	nb_games_per_epoch = GAMES_PER_EPOCH

	results = []
	nb_beads = []
	for r in range(NB_RESETS):
		for e in tqdm(range(nb_epochs)):
			w, d, l = play_epoch(nb_games_per_epoch, dict_of_beads, opponent=pl)
			results.append([w, d, l])
			nb_beads.append(np.sum([len(v) for v in dict_of_beads.values()]))
		if CIRCLE_STRATEGY == "menace":
			pl.set_dict(copy(dict_of_beads))
			dict_of_beads = {}


	# Play and print one game
	#play_game(np.zeros((3,3)), dict_of_beads, opponent=pl, plot_game=True)
	
	#results = results[0::100]
	plt.title("Menace results")
	plt.plot([r[0] for r in results], label="wins")
	plt.plot([r[1] for r in results], label="draw")
	plt.plot([r[2] for r in results], label="loose")
	plt.legend()
	
	plt.figure()
	plt.plot(nb_beads)
	plt.title("Number of beads")
	plt.show()


def play_epoch(nb_games_per_epoch, dict_of_beads, opponent):
	wins, draws = 0, 0
	for g in range(nb_games_per_epoch):
		board = np.zeros((3,3))
		res = play_game(board, dict_of_beads, opponent)
		if res == 1:
			wins += 1
		elif res == 0:
			draws += 1
	return wins / nb_games_per_epoch, draws / nb_games_per_epoch, (nb_games_per_epoch - wins - draws) / nb_games_per_epoch


def play_game(board, dict_of_beads, opponent, plot_game=False):
	moves = []
	#print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	#print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	while not win(board) and not draw(board):
		# Get hash of current board, and which variant it is
		hs, var = hash_board(board)
		# Choose next move
		mm = choose_menace_move(hs, var, dict_of_beads)
		# Save infos
		moves.append((hs, var, mm))
		# Ev. adapt to board variant
		adpt_mm = variate_beads(mm, var)
		# Play move
		board[adpt_mm] = CROSS
		if plot_game: pretty_print_matrix(board)

		# Check if menace won with last move
		if not cross_win(board) and not full_board(board):
			# Play opponents move
			mo = opponent.play(board)
			# Play move
			board[mo] = CIRCLE
			if plot_game: pretty_print_matrix(board)


	### TODO improvement: consider doing this all together only after entire epoch
	#### Similar to batch principle

	# Draw is considered positive, add 1 bead for each one played
	if draw(board):
		# print("draw")
		add_beads(dict_of_beads, moves)
		return 0

	# If win, add 3 beads for each one played
	if cross_win(board):
		# print("win")
		for _ in range(3):
			add_beads(dict_of_beads, moves)
		return 1

	if circle_win(board):
		# print("loose")
		remove_beads(dict_of_beads, moves)
		return -1


def choose_opponent_move(board, strategy="menace"):
	# TODO implement different strategies (random/last menace checkpoint/perfect/...)
	if strategy == "random":
		valid_pos = []
		# TODO find np function to select indices where value == 0
		for i in range(3):
			for j in range(3):
				if board[i][j] == 0:
					valid_pos.append((i, j))
		
		# valid_pos is considered a 2d array, while random.choice only works with 1d
		return valid_pos[np.random.choice(len(valid_pos))]

	if strategy == "menace":
		hs, var = hash_board(board)
		return choose_menace_move(hs, var, circle_menace_dict)


# Generate all possible combinations of (valid) positions with given number of crosses and circles
def generate_specific_combinations(nb_crosses, nb_circles):
	assert nb_crosses >= nb_circles - 1
	assert nb_crosses <= nb_circles + 1
	
	m = np.zeros((3, 3))

	boards = place_tokens(m, nb_crosses, nb_circles, [])

	# Get hash value for each board (do not consider index)
	hs = [hash_board(b)[0] for b in boards]

	# Remove duplicates
	hs = list(set(hs))
	
	return hs


def variate_beads(bead, variation):
	# Create empty matrix
	m = np.zeros((3, 3))

	# Insert bean at right place
	m[bead] = 1

	# Profit from existing function to find new position
	m_v = variate_matrix(m, variation)

	# Extract new position of 1 and take first instance (only 1 instance should exist)
	for i in range(3):
		for j in range(3):
			if m_v[i][j] == 1:
				return (i,j)


# Recursive function
def place_tokens(matrix, nb_crosses, nb_circles, matrices):
	if nb_crosses == 0 and nb_circles == 0:
		m = np.copy(matrix)
		m[m == -1] = 0
		m[m == -2] = 0
		matrices.append(m)
		return matrices

	curr_matrix = matrix

	# Start by placing all the crosses
	if nb_crosses > 0:
		TO_PLACE = CROSS
		# Remove 1 from crosses to place
		nb_crosses -= 1
	else:
		# Once all crosses have been placed, "reset" the block and allow
		#  to place circles in previous spots
		curr_matrix[curr_matrix==-1] = 0
		TO_PLACE = CIRCLE
		# Remove 1 from circles to place
		nb_circles -= 1

	# Place tokens in all positions
	for i in range(3):
		for j in range(3):
			# TODO make it more readable and less contort
			#  To avoid repetitions, do not allow to place a token in a position 
			#  in which a token of the same type has been before
			#  e.g. XX- ... X-X... then after placing the first -X- 
			#   the second X will be placed in position 0 again, 
			#   repeating XX-
			#  Mark those positions with the negative of the other token
			if curr_matrix[i][j] == EMPTY or curr_matrix[i][j] == -TO_PLACE:
				curr_matrix[i][j] = TO_PLACE
				matrices = place_tokens(matrix, nb_crosses, nb_circles, matrices)
				curr_matrix[i][j] = -(3 - TO_PLACE)

	return matrices


if __name__ == "__main__":
	main()