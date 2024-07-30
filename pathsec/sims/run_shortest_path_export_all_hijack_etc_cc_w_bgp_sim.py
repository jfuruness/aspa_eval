from copy import deepcopy
from typing import Optional

from pathsec.policies import ShortestPathExportAllAttacker

from bgpy.as_graphs.base.as_graph.customer_cone_funcs import _get_cone_size_helper
from bgpy.enums import ASGroups, SpecialPercentAdoptions
from bgpy.simulation_engine import (
    BaseSimulationEngine,
    ROV,
    BGP,
    BGPSec,
    PathEnd,
    ASPA,
)

from bgpy.simulation_framework import (
    Simulation,
    ValidPrefix,
    preprocess_anns_funcs,
    ScenarioConfig,
    Scenario,
)
from bgpy.simulation_framework.scenarios.preprocess_anns_funcs import (
    PREPROCESS_ANNS_FUNC_TYPE,
    noop,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs
from .run_shortest_path_export_all_hijack_etc_cc_sim import (
    ASPAwNeighbors,
    CustomerConePrefixHijack,
)


class ValidPrefixKinda(ValidPrefix):
    _get_attacker_asns = Scenario._get_attacker_asns

    def __init__(
        self,
        *,
        scenario_config: ScenarioConfig,
        percent_adoption: float | SpecialPercentAdoptions = 0,
        engine: Optional["BaseSimulationEngine"] = None,
        prev_scenario: Optional["Scenario"] = None,
        preprocess_anns_func: PREPROCESS_ANNS_FUNC_TYPE = noop,
    ):
        assert engine, "Need engine for customer cones"
        self._attacker_customer_cones_asns: set[int] = set()
        super().__init__(
            scenario_config=scenario_config,
            percent_adoption=percent_adoption,
            engine=engine,
            prev_scenario=prev_scenario,
            preprocess_anns_func=preprocess_anns_func,
        )
        # Stores customer cones of attacker ASNs
        # used in untrackable func and when selecting victims
        for attacker_asn in self.attacker_asns:
            self._attacker_customer_cones_asns.update(
                self._get_cone_size_helper(
                    engine.as_graph.as_dict[attacker_asn],
                    dict(),
                ),
            )
        self._non_attacker_customer_cone_asns = set(
            [
                x.asn
                for x in engine.as_graph
                if x.asn not in self._attacker_customer_cones_asns
            ]
        )

    # Just returns customer cone
    _get_cone_size_helper = _get_cone_size_helper

    @property
    def _untracked_asns(self) -> frozenset[int]:
        """Returns ASNs that shouldn't be tracked by the metric tracker

        By default just the default adopters and non adopters
        We extend to exclude all ASes not in customer cone
        """

        return super()._untracked_asns | self._non_attacker_customer_cone_asns


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
    sim = Simulation(
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
            ]
            + [
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
    dct = {"PERCENT ATTACKER SUCCESS": "Percent Attacker Success (Customer Cone)"}
    new_run_kwargs["graph_factory_kwargs"]["y_axis_label_replacement_dict"] = dct  # type: ignore
    sim.run(**new_run_kwargs)  # type: ignore
