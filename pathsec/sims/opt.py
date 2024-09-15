from dataclasses import dataclass

@dataclass(frozen=True)
class Opt:
    """Simulation Options"""

    AdoptPolicyCls: Policy,
    ScenarioCls: Scenario = Scenario
    scenario_label: str = ""
    adoption_subcategory_attrs: tuple[str, ...] = (
        ASGroups.STUBS_OR_MH,
        ASGroups.ETC.value,
        ASGroups.INPUT_CLIQUE.value,
    )
    attacker_subcategory_attr: str = ASGroups.STUB_OR_MH.value
    hardcoded_asn_cls_dict: frozendict[int, Policy] = frozendict()
    num_attackers: int = 1

    @property
    def AttackerBasePolicyCls(self) -> Policy | None:
        """Returns a special ASPA attacker when ASPA is used

        This special attacker sends forged-origin hijacks to customers
        """

        if (
            issubclass(self.AdoptPolicyCls, ASPA)
            and not issubclass(self.AdoptPolicyCls, ASPAwN)
        ):
            return getattr(self.ScenarioCls, "RequiredASPAAttacker", None)
        else:
            return None
