from pathsec.policies import (
    EdgeFilter,
)

from bgpy.simulation_engine import (
    ROV,
    BGPSec,
    Pathend,
)

from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_origin_hijack_sim():
    """Runs sim for an origin hijack"""

    origin_hijack_classes = [
        EdgeFilter,
        Pathend,
        BGPSec,
        ROV,
        # See paper, the following policies overlap with other lines
        # ASPA,  # overlaps with pathend
        # BGPSecEdge,  # overlaps with edge
        # PathendEdge,  # overlaps with pathend
        # ASPAEdge,  # overlaps with pathend
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
                )
                for AdoptPolicyCls in origin_hijack_classes
            ]
        ),
        output_dir=DIR / "forged_origin_export_all_hijack",
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = dict(run_kwargs)
    new_run_kwargs["graph_factory_kwargs"]["label_replacement_dict"] = {
        Pathend.name: "Path-End/ASPA/Pathend+EdgeFilter/ASPA+EdgeFilter",
        EdgeFilter.name: "EdgeFilter/BGPSec+EdgeFilter",
    }
    sim.run(**new_run_kwargs)
