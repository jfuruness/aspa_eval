from frozendict import frozendict

from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP, ASPA
from bgpy.simulation_framework import ScenarioConfig, ShortestPathPrefixHijack
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.as_graphs.base.links import PeerLink
from bgpy.shared.enums import ASNs

from .google_hijack import as_graph_info

google_shortest_path_hijack_aspa = EngineTestConfig(
    name="google_shortest_path_hijack_aspa",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=ShortestPathPrefixHijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ASPA,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({15169}),
        hardcoded_asn_cls_dict=frozendict({x: ASPA for x in (2, 15169)}),
    ),
    as_graph_info=as_graph_info,
)
