from copy import deepcopy
from pathsec.policies import ShortestPathExportAllAttacker

from bgpy.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
    BGPSec,
    PathEnd,
    ASPA,
)

from bgpy.simulation_framework import (
    DependentSimulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


class ASPAwNeighbors(ASPA):
    name = "ASPAWN"


def run_shortest_path_export_all_hijack_etc_sim():
    """Runs sim for shortest path export all"""

    sim_classes = [
        ASPAwNeighbors,
        PathEnd,
        BGPSec,
        ROV,
    ]
    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    attacker_subcategory_attr=ASGroups.ETC.value,
                )
                for AdoptPolicyCls in sim_classes
            ]
            + [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    attacker_subcategory_attr=ASGroups.ETC.value,
                    AttackerBasePolicyCls=ShortestPathExportAllAttacker,
                )
            ]
        ),
        output_dir=DIR / "shortest_path_export_all_hijack_ETC",
        **default_kwargs,  # type: ignore
    )
    sim.run(**deepcopy(run_kwargs))  # type: ignore
