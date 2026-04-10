from infrastructure.persistence.toml.reader import load_config
from infrastructure.repository.local_repo import LocalRepository
from application.services.graph_service import GraphService
from domain.resolver.sat_resolver import SATResolver
from infrastructure.persistence.lock.lock_writer import write_lock

def run(args):
    data = load_config()
    deps = data.get("dependencies", {})

    repo = LocalRepository()
    service = GraphService(repo)

    graph = service.build_graph(deps)

    resolver = SATResolver(graph)
    solution = resolver.solve()

    print("=== SOLUTION ===")
    for k, v in solution.items():
        print(f"{k}=={v}")
        
    write_lock(solution)