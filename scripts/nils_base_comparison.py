from multiprocessing import cpu_count
from pathlib import Path
import sys
import time

from bgpy.enums import ASGroups, SpecialPercentAdoptions
from bgpy.simulation_engine import ROV, ASPA

from bgpy.simulation_framework import (
    DependentSimulation,
    AccidentalRouteLeak,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

DIR = Path.home() / "Desktop" / "aspa_comparison_sims"

default_kwargs = {
    "percent_adoptions": (
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.5,
            0.8,
            0.99,
    ),
    "num_trials": 1 if "quick" in str(sys.argv) else 1000,
    "parse_cpus": cpu_count() - 2,
}

nils_comparison_kwargs = {
    "adoption_subcategory_attrs": (ASGroups.ALL_WOUT_IXPS.value,),
    "attacker_subcategory_attr": ASGroups.ALL_WOUT_IXPS.value,
    "victim_subcategory_attr": ASGroups.ALL_WOUT_IXPS.value,
}


class PrefixHijackVictimRandom(PrefixHijack):
    @property
    def _default_adopters(self) -> frozenset[int]:
        """Nils paper has victim's adopting randomly"""
        return frozenset()

class AccidentalRouteLeakVictimRandomAnyLeaker(AccidentalRouteLeak):
    @property
    def _default_adopters(self) -> frozenset[int]:
        """Nils paper has victim's adopting randomly"""
        return frozenset()

    @property
    def warning_as_groups(self) -> frozenset[str]:
        """Nils paper allows leakers from everywhere

        So we suppress warnings that would normally come up from leaking from stubs
        """
        return frozenset()



def run_origin_hijack_nils_comparison_sim():
    """Runs sim for an origin hijack that is directly comparable to Nils paper"""

    sim = DependentSimulation(
        scenario_configs=[
            ScenarioConfig(
                ScenarioCls=PrefixHijackVictimRandom,
                AdoptPolicyCls=Cls,
                preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
                **nils_comparison_kwargs,
            ) for Cls in (ROV, ASPA)
        ],
        output_dir=DIR / "origin_hijack_nils",
        **default_kwargs,  # type: ignore
    )
    sim.run()


class AccidentalRouteLeakAnyLeaker(AccidentalRouteLeak):


def run_route_leak_nils_comparison_sim():
    """Runs sim for a route leak that is directly comparable to Nils paper"""

    sim = DependentSimulation(
        scenario_configs=[
            ScenarioConfig(
                ScenarioCls=AccidentalRouteLeakVictimRandomAnyLeaker,
                AdoptPolicyCls=Cls,
                propagation_rounds=2,
                **nils_comparison_kwargs,
            ) for Cls in (ROV, ASPA)
        ],
        output_dir=DIR / "route_leak_nils",
        **default_kwargs,  # type: ignore
    )
    sim.run()


def main():
    """Runs the defaults"""

    sim_funcs = (
        run_origin_hijack_nils_comparison_sim,
        run_route_leak_nils_comparison_sim,
    )
    for sim_func in sim_funcs:
        start = time.perf_counter()
        sim_func()  # type: ignore
        print(f"{time.perf_counter() - start}s for {getattr(sim_func, '__name__', '')}")


if __name__ == "__main__":
    print("On Justin's machine this took ~11m using pypy3 -O")
    start = time.perf_counter()
    main()
    print(f"{time.perf_counter() - start}s for all sims")
