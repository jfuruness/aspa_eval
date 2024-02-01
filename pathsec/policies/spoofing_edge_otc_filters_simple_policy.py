from typing import Optional, TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine.policies.bgp import BGPSimplePolicy

if TYPE_CHECKING:
    from bgpy.as_graphs import AS
    from bgpy.simulation_engine import Announcement as Ann


class SpoofingEdgeOTCFiltersSimplePolicy(
    OnlyToCustomersSimplePolicy,
    EdgeFilterSimplePolicy,
    SpoofingFilterSimplePolicy,
    BGPSimplePolicy,
):
    """Runs spoofing, edge, OTC filters and adds OTC attr"""

    name: str = "SpoofingEdgeOTCFiltersSimple"

    def _valid_ann(self, ann: "Ann", from_rel: Relationships) -> bool:  # type: ignore
        """Returns invalid if an edge AS is announcing a path longer than len 1"""

        # Since each class calls super() at the end of it's func call,
        # it will actually run through every class up until BGPSimplePolicy
        super()._valid_ann(ann, from_rel)
