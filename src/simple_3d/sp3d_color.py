from __future__ import annotations


class Sp3dColor:
    """ARGB color with float components in the range [0.0, 1.0].

    This is the Python equivalent of Flutter's ``Color`` class used by
    ``Sp3dMaterial``. All components are stored as floats in ``[0.0, 1.0]``.

    Parameters
    ----------
    a : float
        Alpha component in the range [0.0, 1.0].
    r : float
        Red component in the range [0.0, 1.0].
    g : float
        Green component in the range [0.0, 1.0].
    b : float
        Blue component in the range [0.0, 1.0].
    """

    __slots__ = ("a", "r", "g", "b")

    def __init__(self, a: float, r: float, g: float, b: float) -> None:
        self.a = float(a)
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)

    @classmethod
    def from_argb_int(cls, a: int, r: int, g: int, b: int) -> Sp3dColor:
        """Construct from integer ARGB values in the range [0, 255].

        Parameters
        ----------
        a : int
            Alpha component (0-255).
        r : int
            Red component (0-255).
        g : int
            Green component (0-255).
        b : int
            Blue component (0-255).

        Returns
        -------
        Sp3dColor
            A new color with float components converted from the given integers.
        """
        return cls(a / 255.0, r / 255.0, g / 255.0, b / 255.0)

    def to_argb_int(self) -> tuple[int, int, int, int]:
        """Return ARGB components as integers in the range [0, 255].

        Returns
        -------
        tuple of int
            ``(a, r, g, b)`` each rounded to the nearest integer in [0, 255].
        """
        return (
            round(self.a * 255),
            round(self.r * 255),
            round(self.g * 255),
            round(self.b * 255),
        )

    def deep_copy(self) -> Sp3dColor:
        """Return a deep copy of this color.

        Returns
        -------
        Sp3dColor
            A new ``Sp3dColor`` instance with the same component values.
        """
        return Sp3dColor(self.a, self.r, self.g, self.b)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Sp3dColor):
            return NotImplemented
        return self.a == other.a and self.r == other.r and self.g == other.g and self.b == other.b

    def __hash__(self) -> int:
        return hash((self.a, self.r, self.g, self.b))

    def __repr__(self) -> str:
        return f"Sp3dColor(a={self.a}, r={self.r}, g={self.g}, b={self.b})"
