from frozendict import frozendict

from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP, ROV
from bgpy.simulation_framework import ScenarioConfig, PrefixHijack
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.as_graphs.base.links import PeerLink
from bgpy.shared.enums import ASNs

from .google_hijack import as_graph_info

google_hijack_rov = EngineTestConfig(
    name="google_hijack_rov",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=PrefixHijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ROV,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({15169}),
        hardcoded_asn_cls_dict=frozendict({x: ROV for x in (2, 15169)}),
    ),
    as_graph_info=as_graph_info,
)
