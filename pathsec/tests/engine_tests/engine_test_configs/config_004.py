from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs import PeerLink, CustomerProviderLink as CPLink
from bgpy.enums import ASNs

from frozendict import frozendict
from bgpy.enums import ASNs
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP, ROV, ASPA, Pathend
from pathsec.policies import OTCEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    PrefixHijack,
    preprocess_anns_funcs,
)

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
            CPLink(provider_asn=5, customer_asn=4),
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

config_004 = EngineTestConfig(
    name="004_origin_hijack_aspa_otc_edge",
    desc="Origin hijack against ASPAOTCEdge policy with multihomed and stub AS attackers",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
        BasePolicyCls=BGP,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value, 667}),
        num_attackers=2,
        override_non_default_asn_cls_dict=frozendict(
            {
                4: OTCEdge,
                5: OTCEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info,
)