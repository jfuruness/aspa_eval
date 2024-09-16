from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import ROV, ASPA, PathEnd, ROVEnforceFirstAS
from bgpy.simulation_framework import (
    ScenarioConfig,
    ForgedOriginPrefixHijack,
    FirstASNStrippingPrefixHijack,
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
            for AdoptPolicyCls in [ROV, ASPA, PathEnd]
        ]
    ),
    sim_name="FirstASNStripping_edge",
)
