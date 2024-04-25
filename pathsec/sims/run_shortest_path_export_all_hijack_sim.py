from pathsec.policies import (
    ASPAEdge,
    EdgeFilter,
    PathendEdge,
)

from bgpy.simulation_engine import (
    ROV,
    Pathend,
    ASPA,
)

from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_shortest_path_export_all_hijack_sim(num_attackers=1):
    """Runs sim for shortest path export all"""

    sim_classes = [
        EdgeFilter,
        ASPA,
        ASPAEdge,
        Pathend,
        PathendEdge,
        ROV,
        # See paper, the following policies overlap with other lines
        # BGPSec,  # seen in previous figure, omitted to avoid clutter sicne it sucks
        # BGPSecEdge,  # overlaps with edge, also seen in prev figure
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
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
        output_dir=DIR / f"shortest_path_export_all_hijack_{num_attackers}_attackers",
        **default_kwargs,  # type: ignore
    )
    sim.run(**run_kwargs)
