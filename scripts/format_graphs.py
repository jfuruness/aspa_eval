from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import pickle
import shutil

from frozendict import frozendict

from bgpy.simulation_framework import GraphFactory, LineInfo

BASE_PATH = Path("/home/anon/aspa_sims_2024_10_15_final")

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

for label in (
    "Path-End",
    "BGPsec",
    "ASPA",
    "BGP-iSec",
    "Path-End+EdgeFilter",
    "ASPA+EdgeFilter",
    "OnlyToCustomers",
    "OTC+EdgeFilter",
    "ASPA+OTC+EdgeFilter",
    "BGPsec+EdgeFilter",
    "ASRA",
    # Adoption Scenarios
    "Random Adoption",
    "No Tier-1",
    "Only Edge",
    "Tier-1 Adopts First",
    # Mixed Deployment
    "Origin Hijack (ROV)",
    "Subprefix Hijack (ROV)",
    "Prefix Hijack (ROV)",
):
    line_info_dict[label] = LineInfo(label=label)

edge_filter_line_info = LineInfo(label="EdgeFilter")
line_info_dict["ROV + EdgeFilter"] = edge_filter_line_info
line_info_dict["ASRA"] = LineInfo(label="ASPAwN")

########################
# ROV Mixed Deployment #
########################

x_axis_label_replacement_dict = frozendict(
    {
        "Percent Adoption": "Percent of Additional Adoption"
    }
)
GraphFactory(
    line_info_dict=line_info_dict,
    x_axis_label_replacement_dict=x_axis_label_replacement_dict,
    **path_kwargs("rov_deployment_isbgpsafeyet")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    x_axis_label_replacement_dict=x_axis_label_replacement_dict,
    **path_kwargs("rov_deployment_ROVISTA")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    x_axis_label_replacement_dict=x_axis_label_replacement_dict,
    **path_kwargs("rov_deployment_friends_367")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    x_axis_label_replacement_dict=x_axis_label_replacement_dict,
    **path_kwargs("rov_deployment_APNIC")
).generate_graphs()

#################
# Forged-Origin #
#################

FORGED_ORIGIN_Y_LIMIT = 60

GraphFactory(
    line_info_dict={
        **line_info_dict,
        **{
            "ROV + EdgeFilter": replace(
                edge_filter_line_info,
                label="EdgeFilter/BGPsec+EdgeFilter"
            ),
            "BGP-iSec": replace(
                line_info_dict["BGP-iSec"],
                label="BGP-iSec/Path-End"
            )
           }
    },
    labels_to_remove=frozenset(
        {
            "Path-End",
            "ASRA",
            "Path-End+EdgeFilter",
            "ASPA+EdgeFilter",
            "OnlyToCustomers",
            "OTC+EdgeFilter",
            "ASPA+OTC+EdgeFilter",
            "BGPsec+EdgeFilter",
            "ASRA",
        }
    ),
    y_limit=FORGED_ORIGIN_Y_LIMIT,
    **path_kwargs("forgedoriginprefixhijack_stub_or_multihomed_1_attackers")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    y_limit=FORGED_ORIGIN_Y_LIMIT,
    **path_kwargs("ForgedOriginPrefixHijack_adoption_scenarios")
).generate_graphs()

GraphFactory(
    line_info_dict={
        **line_info_dict,
        **{
            "BGP-iSec": replace(
                line_info_dict["BGP-iSec"],
                label="BGP-iSec/Path-End"
            )
           }
    },
    y_limit=FORGED_ORIGIN_Y_LIMIT,
    labels_to_remove=frozenset(
        {
            "OnlyToCustomers",
            "ASRA",
            "Path-End",
        }
    ),
    **path_kwargs("forgedoriginprefixhijack_etc_1_attackers")
).generate_graphs()

#################
# Shortest-Path #
#################

GraphFactory(
    line_info_dict=line_info_dict,
    labels_to_remove=frozenset({"ROV"}),
    **path_kwargs("papershortestpathprefixhijack_etc_1_attackers")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    labels_to_remove=frozenset({"ROV"}),
    **path_kwargs("ShortestPathPrefixHijack_etc_cc")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    labels_to_remove=frozenset({"ROV"}),
    **path_kwargs("papershortestpathprefixhijack_stub_or_multihomed_1_attackers")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    labels_to_remove=frozenset({"ROV"}),
    **path_kwargs("papershortestpathprefixhijack_stub_or_multihomed_10_attackers")
).generate_graphs()

#######################
# First-ASN Stripping #
#######################

GraphFactory(
    line_info_dict=line_info_dict,
    labels_to_remove=frozenset({"ROV"}),
    **path_kwargs("FirstASNStripping_edge")
).generate_graphs()

##########################
# Accidental Route Leaks #
##########################

ACCIDENTAL_ROUTE_LEAKS_Y_LIMIT = 25

GraphFactory(
    line_info_dict={
        **line_info_dict,
        **{
            "ROV": replace(
                rov_line_info,
                label="ROV/Path-End/BGPsec"
            ),
            "ASPA": replace(
                line_info_dict["ASPA"],
                label="ASPA/OTC/ASPA+OTC",
            ),
            "ASPA+EdgeFilter": replace(
                line_info_dict["ASPA+EdgeFilter"],
                label="ASPA+Edge/OTC+Edge/ASPA+OTC+Edge",
            ),

           },
    },
    labels_to_remove=frozenset(
        {
            "ASRA",
            "OnlyToCustomers",
            "ASPA+OTC+EdgeFilter",
            "OTC+EdgeFilter",
            "BGPsec+EdgeFilter",
            "BGPsec",
        }
    ),
    y_limit=ACCIDENTAL_ROUTE_LEAKS_Y_LIMIT,
    **path_kwargs("accidentalrouteleak_multihomed_1_attackers")
).generate_graphs()

GraphFactory(
    line_info_dict={
        **line_info_dict,
        **{
            "ROV": replace(
                rov_line_info,
                label="ROV/Path-End/BGPsec"
            ),
            "ASPA": replace(
                line_info_dict["ASPA"],
                label="ASPA/OTC/BGP-iSec/ASPA+OTC",
            )
           },
    },
    labels_to_remove=frozenset({
        "ASRA",
        "OnlyToCustomers",
        "BGP-iSec",
        "ASPA+OTC",
        "BGPsec+EdgeFilter",
        "BGPsec",
    }),
    y_limit=ACCIDENTAL_ROUTE_LEAKS_Y_LIMIT,
    **path_kwargs("accidentalrouteleak_transit_1_attackers")
).generate_graphs()

GraphFactory(
    line_info_dict=line_info_dict,
    labels_to_remove=frozenset({"Only Edge"}),
    y_limit=ACCIDENTAL_ROUTE_LEAKS_Y_LIMIT,
    **path_kwargs("AccidentalRouteLeak_adoption_scenarios")
).generate_graphs()





for folder_path in BASE_PATH.iterdir():
    # Copy the attacker success graph to a new location
    atk_success_path = (
        GRAPH_DIR
        / folder_path.name
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

