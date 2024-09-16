from bgpy.simulation_engine import (
    ASPA,
    ROV,
    ASPAwN,
    BGPiSec,
    BGPSec,
    OnlyToCustomers,
    PathEnd,
    ROVEdgeFilter,
)

from aspa_eval.policies import ASPAEdge, ASPAOTCEdge, BGPSecEdge, OTCEdge, PathEndEdge

CLASSES_TO_RUN = [
    PathEnd,
    BGPSec,
    ROV,
    ASPA,
    ASPAwN,
    BGPiSec,
    # Edge
    BGPSecEdge,
    PathEndEdge,
    ROVEdgeFilter,
    ASPAEdge,
    # OTC
    OnlyToCustomers,
    OTCEdge,
    ASPAOTCEdge,
]
