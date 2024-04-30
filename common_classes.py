from dataclasses import dataclass
from typing import Iterator, List, Optional, Set

# frozen to be hashable
@dataclass(frozen=True)
class Literal:
    variable: int
    negation: bool

    def __repr__(self):
        if self.negation:
            return "¬" + str(self.variable)
        else:
            return str(self.variable)

    def neg(self) -> "Literal":
        """
        Return the negation of this literal.
        """
        return Literal(self.variable, not self.negation)


@dataclass
class Clause:
    literals: List[Literal]

    def __repr__(self):
        return '∨'.join(map(str, self.literals))

    def __iter__(self) -> Iterator[Literal]:
        return iter(self.literals)

    def __len__(self):
        return len(self.literals)

    def __hash__(self):
        x = 0 
        for lit in self.literals:
            x ^= hash(lit)
        return x



@dataclass
class Formula:
    clauses: List[Clause]
    __variables: Set[int]

    def __init__(self, clauses: List[Clause]):
        """
        Remove duplicate literals in clauses.
        """
        self.clauses = []
        self.__variables = set()
        for clause in clauses:
            self.clauses.append(Clause(list(set(clause))))
            for lit in clause:
                var = lit.variable
                self.__variables.add(var)

    def variables(self) -> Set[int]:
        """
        Return the set of variables contained in this formula.
        """
        return self.__variables

    def __repr__(self):
        return " ∧ ".join(f"({clause})" for clause in self.clauses)

    def __iter__(self) -> Iterator[Clause]:
        return iter(self.clauses)

    def __len__(self):
        return len(self.clauses)


@dataclass
class Assignment:
    value: bool
    antecedent: Optional[Clause]
    dl: int  # decision level