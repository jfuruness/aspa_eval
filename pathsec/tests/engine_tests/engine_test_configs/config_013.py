from frozendict import frozendict
from bgpy.enums import ASNs
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP
from pathsec.policies import ASPAOTCEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    SubprefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "subprefix origin hijack against ASPAOTCEdge\n"
    "This isn't realistic, just for testing to test the downstream"
    "Use the subprefix to check"
)

config_013 = EngineTestConfig(
    name="013_subprefix_origin_aspa_otc_edge_downstream_verification",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ASPAOTCEdge,
                10: ASPAOTCEdge,
                ASNs.VICTIM.value: ASPAOTCEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)