from frozendict import frozendict
from bgpy.shared.enums import ASNs
from bgpy.tests.engine_tests.engine_test_configs.examples.as_graph_info_000 import (
    as_graph_info_000,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP
from pathsec.policies import PathEndEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    PrefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "shortest path export all attack against pathend edge\n"
    "PathEnd checks the end of the path for valid providers\n"
    "so anything beyond the third AS is not protected"
)

config_006 = EngineTestConfig(
    name="006_shortest_path_pathend_edge",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.shortest_path_hijack,
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
