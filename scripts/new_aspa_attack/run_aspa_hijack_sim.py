from copy import deepcopy
from pathsec.policies import (
    ASPAEdge,
    EdgeFilter,
    PathEndEdge,
)

from bgpy.simulation_engine import (
    ROV,
    PathEnd,
    ASPA,
)

from bgpy.simulation_framework import (
    DependentSimulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from pathsec.sims.sim_kwargs import DIR, default_kwargs, run_kwargs
from preprocess_anns_funcs import aspa_hijack

def run_aspa_hijack_sim(num_attackers=1):

    sim_classes = [
        ASPA,
        PathEnd,
        ROV,
    ]
    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.aspa_hijack
                    ),
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
        **default_kwargs,  # type: ignore
    )
    sim.run(**deepcopy(run_kwargs))  # type: ignore
