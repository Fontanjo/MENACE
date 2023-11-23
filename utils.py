import numpy as np
from itertools import chain

# Store list of matrice outside hash function, to avoid regenerating it every time
list_of_h_matrices = None


# Generate a specific variation of the matrix, from those considered equivalent for this situation
def variate_matrix(m, variation):
	assert variation in range(8), f"Variation should be between 0 and 7, got {variation}"
	
	# Function to rotate the 2D matrix by 90 degrees clockwise
	rotate90 = lambda x: list(zip(*x[::-1]))

	# Function to horizontally flip a matrix
	hflip = lambda x: np.flip(x, 1)


	if variation == 0:
		res = m

	if variation == 1:
		res = rotate90(m)

	if variation == 2:
		res = rotate90(rotate90(m))

	if variation == 3:
		res = rotate90(rotate90(rotate90(m)))

	if variation == 4:
		res = hflip(m)

	if variation == 5:
		res = hflip(rotate90(m))

	if variation == 6:
		res = hflip(rotate90(rotate90(m)))

	if variation == 7:
		res = hflip(rotate90(rotate90(rotate90(m))))

	return res


def flatten(a):
	return (list(chain.from_iterable(a)))

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