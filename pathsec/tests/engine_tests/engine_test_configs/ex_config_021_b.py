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
    AccidentalRouteLeak,
    preprocess_anns_funcs,
)


desc = "accidental route leak against ASPAOTCEdge"

ex_config_021_b = EngineTestConfig(
    name="ex_021_route_leak_aspa_otc_edge_upstream_verification",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=AccidentalRouteLeak,
        preprocess_anns_func=preprocess_anns_funcs.noop,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: ASPAOTCEdge,
                2: ASPAOTCEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
