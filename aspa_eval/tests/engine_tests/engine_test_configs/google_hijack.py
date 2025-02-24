from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP
from bgpy.simulation_framework import PrefixHijack, ScenarioConfig
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

as_graph_info = ASGraphInfo(
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=1, customer_asn=3),
            CPLink(provider_asn=3, customer_asn=15169),
            CPLink(provider_asn=1, customer_asn=2),
            CPLink(provider_asn=2, customer_asn=ASNs.ATTACKER.value),
        ]
    ),
    # diagram_ranks=(
    #     (ASNs.ATTACKER.value, ASNs.VICTIM.value),
    #     (1, 2, 3, 4),
    #     (5, 8, 9, 10),
    #     (11, 12),
    # ),
)

google_hijack = EngineTestConfig(
    name="google_hijack",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({15169}),
        hardcoded_asn_cls_dict=frozendict(),
    ),
    as_graph_info=as_graph_info,
)
