from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP, PathEnd
from bgpy.simulation_framework import (
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from .spoofing_aspa_config import as_graph_info

spoofing_pathend_config = EngineTestConfig(
    name="spoofing Attack against PathEnd",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=PathEnd,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: PathEnd,
                2: PathEnd,
                4: PathEnd,
                5: PathEnd,
                6: PathEnd,
                ASNs.VICTIM.value: PathEnd,
            }
        ),
    ),
    as_graph_info=as_graph_info,
)
