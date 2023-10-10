import numpy as np
from itertools import chain


# Player 1 uses crosses, player 2 uses circles
# Define constants for readability
EMPTY = 0
CROSS = 1
CIRCLE = 2

list_of_h_matrices = None

def main():
	# Generate all possible positions
	return generate_all_combinations()

	# Insert initial tokens

	# Play (against self? against random?)


# Has the board. Equivalent boards (rotated/flipped) should return the same hash
def hash_board(board):
	# The hash consists in the product of the values of a specific matrix
	#  to the exponent of the value in the board
	#  e.g  if the first row of the board contains a cross, a circle and an empty cell
	#  and the custom matrix is   2 | 3 | 5  then the hash value is
	#  2^1 * 3^2 * 5^0 = 18

	# Since we consider rotations and flipping of the board as equivalent, 
	#  the final hash value is the minimum among the values for each possibility

	# There are in total 8 variations
	#  To simplify, we rotate the custom matrix instead of the board
	
	global list_of_h_matrices

	if list_of_h_matrices == None:
		m0 = 	[[2, 3, 5],
				 [7, 11, 13],
				 [17, 19, 23]]

		list_of_h_matrices = [variate_matrix(m0, i) for i in range(8)]


	list_of_hashes = []
	for m in list_of_h_matrices:
		mf = flatten(m)
		bf = flatten(board)
		list_of_hashes.append(np.prod([a**b for a, b in zip(mf, bf)]))

	# TODO return also index, to retrieve movements
	mn = min(list_of_hashes)
	idxmn = np.argmin(list_of_hashes) # Store which variation it is
	return mn, idxmn


# Reconstruct the board given the hash value
def hash_to_board(hs, variation=0):
	board = np.zeros((3,3))

	iii = [0, 0, 0, 1, 1, 1, 2, 2, 2]
	jjj = [0, 1, 2, 0, 1, 2, 0, 1, 2]
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]

	for i, j, base in zip(iii, jjj, primes):
		if hs % (base**2) == 0:
			board[i][j] = 2
		elif hs % base == 0:
			board[i][j] = 1

	# TODO consider variation
	return variate_matrix(board, variation)


# Generate all possible combinations of (valid) positions
def generate_all_combinations():
	# Store hash of combinations
	combinations = []

	# Starting situation
	combinations += generate_specific_combinations(0, 0)
	
	# After playing
	for i in range(1, 5):
		combinations += generate_specific_combinations(i, i-1)
		combinations += generate_specific_combinations(i, i)

	# Case with 5 crosses and 4 circles do not need to be considered, since in this case the game is over
	
	# TODO remove combinations in which one player has won

	
	return combinations

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


# Generate a specific variation of the matrix, from those considered equivalent for this situation
def variate_matrix(m, variation):
	assert variation in range(8), f"Variation should be between 0 and 7, got {variation}"
	
	# Function to rotate the 2D matrix by 90 degrees clockwise
	rotate90 = lambda x: list(zip(*x[::-1]))

	# Function to horizontally flip a matrix
	hflip = lambda x: np.flip(x, 1)


	if variation == 0:
		return m

	if variation == 1:
		return rotate90(m)

	if variation == 2:
		return rotate90(rotate90(m))

	if variation == 3:
		return rotate90(rotate90(rotate90(m)))

	if variation == 4:
		return hflip(m)

	if variation == 5:
		return hflip(rotate90(m))

	if variation == 6:
		return hflip(rotate90(rotate90(m)))

	if variation == 7:
		return hflip(rotate90(rotate90(rotate90(m))))



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


# Visualization/debugging function
def pretty_print_matrices(matrices):
	for m in matrices:
		pretty_print_matrix(m)

def pretty_print_matrix(m):
	print(f"{int(m[0][0])} | {int(m[0][1])} | {int(m[0][2])}")
	print("----------")
	print(f"{int(m[1][0])} | {int(m[1][1])} | {int(m[1][2])}")
	print("----------")
	print(f"{int(m[2][0])} | {int(m[2][1])} | {int(m[2][2])}")

	print("")
	print("")

def flatten(a):
	return (list(chain.from_iterable(a)))

if __name__ == "__main__":
	c = main()

	print(len(c))

	# b = [[0, 2, 0],
	# 	[2, 1, 2],
	# 	[0, 1, 1]]

	# h, v = hash_board(b)

	# print("Starting board")
	# pretty_print_matrix(b)

	# print()

	# print("Hash")
	# print(f"{h} - {v}")

	# print()

	# print("Standard rotation")
	# pretty_print_matrix(hash_to_board(h))

	# print()

	# print("Original rotation")
	# pretty_print_matrix(hash_to_board(h, v))
