from bgpy.simulation_engine import ASPA, ROV, PathEnd, ROVEnforceFirstAS, BGPiSec
from bgpy.simulation_framework import (
    FirstASNStrippingPrefixHijack,
    ForgedOriginPrefixHijack,
    ScenarioConfig,
)

from .utils import ASPASim

first_asn_stripping_sim = ASPASim(
    scenario_configs=tuple(
        [
            ScenarioConfig(
                ScenarioCls=ForgedOriginPrefixHijack,
                AdoptPolicyCls=AdoptPolicyCls,
                scenario_label=f"{AdoptPolicyCls.name} (Forged-Origin Export-All)",
            )
            for AdoptPolicyCls in [ROV, ROVEnforceFirstAS]
        ]
    )
    + tuple(
        [
            ScenarioConfig(
                ScenarioCls=FirstASNStrippingPrefixHijack,
                AdoptPolicyCls=AdoptPolicyCls,
                scenario_label=f"{AdoptPolicyCls.name} (First-ASN-Stripping)",
            )
            for AdoptPolicyCls in [ROV, ASPA, PathEnd, BGPiSec]
        ]
    ),
    sim_name="FirstASNStripping_edge",
)
