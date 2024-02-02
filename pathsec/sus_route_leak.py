from typing import TYPE_CHECKING

from bgpy.enums import Relationships, SpecialPercentAdoptions, Timestamps

from .valid_prefix import ValidPrefix
from ..scenario import Scenario


if TYPE_CHECKING:
    from bgpy.simulation_engine import BaseSimulationEngine
    from bgpy.simulation_engine import Announcement as Ann


class SusRouteLeak(ValidPrefix):

    def post_propagation_hook(
        self,
        engine: "BaseSimulationEngine",
        percent_adopt: float | SpecialPercentAdoptions,
        trial: int,
        propagation_round: int,
    ) -> None:
        "Doing two rounds since order matters for sus algo"""

        if propagation_round == 0:
            for attacker_asn in self.attacker_asns:
                if not engine.as_graph.as_dict[attacker_asn].policy._local_rib:
                    print("Attacker did not recieve announcement, can't leak. ")
                announcements = list()
                for prefix, ann in engine.as_graph.as_dict[
                    attacker_asn
                ].policy._local_rib.items():
                    announcements.append(
                        ann.copy(
                            {
                                "recv_relationship": Relationships.CUSTOMERS,
                                "seed_asn": attacker_asn,
                                "traceback_end": True,
                                "timestamp": Timestamps.ATTACKER.value,
                            }
                        )
                    )
                engine.as_graph.as_dict[attacker_asn].policy._local_rib.data.clear()
                for announcement in announcements:
                    engine.as_graph.as_dict[attacker_asn].policy._local_rib[
                        announcement.prefix] = announcement
        elif propagation_round > 1:
            raise NotImplementedError

    def _get_attacker_asns(self, *args, **kwargs):
        """Gets attacker ASNs, overriding the valid prefix which has no attackers

        There is a very rare case where the attacker can not perform the route leak
        due to a disconnection, which happens around .1% in the CAIDA topology.
        In theory - you could just look at the provider cone of the victim,
        and then the peers of that provider cone (and of the victim itself), and
        then the customer cones of all of those ASes to get the list of possible
        valid attackers. However, we consider the attacker being unable to attack
        in extremely rare cases a valid result, and thus do not change the random
        selection. Doing so would also be a lot slower for a very extreme edge case
        """
        return Scenario._get_attacker_asns(self, *args, **kwargs)
