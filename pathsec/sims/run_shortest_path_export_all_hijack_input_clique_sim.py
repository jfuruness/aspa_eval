from pathsec.policies import ShortestPathExportAllAttacker
from pathsec.attacker_mod_scenario import AttackerModScenario, AttackerModScenarioConfig

from bgpy.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
    BGPSec,
    Pathend,
    ASPA,
)

from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


class ASPAwNeighbors(ASPA):
    name = "ASPAwNeighbors"


def run_shortest_path_export_all_hijack_input_clique_sim():
    """Runs sim for shortest path export all"""

    sim_classes = [
        ASPAwNeighbors,
        Pathend,
        BGPSec,
        ROV,
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    attacker_subcategory_attr=ASGroups.INPUT_CLIQUE.value,
                )
                for AdoptPolicyCls in sim_classes
            ]
            + [
                AttackerModScenarioConfig(
                    ScenarioCls=AttackerModScenario,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    attacker_subcategory_attr=ASGroups.INPUT_CLIQUE.value,
                    AttackerBasePolicyCls=ShortestPathExportAllAttacker,
                )
            ]
        ),
        output_dir=DIR / "shortest_path_export_all_hijack_INPUT_CLIQUE",
        **default_kwargs,  # type: ignore
    )
    sim.run(**run_kwargs)
