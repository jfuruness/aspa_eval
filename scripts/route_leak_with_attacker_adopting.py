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


class AccidentalRouteLeakAttackerAdopting(AccidentalRouteLeak):
    """Unlike the default where attacker never adopts, attacker always adopts

    This is because route leaks are unintentional, so if you believe that
    an AS could both adopt a route leak prevention policy and still route
    leak by accident, then we can check this using this policy.

    Personally I believe this assumption that a route leak prevention
    policy won't prevent a route leak from yourself doesn't make much sense,
    but just to cover our bases I've simulated it
    """

    @property
    def _default_adopters(self) -> frozenset[int]:
        """By default, victim and attacker always adopts"""

        return self.victim_asns | self.attacker_asns

    @property
    def _default_non_adopters(self) -> frozenset[int]:
        """No default non adopters"""
        return frozenset()


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
