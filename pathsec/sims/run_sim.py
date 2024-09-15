from functools import partial

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
    BGPSec,
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
        ),

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
                for opt in opts
            ]
        ),
        output_dir=output_dir,
        **default_kwargs,
    )
    sim.run(**run_kwargs)  # type: ignore

standard_hijack_classes = [
    ROVEdgeFilter,
    PathEnd,
    BGPSec,
    ROV,
    ASPA,
    BGPSecEdge,
    PathEndEdge,
    ASPAEdge,
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
