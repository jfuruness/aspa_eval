from frozendict import frozendict

from bgpy.enums import ASNs
from bgpy.simulation_engine import BGP, Pathend
from bgpy.simulation_framework import (
    preprocess_anns_funcs,
    ScenarioConfig,
    PrefixHijack,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig

from .spoofing_aspa_config import as_graph_info


spoofing_pathend_config = EngineTestConfig(
    name="spoofing Attack against Pathend",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=Pathend,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: Pathend,
                2: Pathend,
                4: Pathend,
                5: Pathend,
                6: Pathend,
                ASNs.VICTIM.value: Pathend,
            }
        ),
    ),
    as_graph_info=as_graph_info,
)