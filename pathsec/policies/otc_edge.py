from typing import TYPE_CHECKING

from bgpy.simulation_engine import EdgeFilter, OnlyToCustomers

if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann
    from bgpy.shared.enums import Relationships


class OTCEdge(OnlyToCustomers):
    """Prevents edge ASes from paths longer than 1, and OnlyToCustomers"""

    name: str = "OTC + EdgeFilter"

    def _valid_ann(self, ann: "Ann", from_rel: "Relationships") -> bool:
        """Returns invalid if an edge AS is announcing a path longer than len 1

        otherwise returns the OnlyToCustomers's _valid_ann
        """

        # NOTE: you could probably use multiple inheritance here, but to save some dev
        # time, I'm just going to use mixins instead
        if EdgeFilter._valid_edge_ann(self, ann, from_rel):
            return super()._valid_ann(ann, from_rel)
        else:
            return False
