//
// Created by mddutton on 4/29/24.
//

#include <unordered_map>
#include <vector>
#include <memory>

#include "CDCL.h"

std::pair<int, std::optional<Clause>> CDCL::unit_propagation(Assignments *assignments,
                                                             std::unordered_map<Literal, std::vector<const Clause*>> lit2clauses,
                                                             std::unordered_map<const Clause*, std::vector<Literal>> clause2lits,
                                                             std::vector<Literal*> to_propagate){
    while(!to_propagate.empty()) {
        to_propagate.back()->negate();
        const Literal *watching_lit = to_propagate.back();
        to_propagate.pop_back();

        // make a copy to avoid problems with the watching_lit clauses changing mid-for loop
        std::vector<const Clause*> tempWatchingClauses = lit2clauses.at(*watching_lit);
        for (auto& watching_clause : tempWatchingClauses) {
            for (auto& lit : watching_clause->literals) {
                // TODO Left off here
            }
        }
    }
}

Assignment CDCL::CDCL_Solve(const Formula& formula) {
    // auto assignments = std::make_unique<Assignment>();
    Assignments *assignments;


    std::unordered_map<Literal, std::vector<const Clause*>> lit2clauses; // C++ shenanigans
    std::unordered_map<const Clause*, std::vector<Literal>> clause2lits; // https://stackoverflow.com/questions/52734630/no-matching-member-function-for-call-to-push-back-error
    std::vector<const Clause*> unit_clauses;
    std::vector<Literal*> to_propagate;

    for (const Clause& clause : formula.clauses) {
        if (clause.literals.size() == 1) {
            lit2clauses[clause.literals[0]].push_back(&clause);
            clause2lits[&clause].push_back(clause.literals[0]);

            unit_clauses.push_back(&clause);
        } else {
            lit2clauses[clause.literals[0]].push_back(&clause);
            lit2clauses[clause.literals[1]].push_back(&clause);
            clause2lits[&clause].push_back(clause.literals[0]);
            clause2lits[&clause].push_back(clause.literals[1]);
        }
    }

    for (const Clause* unit_clause : unit_clauses) {
        Literal literal = unit_clause->literals[0];
        int var = literal.variable;
        bool val = not literal.negation;
        bool inserted = assignments->assign(var, val, std::optional<Clause>(*unit_clause));

        if (inserted) {
            to_propagate.push_back(&literal);
        }
    }

    // UNIT PROPAGATION

}
