from __future__ import annotations

from typing import Any

from .sp3d_color import Sp3dColor


class Sp3dMaterial:
    """Material class for ``Sp3dObj``.

    Handles color, fill, stroke, image, and texture information for a face.
    Mirrors the Dart ``Sp3dMaterial`` class.

    Colors use :class:`Sp3dColor` (ARGB float components in ``[0.0, 1.0]``),
    which corresponds to Flutter's ``Color`` class in the Dart version.

    Texture coordinates are stored as a list of ``(dx, dy)`` float tuples,
    corresponding to Flutter's ``Offset`` in the Dart version.

    Parameters
    ----------
    bg : Sp3dColor
        Background (fill) color.
    is_fill : bool
        If ``True``, fill the face with ``bg``.  If ``False``, draw stroke
        lines only.
    stroke_width : float
        The stroke line width.
    stroke_color : Sp3dColor
        The stroke line color.
    image_index : int or None, optional
        Index into the parent object's image list.  When not ``None`` and
        ``is_fill`` is ``True`` and the face has 4 vertices, fills the face
        with the image.  The vertex order is clockwise from the upper-left.
    texture_coordinates : list of (float, float) or None, optional
        Coordinates specifying the part of the image to cut out.  Specify
        counterclockwise with a triangle (3 vertices) or a rectangle
        (two triangles, 6 vertices).
    name : str or None, optional
        The material name.
    option : dict or None, optional
        Optional attributes that may be added for each application.  Only
        JSON-serializable values are accepted.
    """

    CLASS_NAME = "Sp3dMaterial"
    VERSION = "12"

    def __init__(
        self,
        bg: Sp3dColor,
        is_fill: bool,
        stroke_width: float,
        stroke_color: Sp3dColor,
        image_index: int | None = None,
        texture_coordinates: list[tuple[float, float]] | None = None,
        name: str | None = None,
        option: dict[str, Any] | None = None,
    ) -> None:
        self.bg = bg
        self.is_fill = is_fill
        self.stroke_width = float(stroke_width)
        self.stroke_color = stroke_color
        self.image_index = image_index
        self.texture_coordinates = texture_coordinates
        self.name = name
        self.option = option

    def deep_copy(self) -> Sp3dMaterial:
        """Return a deep copy of this material.

        Returns
        -------
        Sp3dMaterial
            A new ``Sp3dMaterial`` with all fields deep-copied.
        """
        tc = (
            list(self.texture_coordinates)
            if self.texture_coordinates is not None
            else None
        )
        return Sp3dMaterial(
            self.bg.deep_copy(),
            self.is_fill,
            self.stroke_width,
            self.stroke_color.deep_copy(),
            image_index=self.image_index,
            texture_coordinates=tc,
            name=self.name,
            option=dict(self.option) if self.option is not None else None,
        )

    def copy_with(
        self,
        bg: Sp3dColor | None = None,
        is_fill: bool | None = None,
        stroke_width: float | None = None,
        stroke_color: Sp3dColor | None = None,
        image_index: int | None = None,
        texture_coordinates: list[tuple[float, float]] | None = None,
        name: str | None = None,
        option: dict[str, Any] | None = None,
    ) -> Sp3dMaterial:
        """Return a copy with only the specified values replaced.

        Parameters
        ----------
        bg : Sp3dColor, optional
            New background color.
        is_fill : bool, optional
            New fill flag.
        stroke_width : float, optional
            New stroke width.
        stroke_color : Sp3dColor, optional
            New stroke color.
        image_index : int or None, optional
            New image index.
        texture_coordinates : list of (float, float) or None, optional
            New texture coordinates.
        name : str or None, optional
            New material name.
        option : dict or None, optional
            New option dictionary.

        Returns
        -------
        Sp3dMaterial
            A new material with the specified fields replaced.
        """
        tc = texture_coordinates
        if tc is None and self.texture_coordinates is not None:
            tc = list(self.texture_coordinates)
        return Sp3dMaterial(
            bg if bg is not None else self.bg.deep_copy(),
            is_fill if is_fill is not None else self.is_fill,
            stroke_width if stroke_width is not None else self.stroke_width,
            stroke_color if stroke_color is not None else self.stroke_color.deep_copy(),
            image_index=image_index if image_index is not None else self.image_index,
            texture_coordinates=tc,
            name=name if name is not None else self.name,
            option=option if option is not None else (dict(self.option) if self.option is not None else None),
        )

    # ------------------------------------------------------------------
    # Serialization (current format)
    # ------------------------------------------------------------------

    def to_dict(self, version: int = 2) -> dict[str, Any]:
        """Convert this material to a dictionary (current camelCase format).

        Starting with simple_3d version 15, class name and version information
        are excluded from the output.

        Parameters
        ----------
        version : int, optional
            The ``Sp3dMaterialList`` version number.  If ``1``, ARGB components
            are serialized as integers (0-255).  If ``2`` or higher, they are
            serialized as floats (0.0-1.0).  Defaults to ``2``.

        Returns
        -------
        dict
            A dictionary representing this material.
        """
        tc: list[float] | None = None
        if self.texture_coordinates is not None:
            tc = []
            for dx, dy in self.texture_coordinates:
                tc.append(dx)
                tc.append(dy)

        if version == 1:
            bg_v = list(self.bg.to_argb_int())
            sc_v = list(self.stroke_color.to_argb_int())
        else:
            bg_v = [self.bg.a, self.bg.r, self.bg.g, self.bg.b]
            sc_v = [self.stroke_color.a, self.stroke_color.r, self.stroke_color.g, self.stroke_color.b]

        return {
            "bg": bg_v,
            "isFill": self.is_fill,
            "strokeWidth": self.stroke_width,
            "strokeColor": sc_v,
            "imageIndex": self.image_index,
            "textureCoordinates": tc,
            "name": self.name,
            "option": self.option,
        }

    @classmethod
    def from_dict(cls, src: dict[str, Any], version: int = 2) -> Sp3dMaterial:
        """Restore a material from a dictionary produced by :meth:`to_dict`.

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict`.
        version : int, optional
            The ``Sp3dMaterialList`` version number used when serializing.
            If ``1``, ARGB values are read as integers (0-255).  If ``2``
            or higher, they are read as floats (0.0-1.0).  Defaults to ``2``.

        Returns
        -------
        Sp3dMaterial
            The restored material.
        """
        if version == 1:
            bg = Sp3dColor.from_argb_int(*src["bg"])
            sc = Sp3dColor.from_argb_int(*src["strokeColor"])
        else:
            bg = Sp3dColor(*src["bg"])
            sc = Sp3dColor(*src["strokeColor"])

        tc: list[tuple[float, float]] | None = None
        if src.get("textureCoordinates") is not None:
            coords = src["textureCoordinates"]
            tc = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]

        return cls(
            bg,
            src["isFill"],
            src["strokeWidth"],
            sc,
            image_index=src.get("imageIndex"),
            texture_coordinates=tc,
            name=src.get("name"),
            option=src.get("option"),
        )

    def to_dict_v14(self) -> dict[str, Any]:
        """Convert this material to a dictionary (compatibility format for version <= 14).

        ARGB values are serialized as integers (0-255) in this format.

        Returns
        -------
        dict
            A dictionary including ``"class_name"`` and ``"version"`` keys,
            using the older snake_case format with integer ARGB values.
        """
        tc: list[float] | None = None
        if self.texture_coordinates is not None:
            tc = []
            for dx, dy in self.texture_coordinates:
                tc.append(dx)
                tc.append(dy)

        bg_v = list(self.bg.to_argb_int())
        sc_v = list(self.stroke_color.to_argb_int())

        return {
            "class_name": self.CLASS_NAME,
            "version": "9",
            "bg": bg_v,
            "is_fill": self.is_fill,
            "stroke_width": self.stroke_width,
            "stroke_color": sc_v,
            "image_index": self.image_index,
            "texture_coordinates": tc,
            "name": self.name,
            "option": self.option,
        }

    @classmethod
    def from_dict_v14(cls, src: dict[str, Any]) -> Sp3dMaterial:
        """Restore a material from an older-format dictionary (version <= 14).

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dMaterial
            The restored material.
        """
        bg = Sp3dColor.from_argb_int(*src["bg"])
        sc = Sp3dColor.from_argb_int(*src["stroke_color"])

        tc: list[tuple[float, float]] | None = None
        if src.get("texture_coordinates") is not None:
            coords = src["texture_coordinates"]
            tc = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]

        return cls(
            bg,
            src["is_fill"],
            src["stroke_width"],
            sc,
            image_index=src.get("image_index"),
            texture_coordinates=tc,
            name=src.get("name"),
            option=src.get("option"),
        )

    # ------------------------------------------------------------------
    # Index update
    # ------------------------------------------------------------------

    def update_image_indexes(self, update_map: dict[int, int]) -> None:
        """Update the image index according to *update_map*.

        Parameters
        ----------
        update_map : dict of {int: int}
            Maps old image indices to new image indices.  If ``image_index``
            is ``None`` or not in the map, it is left unchanged.
        """
        if self.image_index is not None and self.image_index in update_map:
            self.image_index = update_map[self.image_index]

    # ------------------------------------------------------------------
    # Equality
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Sp3dMaterial):
            return NotImplemented
        return (
            self.bg == other.bg
            and self.is_fill == other.is_fill
            and self.stroke_width == other.stroke_width
            and self.stroke_color == other.stroke_color
            and self.image_index == other.image_index
            and self.texture_coordinates == other.texture_coordinates
            and self.name == other.name
            and self.option == other.option
        )

    def __hash__(self) -> int:
        tc_key = tuple(self.texture_coordinates) if self.texture_coordinates is not None else None
        opt_key = tuple(sorted(self.option.items())) if self.option is not None else None
        return hash((self.bg, self.is_fill, self.stroke_width, self.stroke_color, self.image_index, tc_key, self.name, opt_key))
