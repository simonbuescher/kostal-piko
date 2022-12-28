import collections
from typing import Iterable

InfoEntry = collections.namedtuple("InfoEntry", ["key", "unit", "xpath", "converter"])

DEFAULT_USERNAME = "pvserver"
DEFAULT_PASSWORD = "pvwr"
DEFAULT_TIMEOUT = 2


class InfoEntries:
    RUNNING = InfoEntry(
        key="RUNNING",
        unit="",
        xpath="/html/body/form/font/table[2]/tr[8]/td[3]",
        converter=lambda x: not x == "Aus"
    )
    CURRENT = InfoEntry(
        key="CURRENT",
        unit="W",
        xpath="/html/body/form/font/table[2]/tr[4]/td[3]",
        converter=lambda x: float(x) if x != "x x x&nbsp" else 0.0
    )
    TODAY = InfoEntry(
        key="TODAY",
        unit="kWh",
        xpath="/html/body/form/font/table[2]/tr[6]/td[6]",
        converter=float
    )
    TOTAL = InfoEntry(
        key="TOTAL",
        unit="kWh",
        xpath="/html/body/form/font/table[2]/tr[4]/td[6]",
        converter=float
    )

    @staticmethod
    def all() -> Iterable[InfoEntry]:
        return [
            InfoEntries.RUNNING,
            InfoEntries.CURRENT,
            InfoEntries.TODAY,
            InfoEntries.TOTAL,
        ]

    @staticmethod
    def get_by_key(key: str) -> InfoEntry:
        for entry in InfoEntries.all():
            if entry.key == key:
                return entry

        raise ValueError(f"Unknown key {key}")
