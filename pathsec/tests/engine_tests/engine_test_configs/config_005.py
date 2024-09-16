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

from pathsec.policies import PathEndEdge

desc = (
    "Origin prefix hijack with pathend edge\n"
    "PathEnd checks the end of the path for valid providers\n"
    "and is thus protected against simple origin hijacks"
)

config_005 = EngineTestConfig(
    name="005_origin_prefix_hijack_pathend_edge",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.forged_origin_hijack,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: PathEndEdge,
                ASNs.VICTIM.value: PathEndEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
