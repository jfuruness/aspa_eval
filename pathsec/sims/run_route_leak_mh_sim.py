from copy import deepcopy
from pathsec.policies import (
    EdgeFilter,
    OTCEdge,
    ASPAEdge,
    ASPAOTCEdge,
)

from bgpy.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
    ASPA,
    OnlyToCustomers,
)
from bgpy.simulation_framework import (
    DependentSimulation,
    AccidentalRouteLeak,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_route_leak_mh_sim():

    sim_classes = [
        EdgeFilter,
        OTCEdge,
        ASPAEdge,
        ASPAOTCEdge,
        ASPA,
        OnlyToCustomers,
        ROV,
    ]
    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR / "route_leak_mh",
        **default_kwargs,  # type: ignore
    )
    sim.run(**deepcopy(run_kwargs))  # type: ignore
