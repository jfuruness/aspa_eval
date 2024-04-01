from pathsec.policies import (
    EdgeFilter,
    OTCEdge,
    ASPAEdge,
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


def run_route_leak_mh_sim():
    """Runs sim for an origin hijack"""

    sim_classes = [
        EdgeFilter,
        OTCEdge,
        ASPAEdge,
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
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR / "route_leak_mh",
        **default_kwargs,  # type: ignore
    )
    sim.run(
        graph_factory_kwargs={
            "label_replacement_dict": {
                # Pathend.name: "Pathend/ASPA/PathendEdge/ASPAEdge",
                # EdgeFilter.name: "EdgeFilter/BGPSecEdge"
            },
            # "y_limit": 30,
        },
        **run_kwargs,
    )
