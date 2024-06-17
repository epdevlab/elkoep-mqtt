import json
from dataclasses import dataclass
from operator import itemgetter
from typing import Any, Dict, List, Optional, Union

from inelsmqtt import const


@dataclass
class Bit:
    is_on: bool
    addr: str


@dataclass
class Number:
    value: int
    addr: str


@dataclass
class SimpleRelay:
    """Create simple relay"""

    is_on: bool


@dataclass
class Relay(SimpleRelay):
    """Create relay with overflow detection."""

    overflow: bool


@dataclass
class Shutter:
    """Create a simple shutter."""

    state: const.Shutter_state
    is_closed: Optional[bool]


@dataclass
class Shutter_pos(Shutter):
    """Create a shutter with position."""

    position: int
    set_pos: bool


@dataclass
class SimpleLight:
    brightness: int


@dataclass
class LightCoaToa(SimpleLight):
    toa: bool
    coa: bool


@dataclass
class RGBLight(SimpleLight):
    r: int
    g: int
    b: int


@dataclass
class AOUTLight(SimpleLight):
    aout_coa: bool


@dataclass
class WarmLight(SimpleLight):
    relative_ct: int


@dataclass
class DALILight(SimpleLight):
    alert_dali_communication: bool
    alert_dali_power: bool


def new_object(**kwargs):
    """Create new anonymous object."""
    return type("Object", (), kwargs)


def break_into_bytes(line: str):
    if len(line) % 2 == 0:
        return [line[i : i + 2] for i in range(0, len(line), 2)]
    return []


def trim_inels_status_values(
    inels_status_value: str, selector: Dict[str, Union[int, tuple]], fragment: str, jointer: str
) -> str:
    """Trim inels status from broker into the pure string."""
    data = inels_status_value.split("\n")[:-1]

    # Ensure the selector for the fragment is a tuple, even if it's a single value
    indices = selector[fragment]
    if isinstance(indices, int):
        indices = (indices,)  # Make it a tuple if it's not

    selected = itemgetter(*indices)(data)
    return jointer.join(selected)


def trim_inels_status_bytes(inels_status_value: str, selector: Dict[str, Any], fragment: str) -> List[str]:
    """Split inels status section into its constituting bytes"""
    data = inels_status_value.split("\n")[:-1]

    selected = itemgetter(*selector[fragment])(data)
    return selected


def parse_formated_json(data):
    addr_val_list = []
    data = json.loads(data)
    for addr, val in data["state"].items():
        addr_val_list.append((addr, val))
    return addr_val_list


class Formatter:
    @staticmethod
    def format_data(data: List[int]) -> str:
        """Formats a list of integers into a newline-separated hexadecimal string with a trailing newline."""
        return "\n".join(f"{x:02X}" for x in data) + "\n"
