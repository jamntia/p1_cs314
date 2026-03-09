from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Int64:
    value: int = 0

    MASK = (1 << 64) - 1
    SIGN_BIT = 1 << 63

    # --- normalization on construction ---
    def __post_init__(self):
        object.__setattr__(self, "value", self.to_unsigned(self.value))

    # --- helpers ---
    @staticmethod
    def to_unsigned(x: int) -> int:
        return int(x) & Int64.MASK

    @staticmethod
    def to_signed(u: int) -> int:
        u &= Int64.MASK
        return u - (1 << 64) if (u & Int64.SIGN_BIT) else u

    @staticmethod
    def assert_type(other, op: str) -> "Int64":
        if isinstance(other, Int64):
            return other
        raise TypeError(f"{op} only supports Int64 operands (got {type(other)!r})")

    @classmethod
    def from_unsigned(cls, u: int) -> "Int64":
        # bypass __post_init__ normalization cost if already unsigned
        obj = cls.__new__(cls)
        object.__setattr__(obj, "value", u & cls.MASK)
        return obj

    def bits(self) -> str:
        return f"{self.value:064b}"

    # --- conversions ---
    def __int__(self) -> int:
        return self.to_signed(self.value)

    def __index__(self) -> int:
        return int(self)

    def __repr__(self) -> str:
        return f"Int64({int(self)})"

    # --- arithmetic ---
    def __add__(self, other):
        o = self.assert_type(other, "+")
        return self.from_unsigned(self.value + o.value)

    def __sub__(self, other):
        o = self.assert_type(other, "-")
        return self.from_unsigned(self.value - o.value)

    def __mul__(self, other):
        o = self.assert_type(other, "*")
        return self.from_unsigned(self.value * o.value)

    def __neg__(self):
        return self.from_unsigned(-self.value)

    # --- bitwise ---
    def __xor__(self, other):
        o = self.assert_type(other, "^")
        return self.from_unsigned(self.value ^ o.value)

    def __or__(self, other):
        o = self.assert_type(other, "|")
        return self.from_unsigned(self.value | o.value)

    def __and__(self, other):
        o = self.assert_type(other, "&")
        return self.from_unsigned(self.value & o.value)

    def __invert__(self):
        return self.from_unsigned(~self.value)

    # --- shifts ---
    def __lshift__(self, other):
        o = self.assert_type(other, "<<")
        return self.from_unsigned(self.value << (int(o) & 63))

    def __rshift__(self, other):
        o = self.assert_type(other, ">>")
        return Int64(int(self) >> (int(o) & 63))

    # --- comparisons ---
    def __lt__(self, other):
        o = self.assert_type(other, "<")
        return int(self) < int(o)

    def __le__(self, other):
        o = self.assert_type(other, "<=")
        return int(self) <= int(o)

    def __gt__(self, other):
        o = self.assert_type(other, ">")
        return int(self) > int(o)

    def __ge__(self, other):
        o = self.assert_type(other, ">=")
        return int(self) >= int(o)
