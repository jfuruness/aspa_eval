from frozendict import frozendict
from bgpy.enums import ASNs
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP
from pathsec.policies import ASPAEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    PrefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "shortest path export all against ASPAEdge from a peer\n"
    "AS prevents the attack, this is merely to check attack functionality"
)

config_016 = EngineTestConfig(
    name="016_shortest_path_export_all_aspa_edge_peer",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.shortest_path_export_all_hijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ASPAEdge,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ASPAEdge,
                4: ASPAEdge,
                5: ASPAEdge,
                8: ASPAEdge,
                9: ASPAEdge,
                10: ASPAEdge,
                11: ASPAEdge,
                12: ASPAEdge,
                ASNs.VICTIM.value: ASPAEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
