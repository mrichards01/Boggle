#imports
import random
import string

##setup
max_height = 4
max_width = 4

def display_board(board):
	header = ""
	for y in range(0,max_width+2):
		header+="# "
	print header

	for row in board:
		current_line ="# "
		for column in row:
			current_line+=column+" "
		current_line+="#"
		print current_line

	footer = ""
	for y in range(0,max_width+2):
		footer+="# "
	print footer

#procedure randomly generates a board to work with
def randomize_new_board():
	board = []
	for row in range(0,max_width):
		row_values = []
		for column in range(0,max_height):
			random_letter = random.choice(string.ascii_uppercase)
			row_values.append(random_letter)
		board.append(row_values)

	return board

board = randomize_new_board()
display_board(board)