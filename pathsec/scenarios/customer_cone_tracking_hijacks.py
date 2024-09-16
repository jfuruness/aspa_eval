from bgpy.simulation_framework import VictimsPrefix

from .attacker_customer_cone_tracking_mixin import AttackerCustomerConeTrackingMixin
from .paper_shortest_path_prefix_hijack import PaperShortestPathPrefixHijack


class ShortestPathCustomerConeHijack(
    AttackerCustomerConeTrackingMixin, PaperShortestPathPrefixHijack
):
    """SP-EA attack that only tracks customer cones of the attackers"""

    pass


class VictimsPrefixCustomerConeHijack(AttackerCustomerConeTrackingMixin, VictimsPrefix):
    """passive attack that only tracks customer cones of the attackers"""

    pass
