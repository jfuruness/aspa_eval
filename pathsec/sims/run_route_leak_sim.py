from functools import partial

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
    ASPA,
    EdgeFilter,
    OnlyToCustomers,
)
from bgpy.simulation_framework import (
    Simulation,
    AccidentalRouteLeak,
    ScenarioConfig,
)

from pathsec.policies import OTCEdge, ASPAEdge, ASPAOTCEdge,
from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_route_leak_sim(attacker_subcategory_attr: str) -> None:
    sim_classes = [
        EdgeFilter,
        OTCEdge,
        ASPAEdge,
        ASPAOTCEdge,
        ASPA,
        OnlyToCustomers,
        ROV,
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=attacker_subcategory_attr,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR / f"route_leak_{attacker_subcategory_attr}",
        **default_kwargs,
    )
    sim.run(**run_kwargs)  # type: ignore


run_route_leak_mh_sim = partial(
    run_route_leak_sim,
    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
)

run_route_leak_transit_sim = partial(
    run_route_leak_transit_sim,
    attacker_subcategory_attr=ASGroups.TRANSIT.value,
)
