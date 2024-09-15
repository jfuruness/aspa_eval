from dataclasses import dataclass

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import ASPA, ROV
from bgpy.simulation_framework import (
    Simulation,
    ForgedOriginPrefixHijack,
    AccidentalRouteLeak,
    ScenarioConfig,
)

from ..sim_kwargs import DIR, default_kwargs, run_kwargs


@dataclass(frozen=True)
class Opt:
    """Simulation Options"""

    scenario_label: str = ""
    adoption_subcategory_attrs: tuple[str, ...] = (
        ASGroups.STUBS_OR_MH,
        ASGroups.ETC.value,
        ASGroups.INPUT_CLIQUE.value,
    )
    hardcoded_asn_cls_dict: frozendict[int, Policy] = frozendict()
    AdoptPolicyCls: Policy = ASPA
    ScenarioCls: Scenario = Scenario


def get_adoption_scenario_opts(
    ScenarioCls: Scenario,
    attacker_subcategory_attr: str,
    propagation_rounds: int,
):
    """Runs sim for shortest path export all"""

    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    tier_1_ases = bgp_dag.as_groups[ASGroups.INPUT_CLIQUE.value]
    t1_aspa_hardcoded_asn_cls_dict = frozendict({x.asn: ASPA for x in tier_1_ases})

    opts = [
        Opt(
            "Baseline (ROV)",
            AdoptPolicyCls=ROV,
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
            propagation_rounds=propagation_rounds,
        ),
        Opt(
            "Random Adoption",
            ScenarioCls=ScenarioCls
            attacker_subcategory_attr=attacker_subcategory_attr,
            propagation_rounds=propagation_rounds,
        ),
        Opt(
            "Tier-1 Adopts First"
            hardcoded_asn_cls_dict=t1_aspa_hardcoded_asn_cls_dict,
            # Removed the input clique from this list
            adoption_subcategory_attrs=(
                ASGroups.STUBS_OR_MH.value,
                ASGroups.ETC.value,
            ),
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
            propagation_rounds=propagation_rounds,
        ),
        Opt(
            "No Tier-1"
            # Removed the input clique from this list
            adoption_subcategory_attrs=(
                ASGroups.STUBS_OR_MH.value,
                ASGroups.ETC.value,
            ),
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
            propagation_rounds=propagation_rounds,
        ),
        Opt(
            "Only Edge",
            adoption_subcategory_attrs=(ASGroups.STUBS_OR_MH.value,),
            ScenarioCls=ScenarioCls,
            attacker_subcategory_attr=attacker_subcategory_attr,
            propagation_rounds=propagation_rounds,
        ),
    ]


def run_adoption_scenarios_sim(opts: tuple[Opt, ...]) -> None:
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=opt.ScenarioCls,
                    AdoptPolicyCls=opt.AdoptPolicyCls,
                    hardcoded_asn_cls_dict=opt.hardcoded_asn_cls_dict,
                    adoption_subcategory_attrs=opt.adoption_subcategory_attrs,
                    attacker_subcategory_attr=opt.attacker_subcategory_attr,
                    propagation_rounds=opt.propagation_rounds,
                ) for opt in opts
            ]
        ),
        output_dir=DIR / f"{opts[0].ScenarioCls.__name__}_adoption_scenarios",
        **default_kwargs,
    )
    sim.run(**run_kwargs)  # type: ignore


run_forged_origin_hijack_adoption_scenarios_sim = partial(
    run_adoption_scenarios_sim,
    get_adoption_scenario_opts(
        ScenarioCls=ForgedOriginPrefixHijack,
        attacker_subcategory_attr=ASGroups.STUBS_OR_MH.value,
        propagation_rounds=1,
    )
)
run_route_leak_adoption_scenarios_sim = partial(
    run_adoption_scenarios_sim,
    get_adoption_scenario_opts(
        ScenarioCls=AccidentalRouteLeak,
        attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
        propagation_rounds=2,
    )
)
