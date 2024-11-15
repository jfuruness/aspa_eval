import time
from copy import deepcopy

from bgpy.enums import SpecialPercentAdoptions
from bgpy.simulation_engine import (
    ASPA,
    ROV,
    PathEnd,
)
from bgpy.simulation_framework import (
    DependentSimulation,
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)
from preprocess_anns_funcs import aspa_hijack

from aspa_eval.sims.sim_kwargs import DIR, default_kwargs, run_kwargs


class NewASPAHijack(ASPA):
    name = "ASPA (against new hijack)"
class SPEAASPA(ASPA):
    name = "ASPA (against SPEA)"


def run_aspa_hijack_sim(num_attackers=1):

    kwargs = dict(deepcopy(default_kwargs))
    kwargs["percent_adoptions"] = (
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
    )
    sim_classes = [
        SPEAASPA,
        PathEnd,
        ROV,
    ]
    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=NewASPAHijack,
                    preprocess_anns_func=aspa_hijack,
                    num_attackers=num_attackers,
                )
            ] + [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    num_attackers=num_attackers,
                )
                for AdoptPolicyCls in sim_classes
            ]
        ),
        output_dir=DIR / f"new_aspa_hijack_{num_attackers}_attackers",
        **kwargs,  # type: ignore
    )
    sim.run(**deepcopy(run_kwargs))  # type: ignore

if __name__ == "__main__":
    start = time.perf_counter()
    run_aspa_hijack_sim()
    print(f"{time.perf_counter() - start}s to run new aspa hijack")

