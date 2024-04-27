from copy import deepcopy
from pathsec.policies import (
    ASPAOTCEdge,
)

from bgpy.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
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
        ROV,
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=ASGroups.TRANSIT.value,
                    propagation_rounds=2,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR / "route_leak_transit",
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = dict(deepcopy(run_kwargs))
    new_run_kwargs["graph_factory_kwargs"]["label_replacement_dict"] = {  # type: ignore
        ASPAOTCEdge.name: "ASPA+OTC",
    }
    sim.run(**new_run_kwargs)  # type: ignore
