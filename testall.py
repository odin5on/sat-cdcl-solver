import sys
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


def test_files_in_directory(directory, outputtable, timeout):
    for file in os.listdir(directory):
        print("starting file: ", file)
        start_time = time.time()

        dimacs_cnf = open(directory + "/" + file).read()
        formula = parse_dimacs_cnf(dimacs_cnf)

        try:
            result = run_with_timeout(cdcl_solve, (formula,), timeoutduration)
            duration = time.time() - start_time
        except TimeoutError as e:
            result = "Timeout"
        except Exception as e:
            raise Exception("Error: " + str(e))

        if result == "Timeout":
            outputtable.add_row([file, result, ">" + str(timeoutduration) + "sec"])
        else:
            if result:
                assert result.satisfy(formula)
                outputtable.add_row([file, "sat", f"{duration:.6f}"])
            else:
                outputtable.add_row([file, "unsat", f"{duration:.6f}"])

        print("finished file", file)


if len(sys.argv) != 2:
    print("Provide a timeout interval in seconds.")
    sys.exit(1)

timeoutduration = int(sys.argv[1])

sat_directory = "./project1-revised-tests/sat"
unsat_directory = "./project1-revised-tests/unsat"

sat_table = PrettyTable(["SAT Files", "Result", "Execution Time"])
unsat_table = PrettyTable(["UNSAT Files", "Result", "Execution Time"])

random.seed(5201314)

print("SAT TESTS")
test_files_in_directory(sat_directory, sat_table, timeoutduration)

print("UNSAT TESTS")
test_files_in_directory(unsat_directory, unsat_table, timeoutduration)

print(sat_table)
print(unsat_table)
