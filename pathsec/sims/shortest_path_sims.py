from dataclasses import replace

from frozendict import frozendict

from bgpy.shared.constants import SINGLE_DAY_CACHE_DIR
from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import BGP
from bgpy.simulation_framework import ScenarioConfig, ShortestPathPrefixHijack

from pathsec.scenarios import (
    ShortestPathCustomerConeHijack,
    VictimsPrefixCustomerConeHijack,
)
from .utils import ASPASim, CLASSES_TO_RUN


shortest_path_hijack_confs = [
    ScenarioConfig(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=ShortestPathPrefixHijack,
    )
    for AdoptPolicyCls in CLASSES_TO_RUN
]

shortest_path_edge_sim = ASPASim(
    scenario_configs=tuple(
        [
            replace(conf, attacker_subcategory_attr=ASGroups.STUB_OR_MH.value)
            for conf in shortest_path_hijack_confs
        ]
    ),
)

shortest_path_edge_10_attackers_sim = ASPASim(
    scenario_configs=tuple(
        [
            replace(
                conf,
                attacker_subcategory_attr=ASGroups.STUB_OR_MH.value,
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
    scenario_configs=tuple(
        [
            ScenarioConfig(
                AdoptPolicyCls=AdoptPolicyCls,
                ScenarioCls=ShortestPathCustomerConeHijack,
                attacker_subcategory_attr=ASGroups.ETC.value,
            )
            for AdoptPolicyCls in CLASSES_TO_RUN
        ]
    )
    + (
        ScenarioConfig(
            AdoptPolicyCls=BGP,
            ScenarioCls=VictimsPrefixCustomerConeHijack,
            attacker_subcategory_attr=ASGroups.ETC.value,
            scenario_label="Doomed ASes",
        ),
    ),
    as_graph_constructor_kwargs=frozendict(
        {
            "as_graph_collector_kwargs": frozendict(
                {
                    "cache_dir": SINGLE_DAY_CACHE_DIR,
                }
            ),
            "as_graph_kwargs": frozendict(
                {
                    # When no ASNs are stored, .9gb/core
                    # When one set of cones is stored, 1.6gb/core
                    # When both sets of cones are stored, 2.3gb/core
                    "store_customer_cone_size": True,
                    "store_customer_cone_asns": True,
                    "store_provider_cone_size": False,
                    "store_provider_cone_asns": False,
                }
            ),
            "tsv_path": None,  # Path.home() / "Desktop" / "caida.tsv",
        }
    ),
    sim_name="ShortestPathPrefixHijack_etc_cc",
)
