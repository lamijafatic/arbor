from pysat.formula import CNF
from pysat.solvers import Solver


class SATResolver:
    def __init__(self, graph):
        self.graph = graph
        self.repo = graph.repo
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

            if not vars_:
                continue

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

                    if valid:
                        # ¬p ∨ (valid options)
                        cnf.append([-var_p] + valid)

  
        for pkg in self.graph.dependencies:
            candidates = self.graph.get_candidates(pkg)

            for v in candidates:
                var_p = self._get_var(pkg, v)

                deps = self.graph.get_dependencies(pkg, v)

                for dep_name, constraint in deps:
                    dep_candidates = self.graph.get_candidates(dep_name)

                    for dv in dep_candidates:
                        if not constraint.is_satisfied_by(dv):
                            var_dep = self._get_var(dep_name, dv)

                            # ¬p ∨ ¬invalid_dep
                            cnf.append([-var_p, -var_dep])

        conflicts = self.repo.get_conflicts()

        for c in conflicts:
            p1, p2 = c

            pkg1, ver1 = p1.split("@")
            pkg2, ver2 = p2.split("@")

            v1 = self._get_var(pkg1, ver1)
            v2 = self._get_var(pkg2, ver2)

            # ¬p1 ∨ ¬p2
            cnf.append([-v1, -v2])

        return cnf

    def solve(self):
        cnf = self.build_cnf()

        with Solver(bootstrap_with=cnf) as solver:
            if not solver.solve():
                raise Exception("No solution found")

            model = solver.get_model()

        solution = {}

        for val in model:
            if val > 0 and val in self.reverse_map:
                pkg, ver = self.reverse_map[val]
                solution[pkg] = ver

        return solution