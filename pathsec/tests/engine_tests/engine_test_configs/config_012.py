from frozendict import frozendict
from bgpy.shared.enums import ASNs
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP
from pathsec.policies import ASPAEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    SubprefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "subprefix origin hijack against ASPAEdge\n"
    "This isn't realistic, just for testing to test the downstream"
    "Use the subprefix to check"
)

config_012 = EngineTestConfig(
    name="012_subprefix_origin_aspa_edge_downstream_verification",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.forged_origin_hijack,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ASPAEdge,
                10: ASPAEdge,
                ASNs.VICTIM.value: ASPAEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
