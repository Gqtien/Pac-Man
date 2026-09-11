from enum import Enum


class Color(Enum):
    RED = b"\x00\x00\xff\xff"
    PINK = b"\xff\xb8\xff\xff"
    CYAN = b"\xff\xff\x00\xff"
    ORANGE = b"\x52\xb8\xff\xff"
