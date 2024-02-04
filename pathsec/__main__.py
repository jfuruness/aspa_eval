from copy import deepcopy
from multiprocessing import cpu_count
from pathlib import Path
import sys
import time

# I know this is bad, but I gotta save on the devtime
from pathsec.policies import *

from bgpy.simulation_engine import (
    BGPSimplePolicy,
    ROVSimplePolicy,
    ASPASimplePolicy,
    BGPSecSimplePolicy,
    PathendSimplePolicy,
    OnlyToCustomersSimplePolicy,
)

from bgpy.enums import ASGroups, SpecialPercentAdoptions
from bgpy.simulation_framework import (
    Simulation,
    AccidentalRouteLeak,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
    GraphFactory,
)

default_kwargs = {
    "percent_adoptions": (
        SpecialPercentAdoptions.ONLY_ONE,
        0.1,
        0.2,
        0.5,
        0.8,
        0.99,
        # Using only 1 AS not adopting causes extreme variance
        # SpecialPercentAdoptions.ALL_BUT_ONE,
    ),
    "num_trials": 1 if "quick" in str(sys.argv) else 40,
    "parse_cpus": cpu_count() - 2,
}


class ROVWOriginHijack(ROVSimplePolicy):
    name = "ROV & Origin Hijack"
class ROVWOriginSpoofingHijack(ROVSimplePolicy):
    name = "ROV & Origin Spoofing Hijack"


run_kwargs = {
    "GraphFactoryCls": None if "quick" in str(sys.argv) else GraphFactory,

}


def main():
    """Runs the defaults"""

    DIR = Path.home() / "Desktop" / "aspa_sims"

    # Origin Hijack
    origin_hijack_classes = [
        EdgeFilterSimplePolicy,
        PathendSimplePolicy,
        # ASPASimplePolicy,
        BGPSecSimplePolicy,
        # BGPSecEdgeSimplePolicy,
        # PathendEdgeSimplePolicy,
        # ASPAEdgeSimplePolicy,
        BGPSimplePolicy,
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
        output_dir=DIR / "origin_hijack",
        **default_kwargs,
    )
    start = time.perf_counter()
    sim.run(**run_kwargs)

    print(time.perf_counter() - start)



    # Origin Spoofing Hijack
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROVWOriginHijack,
                    preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROVWOriginSpoofingHijack,
                    preprocess_anns_func=preprocess_anns_funcs.origin_spoofing_hijack,
                ),

            ]
        ),
        output_dir=DIR / "origin_spoofing",
        **default_kwargs,
    )
    start = time.perf_counter()
    sim.run(**run_kwargs)
    print(time.perf_counter() - start)

    # Shortest path export all
    shortest_path_export_all_classes = [
        # EdgeFilterSimplePolicy,
        # PathendSimplePolicy,
        # ASPASimplePolicy,
        PathendEdgeSimplePolicy,
        ASPAEdgeSimplePolicy,
        # PathSusAlgo5SimplePolicy,
        # SpoofingEdgeOTCPathSusFiltersSimplePolicy,  # RENAME in graph
        PathendEdgeSusAlgoSimplePolicy,
        ASPAEdgeSusAlgoSimplePolicy,
        BGPSimplePolicy,
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
                )
                for AdoptPolicyCls in shortest_path_export_all_classes
            ]
        ),
        output_dir=DIR / "shortest_path_export_all",
        **default_kwargs,
    )
    start = time.perf_counter()
    sim.run(**run_kwargs)
    print(time.perf_counter() - start)

    # Shortest path export all multi attackers
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    num_attackers=10,
                )
                for AdoptPolicyCls in shortest_path_export_all_classes
            ]
        ),
        output_dir=DIR / "shortest_path_export_all_multi",
        **default_kwargs,
    )
    start = time.perf_counter()
    sim.run(**run_kwargs)
    print(time.perf_counter() - start)
    # Route leak multihomed
    route_leak_multihomed_classes = [
        EdgeFilterSimplePolicy,
        OnlyToCustomersEdgeSimplePolicy,
        OnlyToCustomersSimplePolicy,
        ASPASimplePolicy,
        ASPAEdgeSimplePolicy,
        ASPAEdgeOTCSimplePolicy,
        PathSusAlgo5SimplePolicy,
        SpoofingEdgeOTCPathSusFiltersSimplePolicy,  # EdgeOTCSus - RENAME
        ASPAEdgeOTCSusAlgoSimplePolicy,
        BGPSimplePolicy,
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=ASGroups.MULTIHOMED.value,
                )
                for AdoptPolicyCls in route_leak_multihomed_classes
            ]
        ),
        propagation_rounds=2,
        output_dir=DIR / "accidental_route_leak_mh",
        **default_kwargs,
    )
    start = time.perf_counter()
    run_kwargs_copy = deepcopy(run_kwargs)
    run_kwargs_copy["graph_factory_kwargs"] = {"y_limit": 30}
    sim.run(**run_kwargs_copy)
    print(time.perf_counter() - start)

    # Route leak transit
    route_leak_transit_classes = [
        OnlyToCustomersSimplePolicy,
        ASPASimplePolicy,
        ASPAEdgeOTCSimplePolicy,  # RENAME - remove edge
        PathSusAlgo5SimplePolicy,
        SpoofingEdgeOTCPathSusFiltersSimplePolicy,  # OTCSus - RENAME
        ASPAEdgeOTCSusAlgoSimplePolicy,  # ASPAEdgeOTCSs - RENAEM
        BGPSimplePolicy, # BGPSec, Pathend, Edge as well as BGP
    ]
    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=AccidentalRouteLeak,
                    AdoptPolicyCls=AdoptPolicyCls,
                    attacker_subcategory_attr=ASGroups.TRANSIT.value,
                )
                for AdoptPolicyCls in route_leak_transit_classes
            ]
        ),
        propagation_rounds=2,
        output_dir=DIR / "accidental_route_leak_transit",
        **default_kwargs,
    )
    start = time.perf_counter()
    run_kwargs_copy = deepcopy(run_kwargs)
    run_kwargs_copy["graph_factory_kwargs"] = {"y_limit": 30}
    sim.run(**run_kwargs_copy)
    print(time.perf_counter() - start)


if __name__ == "__main__":
    main()
