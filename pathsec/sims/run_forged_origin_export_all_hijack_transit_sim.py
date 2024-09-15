from copy import deepcopy
from pathsec.policies import (
    EdgeFilter,
    PathEndEdge,
    ASPAEdge,
)

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
    ROV,
    BGPSec,
    PathEnd,
    ASPA,
)

from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_forged_origin_export_all_hijack_transit_sim():
    """Runs sim for an origin hijack"""

    forged_origin_export_all_hijack_classes = [
        EdgeFilter,
        PathEnd,
        BGPSec,
        ROV,
        # See paper, the following policies overlap with other lines
        ASPA,  # overlaps with pathend
        # BGPSecEdge,  # overlaps with edge
        PathEndEdge,  # overlaps with pathend
        ASPAEdge,  # overlaps with pathend
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=preprocess_anns_funcs.forged_origin_export_all_hijack,
                    attacker_subcategory_attr=ASGroups.ETC.value,
                )
                for AdoptPolicyCls in forged_origin_export_all_hijack_classes
            ]
        ),
        output_dir=DIR / "forged_origin_export_all_hijack_etc_hijacker",
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = dict(deepcopy(run_kwargs))
    # new_run_kwargs["graph_factory_kwargs"]["label_replacement_dict"] = {  # type: ignore
    #     PathEnd.name: "Path-End/ASPA/PathEnd+EdgeFilter/ASPA+EdgeFilter",
    #     EdgeFilter.name: "EdgeFilter/BGPSec+EdgeFilter",
    # }
    sim.run(**new_run_kwargs)  # type: ignore
