import time
from boggle_solver import BoggleSolver

#file contents taken from http://www-01.sil.org/linguistics/wordlists/english/ for private use
dictionary_filename = "words.txt"

while True:
	input ("\n\rPress enter to generate a new Boggle Board\n\r")
	init_start = time.time()
	solver = BoggleSolver(4, 4, dictionary_filename)
	init_end = time.time()
	solver.display_board()
	input("\n\rPress enter to show solutions and highest possible scores\n\r")
	
	start = time.time()
	solver.solve()
	end = time.time()
	print ("\n\rTime Elapsed to initialise and read dictionary: ",init_end - init_start)
	print ("Time Elapsed to find solutions: ",end - start)
	print ("Total Time to solve: ",(init_end- init_start)+(end-start))

