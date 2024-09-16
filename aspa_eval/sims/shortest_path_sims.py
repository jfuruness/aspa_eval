from dataclasses import replace

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import BGP
from bgpy.simulation_framework import ScenarioConfig, ShortestPathPrefixHijack

from aspa_eval.scenarios import (
    PaperShortestPathPrefixHijack,
    ShortestPathCustomerConeHijack,
    VictimsPrefixCustomerConeHijack,
)

from .utils import CLASSES_TO_RUN, ASPASim

shortest_path_hijack_confs = [
    ScenarioConfig(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=PaperShortestPathPrefixHijack,
    )
    for AdoptPolicyCls in CLASSES_TO_RUN
]

shortest_path_edge_sim = ASPASim(
    scenario_configs=tuple(
        [
            replace(conf, attacker_subcategory_attr=ASGroups.STUBS_OR_MH.value)
            for conf in shortest_path_hijack_confs
        ]
    ),
)

shortest_path_edge_10_attackers_sim = ASPASim(
    scenario_configs=tuple(
        [
            replace(
                conf,
                attacker_subcategory_attr=ASGroups.STUBS_OR_MH.value,
                num_attackers=10,
            )
            for conf in shortest_path_hijack_confs
        ]
    ),
)

shortest_path_etc_sim = ASPASim(
    scenario_configs=tuple(
        [
            replace(conf, attacker_subcategory_attr=ASGroups.ETC.value)
            for conf in shortest_path_hijack_confs
        ]
    )
)

shortest_path_etc_cc_sim = ASPASim(
    scenario_configs=(
        *tuple(
            [
                ScenarioConfig(
                    AdoptPolicyCls=AdoptPolicyCls,
                    ScenarioCls=ShortestPathCustomerConeHijack,
                    attacker_subcategory_attr=ASGroups.ETC.value,
                )
                for AdoptPolicyCls in CLASSES_TO_RUN
            ]
        ),
        ScenarioConfig(
            AdoptPolicyCls=BGP,
            ScenarioCls=VictimsPrefixCustomerConeHijack,
            attacker_subcategory_attr=ASGroups.ETC.value,
            scenario_label="Doomed ASes",
        ),
    ),
    sim_name="ShortestPathPrefixHijack_etc_cc",
)
