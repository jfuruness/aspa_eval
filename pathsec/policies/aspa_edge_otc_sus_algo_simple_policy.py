from typing import Optional, TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine import BGPSimplePolicy, ASPASimplePolicy

if TYPE_CHECKING:
    from bgpy.as_graphs import AS
    from bgpy.simulation_engine import Announcement as Ann


from .algo import _get_best_ann_by_gao_rexford
from .edge_filter_simple_policy import EdgeFilterSimplePolicy
from .spoofing_filter_simple_policy import SpoofingFilterSimplePolicy


class ASPAEdgeOTCSusAlgoSimplePolicy(ASPASimplePolicy):

    name: str = "ASPAEdgeOTCSusAlgoSimple"

    def _valid_ann(self, ann: "Ann", from_rel: Relationships) -> bool:  # type: ignore
        """Returns invalid if an edge AS is announcing a path longer than len 1"""

        # EDGE FILTER
        neighbor_as_obj = self.as_.as_graph.as_dict[ann.as_path[0]]
        if (neighbor_as_obj.stub or neighbor_as_obj.multihomed) and len(
            ann.as_path
        ) > 1:
            return False

        # SPOOFING FILTER
        if ann.next_hop_asn != ann.as_path[0]:
            return False

        # OTC FILTER
        # If ann.only_to_customers is set, only accept from a provider
        if ann.only_to_customers and from_rel.value != Relationships.PROVIDERS.value:
            return False


        return super()._valid_ann(ann, from_rel)

    def _policy_propagate(  # type: ignore
        self,
        neighbor: "AS",
        ann: "Ann",
        propagate_to: Relationships,
        send_rels: set[Relationships],
    ) -> bool:
        """If propagating to customers and only_to_customers isn't set, set it"""

        if (
            propagate_to.value == Relationships.CUSTOMERS.value
            and not ann.only_to_customers
        ):
            ann = ann.copy({"only_to_customers": True})
            self._process_outgoing_ann(neighbor, ann, propagate_to, send_rels)
            return True
        else:
            return False


    _get_best_ann_by_gao_rexford = _get_best_ann_by_gao_rexford
