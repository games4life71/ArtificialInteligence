from ArtificialInteligence.lab4 import sudokuState as ss
import os

INSTANCE_FILE_NAME = "instance_hard"
SOLUTION_FILE_NAME = "instance_hard_solved"

os.chdir("D:\Projects\AI\ArtificialInteligence\lab4")

ss.generate_instance(INSTANCE_FILE_NAME, SOLUTION_FILE_NAME)
print("Initial table:")
ss.printTable(ss.TABLE)
ss.init_domains(ss.TABLE)

my_solution = ss.backtracking_with_forward_checkMRV(ss.TABLE, ss.domains)
print("Solution:")
ss.printTable(my_solution)
ss.import_solution(SOLUTION_FILE_NAME)
print(ss.compare_tables(my_solution, ss.SOLUTION))
