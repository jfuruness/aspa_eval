from bgpy.simulation_framework import ShortestPathPrefixHijack

from .pathsec.policies import ASPAEdge, ASPAOTCEdge, PathEndEdge


class PaperShortestPathPrefixHijack(ShortestPathPrefixHijack):
    @property
    def pathend_policy_classes(self) -> frozenset[type[Policy]]:
        """Returns policy classes susceptible to PathEnd attacks"""

        return super().pathend_policy_classes | frozenset({PathEndEdge})

    @property
    def aspa_policy_classes(self) -> frozenset[type[Policy]]:
        """Returns policy classes susceptible to ASPA attacks"""
        return super().aspa_policy_classes | frozenset({ASPAEdge, ASPAOTCEdge})
