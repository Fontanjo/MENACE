# Player 1 uses crosses, player 2 uses circles
# Define constants for readability
EMPTY = 0
CROSS = 1
CIRCLE = 2


def cross_win(board):
	# Not most compact way, but make it readable
	for i in range(3):
		if board[i][0] == CROSS and board[i][1] == CROSS and board[i][2] == CROSS:
			return True

	for j in range(3):
		if board[0][j] == CROSS and board[1][j] == CROSS and board[2][j] == CROSS: 
			return True

	if board[0][0] == CROSS and board[1][1] == CROSS and board[2][2] == CROSS:
		return True

	if board[0][2] == CROSS and board[1][1] == CROSS and board[2][0] == CROSS:
		return True
	
	return False


def circle_win(board):
	# Not most compact way, but make it readable
	for i in range(3):
		if board[i][0] == CIRCLE and board[i][1] == CIRCLE and board[i][2] == CIRCLE:
			return True

	for j in range(3):
		if board[0][j] == CIRCLE and board[1][j] == CIRCLE and board[2][j] == CIRCLE: 
			return True

	if board[0][0] == CIRCLE and board[1][1] == CIRCLE and board[2][2] == CIRCLE:
		return True

	if board[0][2] == CIRCLE and board[1][1] == CIRCLE and board[2][0] == CIRCLE:
		return True
	
	return False


def draw(board):
	return not win(board) and full_board(board)


def full_board(board):
	# Check if there are playable positions (0s)
	for i in range(3):
		for j in range(3):
			if board[i][j] == 0:
				return False
	
	return True


def win(board):
	return cross_win(board) or circle_win(board)