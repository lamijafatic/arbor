from domain.models.dependency import Dependency
from domain.models.graph import DependencyGraph
from domain.models.constraint import Constraint
from domain.models.version import Version


def parse_dep(dep_str):
    import re
    match = re.match(r"([a-zA-Z0-9_]+)(.*)", dep_str)
    return match.group(1), match.group(2)


class GraphService:
    def __init__(self, repo):
        self.repo = repo

    def build_graph(self, dependencies_dict):
        graph = DependencyGraph()
        graph.repo = self.repo  

     
        for name, constraint_str in dependencies_dict.items():
            constraint = Constraint(constraint_str)
            graph.add_dependency(Dependency(name, constraint))

       
        for name, dep in graph.dependencies.items():
            versions = self.repo.get_versions(name)

            candidates = []
            for v in versions:
                v_obj = Version(v)

                if dep.constraint.is_satisfied_by(v_obj):
                    candidates.append(v_obj)

            graph.set_candidates(name, candidates)

        
        queue = list(graph.dependencies.keys())

        while queue:
            name = queue.pop(0)

            candidates = graph.get_candidates(name)

            for v in candidates:
                subdeps = self.repo.get_dependencies(name, str(v))

                parsed = []

                for sub in subdeps:
                    sub_name, sub_constraint = parse_dep(sub)

                    constraint_obj = Constraint(sub_constraint)
                    parsed.append((sub_name, constraint_obj))

                    
                    if sub_name not in graph.dependencies:
                        graph.add_dependency(
                            Dependency(sub_name, constraint_obj)
                        )

                        versions = self.repo.get_versions(sub_name)

                        sub_candidates = []
                        for sv in versions:
                            sv_obj = Version(sv)

                            if constraint_obj.is_satisfied_by(sv_obj):
                                sub_candidates.append(sv_obj)

                        graph.set_candidates(sub_name, sub_candidates)

                        queue.append(sub_name)  

                
                graph.add_edge(name, v, parsed)

        return graph