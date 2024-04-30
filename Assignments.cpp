//
// Created by mddutton on 4/29/24.
//

#include "Assignments.h"

bool Assignments::value(const Literal &literal) {
    auto it = assignments.find(literal.variable);
    if (it != assignments.end()) {
        return literal.negation == !it->second.value;
    }
    throw std::runtime_error("Variable not found");
}

bool Assignments::assign(int variable, bool value, const std::optional<Clause>& antecedent) {
    // returns true if the insertion took place (the element wasn't already in the unordered map
    // https://en.cppreference.com/w/cpp/container/unordered_map/emplace
    return assignments.try_emplace(variable, value, antecedent, decisionLevel).second;
}

void Assignments::unassign(int variable) {
    assignments.erase(variable);
}

bool Assignments::satisfy(const std::vector<Clause>& formula) {
    for (const auto& clause : formula) {
        bool clauseSatisfied = false;
        for (const auto& lit : clause.literals) {
            if (value(lit)) {
                clauseSatisfied = true;
                break;
            }
        }
        if (!clauseSatisfied) {
            return false;
        }
    }
    return true;
}

void Assignments::incrementDecisionLevel() {
    ++decisionLevel;
}

void Assignments::decrementDecisionLevel() {
    if (decisionLevel > 0) {
        --decisionLevel;
    }
}