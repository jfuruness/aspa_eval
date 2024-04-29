from copy import deepcopy
from typing import Optional

from pathsec.policies import ShortestPathExportAllAttacker

from bgpy.as_graphs.base.as_graph.customer_cone_funcs import _get_cone_size_helper
from bgpy.enums import ASGroups, SpecialPercentAdoptions
from bgpy.simulation_engine import (
    BaseSimulationEngine,
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
    Scenario,
)
from bgpy.simulation_framework.scenarios.preprocess_anns_funcs import (
    PREPROCESS_ANNS_FUNC_TYPE,
    noop,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs
from .run_shortest_path_export_all_hijack_etc_cc_sim import ASPAwNeighbors, CustomerConePrefixHijack


from typing import Optional, TYPE_CHECKING

from bgpy.simulation_framework.scenarios.scenario import Scenario
from bgpy.simulation_framework.scenarios.roa_info import ROAInfo
from bgpy.enums import Prefixes
from bgpy.enums import Relationships
from bgpy.enums import Timestamps


from bgpy.as_graphs.base.as_graph.customer_cone_funcs import _get_cone_size_helper

if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann
    from bgpy.simulation_engine import BaseSimulationEngine


class ValidPrefixKinda(ValidPrefix):
    _get_attacker_asns = Scenario._get_attacker_asns

    __init__ = CustomerConePrefixHijack.__init__
    _get_cone_size_helper = _get_cone_size_helper
    _untracked_asns = CustomerConePrefixHijack._untracked_asns


class BGPSpecial(BGP):
    name = "Doomed ASes"


def run_shortest_path_export_all_hijack_etc_cc_w_bgp_sim():
    """Runs sim for shortest path export all"""

    sim_classes = [
        ASPAwNeighbors,
        PathEnd,
        BGPSec,
        ROV,
    ]
    sim = DependentSimulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=CustomerConePrefixHijack,
                    AdoptPolicyCls=AdoptPolicyCls,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    attacker_subcategory_attr=ASGroups.ETC.value,
                )
                for AdoptPolicyCls in sim_classes
            ]
            + [
                ScenarioConfig(
                    ScenarioCls=CustomerConePrefixHijack,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.shortest_path_export_all_hijack
                    ),
                    attacker_subcategory_attr=ASGroups.ETC.value,
                    AttackerBasePolicyCls=ShortestPathExportAllAttacker,
                )
            ] + [
                ScenarioConfig(
                    ScenarioCls=ValidPrefixKinda,
                    AdoptPolicyCls=BGPSpecial,
                    attacker_subcategory_attr=ASGroups.ETC.value,
                )
            ]
        ),
        output_dir=DIR / "shortest_path_export_all_hijack_ETC_CC_W_BGP",
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = dict(deepcopy(run_kwargs))
    new_run_kwargs["graph_factory_kwargs"]["y_axis_label_replacement_dict"] = {  # type: ignore
        "PERCENT ATTACKER SUCCESS": "Percent Attacker Success (Customer Cone)"
    }
    sim.run(**new_run_kwargs)  # type: ignore
