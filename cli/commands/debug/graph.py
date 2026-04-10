from infrastructure.persistence.toml.reader import load_config
from infrastructure.repository.local_repo import LocalRepository
from application.services.graph_service import GraphService


def run(args):
    data = load_config()
    deps = data.get("dependencies", {})

    repo = LocalRepository()
    service = GraphService(repo)

    graph = service.build_graph(deps)

    print("=== DEBUG GRAPH ===")
    print(graph)