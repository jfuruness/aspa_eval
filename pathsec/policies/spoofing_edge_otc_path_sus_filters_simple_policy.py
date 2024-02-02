from typing import Optional, TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine import BGPPolicy, OnlyToCustomersPolicy

if TYPE_CHECKING:
    from bgpy.as_graphs import AS
    from bgpy.simulation_engine import Announcement as Ann

from .edge_filter_simple_policy import EdgeFilterPolicy
from .spoofing_filter_simple_policy import SpoofingFilterPolicy
from .path_sus_algo_simple_policy import PathSusAlgo5Policy


class SpoofingEdgeOTCPathSusFiltersPolicy(
    OnlyToCustomersPolicy,
    PathSusAlgo5Policy,
    # EdgeFilterPolicy,
    # SpoofingFilterPolicy,
    # BGPPolicy,
):
    """Runs spoofing, edge, OTC filters and adds OTC attr"""

    name: str = "SpoofingEdgeOTCPathSus5Filters"

    def _valid_ann(self, ann: "Ann", from_rel: Relationships) -> bool:  # type: ignore
        """Returns invalid if an edge AS is announcing a path longer than len 1"""

        # Since each class calls super() at the end of it's func call,
        # it will actually run through every class up until BGPPolicy
        # https://stackoverflow.com/a/55006027/8903959
        # super()._valid_ann(ann, from_rel)

        # There is some bug above that causes massive disconnections...

        # EDGE FILTER
        neighbor_as_obj = self.as_.as_graph.as_dict[ann.as_path[0]]
        if (neighbor_as_obj.stub or neighbor_as_obj.multihomed) and len(
            ann.as_path
        ) > 1:
            return False

        # SPOOFING FILTER
        if ann.next_hop_asn != ann.as_path[0]:
            return False

        return super()._valid_ann(ann, from_rel)
