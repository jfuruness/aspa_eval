from frozendict import frozendict
from bgpy.enums import ASNs
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP, ASPA
from pathsec.policies import ASPAEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    PrefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "shortest path export all against ASPAEdge from a customer\n"
    "AS 5 fails to detect the shortest path export all"
)

ex_config_025_a = EngineTestConfig(
    name="ex_025_shortest_path_export_all_aspa_edge_customer",
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
                5: ASPAEdge,
                10: ASPAEdge,
                ASNs.VICTIM.value: ASPAEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
