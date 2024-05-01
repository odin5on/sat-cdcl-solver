import sys
import random
import time
from cdcl_solver import parse_dimacs_cnf, cdcl_solve

# test commit

if __name__ == "__main__":
    # you might comment it to get inconsistent execution time
    random.seed(5201314)

    start_time = time.time()

    if len(sys.argv) != 2:
        print("Provide one DIMACS cnf filename as argument.")
        sys.exit(1)

    dimacs_cnf = open(sys.argv[1]).read()
    formula = parse_dimacs_cnf(dimacs_cnf)
    result = cdcl_solve(formula)

    total_time = time.time() - start_time

    if result:
        assert result.satisfy(formula)
        print("sat")
        sorted_items = sorted(result.items(), key=lambda x: int(x[0]))
        for var, assignment in sorted_items:
            print(str(var) + " := " + str(assignment.value).lower())
    else:
        print("unsat")

    print(f"Execution time: {total_time:.6f} seconds")  # Print the execution time