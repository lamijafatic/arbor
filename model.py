from pysat.formula import CNF
from pysat.solvers import Solver


class SATResolver:
    def __init__(self, graph):
        self.graph = graph
        self.var_map = {}
        self.reverse_map = {}
        self.counter = 1

    def _get_var(self, package, version):
        key = (package, str(version))

        if key not in self.var_map:
            self.var_map[key] = self.counter
            self.reverse_map[self.counter] = key
            self.counter += 1

        return self.var_map[key]

    def build_cnf(self):
        cnf = CNF()

        for pkg in self.graph.dependencies:
            candidates = self.graph.get_candidates(pkg)

            vars_ = [self._get_var(pkg, v) for v in candidates]

            # at least one
            cnf.append(vars_)

            # at most one
            for i in range(len(vars_)):
                for j in range(i + 1, len(vars_)):
                    cnf.append([-vars_[i], -vars_[j]])

     
        for pkg in self.graph.dependencies:
            candidates = self.graph.get_candidates(pkg)

            for v in candidates:
                var_p = self._get_var(pkg, v)

                deps = self.graph.get_dependencies(pkg, v)

                for dep_name, constraint in deps:
                    dep_candidates = self.graph.get_candidates(dep_name)

                    valid = [
                        self._get_var(dep_name, dv)
                        for dv in dep_candidates
                        if constraint.is_satisfied_by(dv)
                    ]

                    # ¬p ∨ (d1 ∨ d2 ...)
                    clause = [-var_p] + valid
                    cnf.append(clause)

        return cnf

    def solve(self):
        cnf = self.build_cnf()

        with Solver(bootstrap_with=cnf) as solver:
            if not solver.solve():
                raise Exception("No solution")

            model = solver.get_model()

        solution = {}

        for val in model:
            if val > 0 and val in self.reverse_map:
                pkg, ver = self.reverse_map[val]
                solution[pkg] = ver

        return solution