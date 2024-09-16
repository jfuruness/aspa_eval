from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP
from bgpy.simulation_framework import (
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from pathsec.policies import ASPAOTCEdge

desc = (
    "shortest path export all against ASPAOTCEdge from a customer\n"
    "AS 5 fails to detect the shortest path export all"
)

config_015 = EngineTestConfig(
    name="015_shortest_path_aspa_otc_edge_customer",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.shortest_path_hijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ASPAOTCEdge,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ASPAOTCEdge,
                5: ASPAOTCEdge,
                10: ASPAOTCEdge,
                ASNs.VICTIM.value: ASPAOTCEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
