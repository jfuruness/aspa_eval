from functools import partial

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
    ASPA,
    ASPAwN,
    ROV,
    BGPSec,
    BGPiSec,
    PathEnd,
    ROVEdgeFilter
)

from bgpy.simulation_framework import (
    Simulation,
    ScenarioConfig,
    ForgedOriginPrefixHijack,
)


standard_classes = [
    PathEnd,
    BGPSec,
    ROV,
    ASPA,
    ASPAwN,
    BGPiSec,
    # Edge
    BGPSecEdge,
    PathEndEdge,
    ROVEdgeFilter,
    ASPAEdge,
    # OTC
    OnlyToCustomers,
    OTCEdge,
    ASPAOTCEdge,
]

#############################
# Forged Origin Hijack Sims #
#############################

forged_origin_hijack_opts = [
    Opt(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=ForgedOriginPrefixHijack,
    ) for AdoptPolicyCls in standard_hijack_classes
]

run_forged_origin_hijack_edge_sim = partial(
    run_sim,
    opts=[
        replace(opt, attacker_subcategory_attr=ASGroups.STUB_OR_MH.value)
        for opt in forged_origin_hijack_opts
    ],
)

run_forged_origin_hijack_etc_sim = partial(
    run_sim,
    opts=[
        replace(opt, attacker_subcategory_attr=ASGroups.ETC.value)
        for opt in forged_origin_hijack_opts
    ]
)

#############################
# Shortest Path Hijack Sims #
#############################

shortest_path_hijack_opts = [
    Opt(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=ShortestPathPrefixHijack,
    ) for AdoptPolicyCls in standard_hijack_classes
]

run_shortest_path_hijack_edge_sim = partial(
    run_sim,
    opts=[
        replace(opt, attacker_subcategory_attr=ASGroups.STUB_OR_MH.value)
        for opt in shortest_path_hijack_opts
    ],
)

run_shortest_path_hijack_etc_sim = partial(
    run_sim,
    opts=[
        replace(opt, attacker_subcategory_attr=ASGroups.ETC.value)
        for opt in shortest_path_hijack_opts
    ]
)

############################
# AccidentalRouteLeak Sims #
############################

route_leak_opts = [
    Opt(
        AdoptPolicyCls=AdoptPolicyCls,
        ScenarioCls=AccidentalRouteLeak,
    ) for AdoptPolicyCls in standard_hijack_classes
]

run_route_leak_edge_sim = partial(
    run_sim,
    opts=[
        replace(opt, attacker_subcategory_attr=ASGroups.MULTIHOMED.value)
        for opt in route_leak_opts
    ],
)

run_route_leak_transit_sim = partial(
    run_sim,
    opts=[
        replace(opt, attacker_subcategory_attr=ASGroups.TRANSIT.value)
        for opt in route_leak_opts
    ]
)
