from copy import deepcopy

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.enums import ASGroups
from bgpy.simulation_engine import ASPA
from bgpy.simulation_framework import (
    DependentSimulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


class RandomAdoption(ASPA):
    name = "Random Adoption (ASPA)"


class Tier1ASesAdoptFirst(ASPA):
    name = "Tier-1 ASes Adopt First (ASPA)"


class NoTier1ASes(ASPA):
    name = "No Tier-1 ASes (ASPA)"


class OnlyEdgeASes(ASPA):
    name = "OnlyEdgeASes (ASPA)"


class ForcedASPA(ASPA):
    name = "hardcoded_aspa"


def run_shortest_path_export_all_hijack_adoption_scenarios_sim():
    """Runs sim for shortest path export all"""

    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    tier_1_ases = bgp_dag.as_groups[ASGroups.INPUT_CLIQUE.value]
    hardcoded_asn_cls_dict = frozendict({x.asn: ForcedASPA for x in tier_1_ases})

    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=RandomAdoption,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=Tier1ASesAdoptFirst,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    hardcoded_asn_cls_dict=hardcoded_asn_cls_dict,
                    # Removed the input clique from this list
                    adoption_subcategory_attrs=(
                        ASGroups.STUBS_OR_MH.value,
                        ASGroups.ETC.value,
                    ),
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=NoTier1ASes,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    # Removed the input clique from this list
                    adoption_subcategory_attrs=(
                        ASGroups.STUBS_OR_MH.value,
                        ASGroups.ETC.value,
                    ),
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=OnlyEdgeASes,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    # Removed the input clique and etcfrom this list
                    adoption_subcategory_attrs=(
                        ASGroups.STUBS_OR_MH.value,
                    ),
                ),
            ]
        ),
        output_dir=DIR / "shortest_path_export_all_hijack_adoption_scenarios",
        **default_kwargs,  # type: ignore
    )
    sim.run(**deepcopy(run_kwargs))  # type: ignore
