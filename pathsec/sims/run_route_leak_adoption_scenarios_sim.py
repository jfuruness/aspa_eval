from copy import deepcopy

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.enums import ASGroups
from bgpy.simulation_engine import ASPA, ROV
from bgpy.simulation_framework import (
    Simulation,
    AccidentalRouteLeak,
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
    name = "Only Edge ASes (ASPA)"


class ForcedASPA(ASPA):
    name = "hardcoded_aspa"


def run_route_leak_adoption_scenarios_sim():
    """Runs sim for shortest path export all"""

    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    tier_1_ases = bgp_dag.as_groups[ASGroups.INPUT_CLIQUE.value]
    hardcoded_asn_cls_dict = frozendict({x.asn: ForcedASPA for x in tier_1_ases})

    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=ROV,
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                ),
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=RandomAdoption,
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                ),
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=Tier1ASesAdoptFirst,
                    hardcoded_asn_cls_dict=hardcoded_asn_cls_dict,
                    # Removed the input clique from this list
                    adoption_subcategory_attrs=(
                        ASGroups.STUBS_OR_MH.value,
                        ASGroups.ETC.value,
                    ),
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                ),
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=NoTier1ASes,
                    # Removed the input clique from this list
                    adoption_subcategory_attrs=(
                        ASGroups.STUBS_OR_MH.value,
                        ASGroups.ETC.value,
                    ),
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                ),
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=OnlyEdgeASes,
                    # Removed the input clique and etcfrom this list
                    adoption_subcategory_attrs=(ASGroups.STUBS_OR_MH.value,),
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                ),
            ]
        ),
        output_dir=DIR / "accidental_route_leak_adoption_scenarios_mh",
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = deepcopy(run_kwargs)
    new_run_kwargs["graph_factory_kwargs"]["y_limit"] = 40
    sim.run(**new_run_kwargs)  # type: ignore
