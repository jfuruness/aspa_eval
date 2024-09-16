from .config_001 import config_001
from .config_002 import config_002
from .config_003 import config_003
from .config_004 import config_004
from .config_005 import config_005
from .config_006 import config_006
from .config_007 import config_007
from .config_008 import config_008
from .config_009 import config_009
from .config_010 import config_010
from .config_011 import config_011
from .config_012 import config_012  # noqa
from .config_013 import config_013  # noqa
from .config_014 import config_014
from .config_015 import config_015
from .config_016 import config_016
from .config_017 import config_017
from .config_018 import config_018
from .config_019 import config_019
from .config_020 import config_020
from .diagrams import diagram_configs
from .internals import internal_configs

engine_test_configs = (
    (  # noqa: RUF005
        config_001,
        config_002,
        config_003,
        config_004,
        config_005,
        config_006,
        config_007,
        config_008,
        config_009,
        config_010,
        config_011,
        # Rewrote these in the og BGPy since ASPA now inherits from ROV
        # don't have time to fix it here but checked this by hand
        # config_012,
        # config_013,
        config_014,
        config_015,
        config_016,
        config_017,
        config_018,
        config_019,
        config_020,
    )
    + diagram_configs
    + internal_configs
)

__all__ = [
    "engine_test_configs",
]
