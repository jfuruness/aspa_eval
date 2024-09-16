from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs import CustomerProviderLink as CPLink
from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import ASPA, BGP
from bgpy.simulation_framework import (
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from pathsec.policies import ShortestPathExportAllAttacker

as_graph_info = ASGraphInfo(
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=4, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=2, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=ASNs.ATTACKER.value, customer_asn=1),
            CPLink(provider_asn=3333, customer_asn=2),
            CPLink(provider_asn=8, customer_asn=1),
            CPLink(provider_asn=8, customer_asn=2),
            CPLink(provider_asn=4, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=5, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=6, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=6, customer_asn=3333),
        ]
    ),
    diagram_ranks=(
        (4, 5, 6),
        (ASNs.ATTACKER.value, 8, 3333),
        (1, 2),
        (ASNs.VICTIM.value,),
    ),
)


spoofing_aspa_config = EngineTestConfig(
    name="Spoofing Attack against ASPA",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ASPA,
        AttackerBasePolicyCls=ShortestPathExportAllAttacker,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: ASPA,
                2: ASPA,
                4: ASPA,
                5: ASPA,
                6: ASPA,
                ASNs.VICTIM.value: ASPA,
            }
        ),
    ),
    as_graph_info=as_graph_info,
)
