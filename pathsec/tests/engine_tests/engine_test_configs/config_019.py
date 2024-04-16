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
    PrefixHijack,
    preprocess_anns_funcs,
)


desc = (
    "shortest path export all against ASPAOTCEdge from a provider\n"
    "AS prevents the attack, this is merely to check attack functionality"
)

config_019 = EngineTestConfig(
    name="019_shortest_path_export_all_aspa_otc_edge_provider",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.shortest_path_export_all_hijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ASPAOTCEdge,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ASPAOTCEdge,
                3: ASPAOTCEdge,
                4: ASPAOTCEdge,
                5: ASPAOTCEdge,
                8: ASPAOTCEdge,
                9: ASPAOTCEdge,
                10: ASPAOTCEdge,
                11: ASPAOTCEdge,
                12: ASPAOTCEdge,
                ASNs.VICTIM.value: ASPAOTCEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)