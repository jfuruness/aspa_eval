from typing import Optional, TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine.policies.bgp import BGPPolicy

if TYPE_CHECKING:
    from bgpy.as_graphs import AS
    from bgpy.simulation_engine import Announcement as Ann


class SpoofingFilterSimplePolicy(BGPPolicy):
    """Prevents anns where next_hop != ann.as_path[0]"""

    name: str = "SpoofingFilterSimple"

    def _valid_ann(self, ann: "Ann", from_rel: Relationships) -> bool:  # type: ignore
        """Prevents anns where next_hop != ann.as_path[0]"""
        if ann.next_hop_asn != ann.as_path[0]:
            return False
        else:
            return super()._valid_ann(ann, from_rel)
