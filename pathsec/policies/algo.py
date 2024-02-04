from typing import Optional, TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine.policies.bgp import BGPSimplePolicy

if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann


def _get_best_ann_by_gao_rexford(
    self: "BGPSimplePolicy",
    current_ann: Optional["Ann"],
    new_ann: "Ann",
) -> "Ann":
    """Determines if the new ann > current ann by Gao Rexford"""

    assert new_ann is not None, "New announcement can't be None"

    if current_ann is None:
        return new_ann
    else:
        if (
            current_ann.recv_relationship.value == Relationships.CUSTOMERS.value
            and new_ann.recv_relationship.value == Relationships.PROVIDERS.value
            and len(current_ann.as_path) > len(new_ann.as_path)
            and len(current_ann.as_path) >= 5
        ):
            return new_ann
        else:
            ann = self._get_best_ann_by_local_pref(current_ann, new_ann)
            if ann:
                return ann
            else:
                ann = self._get_best_ann_by_as_path(current_ann, new_ann)
                if ann:
                    return ann
                else:
                    return self._get_best_ann_by_lowest_neighbor_asn_tiebreaker(
                        current_ann, new_ann
                    )
        raise Exception("No ann was chosen")
