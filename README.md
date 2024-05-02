# sat-cdcl-solver
by Daniel Bodin and Matthew Dutton

## Description:

We implemented a SAT solver that implements Conflict-Driven Clause Learning (CDCL). It is largely based off this [Python implementation](https://kienyew.github.io/CDCL-SAT-Solver-from-Scratch/) except we added a Variable State Independent Decaying Sum (VSIDS) heuristic to pick an unassigned variable for the DECIDE decision.

## Requirements:

To run our solver you only need to have python installed. We are using __Python 3.8.5__ and it should work with this and newer. We think it will work with older versions but we do not guarentee.

You will need the [PrettyTable](https://pypi.org/project/prettytable/) library to run testall.py. Follow the link for installation guide.

To run on a specific file run: ```python main.py <original | vsids> <path to file>```.  
The path to file should be a relative path. You can only indicate 'original' or 'vsids' as one of the solvers. If you type it wrong it will give an error and tell you to specify correctly  .
For example if you are in the root directory of this repository you can run ```python main.py original project1-revised-tests/sat/block0.cnf```.

To test all of the files in project1-revised-tests you can run the testall.py file. You would do this by running ```python testall.py <original | vsids> <timoutduration in seconds>```.  
For example to run all of the tests through the vsids solver with a 120 second timeout (If it takes longer than 120 seconds to solve it will give up) you would run ```python testall.py vsids 120```.  
All of the tests are specified as the tests in the project1-revised-tests/sat and project1-revised-tests/unsat directories in this project.

## Credits

This project is largely based off this [Python implementation](https://kienyew.github.io/CDCL-SAT-Solver-from-Scratch/)