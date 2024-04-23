from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs import PeerLink, CustomerProviderLink as CPLink
from bgpy.enums import ASNs

from frozendict import frozendict
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP
from pathsec.policies import OTCEdge
from bgpy.simulation_framework import (
    ScenarioConfig,
    AccidentalRouteLeak,
)

r"""
            2
        /      \
 777 - 3        5 
       |  \     | 
       4   8    6
       |    \/  |
       |   /  \ |
       666      667
       |
       7
"""

as_graph_info = ASGraphInfo(
    peer_links=frozenset(
        [
            PeerLink(ASNs.VICTIM.value, 3),
        ]
    ),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=2, customer_asn=3),
            CPLink(provider_asn=2, customer_asn=5),
            CPLink(provider_asn=3, customer_asn=4),
            CPLink(provider_asn=3, customer_asn=8),
            CPLink(provider_asn=4, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=5, customer_asn=6),
            CPLink(provider_asn=6, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=ASNs.ATTACKER.value, customer_asn=7),
            CPLink(provider_asn=8, customer_asn=667),
            CPLink(provider_asn=6, customer_asn=667),
        ]
    ),
    diagram_ranks=(
        (2,),
        (ASNs.VICTIM.value, 3, 5),
        (4, 8, 6),
        (ASNs.ATTACKER.value, 667),
        (7,),
    ),
)

desc = (
    "Accidental route leak against OTCEdge policy with an attacker with a customer\n"
    "as well as a multihomed attacker. AS 6 cannot prevent the attack if it only\n"
    "adopts OTC instead of OTCEdge."
)


config_004 = EngineTestConfig(
    name="004_accidental_route_leak_otc_edge",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=AccidentalRouteLeak,
        BasePolicyCls=BGP,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value, 667}),
        num_attackers=2,
        override_non_default_asn_cls_dict=frozendict(
            {
                4: OTCEdge,
                6: OTCEdge,
            }
        ),
    ),
    as_graph_info=as_graph_info,
)
