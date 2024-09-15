from functools import partial

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
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

from ..sim_kwargs import DIR, default_kwargs, run_kwargs


def run_sim(opts: list[Opt], output_dir: Path | None = None) -> None:
    """Runs sim for an origin hijack"""

    if output_dir is None:
        output_dir = (
            DIR /
            opts[0].ScenarioCls.__name__.lower() /
            opts[0].attacker_subcategory_attr /
            f"{opts[0].num_attackers}_attackers"
        )

    # Remove options that aren't applicable for speed
    filtered_opts = list()
    for opt in opts:
        # Only run OTC with route leaks
        if opt.ScenarioCls != AccidentalRouteLeak and "OTC" in opt.AdoptPolicyCls.name:
            continue
        # EdgeFilter isn't applicable when attacker isn't at the edge
        elif opt.attacker_subcategory_attr in (
            ASGroups.TRANSIT.value, ASGroups.ETC.value, ASGroups.INPUT_CLIQUE.value
        ) and "Edge" in opt.AdoptPolicyCls.name:
            continue
        # Pathend and BGPSec variants do nothing against route leaks
        elif opt.ScenarioCls == AccidentalRouteLeak and (
            "Path-End" in opt.AdoptPolicyCls.name
            or "BGPSec" in opt.AdoptPolicyCls.name
            or "BGP-iSec" in opt.AdoptPolicyCls.name
        ):
            continue
        else:
            filtered_opts.append(opt)

    # Create sim and run it
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=opt.ScenarioCls,
                    AdoptPolicyCls=opt.AdoptPolicyCls,
                    AttackerBasePolicyCls=opt.AttackerBasePolicyCls,
                    attacker_subcategory_attr=attacker_subcategory_attr,
                    adoption_subcategory_attrs=opt.adoption_subcategory_attrs,
                    hardcoded_asn_cls_dict=opt.hardcoded_asn_cls_dict,
                    num_attackers=opt.num_attackers
                )
                for opt in filtered_opts
            ]
        ),
        output_dir=output_dir,
        **default_kwargs,
    )
    sim.run(**run_kwargs)  # type: ignore

standard_classes = [
    PathEnd,
    BGPSec,
    ROV,
    ASPA,
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
