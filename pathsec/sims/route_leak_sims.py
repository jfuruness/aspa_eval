from bgpy.shared.enums import ASGroups
from bgpy.simulation_framework import ScenarioConfig, AccidentalRouteLeak

from .utils import ASPASim, CLASSES_TO_RUN


route_leak_confs = [
    ScenarioConfig(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=AccidentalRouteLeak,
    ) for AdoptPolicyCls in standard_hijack_classes
]

route_leak_edge_sim = ASPASim(
    run_sim,
    confs=[
        replace(conf, attacker_subcategory_attr=ASGroups.MULTIHOMED.value)
        for conf in route_leak_confs
    ],
)

route_leak_transit_sim = ASPASim(
    run_sim,
    confs=[
        replace(conf, attacker_subcategory_attr=ASGroups.TRANSIT.value)
        for conf in route_leak_confs
    ]
)
