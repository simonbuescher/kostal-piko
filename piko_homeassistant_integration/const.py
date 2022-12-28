import collections

from homeassistant.components.sensor import SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.const import POWER_WATT, ENERGY_KILO_WATT_HOUR

PikoInformationEntry = collections.namedtuple("InfoEntry", ["key", "xpath", "converter"])

DOMAIN = "piko-homeassistant-integration"
UNIQUE_ID = "abc-123-whatever"

PIKO_DEFAULT_USERNAME = "pvserver"
PIKO_DEFAULT_PASSWORD = "pvwr"
PIKO_DEFAULT_TIMEOUT = 10
PIKO_RUNNING_ENTRY = PikoInformationEntry(
    key="RUNNING",
    xpath="/html/body/form/font/table[2]/tr[8]/td[3]",
    converter=lambda x: not x == "Aus"
)
PIKO_CURRENT_ENTRY = PikoInformationEntry(
    key="CURRENT",
    xpath="/html/body/form/font/table[2]/tr[4]/td[3]",
    converter=lambda x: float(x) if x != "x x x&nbsp" else 0.0
)
PIKO_TODAY_ENTRY = PikoInformationEntry(
    key="TODAY",
    xpath="/html/body/form/font/table[2]/tr[6]/td[6]",
    converter=float
)
PIKO_TOTAL_ENTRY = PikoInformationEntry(
    key="TOTAL",
    xpath="/html/body/form/font/table[2]/tr[4]/td[6]",
    converter=float
)
PIKO_INFORMATION_ENTRIES = (
    PIKO_RUNNING_ENTRY,
    PIKO_CURRENT_ENTRY,
    PIKO_TODAY_ENTRY,
    PIKO_TOTAL_ENTRY
)

SENSOR_TYPES = (
    SensorEntityDescription(
        device_class="running",
        key=PIKO_RUNNING_ENTRY.key,
        name="Piko Running",
    ),
    SensorEntityDescription(
        device_class=SensorDeviceClass.POWER,
        key=PIKO_CURRENT_ENTRY.key,
        name="Piko Current Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        device_class=SensorDeviceClass.ENERGY,
        key=PIKO_TODAY_ENTRY.key,
        name="Piko Generated Energy Today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        device_class=SensorDeviceClass.ENERGY,
        key=PIKO_TOTAL_ENTRY.key,
        name="Piko Generated Energy Total",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    )
)
