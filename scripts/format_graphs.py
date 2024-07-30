from pathlib import Path

from bgpy.simulation_framework import GraphFactory

BASE_PATH = Path("/home/anon/aspa_sims")

GRAPH_DIR = Path("/home/anon/aspa_sims_formatted")
GRAPH_DIR.mkdir(exist_ok=True, parents=True)

def path_kwargs(dir_name: str) -> dict[str, Path]:
    pickle_path = BASE_PATH / dir_name / "data.pickle"
    graph_dir = GRAPH_DIR / dir_name
    return {"pickle_path": pickle_path, "graph_dir": graph_dir}

GraphFactory(
    **path_kwargs("forged_origin_export_all_hijack")
).generate_graphs()
