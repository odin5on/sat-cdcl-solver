import os
import random
import time
import signal
from prettytable import PrettyTable
from cdcl_solver import parse_dimacs_cnf, cdcl_solve

def handler(signum, frame):
    raise TimeoutError("Timeout")


def run_with_timeout(func, args=(), timeout=1):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)

    try:
        result = func(*args)
    finally:
        signal.alarm(0)
    return result
    

sat_directory = "./project1-revised-tests/sat"
unsat_directory = "./project1-revised-tests/unsat"

sat_table = PrettyTable(["SAT Files", "Result", "Execution Time"])
unsat_table = PrettyTable(["UNSAT Files", "Result", "Execution Time"])

random.seed(5201314)

for file in os.listdir(sat_directory):
    print('starting file: ',file)
    start_time = time.time()

    dimacs_cnf = open(sat_directory + "/" + file).read()
    formula = parse_dimacs_cnf(dimacs_cnf)

    try:
        result = run_with_timeout(cdcl_solve, (formula,), 1)
        duration = time.time() - start_time
    except TimeoutError as e:
        result = "Timeout"
    except Exception as e:
        raise Exception("Error: " + str(e))
    
    if result=="Timeout":
        sat_table.add_row([file, result, ">1sec"])
    else:
        if result:
            assert result.satisfy(formula)
            sat_table.add_row([file, "sat", f"{duration:.6f}"])
        else:
            sat_table.add_row([file, "unsat", f"{duration:.6f}"])
            
    print('finished file',file)

print('moving to unsat tests')

for file in os.listdir(unsat_directory):
    print('starting file: ',file)
    start_time = time.time()

    dimacs_cnf = open(unsat_directory + "/" + file).read()
    formula = parse_dimacs_cnf(dimacs_cnf)
    
    try:
        result = run_with_timeout(cdcl_solve, (formula,), 1)
        duration = time.time() - start_time
    except TimeoutError as e:
        result = "Timeout"
    except Exception as e:
        raise Exception("Error: " + str(e))
    
    if result=="Timeout":
        unsat_table.add_row([file, result, ">1sec"])
    else:
        if result:
            print('result is:',result)
            assert result.satisfy(formula)
            unsat_table.add_row([file, "sat", f"{duration:.6f}"])
        else:
            unsat_table.add_row([file, "unsat", f"{duration:.6f}"])
            
    print('finished file',file)

print(sat_table)
print(unsat_table)
