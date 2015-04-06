#imports
import random
import string
import copy
##setup
max_height = 4
max_width = 4

#file contents taken from http://www-01.sil.org/linguistics/wordlists/english/ for private use
dictionary_filename = "words.txt"

def display_board(board):
	header = ""
	for x in range(0,max_width+2):
		header+="# "
	print header

	for row in board:
		current_line ="# "
		for value in row:
			current_line+=value+" "
		current_line+="#"
		print current_line

	footer = ""
	for x in range(0,max_width+2):
		footer+="# "
	print footer

def is_a_word(dictionary_set, word):
	return True if check_word_score(dictionary_set,word)>0 else False

#check if proposed word is a word, and return an applicable score based on length
def check_word_score(dictionary_set, word):
	if word in dictionary_set:
		return len(word)
	return 0

#procedure randomly generates a board to work with
def randomize_new_board():
	board = []
	used_chars = {}
	for column in range(0,max_width):
		row_values = []
		for row in range(0,max_height):
			random_letter = random.choice(string.ascii_uppercase)
			while random_letter in used_chars:
				random_letter = random.choice(string.ascii_uppercase)
				if random_letter=="Q":
					random_letter= "QU"
			row_values.append(random_letter)
			used_chars[random_letter]=True
		board.append(row_values)

	return board

#procedure to read from a text file a list of all possible words
def load_dictionary_set():
	dictionary_file = open(dictionary_filename,"r")
	dictionary_string = dictionary_file.read()
	dictionary = set(dictionary_string.split("\n"))
	return dictionary

#function returns all words found based on the current tile as a set
def check_tiles_and_neighbours_for_words(board, dictionary_set, current_string, current_tile, visited):
	#if current string has already been visited - base case to stop checking
	x = current_tile[0]
	y = current_tile[1]
	
	if visited[x][y]==True:
		return set()

	found_words = set([current_string]) if is_a_word(dictionary_set, current_string)==True else set()
	# check neighbours if within bounds

	adjacent_tiles = []
	adjacent_tiles.append((x-1,y))
	adjacent_tiles.append((x-1,y+1))
	adjacent_tiles.append((x-1,y-1))
	adjacent_tiles.append((x,y+1))
	adjacent_tiles.append((x,y-1))
	adjacent_tiles.append((x+1,y))
	adjacent_tiles.append((x+1,y+1))
	adjacent_tiles.append((x+1,y-1))

	visited[x][y]=True
	#get words in neighbouring tiles
	for tile in adjacent_tiles:
		#get smallest x/y value
		smallest = min(tile)
		largest = max(tile)
		if smallest>=0 and largest<len(board):
			#print tile
			tile_x = tile[0]
			tile_y = tile[1]
			letter = board[tile_x][tile_y]
			new_proposed_string = current_string+letter
			#print new_proposed_string
			found_words = found_words.union(check_tiles_and_neighbours_for_words(board, dictionary_set, new_proposed_string,tile,copy.deepcopy(visited)))
			if len(found_words)>0:
				print found_words
	return found_words

def naive_implementation(board,dictionary_set):
		# to find all possible solutions:
	# 1) iterate over each character as a starting tile
	# 2) with each tile, check if existing current list of characters is  word this empty if starting
	# 3) if the current list of characters is a word, add to found list and add to total points
	# 4) check adjacent vertical/horizontal/diagonal tiles, recursively perform 2-4 for all subsequent adjacent tiles 
	# until no possible word can be found on the current list of chracters
	# 5) Choose the next tile and 1-4 until all tiles have been checked
	words = load_dictionary_set()

	visited_tiles = {}
	for x in range(0,len(board)):
		visited_tiles[x]={}
		for y in range(0,len(board)):
			visited_tiles[x][y]=False
	for x in range(0,len(board)):
		values = board[x]
		
		for y in range(0,len(values)):
			current_letter = values[y]
			check_tiles_and_neighbours_for_words(board, words, current_letter,(x,y), copy.deepcopy(visited_tiles))

board = randomize_new_board()
display_board(board)
#
#initialise visited tiles
naive_implementation(board)