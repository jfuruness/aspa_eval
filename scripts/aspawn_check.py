from pathlib import Path
import time

from bgpy.enums import ASGroups
from bgpy.simulation_engine import ROV, ASPA, OnlyToCustomers

from bgpy.simulation_framework import (
    Simulation,
    AccidentalRouteLeak,
    ScenarioConfig,
)
from pathsec.policies import (
    EdgeFilter,
    OTCEdge,
    ASPAEdge,
    ASPAOTCEdge,
)
from pathsec.sims.sim_kwargs import default_kwargs


DIR = Path.home() / "Desktop" / "aspa_route_leak_w_attacker_adopting"


def run_route_leak_attacker_adopting():
    """Runs sim for a route leak that is directly comparable to Nils paper"""

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
                    ScenarioCls=AccidentalRouteLeakAttackerAdopting,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                    propagation_rounds=2,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR,
        **default_kwargs,  # type: ignore
    )
    sim.run()


def main():
    """Runs the defaults"""

    start = time.perf_counter()
    run_route_leak_attacker_adopting()
    print(f"{time.perf_counter() - start}s")


if __name__ == "__main__":
    main()
