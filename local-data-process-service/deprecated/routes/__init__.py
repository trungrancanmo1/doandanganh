from .sensor_routes import sensor_bp
from .feed_routes import feed_bp
import warnings


warnings.warn(
    "The 'my_package' package is deprecated and will be removed in future versions. "
    "Consider using 'new_package' instead.",
    DeprecationWarning,
    stacklevel=2
)
