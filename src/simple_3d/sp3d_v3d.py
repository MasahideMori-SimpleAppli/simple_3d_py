from __future__ import annotations

import math
import random
from typing import Any


class Sp3dV3D:
    """3D vector class for handling 3D coordinates and directions.

    Mirrors the Dart ``Sp3dV3D`` class.

    Parameters
    ----------
    x : float
        The x coordinate of the 3D vertex.
    y : float
        The y coordinate of the 3D vertex.
    z : float
        The z coordinate of the 3D vertex.
    """

    CLASS_NAME = "Sp3dV3D"
    VERSION = "22"

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def zero(cls) -> Sp3dV3D:
        """Return a vector with x, y, and z equal to 0.

        Returns
        -------
        Sp3dV3D
            A new zero vector ``(0, 0, 0)``.
        """
        return cls(0.0, 0.0, 0.0)

    def deep_copy(self) -> Sp3dV3D:
        """Return a deep copy of this vector.

        Returns
        -------
        Sp3dV3D
            A new ``Sp3dV3D`` with the same x, y, z values.
        """
        return Sp3dV3D(self.x, self.y, self.z)

    def copy_with(
        self,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
    ) -> Sp3dV3D:
        """Return a copy with only the specified values replaced.

        Parameters
        ----------
        x : float, optional
            New x coordinate. Uses the current value if ``None``.
        y : float, optional
            New y coordinate. Uses the current value if ``None``.
        z : float, optional
            New z coordinate. Uses the current value if ``None``.

        Returns
        -------
        Sp3dV3D
            A new vector with the specified components replaced.
        """
        return Sp3dV3D(
            self.x if x is None else x,
            self.y if y is None else y,
            self.z if z is None else z,
        )

    # ------------------------------------------------------------------
    # Serialization (current format, version >= 15)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert this vector to a dictionary.

        Starting with simple_3d version 15, class name and version information
        are excluded from the output.

        Returns
        -------
        dict
            A dictionary with keys ``"x"``, ``"y"``, ``"z"``.
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    @classmethod
    def from_dict(cls, src: dict[str, Any]) -> Sp3dV3D:
        """Restore a vector from a dictionary produced by :meth:`to_dict`.

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict`.

        Returns
        -------
        Sp3dV3D
            The restored vector.
        """
        return cls(src["x"], src["y"], src["z"])

    def to_dict_v14(self) -> dict[str, Any]:
        """Convert this vector to a dictionary (compatibility format for version <= 14).

        Returns
        -------
        dict
            A dictionary including ``"class_name"`` and ``"version"`` keys,
            using the older snake_case format.
        """
        return {
            "class_name": self.CLASS_NAME,
            "version": "16",
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    @classmethod
    def from_dict_v14(cls, src: dict[str, Any]) -> Sp3dV3D:
        """Restore a vector from an older-format dictionary (version <= 14).

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dV3D
            The restored vector.
        """
        return cls(src["x"], src["y"], src["z"])

    # ------------------------------------------------------------------
    # Arithmetic operators (return new vectors)
    # ------------------------------------------------------------------

    def __add__(self, other: Sp3dV3D) -> Sp3dV3D:
        """Return the element-wise sum as a new vector."""
        return Sp3dV3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Sp3dV3D) -> Sp3dV3D:
        """Return the element-wise difference as a new vector."""
        return Sp3dV3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Sp3dV3D:
        """Return this vector scaled by *scalar* as a new vector."""
        return Sp3dV3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> Sp3dV3D:
        """Return this vector divided by *scalar* as a new vector."""
        return Sp3dV3D(self.x / scalar, self.y / scalar, self.z / scalar)

    # ------------------------------------------------------------------
    # In-place mutating methods (return self for chaining)
    # ------------------------------------------------------------------

    def set(self, v: Sp3dV3D) -> Sp3dV3D:
        """Overwrite this vector's components with those of *v* and return self.

        Parameters
        ----------
        v : Sp3dV3D
            The source vector whose values are copied into this vector.

        Returns
        -------
        Sp3dV3D
            This vector after the update.
        """
        self.x = v.x
        self.y = v.y
        self.z = v.z
        return self

    def add(self, v: Sp3dV3D) -> Sp3dV3D:
        """Add *v* to this vector in place and return self.

        Parameters
        ----------
        v : Sp3dV3D
            The vector to add.

        Returns
        -------
        Sp3dV3D
            This vector after addition.
        """
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def sub(self, v: Sp3dV3D) -> Sp3dV3D:
        """Subtract *v* from this vector in place and return self.

        Parameters
        ----------
        v : Sp3dV3D
            The vector to subtract.

        Returns
        -------
        Sp3dV3D
            This vector after subtraction.
        """
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def mul(self, scalar: float) -> Sp3dV3D:
        """Multiply this vector by *scalar* in place and return self.

        Parameters
        ----------
        scalar : float
            The scalar multiplier.

        Returns
        -------
        Sp3dV3D
            This vector after multiplication.
        """
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self

    def div(self, scalar: float) -> Sp3dV3D:
        """Divide this vector by *scalar* in place and return self.

        Parameters
        ----------
        scalar : float
            The scalar divisor.

        Returns
        -------
        Sp3dV3D
            This vector after division.
        """
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self

    # ------------------------------------------------------------------
    # Vector operations
    # ------------------------------------------------------------------

    def len(self) -> float:
        """Return the Euclidean length of this vector.

        Returns
        -------
        float
            The length (magnitude) of this vector.
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def nor(self) -> Sp3dV3D:
        """Return the normalized (unit) vector.

        If this vector has zero length, a copy of this vector is returned
        unchanged.

        Returns
        -------
        Sp3dV3D
            A new unit vector pointing in the same direction, or a copy of this
            vector if its length is zero.
        """
        length = self.len()
        if length == 0:
            return self.deep_copy()
        return self / length

    def nor_safe(self, eps: float = 1e-6) -> Sp3dV3D:
        """Return a safely normalized vector for rendering or UI use.

        This method is not intended for mathematical computations.
        Degenerate, non-finite, or vectors with a length less than or equal to
        *eps* are treated as invalid and converted to ``(0, 0, 0)``.

        Parameters
        ----------
        eps : float, optional
            Epsilon threshold. Vectors with length <= *eps* return zero.
            Defaults to ``1e-6``.

        Returns
        -------
        Sp3dV3D
            A unit vector, or ``(0, 0, 0)`` if the vector is degenerate.
        """
        length = self.len()
        if not math.isfinite(length) or length <= eps:
            return Sp3dV3D(0.0, 0.0, 0.0)
        return self / length

    @staticmethod
    def dot(a: Sp3dV3D, b: Sp3dV3D) -> float:
        """Return the dot product of vectors *a* and *b*.

        Parameters
        ----------
        a : Sp3dV3D
            First vector.
        b : Sp3dV3D
            Second vector.

        Returns
        -------
        float
            The dot product ``a · b``.
        """
        return a.x * b.x + a.y * b.y + a.z * b.z

    def dot_to(self, other: Sp3dV3D) -> float:
        """Return the dot product of this vector and *other*.

        Parameters
        ----------
        other : Sp3dV3D
            The other vector.

        Returns
        -------
        float
            The dot product ``self · other``.
        """
        return Sp3dV3D.dot(self, other)

    @staticmethod
    def cross(a: Sp3dV3D, b: Sp3dV3D) -> Sp3dV3D:
        """Return the cross product of vectors *a* and *b*.

        Parameters
        ----------
        a : Sp3dV3D
            First vector.
        b : Sp3dV3D
            Second vector.

        Returns
        -------
        Sp3dV3D
            A new vector equal to ``a × b``.
        """
        return Sp3dV3D(
            a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x,
        )

    def cross_to(self, other: Sp3dV3D) -> Sp3dV3D:
        """Return the cross product of this vector and *other*.

        Parameters
        ----------
        other : Sp3dV3D
            The other vector.

        Returns
        -------
        Sp3dV3D
            A new vector equal to ``self × other``.
        """
        return Sp3dV3D.cross(self, other)

    @staticmethod
    def angle(a: Sp3dV3D, b: Sp3dV3D) -> float:
        """Return the angle in radians between vectors *a* and *b*.

        To convert to degrees: ``degrees = radian * 180 / pi``.

        Parameters
        ----------
        a : Sp3dV3D
            First vector.
        b : Sp3dV3D
            Second vector.

        Returns
        -------
        float
            The unsigned angle between *a* and *b* in radians.
        """
        return math.acos(Sp3dV3D.dot(a, b) / (a.len() * b.len()))

    def angle_to(self, other: Sp3dV3D) -> float:
        """Return the angle in radians between this vector and *other*.

        To convert to degrees: ``degrees = radian * 180 / pi``.

        Parameters
        ----------
        other : Sp3dV3D
            The other vector.

        Returns
        -------
        float
            The unsigned angle between this vector and *other* in radians.
        """
        return Sp3dV3D.angle(self, other)

    @staticmethod
    def signed_angle(a: Sp3dV3D, b: Sp3dV3D, normal: Sp3dV3D) -> float:
        """Return the signed angle in radians from vector *a* to vector *b*
        around the specified *normal* axis.

        The result range is ``(-pi, pi]``.

        The sign is determined by the right-hand rule: if the rotation from
        *a* to *b* follows the direction of *normal*, the angle is positive;
        otherwise negative.

        Input vectors do not need to be normalized. If either vector or
        *normal* has zero length, ``0`` is returned.

        Parameters
        ----------
        a : Sp3dV3D
            Starting vector (normalized internally).
        b : Sp3dV3D
            Ending vector (normalized internally).
        normal : Sp3dV3D
            Reference axis defining the rotation direction (normalized
            internally).

        Returns
        -------
        float
            Signed angle from *a* to *b* in radians, in the range
            ``(-pi, pi]``.
        """
        len_a = a.len()
        len_b = b.len()
        len_n = normal.len()
        if len_a == 0 or len_b == 0 or len_n == 0:
            return 0.0
        na = a / len_a
        nb = b / len_b
        nn = normal / len_n
        c = Sp3dV3D.cross(na, nb)
        d = max(-1.0, min(1.0, Sp3dV3D.dot(na, nb)))
        sign = Sp3dV3D.dot(nn, c)
        return math.atan2(sign, d)

    @staticmethod
    def signed_angle_on_plane(a: Sp3dV3D, b: Sp3dV3D, normal: Sp3dV3D) -> float:
        """Return the signed angle in radians from *a* to *b* after projecting
        both onto the plane defined by *normal*.

        The result range is ``(-pi, pi]``. Components along *normal* are
        ignored; only the in-plane rotation is measured.

        Parameters
        ----------
        a : Sp3dV3D
            Starting direction (projected onto the plane).
        b : Sp3dV3D
            Target direction (projected onto the plane).
        normal : Sp3dV3D
            Normal vector defining the projection plane (normalized
            internally).

        Returns
        -------
        float
            Signed in-plane angle from *a* to *b* in radians, in the range
            ``(-pi, pi]``.  Returns ``0`` if *normal* has zero length or
            either projection is zero.
        """
        len_n = normal.len()
        if len_n == 0:
            return 0.0
        n = normal / len_n
        pa = a - n * Sp3dV3D.dot(a, n)
        pb = b - n * Sp3dV3D.dot(b, n)
        return Sp3dV3D.signed_angle(pa, pb, n)

    def project_on_plane(self, normal: Sp3dV3D) -> Sp3dV3D:
        """Return the projection of this vector onto the plane defined by
        *normal*.

        The component along *normal* is removed::

            v_proj = v − (v·n̂) n̂

        *normal* does not need to be normalized. If *normal* has zero length,
        this vector is returned unchanged.

        Parameters
        ----------
        normal : Sp3dV3D
            Plane normal defining the projection plane (normalized internally).

        Returns
        -------
        Sp3dV3D
            The projected vector lying in the plane.
        """
        n_len = normal.len()
        if n_len == 0:
            return self.deep_copy()
        n = normal / n_len
        return self - n * Sp3dV3D.dot(self, n)

    def direction_on_plane(self, normal: Sp3dV3D) -> Sp3dV3D:
        """Return the unit direction of this vector projected onto the plane
        defined by *normal*.

        Equivalent to ``normalize(project_on_plane(normal))``.

        If the projected vector has zero length (this vector is parallel to
        *normal* or is a zero vector), a zero vector is returned.
        *normal* does not need to be normalized.

        Parameters
        ----------
        normal : Sp3dV3D
            Plane normal defining the projection plane (normalized internally).

        Returns
        -------
        Sp3dV3D
            The unit in-plane direction, or ``(0, 0, 0)`` if the projection
            has zero length.
        """
        p = self.project_on_plane(normal)
        length = p.len()
        if length == 0:
            return Sp3dV3D.zero()
        return p / length

    @staticmethod
    def angle_on_plane(a: Sp3dV3D, b: Sp3dV3D, normal: Sp3dV3D) -> float:
        """Return the unsigned angle in radians between *a* and *b* after
        projecting both onto the plane defined by *normal*.

        The result range is ``[0, pi]``. Components along *normal* are ignored.
        Input vectors do not need to be normalized. Returns ``0`` if either
        projected vector has zero length.

        Parameters
        ----------
        a : Sp3dV3D
            First vector (projected onto the plane).
        b : Sp3dV3D
            Second vector (projected onto the plane).
        normal : Sp3dV3D
            Plane normal defining the projection plane (normalized internally).

        Returns
        -------
        float
            Unsigned in-plane angle between *a* and *b* in radians,
            in the range ``[0, pi]``.
        """
        n_len = normal.len()
        if n_len == 0:
            return 0.0
        n = normal / n_len
        pa = a - n * Sp3dV3D.dot(a, n)
        pb = b - n * Sp3dV3D.dot(b, n)
        if pa.len() == 0 or pb.len() == 0:
            return 0.0
        return Sp3dV3D.angle(pa, pb)

    @staticmethod
    def surface_normal(face: list[Sp3dV3D]) -> Sp3dV3D:
        """Calculate and return the surface normal of a polygon.

        The vertices must be in counterclockwise order.
        This method cannot be used for degenerate polygons.

        For triangles, the normal is computed as
        ``cross(face[1] - face[0], face[1] - face[2])``.
        For polygons with four or more vertices, the reversed Newell's method
        is used.

        Parameters
        ----------
        face : list of Sp3dV3D
            The ordered list of face vertices (counterclockwise).

        Returns
        -------
        Sp3dV3D
            The (unnormalized) surface normal vector.
        """
        v_len = len(face)
        if v_len == 3:
            return Sp3dV3D.cross(face[1] - face[0], face[1] - face[2])
        # Newell's method (reversed)
        r = Sp3dV3D(0.0, 0.0, 0.0)
        for i in range(v_len):
            cv = face[i]
            nv = face[(i + 1) % v_len]
            r.x -= (cv.y - nv.y) * (cv.z + nv.z)
            r.y -= (cv.z - nv.z) * (cv.x + nv.x)
            r.z -= (cv.x - nv.x) * (cv.y + nv.y)
        return r

    @staticmethod
    def proj(v: Sp3dV3D, nor_v: Sp3dV3D) -> Sp3dV3D:
        """Return the projection of *v* onto the normalized vector *nor_v*.

        Parameters
        ----------
        v : Sp3dV3D
            The vector to project.
        nor_v : Sp3dV3D
            A normalized (unit) vector defining the projection direction.

        Returns
        -------
        Sp3dV3D
            The projection of *v* onto *nor_v*.

        Raises
        ------
        AssertionError
            If *nor_v* is not normalized (checked in debug mode only).
        """
        assert abs(nor_v.len() - 1.0) < 1e-6, "nor_v must be normalized"
        return nor_v * Sp3dV3D.dot(v, nor_v)

    @staticmethod
    def dist(a: Sp3dV3D, b: Sp3dV3D) -> float:
        """Return the Euclidean distance between *a* and *b*.

        Parameters
        ----------
        a : Sp3dV3D
            First point.
        b : Sp3dV3D
            Second point.

        Returns
        -------
        float
            The Euclidean distance ``|a - b|``.
        """
        return (a - b).len()

    def dist_to(self, other: Sp3dV3D) -> float:
        """Return the Euclidean distance from this vector to *other*.

        Parameters
        ----------
        other : Sp3dV3D
            The target point.

        Returns
        -------
        float
            The Euclidean distance ``|self - other|``.
        """
        return Sp3dV3D.dist(self, other)

    def rotated(self, nor_axis: Sp3dV3D, radian: float) -> Sp3dV3D:
        """Return a new vector that is this vector rotated around *nor_axis*.

        Parameters
        ----------
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dV3D
            A new rotated vector.
        """
        c = Sp3dV3D.proj(self, nor_axis)
        w = self - c
        return c + (w * math.cos(radian)) + (Sp3dV3D.cross(nor_axis, w) * math.sin(radian))

    def rotate(self, nor_axis: Sp3dV3D, radian: float) -> Sp3dV3D:
        """Rotate this vector around *nor_axis* in place and return self.

        Parameters
        ----------
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dV3D
            This vector after rotation.
        """
        c = self.rotated(nor_axis, radian)
        self.x = c.x
        self.y = c.y
        self.z = c.z
        return self

    def rotated_by(self, center: Sp3dV3D, nor_axis: Sp3dV3D, radian: float) -> Sp3dV3D:
        """Return a new vector that is this vector rotated around *center*.

        Parameters
        ----------
        center : Sp3dV3D
            The center of rotation.
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dV3D
            A new vector rotated around *center*.
        """
        return (self - center).rotated(nor_axis, radian) + center

    def rotate_by(self, center: Sp3dV3D, nor_axis: Sp3dV3D, radian: float) -> Sp3dV3D:
        """Rotate this vector around *center* in place and return self.

        Parameters
        ----------
        center : Sp3dV3D
            The center of rotation.
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dV3D
            This vector after rotation.
        """
        c = self.rotated_by(center, nor_axis, radian)
        self.x = c.x
        self.y = c.y
        self.z = c.z
        return self

    def is_zero(self) -> bool:
        """Return ``True`` if all components are exactly zero, otherwise ``False``.

        Returns
        -------
        bool
            ``True`` if x == y == z == 0.
        """
        return self.x == 0 and self.y == 0 and self.z == 0

    def ortho(self) -> Sp3dV3D:
        """Return a random vector orthogonal to this vector.

        If this vector is a zero vector, a copy of this vector is returned.

        Returns
        -------
        Sp3dV3D
            A vector perpendicular to this vector.
        """
        if self.is_zero():
            return self.deep_copy()
        r = random.random() + 1.0
        if self.x != 0:
            return Sp3dV3D((-self.y * r - self.z * r) / self.x, r, r)
        elif self.y != 0:
            return Sp3dV3D(r, (-self.x * r - self.z * r) / self.y, r)
        else:
            return Sp3dV3D(r, r, (-self.x * r - self.y * r) / self.z)

    @staticmethod
    def ave(v: list[Sp3dV3D]) -> Sp3dV3D:
        """Return the component-wise average of a list of vectors.

        Parameters
        ----------
        v : list of Sp3dV3D
            The vectors to average.

        Returns
        -------
        Sp3dV3D
            A new vector equal to the mean of all vectors in *v*.
        """
        n = len(v)
        sx = sy = sz = 0.0
        for i in v:
            sx += i.x
            sy += i.y
            sz += i.z
        return Sp3dV3D(sx / n, sy / n, sz / n)

    def equals(self, other: Sp3dV3D, e_range: float) -> bool:
        """Compare this vector to *other* with an allowable error range.

        Returns ``True`` if the absolute difference of each component
        is within *e_range*.

        Parameters
        ----------
        other : Sp3dV3D
            The vector to compare against.
        e_range : float
            The maximum allowable absolute difference per component.
            Must be a positive number.

        Returns
        -------
        bool
            ``True`` if all components are within *e_range* of each other.
        """
        if self is other:
            return True
        return (
            abs(self.x - other.x) <= e_range
            and abs(self.y - other.y) <= e_range
            and abs(self.z - other.z) <= e_range
        )

    # ------------------------------------------------------------------
    # Python dunder methods
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Sp3dV3D):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"[{self.x},{self.y},{self.z}]"
