from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from bgpy.simulation_engine import BGP, Policy
from bgpy.simulation_framework import ScenarioConfig, PrefixHijack


if TYPE_CHECKING:
    from bgpy.enums import SpecialPercentAdoptions
    from bgpy.simulation_engine import BaseSimulationEngine
    from bgpy.simulation_framework import Scenario


@dataclass(frozen=True)
class AttackerModScenarioConfig(ScenarioConfig):
    AttackerBasePolicyCls: type[Policy] = BGP


class AttackerModScenario(PrefixHijack):
    """This class came up as the need for an attacker class arose.

    For example, for the shortest path export all attack against ASPA,
    attackers must use the shortest path export all algo when sending to peers
    and providers, but when sending to customers, they can simply use an origin
    hijack. As such, you can no longer do a shortest path export all hijack
    by preprocessing the announcements from a prefix hijack - you must
    actively modify the attacker's behavior.

    Doing so would be great to have in the base BGPy simulator, however,
    this would be yet another major release with backwards compatability
    breaking changes due to the YAML on top of so many others, so we want
    to avoid this.

    In this class is a workaround where you can modify the attacker's Policy
    class during simulation, and revert it before tracking occurs. While it
    doesn't need to be done dynamically like this for our paper, we figured
    just in case the need arose in other papers, this would serve as a nice
    example of how to do this (the altnernative is merely overwriting functions
    on an instance of the attacker's policy, but this isn't as clean)

    Also note - we could have used the base Scenario class for this, and made a
    secondary subclass that inherits from both PrefixHijack and this class. But
    since this is a one-off, to save on development time and avoid a multi
    inheritance nuisance, we simply inherit directly from the PrefixHijack class
    """

    def setup_engine(
        self, engine: BaseSimulationEngine, prev_scenario: Optional["Scenario"] = None
    ) -> None:
        """Sets up engine"""

        super().setup_engine(engine, prev_scenario)
        for attacker_asn in self.attacker_asns:
            as_obj = engine.as_graph.as_dict[attacker_asn]
            assert isinstance(self.scenario_config, AttackerModScenarioConfig), "Mypy"
            self.__OGAttackerBasePolicyCls = as_obj.policy
            as_obj.policy.__class__ = self.scenario_config.AttackerBasePolicyCls

    def pre_aggregation_hook(
        self,
        engine: "BaseSimulationEngine",
        percent_adopt: float | SpecialPercentAdoptions,
        trial: int,
        propagation_round: int,
    ) -> None:
        """Reverts attacker back to original class prior to aggregation

        in general, attacker isn't counted anyways, but changing the policy
        to something unique could cause errors, best to change it back
        """
        for attacker_asn in self.attacker_asns:
            as_obj = engine.as_graph.as_dict[attacker_asn]
            assert issubclass(self.__OGAttackerBasePolicyCls, Policy), "For mypy"
            as_obj.policy.__class__ = self.__OGAttackerBasePolicyCls
