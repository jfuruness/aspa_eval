from bgpy.as_graphs import ASGraphInfo, PeerLink
from bgpy.as_graphs import CustomerProviderLink as CPLink
from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP
from bgpy.simulation_framework import (
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from pathsec.policies import EdgeFilter

r"""
          2
        /   \
 777 - 3     5
       |     |
       4 --- 667
       |
       666

667 is a multihomed attacker
666 is a stub attacker
"""

as_graph_info = ASGraphInfo(
    peer_links=frozenset([PeerLink(ASNs.VICTIM.value, 3), PeerLink(4, 667)]),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=2, customer_asn=3),
            CPLink(provider_asn=2, customer_asn=5),
            CPLink(provider_asn=3, customer_asn=4),
            CPLink(provider_asn=5, customer_asn=667),
            CPLink(provider_asn=4, customer_asn=ASNs.ATTACKER.value),
        ]
    ),
    diagram_ranks=(
        (2,),
        (ASNs.VICTIM.value, 3, 5),
        (4, 667),
        (ASNs.ATTACKER.value,),
    ),
)

config_001 = EngineTestConfig(
    name="001_forged_origin_hijack_edge_filter",
    desc="Origin hijack against EdgeFilter policy with multihomed and stub AS attackers",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.forged_origin_hijack,
        BasePolicyCls=BGP,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value, 667}),
        num_attackers=2,
        override_non_default_asn_cls_dict=frozendict(
            {
                4: EdgeFilter,
                5: EdgeFilter,
            }
        ),
    ),
    as_graph_info=as_graph_info,
)
