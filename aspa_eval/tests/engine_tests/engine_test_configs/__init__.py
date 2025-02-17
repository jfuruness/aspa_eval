from .google_hijack import google_hijack
from .google_hijack_rov import google_hijack_rov
from .google_origin_hijack import google_origin_hijack
from .google_origin_hijack_aspa import google_origin_hijack_aspa
from .google_sp_hijack_aspa import google_shortest_path_hijack_aspa

engine_test_configs = (
    google_hijack,
    google_hijack_rov,
    google_origin_hijack,
    google_origin_hijack_aspa,
    google_shortest_path_hijack_aspa,
)

__all__ = ["engine_test_configs"]
