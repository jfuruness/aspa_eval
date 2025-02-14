from typing import TYPE_CHECKING

from bgpy.simulation_framework import Scenario

if TYPE_CHECKING:
    from bgpy.shared.enums import SpecialPercentAdoptions
    from bgpy.simulation_engine import BaseSimulationEngine
    from bgpy.simulation_framework import ScenarioConfig


class AttackerCustomerConeTrackingMixin(Scenario):
    """Mixin that tracks customer cones"""

    def __init__(
        self,
        *,
        scenario_config: "ScenarioConfig",
        percent_adoption: "float | SpecialPercentAdoptions" = 0,
        engine: "BaseSimulationEngine | None" = None,
        attacker_asns: frozenset[int] | None = None,
        victim_asns: frozenset[int] | None = None,
        adopting_asns: frozenset[int] | None = None,
    ):
        assert engine, "Need engine for customer cones"
        super().__init__(
            scenario_config=scenario_config,
            percent_adoption=percent_adoption,
            engine=engine,
            attacker_asns=attacker_asns,
            victim_asns=victim_asns,
            adopting_asns=adopting_asns,
        )

        self._attacker_customer_cone_asns: set[int] = set()
        for attacker_asn in self.attacker_asns:
            assert isinstance(
                engine.as_graph.as_dict[attacker_asn].customer_cone_asns, frozenset
            ), "setting!"
            self._attacker_customer_cone_asns.update(
                engine.as_graph.as_dict[attacker_asn].customer_cone_asns  # type: ignore
            )

        # These are the ASNs we want to avoid tracking
        self._non_attacker_customer_cone_asns: set[int] = {
            x.asn
            for x in engine.as_graph
            if x.asn not in self._attacker_customer_cone_asns
        }

    @property
    def untracked_asns(self) -> frozenset[int]:
        """Returns ASNs that shouldn't be tracked by the metric tracker

        By default just the default adopters and non adopters
        We extend to exclude all ASes not in customer cone
        """

        return super().untracked_asns | self._non_attacker_customer_cone_asns
