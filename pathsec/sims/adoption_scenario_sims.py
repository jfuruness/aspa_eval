from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import ASPA, ROV
from bgpy.simulation_framework import (
    AccidentalRouteLeak,
    ForgedOriginPrefixHijack,
    Scenario,
    ScenarioConfig,
)
from frozendict import frozendict

from .utils import ASPASim


def get_adoption_scenario_confs(
    ScenarioCls: Scenario,
    attacker_subcategory_attr: str,
) -> tuple[ScenarioConfig, ...]:
    """Runs sim for shortest path export all"""

    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    tier_1_ases = bgp_dag.as_groups[ASGroups.INPUT_CLIQUE.value]
    t1_aspa_hardcoded_asn_cls_dict = frozendict({x.asn: ASPA for x in tier_1_ases})

    return (
        ScenarioConfig(
            scenario_label="Baseline (ROV)",
            AdoptPolicyCls=ROV,
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
        ),
        ScenarioConfig(
            scenario_label="Random Adoption",
            AdoptPolicyCls=ASPA,
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
        ),
        ScenarioConfig(
            scenario_label="Tier-1 Adopts First",
            AdoptPolicyCls=ASPA,
            hardcoded_asn_cls_dict=t1_aspa_hardcoded_asn_cls_dict,
            # Removed the input clique from this list
            adoption_subcategory_attrs=(
                ASGroups.STUBS_OR_MH.value,
                ASGroups.ETC.value,
            ),
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
        ),
        ScenarioConfig(
            scenario_label="No Tier-1",
            AdoptPolicyCls=ASPA,
            # Removed the input clique from this list
            adoption_subcategory_attrs=(
                ASGroups.STUBS_OR_MH.value,
                ASGroups.ETC.value,
            ),
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
        ),
        ScenarioConfig(
            scenario_label="Only Edge",
            AdoptPolicyCls=ASPA,
            adoption_subcategory_attrs=(ASGroups.STUBS_OR_MH.value,),
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
        ),
    )


forged_origin_hijack_adoption_scenarios_sim = ASPASim(
    scenario_configs=get_adoption_scenario_confs(
        ScenarioCls=ForgedOriginPrefixHijack,
        attacker_subcategory_attr=ASGroups.STUBS_OR_MH.value,
    ),
    sim_name="ForgedOriginPrefixHijack_adoption_scenarios",
)
route_leak_adoption_scenarios_sim = ASPASim(
    scenario_configs=get_adoption_scenario_confs(
        ScenarioCls=AccidentalRouteLeak,
        attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
    ),
    sim_name="AccidentalRouteLeak_adoption_scenarios",
)
