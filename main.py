#imports
import random
import string
import copy
import time

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

def get_adjacent_tiles(x,y):
	adjacent_tiles = []
	adjacent_tiles.append((x-1,y))
	adjacent_tiles.append((x-1,y+1))
	adjacent_tiles.append((x-1,y-1))
	adjacent_tiles.append((x,y+1))
	adjacent_tiles.append((x,y-1))
	adjacent_tiles.append((x+1,y))
	adjacent_tiles.append((x+1,y+1))
	adjacent_tiles.append((x+1,y-1))
	new_tiles = []
	for tile in adjacent_tiles:
		#get smallest x/y value
		smallest = min(tile)
		largest = max(tile)
		if smallest>=0 and largest<len(board):
			new_tiles.append(tile)
	return new_tiles

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

def make_prefix_tree(dictionary):
	prefix_tree = {}
	for word in dictionary:
		current_subtree = prefix_tree
		for letter in word:
			#fetch child letter, if there is none then create one
			prefix_entry = current_subtree.get(letter.upper())
			if prefix_entry is None:
				current_subtree[letter.upper()] = {}
				prefix_entry = current_subtree.get(letter.upper())
			current_subtree = prefix_entry
	return prefix_tree

def get_size_of_max_string(array):
	max_size = max(array, key=len)
	return max_size

#function returns all words found based on the current tile as a set
def check_tiles_and_neighbours_for_words(board, dictionary_set, current_string, current_tile, visited, prefix_tree=None):
	#if current string has already been visited - base case to stop checking
	x = current_tile[0]
	y = current_tile[1]
	
	if visited[x][y]==True:
		return set()

	found_words = set()
	prev_letter = current_string[-1]

	#if using a prefix tree, check if any possible words begin with the current word
	if prefix_tree is not None:
		#back trace early if current string is not a prefix of the word to seek
		prefix_subtree = prefix_tree.get(prev_letter)
		if prefix_subtree is None:
			return set()
		#print prev_letter
		if len(prefix_subtree)==0 and len(current_string)>2:
			print current_string
			return set([current_string])
	else:	
		found_words = set([current_string]) if is_a_word(dictionary_set, current_string)==True else set()

	adjacent_tiles = get_adjacent_tiles(x,y)

	visited[x][y]=True
	#get words in neighbouring tiles
	for tile in adjacent_tiles:
		#print tile
		tile_x = tile[0]
		tile_y = tile[1]
		letter = board[tile_x][tile_y]
		new_proposed_string = current_string+letter
		found_words = found_words.union(check_tiles_and_neighbours_for_words(board, dictionary_set, new_proposed_string,tile,copy.deepcopy(visited),prefix_subtree))

	return found_words

#performance - very poor
def naive_implementation(board):
	# to find all possible solutions:
	# 1) iterate over each character as a starting tile
	# 2) with each tile, check if existing current list of characters is  word this empty if starting
	# 3) if the current list of characters is a word, add to found list and add to total points
	# 4) check adjacent vertical/horizontal/diagonal tiles, recursively perform steps 2-4 for all subsequent adjacent tiles 
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

#method as above in the pruned solution, only th
def pruned_implementation(board):
	words = load_dictionary_set()
	prefix_tree = make_prefix_tree(words)

	visited_tiles = {}
	for x in range(0,len(board)):
		visited_tiles[x]={}
		for y in range(0,len(board)):
			visited_tiles[x][y]=False

	for x in range(0,len(board)):
		values = board[x]
		for y in range(0,len(values)):
			current_letter = values[y]
			check_tiles_and_neighbours_for_words(board, words, current_letter, (x,y), copy.deepcopy(visited_tiles),prefix_tree)				

#naive_implementation(board)
board = randomize_new_board()
display_board(board)
start = time.time()
pruned_implementation(board)
end = time.time()
print "Time Elapsed: ",end - start