from .mqttclient import mqtt_listener
from .mqttclient import mqtt_client
from .restclient import rest_client
from .restclient import add_feed


import warnings

warnings.warn(
    "The 'my_package' package is deprecated and will be removed in future versions. "
    "Consider using 'new_package' instead.",
    DeprecationWarning,
    stacklevel=2
)
