from .rfc_config import rfc_config
from .spea_aspa_config import spea_aspa_config
from .spea_pathend_config import spea_pathend_config

diagram_configs = (rfc_config, spea_aspa_config, spea_pathend_config)

__all__ = ["diagram_configs"]
