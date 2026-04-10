class DependencyGraph:
    def __init__(self):
        self.dependencies = {} 
        self.candidates = {} 
        self.edges = {}  

    def add_dependency(self, dependency):
        self.dependencies[dependency.name] = dependency

    def set_candidates(self, name, versions):
        self.candidates[name] = versions

    def get_candidates(self, name):
        return self.candidates.get(name, [])

    def add_edge(self, package, version, deps):
        self.edges[(package, str(version))] = deps

    def get_dependencies(self, package, version):
        return self.edges.get((package, str(version)), [])
    def __str__(self):
        out = []
        for name, dep in self.dependencies.items():
            candidates = self.candidates.get(name, [])
            out.append(f"{dep} -> {candidates}")
        return "\n".join(out)