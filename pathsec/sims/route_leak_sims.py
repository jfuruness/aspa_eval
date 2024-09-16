from dataclasses import replace

from bgpy.shared.enums import ASGroups
from bgpy.simulation_framework import AccidentalRouteLeak, ScenarioConfig

from .utils import CLASSES_TO_RUN, ASPASim

route_leak_confs = [
    ScenarioConfig(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=AccidentalRouteLeak,
    ) for AdoptPolicyCls in CLASSES_TO_RUN
]

route_leak_mh_sim = ASPASim(
    scenario_configs=tuple([
        replace(conf, attacker_subcategory_attr=ASGroups.MULTIHOMED.value)
        for conf in route_leak_confs
    ]),
)

route_leak_transit_sim = ASPASim(
    scenario_configs=tuple([
        replace(conf, attacker_subcategory_attr=ASGroups.TRANSIT.value)
        for conf in route_leak_confs
    ])
)
