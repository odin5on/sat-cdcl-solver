//
// Created by mddutton on 4/29/24.
//

#ifndef UNTITLED1_ASSIGNMENTS_H
#define UNTITLED1_ASSIGNMENTS_H

#include <iostream>
#include <unordered_map>
#include <optional>
#include <vector>

#include "CommonTypes.h"

class Assignments {
private:
    std::unordered_map<int, Assignment> assignments;
    int decisionLevel = 0;

public:
    bool value(const Literal& literal);
    bool assign(int variable, bool value, const std::optional<Clause>& antecedent);
    void unassign(int variable);
    bool satisfy(const std::vector<Clause>& formula);
    void incrementDecisionLevel();
    void decrementDecisionLevel();
};


#endif //UNTITLED1_ASSIGNMENTS_H
