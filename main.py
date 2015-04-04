#imports
import random
import string

##setup
max_height = 4
max_width = 4

#file contents taken from http://www-01.sil.org/linguistics/wordlists/english/ for private use
dictionary_filename = "words.txt"

def display_board(board):
	header = ""
	for y in range(0,max_width+2):
		header+="# "
	print header

	for row in board:
		current_line ="# "
		for column_value in row:
			current_line+=column_value+" "
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

#procedure to read from a text file a list of all possible words
def load_dictionary():
	dictionary_file = open(dictionary_filename,"r")
	dictionary_string = dictionary_file.read()
	dictionary = dictionary_string.split("\n")
	return dictionary

def check_adjacent_tiles_for_words(board, current_string, x_pos, y_pos):


board = randomize_new_board()
display_board(board)
words = load_dictionary()
# to find all possible solutions:
# 1) iterate over each character as a starting tile
# 2) with each tile, check if existing current list of characters is  word this empty if starting
# 3) if the current list of characters is a word, add to found list and add to total points
# 4) check adjacent vertical/horizontal/diagonal tiles, recursively perform 2-4 for all subsequent adjacent tiles 
# until no possible word can be found on the current list of chracters
# 5) Choose the next tile and 1-4 until all tiles have been checked

for x in range(0,len(board)):
	values = board[x]
	for y in range(0,len(y_values)):
		current_letter = values[y]
		check_adjacent_files_for_words(board, current_letter,x,y)
