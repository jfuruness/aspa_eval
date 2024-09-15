from bgpy.simulation_engine import (
    ASPA,
    ASPAwN,
    ROV,
    BGPSec,
    BGPiSec,
    PathEnd,
    ROVEdgeFilter
)

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
