import random
import string
import copy

class BoggleSolver:

	def __init__(self, height, width, word_file):
		self._height = height
		self._width = width
		if not isinstance(word_file, str):
			raise TypeEror("word_file arguement must be specified as a string")
		try:
			self._words = self.load_dictionary_set(word_file)
		except IOError:
			raise 
		self.board = []
		self._letters_on_board = self.init_new_board()

	def display_board(self):
		header = "{0} ".format("# "*(self._width+2))
		print (header)

		for row in self._board:
			current_line ="{0}{1}{2}".format("# "," ".join(row)," #")
			print (current_line)

		footer = "{0} ".format("# "*(self._height+2))
		print (footer)
	
	def solve(self):
		solutions = self.pruned_implementation()
		max_score = 0
		total_score = 0
		for sol in solutions:
			max_score = len(sol) if len(sol)>max_score else max_score
			total_score+=len(sol)
			print (sol)
		print ("Total Highest Score: ",total_score)
		print ("Highest Scoring word: ",max_score)

	#procedure to read from a text file a list of all possible words as a set
	def load_dictionary_set(self, filename):
		dictionary_file = open(filename, "r")
		dictionary_string = dictionary_file.read()
		dictionary = set(dictionary_string.split("\n"))
		return dictionary

	#method maps all words to a nested dictionary of letters.
	#each key maps to a letter at any given position in the current word
	def make_prefix_tree(self, dictionary):
		prefix_tree = {}
		for word in dictionary:
			current_subtree = prefix_tree
			for letter in word:
				# if letter cannot be found on the board, do not add anymore
				if letter not in self._letters_on_board:
					break

				#fetch child letter, if there is none then create one
				if letter not in current_subtree:
					current_subtree[letter] = {}

				# traverse tree for each letter
				current_subtree = current_subtree[letter]
		return prefix_tree

	def is_a_word(self, word):
		return True if self.check_word_score(word)>0 else False

	#function returns all words found based on the current tile. Words are returned as a set
	def check_tiles_and_neighbours_for_words(self, current_string, current_tile, visited, prefix_tree):
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
			
			# back trace early if current string is not a prefix of the word to seek
			if current_letter not in prefix_tree:
				return set()
			prefix_subtree = prefix_tree[current_letter]

			if len(current_string)>2:
				#If the current root is a word then add the word to the set
				if self.is_a_word(current_string)==True:
					found_words.add(current_string)
		else:
			# otherwise simpy add to the found words if this is a word
			found_words = set([current_string]) if self.is_a_word(current_string)==True else set()

		adjacent_tiles = self.get_adjacent_tiles(x,y)

		visited[x][y]=True
		# get any words in neighbouring tiles
		for tile in adjacent_tiles:
			tile_x = tile[0]
			tile_y = tile[1]
			letter = self._board[tile_x][tile_y]
			new_proposed_string = "{}{}".format(current_string, letter)
			# union current words found and those found in any neighbours
			found_words = found_words.union(self.check_tiles_and_neighbours_for_words(new_proposed_string, tile, copy.deepcopy(visited), prefix_subtree))

		return found_words

	#check if proposed word is a word, and return an applicable score based on length
	def check_word_score(self, word):
		if word in self._words:
			return len(word)
		return 0

	def get_adjacent_tiles(self,x,y):
		adjacent_tiles = []
		for i in range (x-1,x+2):
			for j in range (y-1,y+2):
				if i==x and j==y:
					continue
				if i<0 or j<0:
					continue
				if i>=self._width or j>=self._height:
					continue
				adjacent_tiles.append((i,j))
		return adjacent_tiles

	#procedure randomly generates a board to work with
	def init_new_board(self):
		self._board = []
		used_chars = set()
		for x in range(0,self._width):
			values = []
			for y in range(0,self._height):
				random_letter = random.choice(string.ascii_lowercase)
				while random_letter in used_chars:
					random_letter = random.choice(string.ascii_lowercase)
				# boggle normally substitutes q with qu. This implementation ignores this.
				values.append(random_letter)
				used_chars.add(random_letter)
			self._board.append(values)

		return used_chars

	def naive_implementation(self):
		# brute force all letters 
		visited_tiles = {}
		for x in range(0,len(self._board)):
			visited_tiles[x]={}
			for y in range(0,len(self._board)):
				visited_tiles[x][y]=False

		for x in range(0,len(board)):
			values = board[x]
			
			for y in range(0,len(values)):
				current_letter = values[y]
				self.check_tiles_and_neighbours_for_words(current_letter, (x,y), copy.deepcopy(visited_tiles), None)

	#method uses backtracing/pruning so that recursive calls are halted when the current string is not a substring of any possible word
	def pruned_implementation(self):
		prefix_tree = self.make_prefix_tree(self._words)

		visited_tiles = {}
		for x in range(0,len(self._board)):
			visited_tiles[x] = {}
			for y in range(0,len(self._board)):
				visited_tiles[x][y]=False
		
		all_found = set()
		for x in range(0,len(self._board)):
			values = self._board[x]
			for y in range(0,len(values)):
				current_letter = values[y]
				all_found = all_found.union(self.check_tiles_and_neighbours_for_words(current_letter, (x,y), copy.deepcopy(visited_tiles), prefix_tree))
		return all_found