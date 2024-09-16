from bgpy.as_graphs import ASGraphInfo, PeerLink
from bgpy.as_graphs import CustomerProviderLink as CPLink
from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP, PathEnd
from bgpy.simulation_framework import (
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from pathsec.policies import PathEndEdge

r"""
          2
        /   \
 777 - 3     5
       |     |
       4     6 - 7
       |     |  /
       666   667

667 is a multihomed attacker
666 is a stub attacker
"""

as_graph_info = ASGraphInfo(
    peer_links=frozenset(
        [
            PeerLink(ASNs.VICTIM.value, 3),
            PeerLink(6, 7),
        ]
    ),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=2, customer_asn=3),
            CPLink(provider_asn=2, customer_asn=5),
            CPLink(provider_asn=3, customer_asn=4),
            CPLink(provider_asn=4, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=5, customer_asn=6),
            CPLink(provider_asn=6, customer_asn=667),
            CPLink(provider_asn=7, customer_asn=667),
        ]
    ),
    diagram_ranks=(
        (2,),
        (ASNs.VICTIM.value, 3, 5),
        (4, 6, 7),
        (ASNs.ATTACKER.value, 667),
    ),
)

config_020 = EngineTestConfig(
    name="020_forged_origin_hijack_pathend_edge",
    desc="Origin hijack against PathEndEdge with multihomed and stub AS attackers",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.forged_origin_hijack,
        BasePolicyCls=BGP,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value, 667}),
        num_attackers=2,
        override_non_default_asn_cls_dict=frozendict(
            {
                4: PathEndEdge,
                5: PathEndEdge,
                ASNs.VICTIM.value: PathEnd,  # Origin deploys PathEnd
            }
        ),
    ),
    as_graph_info=as_graph_info,
)
