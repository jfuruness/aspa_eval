from bgpy.shared.enums import ASGroups
from bgpy.simulation_framework import ScenarioConfig, ShortestPathPrefixHijack

from .utils import ASPASim, CLASSES_TO_RUN


shortest_path_hijack_confs = [
    ScenarioConfig(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=ShortestPathPrefixHijack,
    ) for AdoptPolicyCls in standard_hijack_classes
]

shortest_path_edge_sim = partial(
    run_sim,
    confs=[
        replace(conf, attacker_subcategory_attr=ASGroups.STUB_OR_MH.value)
        for conf in shortest_path_hijack_confs
    ],
)

shortest_path_etc_sim = partial(
    run_sim,
    confs=[
        replace(conf, attacker_subcategory_attr=ASGroups.ETC.value)
        for conf in shortest_path_hijack_confs
    ]
)
