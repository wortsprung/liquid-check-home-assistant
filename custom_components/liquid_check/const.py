"""Constants for the Liquid Check integration."""

DOMAIN = "liquid_check"

CONF_NAME = "name"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_USE_HTTPS = "use_https"
CONF_TANK_NAME = "tank_name"
CONF_MAX_VOLUME = "max_volume"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_MEASURE_DELAY = "measure_delay"
CONF_TIMEOUT = "timeout"
CONF_KEEP_LAST_VALUE = "keep_last_value"

DEFAULT_NAME = "Liquid Check IBC"
DEFAULT_HOST = "192.168.10.252"
DEFAULT_PORT = 80
DEFAULT_USE_HTTPS = False
DEFAULT_TANK_NAME = "IBC Container"
DEFAULT_MAX_VOLUME = 1110
DEFAULT_SCAN_INTERVAL = 120
DEFAULT_MEASURE_DELAY = 10
DEFAULT_TIMEOUT = 10
DEFAULT_KEEP_LAST_VALUE = True

PLATFORMS = ["sensor", "binary_sensor", "button"]

SERVICE_REFRESH = "refresh"
SERVICE_MEASURE = "measure"
