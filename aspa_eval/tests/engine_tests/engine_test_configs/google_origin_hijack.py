from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP, ROV
from bgpy.simulation_framework import ForgedOriginPrefixHijack, ScenarioConfig
from bgpy.tests.engine_tests.utils import EngineTestConfig
from frozendict import frozendict

from .google_hijack import as_graph_info

google_origin_hijack = EngineTestConfig(
    name="google_origin_hijack",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=ForgedOriginPrefixHijack,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ROV,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({15169}),
        hardcoded_asn_cls_dict=frozendict({x: ROV for x in (2, 15169)}),
    ),
    as_graph_info=as_graph_info,
)
