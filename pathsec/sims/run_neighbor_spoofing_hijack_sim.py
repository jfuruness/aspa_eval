from copy import deepcopy

from bgpy.simulation_engine import ROV, ASPA, PathEnd
from bgpy.simulation_framework import (
    DependentSimulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


class ROVWOriginHijack(ROV):
    name = "ROV & Forged Origin Export All Hijack"


class ROVWNeighborSpoofingHijack(ROV):
    name = "ROV & Neighbor Spoofing Hijack"


class ASPAWNeighborSpoofingHijack(ASPA):
    name = "ASPA & Neighbor Spoofing Hijack"


class PathEndWNeighborSpoofingHijack(PathEnd):
    name = "Path-End & Neighbor Spoofing Hijack"


def run_neighbor_spoofing_hijack_sim():
    """Runs sim for an neighbor spoofing hijack"""

    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROVWOriginHijack,
                    preprocess_anns_func=preprocess_anns_funcs.forged_origin_export_all_hijack,
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROVWNeighborSpoofingHijack,
                    preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPAWNeighborSpoofingHijack,
                    preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=PathEndWNeighborSpoofingHijack,
                    preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
                ),
            ]
        ),
        output_dir=DIR / "neighbor_spoofing_hijack",
        **default_kwargs,  # type: ignore
    )
    sim.run(**deepcopy(run_kwargs))  # type: ignore
