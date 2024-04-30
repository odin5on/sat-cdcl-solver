//
// Created by mddutton on 4/29/24.
//

#ifndef UNTITLED1_COMMONTYPES_H
#define UNTITLED1_COMMONTYPES_H


#include <utility>
#include <vector>
#include <set>
#include <optional> // NEED C++17 OR NEWER

struct Literal {
    int variable;
    bool negation;

    bool operator==(const Literal& otherLiteral) const {
        return variable == otherLiteral.variable && negation == otherLiteral.negation;
    }

    void negate() { this->negation = not this->negation;}

    Literal(int v, bool n) : variable(v), negation(n) {}

    friend struct std::hash<Literal>;
};

namespace std {
    template <>
    struct hash<Literal> {
        size_t operator()(const Literal& lit) const {
            return std::hash<int>()(lit.variable) ^ (std::hash<bool>()(lit.negation) << 1);
        }
    };
}

struct Clause {
    std::vector<Literal> literals;

    explicit Clause(std::vector<Literal> l) : literals(std::move(l)) {}
};

struct Formula {
    std::vector<Clause> clauses;
    std::set<int> variables;

    explicit Formula(const std::vector<Clause>& clauses) {
        for (const auto& clause : clauses) {
            this->clauses.push_back(clause);
            for (const auto& literal : clause.literals) {
                this->variables.insert(literal.variable);
            }
        }
    }

    Formula(std::vector<Clause> c, std::set<int> v) : clauses(std::move(c)), variables(std::move(v)) {}
};

struct Assignment {
    bool value{};
    std::optional<Clause> antecedent;
    int decisionLevel{};

    Assignment() = default;
    Assignment(bool v, std::optional<Clause> a, int d) : value(v), antecedent(std::move(a)), decisionLevel(d) {}
};


#endif //UNTITLED1_COMMONTYPES_H
