from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import pickle
import shutil

from bgpy.simulation_framework import GraphFactory, LineInfo

BASE_PATH = Path("/home/anon/aspa_sims_2024_10_14")

GRAPH_DIR = Path("/home/anon/Desktop/aspa_sims_formatted")
GRAPH_DIR.mkdir(exist_ok=True, parents=True)

PAPER_DIR = Path("/home/anon/Desktop/aspa_paper_graphs")
PAPER_DIR.mkdir(exist_ok=True, parents=True)


def path_kwargs(dir_name: str) -> dict[str, Path]:
    pickle_path = BASE_PATH / dir_name / "data.pickle"
    graph_dir = GRAPH_DIR / dir_name
    return {"pickle_path": pickle_path, "graph_dir": graph_dir}

rov_line_info = LineInfo("ROV", unrelated_to_adoption=True)

line_info_dict = {
    "ROV": rov_line_info,
}

for label in ("BGPSec", "EdgeFilter", "Path-End", "BGP-iSec"):
    line_info_dict[label] = LineInfo(label=label)

for folder_path in BASE_PATH.iterdir():
    # Generate formatted graph
    GraphFactory(
        line_info_dict=line_info_dict,
        **path_kwargs(folder_path.name)
    ).generate_graphs()
    # Copy the attacker success graph to a new location
    atk_success_path = (
        folder_path
        / "graphs"
        / "all_wout_ixps"
        / "in_adopting_asns_is_Any"
        / "DATA"
        / "ATTACKER_SUCCESS.png"
    )
    shutil.copy(atk_success_path, PAPER_DIR / f"{folder_path.name}.png")







# line_info_dict = {
#     # Strongest attack graphs
#     "Forged-Origin (ROV)": replace(rov_line_info, label="Forged-Origin (ROV)"),
#     "shortest_path_export_all_hijack (ASPA)": LineInfo("Shortest-Path (ASPA)"),
#     "forged_origin_export_all_hijack (ASPA)": LineInfo("Forged-Origin (ASPA)"),
#     **line_info_dict,
# }
# strongest_attacker_line_info_dict = deepcopy(line_info_dict)
# strongest_attacker_line_info_dict["Prior works strongest attacker"] = LineInfo(
#     "Prior works strongest attacker",
#     hardcoded_xs=(0, 10, 20, 50, 80, 99),
#     hardcoded_ys=(10.71, 10.71, 10.71, 0.7 * 10.71, 0.4 * 10.71, 0),
#     hardcoded_yerrs=(0, 0, 0, 0, 0, 0),
# )
# GraphFactory(
#     line_info_dict=strongest_attacker_line_info_dict,
#     strongest_attacker_labels=(
#         "shortest_path_export_all_hijack (ASPA)",
#         "forged_origin_export_all_hijack (ASPA)",
#     ),
#     strongest_attacker_legend_label="Strongest Attacker",
#     **path_kwargs("strongest_attack")
# ).generate_graphs()

