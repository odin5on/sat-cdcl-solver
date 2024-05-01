import random
from typing import List, Tuple, Optional
from common_classes import Literal, Clause, Formula, Assignment

class Assignments(dict):
    """
    The assignments, also stores the current decision level.
    """

    def __init__(self):
        super().__init__()

        # the decision level
        self.dl = 0

    def value(self, literal: Literal) -> bool:
        """
        Return the value of the literal with respect the current assignments.
        """
        if literal.negation:
            return not self[literal.variable].value
        else:
            return self[literal.variable].value

    def assign(self, variable: int, value: bool, antecedent: Optional[Clause]):
        self[variable] = Assignment(value, antecedent, self.dl)

    def unassign(self, variable: int):
        self.pop(variable)

    def satisfy(self, formula: Formula) -> bool:
        """
        Check whether the assignments actually satisfies the formula.
        """
        for clause in formula:
            if True not in [self.value(lit) for lit in clause]:
                return False

        return True
    
# class VSIDS:
#     def __init__(self):
#         self.scores = {}
#         self.decay_factor = 0.95

#     def initialize_scores(self, variables):
#         for var in variables:
#             self.scores[var] = 0

#     def increment_score(self, clause):
#         for var in clause:
#             if var in self.scores:
#                 self.scores[var] += 1
#             else:
#                 self.scores[var] = 1

#     def decay_scores(self):
#         for var in self.scores:
#             self.scores[var] *= self.decay_factor

#     def get_best_variable(self):
#         return max(self.scores, key=self.scores.get)

# import heapq

# class VSIDS:
#     def __init__(self):
#         self.scores = {}
#         self.heap = []
#         self.decay_factor = 0.95
#         self.invalidated = set()

#     def initialize_scores(self, variables):
#         for var in variables:
#             self.scores[var] = 0
#             heapq.heappush(self.heap, (-self.scores[var], var))

#     def increment_score(self, clause):
#         for var in clause:
#             if var in self.scores:
#                 self.scores[var] += 1
#                 # Since we cannot directly increase a key in the heap, push the new score
#                 heapq.heappush(self.heap, (-self.scores[var], var))
#                 # Track invalidated entries
#                 self.invalidated.add((self.scores[var] - 1, var))

#     def decay_scores(self):
#         # Apply decay to scores
#         new_heap = []
#         for var, score in self.scores.items():
#             new_score = score * self.decay_factor
#             self.scores[var] = new_score
#             heapq.heappush(new_heap, (-new_score, var))
#         self.heap = new_heap
#         self.invalidated.clear()

#     def get_best_variable(self):
#         # Pop until you find a valid entry
#         while self.heap:
#             score, var = heapq.heappop(self.heap)
#             if (-score, var) not in self.invalidated:
#                 # Return the first valid variable found
#                 return var
#         return None  # In case all entries are invalidated

import heapq

class VSIDS:
    def __init__(self):
        self.scores = {}
        self.heap = []
        self.conflict_count = 0
        self.decay_interval = 256  # Perform decay every 256 conflicts

    def initialize_scores(self, variables):
        for var in variables:
            self.scores[var] = 0
            heapq.heappush(self.heap, (-self.scores[var], var))

    def increment_score(self, clause):
        for var in clause:
            if var in self.scores:
                self.scores[var] += 1
                # Update the heap with the new score
                heapq.heappush(self.heap, (-self.scores[var], var))

    def maybe_decay_scores(self):
        self.conflict_count += 1
        if self.conflict_count >= self.decay_interval:
            self.decay_scores()
            self.conflict_count = 0  # Reset conflict counter after decay

    def decay_scores(self):
        # Halve scores and rebuild the heap
        new_heap = []
        for var, score in self.scores.items():
            new_score = score / 2
            self.scores[var] = new_score
            heapq.heappush(new_heap, (-new_score, var))
        self.heap = new_heap

    def get_best_variable(self):
        # Pop from the heap until a valid entry is found
        while self.heap:
            score, var = heapq.heappop(self.heap)
            if -score == self.scores[var]:  # Check if the entry is still valid
                return var
        return None

    
from collections import defaultdict
def init_watches(formula: Formula):
    """
    Return lit2clauses and clause2lits
    """
    
    lit2clauses = defaultdict(list)
    clause2lits = defaultdict(list)
    
    for clause in formula:
        if len(clause) == 1:
            # For unit clause, we watch the only literal
            lit2clauses[clause.literals[0]].append(clause)
            clause2lits[clause].append(clause.literals[0])
        elif len(clause) > 1:
            # For other clause, we choose any 2 literals to watch
            lit2clauses[clause.literals[0]].append(clause)
            lit2clauses[clause.literals[1]].append(clause)
            clause2lits[clause].append(clause.literals[0])
            clause2lits[clause].append(clause.literals[1])
            
    return lit2clauses, clause2lits



def cdcl_solve(formula: Formula) -> Optional[Assignments]:
    """
    Solve the CNF formula.

    If SAT, return the assignments.
    If UNSAT, return None.
    """
    assignments = Assignments()
    lit2clauses, clause2lits = init_watches(formula)

    # Initialize VSIDS with all variables in the formula
    vsids = VSIDS()
    vsids.initialize_scores(formula.variables())
    
    # First, do unit propagation to assign the initial unit clauses 
    unit_clauses = [clause for clause in formula if len(clause) == 1]
    to_propagate = []
    for clause in unit_clauses:
        lit = clause.literals[0]
        var = lit.variable
        val = not lit.negation
        if var not in assignments:
            assignments.assign(var, val, clause)
            to_propagate.append(lit)
    
    reason, clause = unit_propagation(assignments, lit2clauses, clause2lits, to_propagate)
    if reason == 'conflict':
        return None

    conflict_count = 0
    decay_interval = 256 # TODO can change based on accuracy

    while not all_variables_assigned(formula, assignments):
        var, val = pick_branching_variable(formula, assignments, vsids)
        if var is None:
            break
        assignments.dl += 1
        assignments.assign(var, val, antecedent=None)
        to_propagate = [Literal(var, not val)]
        
        while True:
            reason, clause = unit_propagation(assignments, lit2clauses, clause2lits, to_propagate)
            #i+=1
            #print("unit propagation #" + str(i))

            if reason != 'conflict':
                # no conflict after unit propagation, we back
                # to the decision (guessing) step
                break
                
            b, learnt_clause = conflict_analysis(clause, assignments)
            if b < 0:
                return None
            
            add_learnt_clause(formula, learnt_clause, assignments, lit2clauses, clause2lits, vsids)
            backtrack(assignments, b)
            assignments.dl = b

            # The learnt clause must be a unit clause, so the
            # next step must again be unit progagation
            literal = next(literal for literal in learnt_clause if literal.variable not in assignments)
            var = literal.variable
            val = not literal.negation
            assignments.assign(var, val, antecedent=learnt_clause)
            to_propagate = [Literal(var, not val)]

            if conflict_count % decay_interval == 0:
                vsids.decay_scores()  # Periodically decay scores

    return assignments



def add_learnt_clause(formula, clause, assignments, lit2clauses, clause2lits, vsids: VSIDS):
    formula.clauses.append(clause)
    vsids.increment_score(clause)  # Update VSIDS scores based on the new learnt clause
    vsids.maybe_decay_scores()
    # for lit in sorted(clause, key=lambda lit: -assignments[lit.variable].dl):
    #     if len(clause2lits[clause]) < 2:
    #         clause2lits[clause].append(lit)
    #         lit2clauses[lit].append(clause)
    #     else:
    #         break
    for lit in sorted(clause, key=lambda lit: -assignments[lit.variable].dl if lit.variable in assignments else float('inf')):
        if len(clause2lits[clause]) < 2:
            clause2lits[clause].append(lit)
            lit2clauses[lit].append(clause)
        else:
            break




def all_variables_assigned(formula: Formula, assignments: Assignments) -> bool:
    return len(formula.variables()) == len(assignments)



def pick_branching_variable(formula: Formula, assignments: Assignments, vsids: VSIDS) -> Tuple[int, bool]:
    unassigned_vars = [var for var in formula.variables() if var not in assignments]
    if unassigned_vars:
        var = vsids.get_best_variable()  # Use VSIDS to get the best variable
        val = random.choice([True, False])  # Choose a value randomly or based on some heuristic
        return var, val
    return None



def backtrack(assignments: Assignments, b: int):
    to_remove = []
    for var, assignment in assignments.items():
        if assignment.dl > b:
            to_remove.append(var)

    for var in to_remove:
        assignments.pop(var)


def clause_status(clause: Clause, assignments: Assignments) -> str:
    """
    Return the status of the clause with respect to the assignments.

    There are 4 possible status of a clause:
      1. Unit - All but one literal are assigned False
      2. Unsatisfied - All literals are assigned False
      3. Satisfied - All literals are assigned True
      4. Unresolved - Neither unit, satisfied nor unsatisfied
    """
    values = []
    for literal in clause:
        if literal.variable not in assignments:
            values.append(None)
        else:
            values.append(assignments.value(literal))

    if True in values:
        return "satisfied"
    elif values.count(False) == len(values):
        return "unsatisfied"
    elif values.count(False) == len(values) - 1:
        return "unit"
    else:
        return "unresolved"


def unit_propagation(assignments, lit2clauses, clause2lits, to_propagate: List[Literal]) -> Tuple[str, Optional[Clause]]:
    #print("\nUNIT PROPAGATION\n");
    while len(to_propagate) > 0:
        # print("to_propagate length: " + str(len(to_propagate)))
        watching_lit = to_propagate.pop().neg()

        # use list(.) to copy it because size of 
        # lit2clauses[watching_lit]might change during for-loop
        watching_clauses = list(lit2clauses[watching_lit])
        for watching_clause in watching_clauses:
            for lit in watching_clause:
                if lit in clause2lits[watching_clause]:
                    # lit is another watching literal of watching_clause
                    continue
                elif lit.variable in assignments and assignments.value(lit) == False:
                    # lit is a assigned False
                    continue
                else:
                    # lit is not another watching literal of watching_clause
                    # and is non-False literal, so we rewatch it. (case 1)
                    clause2lits[watching_clause].remove(watching_lit)
                    clause2lits[watching_clause].append(lit)
                    lit2clauses[watching_lit].remove(watching_clause)
                    lit2clauses[lit].append(watching_clause)
                    break
            else:
                # we cannot find another literal to rewatch (case 2,3,4)
                watching_lits = clause2lits[watching_clause]
                if len(watching_lits) == 1:
                    # watching_clause is unit clause, and the only literal
                    # is assigned False, thus indicates a conflict
                    return ('conflict', watching_clause)
               	
                # the other watching literal
                other = watching_lits[0] if watching_lits[1] == watching_lit else watching_lits[1]
                if other.variable not in assignments:
                    # the other watching literal is unassigned. (case 3)
                    assignments.assign(other.variable, not other.negation, watching_clause)
                    to_propagate.insert(0, other)
                elif assignments.value(other) == True:
                    # the other watching literal is assigned True. (case 2)
                    continue
                else:
                    # the other watching literal is assigned False. (case 4)
                    return ('conflict', watching_clause)

    return ('unresolved', None)



def resolve(a: Clause, b: Clause, x: int) -> Clause:
    """
    The resolution operation
    """
    result = set(a.literals + b.literals) - {Literal(x, True), Literal(x, False)} # TODO this takes a while
    result = list(result)
    return Clause(result)


def conflict_analysis(clause: Clause, assignments: Assignments) -> Tuple[int, Clause]:
    if assignments.dl == 0:
        return (-1, None)

    # literals with current decision level
    literals = [
        literal
        for literal in clause
        if assignments[literal.variable].dl == assignments.dl
    ]
    while len(literals) != 1:
        # implied literals
        literals = filter(
            lambda lit: assignments[lit.variable].antecedent != None, literals
        )

        # select any literal that meets the criterion
        literal = next(literals)
        antecedent = assignments[literal.variable].antecedent
        clause = resolve(clause, antecedent, literal.variable)

        # literals with current decision level
        literals = [
            literal
            for literal in clause
            if literal.variable in assignments and assignments[literal.variable].dl == assignments.dl #TODO takes time
        ]

    # out of the loop, `clause` is now the new learnt clause
    # compute the backtrack level b (second largest decision level)
    # decision_levels = sorted(
    #     set(assignments[literal.variable].dl for literal in clause)
    # )

    decision_levels = {
        assignments[literal.variable].dl
        for literal in clause
        if literal.variable in assignments
    }

    # if len(decision_levels) <= 1:
    #     return 0, clause
    # else:
    #     return decision_levels[-2], clause

    if len(decision_levels) <= 1:
        return 0, clause  # Or handle the case where there's less than two decision levels
    else:
        sorted_decision_levels = sorted(decision_levels, reverse=True)
        if len(sorted_decision_levels) > 1:
            return sorted_decision_levels[1], clause  # Access the second largest decision level
        else:
            return sorted_decision_levels[0], clause  # Fallback if there's only one unique decision level



def parse_dimacs_cnf(content: str) -> Formula:
    """
    parse the DIMACS cnf file format into corresponding Formula.
    """
    clauses = [Clause([])]
    for line in content.splitlines():
        tokens = line.split()
        if ((len(tokens) != 0 and tokens[0] not in ("p", "c")) and
                (len(tokens[0]) != 0 and tokens[0][0] != "c")):
            for tok in tokens:
                lit = int(tok)
                if lit == 0:
                    clauses.append(Clause([]))
                else:
                    var = abs(lit)
                    neg = lit < 0
                    clauses[-1].literals.append(Literal(var, neg))

    if len(clauses[-1]) == 0:
        clauses.pop()

    return Formula(clauses)
