from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP
from bgpy.simulation_framework import (
    AccidentalRouteLeak,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from pathsec.policies import ASPAEdge

desc = "accidental route leak against ASPAEdge"

config_010 = EngineTestConfig(
    name="010_route_leak_aspa_edge_upstream_verification",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=AccidentalRouteLeak,
        preprocess_anns_func=preprocess_anns_funcs.noop,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: ASPAEdge,
                2: ASPAEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
