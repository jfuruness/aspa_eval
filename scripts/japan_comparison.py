from copy import deepcopy
import time
from aspa_eval.policies import (
    EdgeFilter,
)
from bgpy.enums import ASGroups

from bgpy.simulation_engine import (
    ROV,
    BGPSec,
    PathEnd,
    ASPA,
)

from bgpy.simulation_framework import (
    DependentSimulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from aspa_eval.sims.sim_kwargs import DIR, default_kwargs, run_kwargs


def run_forged_origin_export_all_hijack_sim():
    """Runs sim for an origin hijack"""

    forged_origin_export_all_hijack_classes = [
        PathEnd,
        BGPSec,
        ROV,
        # See paper, the following policies overlap with other lines
        ASPA,  # overlaps with pathend
        # BGPSecEdge,  # overlaps with edge
        # PathEndEdge,  # overlaps with pathend
        # ASPAEdge,  # overlaps with pathend
    ]
    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=preprocess_anns_funcs.forged_origin_export_all_hijack,
                    adoption_subcategory_attrs = (
                        ASGroups.STUBS_OR_MH.value,
                        ASGroups.ETC.value,
                    )
                )
                for AdoptPolicyCls in forged_origin_export_all_hijack_classes
            ]
        ),
        output_dir=DIR / "japan_only_non_transit_forged_origin_export_all_hijack",
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = dict(deepcopy(run_kwargs))
    # new_run_kwargs["graph_factory_kwargs"]["label_replacement_dict"] = {  # type: ignore
    #     PathEnd.name: "Path-End/ASPA/PathEnd+EdgeFilter/ASPA+EdgeFilter",
    #     EdgeFilter.name: "EdgeFilter/BGPSec+EdgeFilter",
    # }
    sim.run(**new_run_kwargs)  # type: ignore

if __name__ == "__main__":
    start = time.perf_counter()
    run_forged_origin_export_all_hijack_sim()
    print(f"{time.perf_counter() - start}s to run new aspa hijack")

