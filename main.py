#imports
import random
import string
import copy
import time

#setup
max_height = 4
max_width = 4

#file contents taken from http://www-01.sil.org/linguistics/wordlists/english/ for private use
dictionary_filename = "words.txt"

def display_board(board):
	header = "{0} ".format("# "*(max_width+2))
	print (header)

	for row in board:
		current_line ="{0}{1}{2}".format("# "," ".join(row)," #")
		print (current_line)

	footer = "{0} ".format("# "*(max_width+2))
	print (footer)

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
			random_letter = random.choice(string.ascii_lowercase)
			while random_letter in used_chars:
				random_letter = random.choice(string.ascii_lowercase)
				#substitute Q with QU as intended in boggle
			#if random_letter=="q":
			#	random_letter= "qu"
			row_values.append(random_letter)
			used_chars[random_letter]=True
		board.append(row_values)

	return board

#procedure to read from a text file a list of all possible words as a set
def load_dictionary_set():
	dictionary_file = open(dictionary_filename,"r")
	dictionary_string = dictionary_file.read()
	dictionary = set(dictionary_string.split("\n"))
	return dictionary

#method maps all words to a nested dictionary of letters each corresponding prefix to words. Prefixs could be seen
def make_prefix_tree(dictionary):
	prefix_tree = {}
	for word in dictionary:
		current_subtree = prefix_tree
		for letter in word:
			#fetch child letter, if there is none then create one
			prefix_entry = current_subtree.get(letter)
			if prefix_entry is None:
				current_subtree[letter] = {}
				prefix_entry = current_subtree.get(letter)
			current_subtree = prefix_entry
	return prefix_tree

#function returns all words found based on the current tile. Words are returned as a set
def check_tiles_and_neighbours_for_words(board, dictionary_set, current_string, current_tile, visited, prefix_tree=None):
	#if current string has already been visited - base case to stop checking
	x = current_tile[0]
	y = current_tile[1]
	
	if visited[x][y]==True:
		return set()

	found_words = set()
	current_letter = current_string[len(current_string)-1]
	prefix_subtree = None

	#if using a prefix tree, check if any possible words begin with the current word
	if prefix_tree is not None:
		
		prefix_subtree = prefix_tree.get(current_letter)
		#back trace early if current string is not a prefix of the word to seek
		if prefix_subtree is None:
			return set()
		if len(current_string)>2:
			#If the current root is a word then add the word to the set
			if is_a_word(dictionary_set, current_string)==True:
				#print current_string
				found_words.add(current_string)
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

def naive_implementation(board):
	words = load_dictionary_set()
	# to find all possible solutions:
	# 1) iterate over each tile as a starting character
	# 2) with the current tile, check if this tile and subsequent adjacent tiles form any words
	# 3) if the tile has been visited in the chain before, return an empty set 
	# 4) if the current list of characters is a word, add to the found list and add to the total points
	# 5) check adjacent vertical/horizontal/diagonal tiles, recursively perform steps 2-4 for all subsequent adjacent tiles 
	# 	 until no possible word can be found on the current list of characters
	# 6) choose the next tile and repeat 1-5 until all tiles on the board have been checked
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

#method uses backtracing/pruning so that recursive calls are halted when the current string is not a substring of any possible word
def pruned_implementation(board):
	words = load_dictionary_set()
	# to find all possible solutions:
	# 1) iterate over each tile as a starting character
	# 2) with each tile, check if this tile and subsequent adjacent tiles form any words
	# 3) if the tile has been visited in the chain before, return an empty set
	# 4) in check_tiles_and_neighbours_for_words use a prefix tree to determine if the current chain of a string is a valid prefix to any possible word
	# 5) if the current string called in check_tiles_and_neighbours is not a prefix to any posible word then return an empty set. No possible words exist under this prefix.
	# 6) if the current string called in check_tiles_and_neighbours is a prefix and in fact is a real word then add this to found list
	# 7) check adjacent vertical/horizontal/diagonal tiles, recursively perform steps 2-6 for all subsequent adjacent tiles 
	# 	 until no possible word can be found on the current list of characters
	# 8) choose the next tile and repeat 1-7 until all tiles on the board have been checked
	prefix_tree = make_prefix_tree(words)

	visited_tiles = {}
	for x in range(0,len(board)):
		visited_tiles[x]={}
		for y in range(0,len(board)):
			visited_tiles[x][y]=False
	
	all_found = set()
	for x in range(0,len(board)):
		values = board[x]
		for y in range(0,len(values)):
			current_letter = values[y]
			all_found = all_found.union(check_tiles_and_neighbours_for_words(board, words, current_letter, (x,y), copy.deepcopy(visited_tiles),prefix_tree))			
	return all_found

# main code
board = randomize_new_board()
display_board(board)
start = time.time()
solutions = pruned_implementation(board)
end = time.time()
print ("Time Elapsed: ",end - start)
max_score = 0
total_score = 0
for sol in solutions:
	max_score = len(sol) if len(sol)>max_score else max_score
	total_score+=len(sol)
	print (sol)
print ("Total Highest Score: ",total_score)
print ("Highest Scoring word: ",max_score)
	
