import numpy as np
from copy import copy

from utils import hash_board, pretty_print_matrix
from menace import choose_menace_move
from tic_tac_toe import full_board, cross_win, circle_win, draw, win

# Player 1 uses crosses, player 2 uses circles
# Define constants for readability
EMPTY = 0
CROSS = 1
CIRCLE = 2


class RandomPlayer:
	def __init__(self):
		pass

	def play(self, board):
		valid_pos = get_valid_positions(board)
		
		# valid_pos is considered a 2d array, while random.choice only works with 1d
		return valid_pos[np.random.choice(len(valid_pos))]


class MenacePlayer:
	def __init__(self):
		self.circle_menace_dict = {}

	def play(self, board):
		hs, var = hash_board(board)
		return choose_menace_move(hs, var, self.circle_menace_dict)

	def set_dict(self, new_dict):
		self.circle_menace_dict = new_dict


class MiniMaxPlayer:
	def __init__(self, max_depth=9):
		self.max_depth = max_depth

	def play(self, board):
		output = minimax(board, min(len(get_valid_positions(board)), self.max_depth), CIRCLE)
		move, _ = output
		#print(output)

		# print(output)
		# If there is not a best move, play random
		if (move == None):
			valid_pos = get_valid_positions(board)
			print("Random")
			return valid_pos[np.random.choice(len(valid_pos))] 
		#else:
		#	pretty_print_matrix(board)
		#	print(move)
		
		return move


def minimax(board, depth, player):
	# Initialize values
	if (player == CIRCLE):
		best = [None, -np.inf]
	else:
		best = [None, np.inf]

	# Possibly stop recursive calls, if dpt = 0 or end of game
	if depth == 0 or win(board) or draw(board):
		if circle_win(board):
			score = 1
		elif cross_win(board):
			score = -1
		else:
			score = 0
		return [None, score]

	for m in get_valid_positions(board):
		# Execute move
		board[m] = player
		# Recursive call, inverting player
		opponent = (CROSS + CIRCLE - player)
		_, new_score = minimax(board, depth-1, opponent)
		# Undo move
		board[m] = EMPTY

		if player == CIRCLE:
			if new_score > best[1]:
				best = [m, new_score]
		else:
			if new_score < best[1]:
				best = [m, new_score]

	return best

def get_valid_positions(board):
	valid_pos = []
	# TODO find np function to select indices where value == 0
	for i in range(3):
		for j in range(3):
			if board[i][j] == 0:
				valid_pos.append((i, j))

	return valid_pos