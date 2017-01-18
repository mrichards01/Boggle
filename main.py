import time
import boggle_solver

#file contents taken from http://www-01.sil.org/linguistics/wordlists/english/ for private use
dictionary_filename = "words.txt"

solver = boggle_solver.BoggleSolver(4, 4, dictionary_filename)
solver.display_board()
# time solution
start = time.time()
solver.solve()
end = time.time()
print ("Time Elapsed: ",end - start)

