from typing import TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine import BGPSecSimplePolicy

if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann


class BGPSecEdgeSimplePolicy(BGPSecSimplePolicy):
    name: str = "BGPSecEdgeSimplePolicy"

    def _valid_ann(self, ann: "Ann", from_rel: Relationships) -> bool:  # type: ignore
        """Returns invalid if an edge AS is announcing a path longer than len 1"""

        # EDGE FILTER
        neighbor_as_obj = self.as_.as_graph.as_dict[ann.as_path[0]]
        if (neighbor_as_obj.stub or neighbor_as_obj.multihomed) and len(
            ann.as_path
        ) > 1:
            return False

        return super()._valid_ann(ann, from_rel)
