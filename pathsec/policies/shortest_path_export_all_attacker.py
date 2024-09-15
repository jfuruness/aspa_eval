from typing import TYPE_CHECKING

from bgpy.shared.enums import Relationships
from bgpy.simulation_engine import BGP


if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann
    from bgpy.as_graphs import AS


class ShortestPathExportAllAttacker(BGP):
    """Shortest path export all attacker uses origin hijacks to customers with ASPA

    NOTE: This is meant only to be used in our paper results. This is because
    we currently use the bulk of the shortest path export all functionality within
    the preprocess anns func, a bug in BGPy that we have to fix. So we harcode in our
    results to use the preprocess anns func, and then also use this policy, but we
    don't assert this anywhere, so use outside of our results is not advised.

    Also see comment below about using the timestamp... just use this policy here
    """

    def _policy_propagate(  # type: ignore
        self: "BGP",
        neighbor: "AS",
        ann: "Ann",
        propagate_to: Relationships,
        send_rels: set[Relationships],
    ) -> bool:
        """As defined in ASPA RFC section 12, use origin hijack for customers"""

        # This ann is the one we want to overwrite - the ann seeded at the attacker
        # NOTE: tried ann.seed_asn, but due to other funcs overwriting the ann.seed_asn,
        # we must use the timestamp and just check for 1.
        # Janky, but it works for these
        if ann.timestamp == 1 and propagate_to == Relationships.CUSTOMERS:
            # Only need origin hijack when sending to customers
            new_ann = ann.copy({"as_path": (self.as_.asn, ann.origin)})
            self._process_outgoing_ann(neighbor, new_ann, propagate_to, send_rels)
            return True
        else:
            return False
