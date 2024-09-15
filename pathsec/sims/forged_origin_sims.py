from bgpy.shared.enums import ASGroups
from bgpy.simulation_framework import ScenarioConfig, ForgedOriginPrefixHijack

from .utils import ASPASim, CLASSES_TO_RUN


forged_origin_hijack_confs = [
    ScenarioConfig(AdoptPolicyCls=AdoptPolicyCls, ScenarioCls=ForgedOriginPrefixHijack)
    for AdoptPolicyCls in CLASSES_TO_RUN
]

forged_origin_edge_sim = ASPASim(
    scenario_configs=tuple([
        replace(conf, attacker_subcategory_attr=ASGroups.STUB_OR_MH.value)
        for conf in forged_origin_hijack_confs
    ]),
)

forged_origin_etc_sim = ASPASim(
    scenario_configs=tuple([
        replace(conf, attacker_subcategory_attr=ASGroups.ETC.value)
        for conf in forged_origin_hijack_confs
    ])
)
