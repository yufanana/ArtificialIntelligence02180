#!/usr/bin/env python3

from sympy.logic.boolalg import (
    to_cnf,
    Not,
    And,
    Or,
    Implies,
    Equivalent,
)
import itertools


def disjuncts(clause) -> list:
    """
    Separate the clause by the Or operator. Adapted from
    https://github.com/tdiam/belief-revision-engine.

    Returns:
        list: a list of disjuncts in the given clause.

    Usage:
        disjuncts(A | B | C) -> [A, B, C]
        disjuncts(A | (B & C)) -> [A, B & C]
    """
    return dissociate(Or, [clause])


def conjuncts(clause) -> list:
    """
    Separate the clause by the And operator. Adapted from
    https://github.com/tdiam/belief-revision-engine.

    Returns:
        list: a list of conjuncts in the given clause.

    Usage:
        conjuncts(A & B & C) -> [A, B, C]
    """
    return dissociate(And, [clause])


def dissociate(op, args: list) -> list:
    """
    Separate the arguments of a clause by the given operator.
    Adapted from https://github.com/tdiam/belief-revision-engine.

    Args:
        op (And, Or): the SymPy operator to separate the arguments by
        args (list): the arguments to dissociate

    Returns:
        list: a list of arguments in the given clause

    Usage:
        dissociate(Or, [A | B | C]) -> [A, B, C]
        dissociate(And, [A & B & C]) -> [A, B, C]
        dissociate(Or, [A | B & C]) -> [A, B & C]
    """
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result


def make_clause(args):
    """
    Create a disjunction of clauses from a list of arguments.

    Usage:
        make_clause([A, B, C]) -> A | B | C
        make_clause([A, B & C]) -> A | (B & C)
    """
    args = dissociate(Or, args)
    if len(args) == 0:  # there are no arguments
        return False
    elif len(args) == 1:
        return args[0]
    else:
        return Or(*args)


class BeliefBase:
    def __init__(self) -> None:
        self.beliefs = []
        self.belief_base = []
        self.operations = set([Not, And, Or, Implies, Equivalent])

    def __str__(self) -> str:
        return str(self.belief_base)

    def expand(self, belief: str) -> None:
        """
        Expand the belief base by adding new beliefs as CNF formulas.
        """
        self.beliefs.append(belief)

        # Eliminate bi-implications, assume one bi-imp per belief
        ## Find the bi-imp operator
        imp_op = None
        belief_s = belief.split()
        for i in range(len(belief_s)):
            if belief_s[i] == "<>":
                a = " ".join(belief_s[:i])
                b = " ".join(belief_s[i + 1 :])
                imp_op = belief_s[i]
                break
        ## Add the beliefs to the belief base
        if imp_op is None:  # No bi-imp op found
            self.belief_base.append(to_cnf(belief))
        elif imp_op == "<>":
            imply1 = to_cnf(f"{a} >> {b}")
            imply2 = to_cnf(f"{b} >> {a}")
            self.belief_base.extend([imply1, imply2])
        else:
            raise ValueError("Invalid implication operator")

    def pl_resolution(self, belief_base, alpha) -> bool:
        """
        Checks for entailment using the pl-resolution algorithm
        for clauses resolution.

        Args:
            alpha (sympy.Expr): A SymPy sentence representing the query.

        Returns:
            bool: True if the query is entailed by the knowledge base, False otherwise.
        """
        # Split each clause in the base by the "And" symbol
        KB_clauses = []  # KB as list of disjunctions (CNF form)
        for clause in belief_base:
            KB_clauses += conjuncts(clause)

        # Convert KB & ~alpha to CNF
        alpha_lit = conjuncts(to_cnf(Not(alpha)))  # Add negation of alpha as clause
        # print(f"alpha_lit: {alpha_lit}")
        for clause in alpha_lit:
            KB_clauses.append(clause)

        # Apply resolution rule to resulting clauses
        new_clauses = set()
        while True:
            resolvents = set()
            for ci in KB_clauses:
                for cj in KB_clauses:
                    if ci != cj:
                        resolvents |= self.pl_resolve(ci, cj)
                if any(clause is False for clause in resolvents):  # Empty clause found
                    return True
            if resolvents.issubset(KB_clauses):  # No new clauses derived
                return False

            # Add new clauses to KB
            new_clauses |= resolvents
            KB_clauses.extend(new_clauses)

    def pl_resolve(self, clause1, clause2) -> set:
        """
        Performs the full resolution of two clauses.

        Args:
            clause1 (sympy.Expr): A SymPy sentence representing a clause.
            clause2 (sympy.Expr): A SymPy sentence representing a clause.

        Returns:
            set: a set of resulting clauses from resolution.

        Usage:
            pl_resolve(A | B | C | ~D, ~A | D | E | F) -> {B | C | D | E | F}
        """
        clause1 = disjuncts(clause1)
        clause2 = disjuncts(clause2)
        resolvents = set()

        for ci in clause1:
            for cj in clause2:
                if ci == Not(cj) or cj == Not(ci):
                    # remove ci and cj from resolved clause
                    res = (set(clause1) - {ci}).union(set(clause2) - {cj})
                    resolvents.add(make_clause(res))
        return resolvents

    def contraction_success(self, KB_new, alpha):
        """
        Implements the success postulate for partial_meet_contractionion.

        Args:
            alpha (sympy.Expr): The belief to be removed from the belief base.
        """
        return not self.pl_resolution(KB_new, alpha)

    def contraction_inclusion(self, KB_original, KB_new):
        """
        Implements the inclusion postulate for contraction.

        Args:
            KB_original (list): The original belief base.
            alpha (sympy.Expr): The belief to be removed from the belief base.
        """
        return KB_new.issubset(set(KB_original))

    def contraction_vacuity(self, KB_original, KB_new, alpha):
        """
        Implements the vacuity postulate for contraction.

        Args:
            KB_original (list): The original belief base.
            alpha (sympy.Expr): The belief to be removed from the belief base.
        """
        if not self.pl_resolution(KB_original, alpha):
            return KB_new == KB_original
        return True

    def contraction_extensionality(self, KB_original, alpha, beta):
        """
        Implements the extensionality postulate for contraction.

        Args:
            KB_original (list): The original belief base.
            alpha (sympy.Expr): The belief to be removed from the belief base.
            beta (sympy.Expr): The equivalent belief to be removed from the belief base.
        """
        KB_new_alpha = self.partial_meet_contraction(KB_original, alpha)
        KB_new_beta = self.partial_meet_contraction(KB_original, beta)
        return KB_new_alpha == KB_new_beta

    def agm_contraction_postulates(self, KB_original, KB_new, alpha):
        """
        Implements the AGM postulates for contraction: success,
        inclusion, vacuity, extensionality.

        Args:
            KB_original (list): The original belief base.
            alpha (sympy.Expr): The belief to be removed from the belief base.
        """
        KB_original = set(KB_original)
        KB_new = set(KB_new)
        success = self.contraction_success(KB_new, alpha)
        inclusion = self.contraction_inclusion(KB_original, KB_new)
        vacuity = self.contraction_vacuity(KB_original, KB_new, alpha)
        extensionality = self.contraction_extensionality(KB_original, alpha, alpha)

        print(
            f"Success: {success}, Inclusion: {inclusion}, Vacuity: {vacuity}, Extensionality: {extensionality}",
        )

        if success and inclusion and vacuity and extensionality:
            print("Contraction satisfies AGM postulates.")
            return True
        print("Contraction does not satisfy AGM postulates.")
        return False

    def generate_combinations(self, lst):
        """
        Generate all possible combinations of elements from a list.

        Usage:
            generate_combinations([1, 2, 3]) ->
            [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
        """
        all_combinations = []
        for r in range(1, len(lst) + 1):  # Generate combinations of all lengths
            combinations = itertools.combinations(lst, r)
            all_combinations.extend(combinations)
        return all_combinations

    def partial_meet_contraction(self, kb, p):
        """
        Implements the partial meet contraction for knowlegde bases.

        Args:
            kb (list): The knowledge base.
            p (sympy.Expr): The belief to be removed from the knowledge base.
        """
        subsets = self.generate_combinations(kb)

        # Remove subsets that entails p
        subset_copy = subsets.copy()
        for subset in subset_copy:
            if self.pl_resolution(subset, p):
                subsets.remove(subset)

        subset_set = [set(sub) for sub in subsets]

        # Keep maximal subsets
        subsets_tmp = subset_set.copy()
        for subset in subset_set:
            for subset2 in subset_set:
                if subset.issubset(subset2) and subset != subset2:
                    subsets_tmp.remove(subset)
                    break

        # Select the best subsets
        best_subsets = self.subset_selection(subsets_tmp)
        updated_kb = list(set(best_subsets[0]).intersection(*best_subsets[1:]))
        return updated_kb

    def subset_selection(self, subsets):
        """
        Returns at most 2 of the largest sets contained in "subsets".

        Args:
            subsets (list): The list of subsets.
        """
        max = len(subsets[0])
        best_subsets = []
        for subset in subsets:
            if len(subset) > max and len(subset) < 2:
                max = len(subset)
                best_subsets = [subset]
            elif len(subset) == max:
                best_subsets.append(subset)
        return best_subsets

    def revise(self, belief):
        """
        Implements the belief revision operation by contracting
        inconsistencies with the new belief, checking AGM postulates,
        and expanding the belief base.

        Args:
            belief (sympy.Expr): The belief to be added to the belief base.
        """
        print(f"KB before revision: {self.belief_base}")
        print(f"Belief to be added: {belief}")
        KB_old = self.belief_base.copy()
        self.belief_base = self.partial_meet_contraction(self.belief_base, Not(belief))
        # Check AGM postulates
        self.agm_contraction_postulates(KB_old, self.belief_base, Not(belief))
        self.expand(belief)
        print(f"KB after revision: {self.belief_base} \n")
