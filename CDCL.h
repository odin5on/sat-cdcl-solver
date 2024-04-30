//
// Created by mddutton on 4/29/24.
//

#ifndef UNTITLED1_CDCL_H
#define UNTITLED1_CDCL_H

#include "CommonTypes.h"
#include "Assignments.h"

class CDCL {
public:
    Assignment CDCL_Solve(const Formula &formula);
    std::pair<int, std::optional<Clause>> unit_propagation(Assignments *assignments,
                                                           std::unordered_map<Literal, std::vector<const Clause*>> lit2clauses,
                                                           std::unordered_map<const Clause*, std::vector<Literal>> clause2lits,
                                                           std::vector<Literal*> to_propagate);
};


#endif //UNTITLED1_CDCL_H
