#!/usr/bin/env python3
# USAGE: python3 update_graphs.py

from pathlib import Path
from graph_factory import GraphFactory  # modified version of BGPy's GraphFactory
import shutil

SIMS_DIR = Path("/Users/arvind/Downloads/aspa_sims_new")  # set sim data folder here
GRAPHS_DIR = Path("./graphs")
OUT_DIR = Path("./results")


def list_directories(path: Path):
    return [entry for entry in path.iterdir() if entry.is_dir()]


def main():
    # rename labels in legend
    replacement_labels = {
        "shortest_path_export_all_hijack_ETC_CC": {},
        "shortest_path_export_all_hijack_INPUT_CLIQUE": {},
        "neighbor_spoofing_hijack": {},
        "route_leak_transit": {
            "ASPA+OTC+EdgeFilter": "ASPA+OTC",
        },
        "route_leak_mh": {},
        "shortest_path_export_all_hijack_1_attackers": {},
        "shortest_path_export_all_hijack_ETC": {},
        "forged_origin_export_all_hijack": {
            "Path-End": "Path-End/ASPA/PathEnd+EdgeFilter/ASPA+EdgeFilter",
            "EdgeFilter": "EdgeFilter/BGPSec+EdgeFilter",
        },
        "shortest_path_export_all_hijack_10_attackers": {},
    }

    # display labels in legend in specific order
    # (labels must be original names)
    ordered_labels = {
        "shortest_path_export_all_hijack_ETC_CC": (
            "ROV",
            "BGPSec",
            "ASPA",
            "Path-End",
            "ASPAWN",
        ),
        "shortest_path_export_all_hijack_INPUT_CLIQUE": (
            "ROV",
            "BGPSec",
            "ASPA",
            "Path-End",
            "ASPAWN",
        ),
        "neighbor_spoofing_hijack": (
            "ROV & Neighbor Spoofing Hijack",
            "Path-End & Neighbor Spoofing Hijack",
            "ROV & Forged Origin Export All Hijack",
            "ASPA & Neighbor Spoofing Hijack",
        ),
        "route_leak_transit": ("ROV", "ASPA", "OnlyToCustomers", "ASPA+OTC+EdgeFilter"),
        "route_leak_mh": ("ROV", "EdgeFilter", "OnlyToCustomers", "ASPA"),
        "shortest_path_export_all_hijack_1_attackers": (
            "ROV",
            "EdgeFilter",
            "Path-End",
            "ASPA",
            "Path-End+EdgeFilter",
        ),
        "shortest_path_export_all_hijack_ETC": (
            "ROV",
            "BGPSec",
            "ASPA",
            "Path-End",
            "ASPAWN",
        ),
        "forged_origin_export_all_hijack": ("ROV", "BGPSec", "EdgeFilter", "Path-End"),
        "shortest_path_export_all_hijack_10_attackers": (
            "ROV",
            "EdgeFilter",
            "Path-End",
            "ASPA",
            "Path-End+EdgeFilter",
        ),
        "rov_deployment": (  # order for all rov deployment graphs
            "Subprefix Hijack (ROV)",
            "Neighbor Spoofing Hijack (ROV)",
            "Origin Hijack (ROV)",
            "Prefix Hijack (ROV)",
        ),
    }

    # any label that is not specified will have a color automatically selected from
    # the color cycle, beginning with blue. colors are from matplotlib site:
    # https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html#id2
    # (labels must be original names)
    label_colors = {
        # "ROV": "C0",  # blue
        # "ASPA": "C2",  # green
        # "OnlyToCustomers": "C1",  # orange
        # "ASPA+OTC+EdgeFilter": "C3",  # red
    }

    # limit y-axis of graphs
    y_limits = {
        "shortest_path_export_all_hijack_ETC_CC": 100,
        "shortest_path_export_all_hijack_INPUT_CLIQUE": 50,
        "neighbor_spoofing_hijack": 80,
        "route_leak_transit": 30,
        "route_leak_mh": 40,
        "shortest_path_export_all_hijack_1_attackers": 70,
        "shortest_path_export_all_hijack_ETC": 70,
        "forged_origin_export_all_hijack": 40,
        "shortest_path_export_all_hijack_10_attackers": 100,
    }

    # iterate over each folder in aspa_sims folder
    for i, sim in enumerate(list_directories(SIMS_DIR)):
        # rov deployments graphs
        if i == 4:
            # iterate over each folder in rov_deployment folder
            for j, rov_sim in enumerate(list_directories(sim)):
                print(i, j, rov_sim)

                # create graph
                GraphFactory(
                    pickle_path=rov_sim / "data.pickle",
                    graph_dir=GRAPHS_DIR / rov_sim.name,
                    label_replacement_dict=replacement_labels.get(rov_sim.name, None),
                    label_color_dict=label_colors,
                    ordered_labels=ordered_labels.get(sim.name, None),
                    x_axis_label_replacement_dict={
                        "Percent Adoption": "Percent of Additional Adoption"
                    },
                    y_axis_label_replacement_dict={
                        "PERCENT ATTACKER SUCCESS": "Percent Attacker Success"
                    },
                    y_limit=y_limits.get(rov_sim.name, 100),
                ).generate_graphs()

                # copy adopting_is_any/ATTACKER_SUCCESS graph to results/rov_deployment
                # folder
                dest_dir = OUT_DIR / sim.name
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy(
                    list_directories(GRAPHS_DIR / rov_sim.name)[0]
                    / "all_wout_ixps/adopting_is_Any/DATA/ATTACKER_SUCCESS.png",
                    dest_dir / f"{rov_sim.name}.png",
                )
            continue

        print(i, sim)

        # create graph
        GraphFactory(
            pickle_path=sim / "data.pickle",
            graph_dir=GRAPHS_DIR / sim.name,
            label_replacement_dict=replacement_labels.get(sim.name, None),
            label_color_dict=label_colors,
            ordered_labels=ordered_labels.get(sim.name, None),
            bottom_legend=i == 8,  # foea
            y_axis_label_replacement_dict={
                "PERCENT ATTACKER SUCCESS": f"Percent Attacker Success{' (Customer Cone)' if i == 0 else ''}"  # spea_etc_cc
            },
            y_limit=y_limits.get(sim.name, 100),
        ).generate_graphs()

        # copy adopting_is_any/ATTACKER_SUCCESS graph to results folder
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy(
            list_directories(GRAPHS_DIR / sim.name)[0]
            / "all_wout_ixps/adopting_is_Any/DATA/ATTACKER_SUCCESS.png",
            OUT_DIR / f"{sim.name}.png",
        )


if __name__ == "__main__":
    main()
