from pathsec.policies import (
    ASPAOTCEdge,
)

from bgpy.enums import ASGroups
from bgpy.simulation_engine import (
    BGP,
    ASPA,
    OnlyToCustomers,
)
from bgpy.simulation_framework import (
    Simulation,
    AccidentalRouteLeak,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_route_leak_transit_sim():
    """Runs sim for an transit attacker's route leak"""

    sim_classes = [
        ASPAOTCEdge,
        ASPA,
        OnlyToCustomers,
        BGP,
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=ASGroups.TRANSIT.value,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR / "route_leak_transit",
        propagation_rounds=2,
        **default_kwargs,  # type: ignore
    )
    sim.run(
        graph_factory_kwargs={
            "label_replacement_dict": {
                ASPAOTCEdge.name: "ASPA & OTC",
            },
            "y_limit": 30,
        },
        **run_kwargs,
    )
