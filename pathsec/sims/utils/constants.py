from bgpy.simulation_engine import (
    ASPA,
    ROV,
    ASPAwN,
    BGPiSec,
    BGPSec,
    PathEnd,
    ROVEdgeFilter,
    OnlyToCustomers,
)
from pathsec.policies import ASPAOTCEdge, ASPAEdge, OTCEdge, PathEndEdge, BGPSecEdge

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
