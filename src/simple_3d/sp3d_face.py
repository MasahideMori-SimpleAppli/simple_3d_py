from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .sp3d_obj import Sp3dObj
    from .sp3d_v3d import Sp3dV3D


class Sp3dFace:
    """Face class used inside ``Sp3dFragment``.

    Handles vertex index information and an optional material reference for
    a single polygon face.  Mirrors the Dart ``Sp3dFace`` class.

    Parameters
    ----------
    vertex_index_list : list of int
        Ordered list of 3D vertex indices (counterclockwise from upper-left).
    material_index : int or None
        Index into the parent object's materials list.  ``None`` disables
        material assignment for this face.
    """

    CLASS_NAME = "Sp3dFace"
    VERSION = "13"

    def __init__(
        self,
        vertex_index_list: list[int],
        material_index: int | None,
    ) -> None:
        self.vertex_index_list: list[int] = list(vertex_index_list)
        self.material_index: int | None = material_index

    def deep_copy(self) -> Sp3dFace:
        """Return a deep copy of this face.

        Returns
        -------
        Sp3dFace
            A new ``Sp3dFace`` with copied index lists.
        """
        return Sp3dFace(list(self.vertex_index_list), self.material_index)

    # ------------------------------------------------------------------
    # Serialization (current format)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert this face to a dictionary (current camelCase format).

        Starting with simple_3d version 15, class name and version information
        are excluded from the output.

        Returns
        -------
        dict
            A dictionary with keys ``"vertexIndexList"`` and
            ``"materialIndex"``.
        """
        return {
            "vertexIndexList": list(self.vertex_index_list),
            "materialIndex": self.material_index,
        }

    @classmethod
    def from_dict(cls, src: dict[str, Any]) -> Sp3dFace:
        """Restore a face from a dictionary produced by :meth:`to_dict`.

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict`.

        Returns
        -------
        Sp3dFace
            The restored face.
        """
        return cls(
            [int(i) for i in src["vertexIndexList"]],
            src["materialIndex"],
        )

    def to_dict_v14(self) -> dict[str, Any]:
        """Convert this face to a dictionary (compatibility format for version <= 14).

        Returns
        -------
        dict
            A dictionary including ``"class_name"`` and ``"version"`` keys,
            using the older snake_case format.
        """
        return {
            "class_name": self.CLASS_NAME,
            "version": "12",
            "vertex_index_list": list(self.vertex_index_list),
            "material_index": self.material_index,
        }

    @classmethod
    def from_dict_v14(cls, src: dict[str, Any]) -> Sp3dFace:
        """Restore a face from an older-format dictionary (version <= 14).

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dFace
            The restored face.
        """
        return cls(
            [int(i) for i in src["vertex_index_list"]],
            src["material_index"],
        )

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------

    def get_vertices(self, obj: Sp3dObj) -> list[Sp3dV3D]:
        """Return the ``Sp3dV3D`` vertices referenced by this face.

        Parameters
        ----------
        obj : Sp3dObj
            The parent object that owns the vertex list.

        Returns
        -------
        list of Sp3dV3D
            The vertices of this face in index order.
        """
        return [obj.vertices[i] for i in self.vertex_index_list]

    def reverse(self) -> None:
        """Reverse the orientation of this face in place.

        Internally, the order of the referenced vertex indices is reversed.
        Has no effect if the face has fewer than three vertices.
        """
        if len(self.vertex_index_list) > 2:
            self.vertex_index_list = list(reversed(self.vertex_index_list))

    def reversed(self) -> Sp3dFace:
        """Return a new face with the orientation of this face reversed.

        Internally, the order of the referenced vertex indices is reversed.

        Returns
        -------
        Sp3dFace
            A new face with the reversed vertex order.
        """
        r = self.deep_copy()
        r.reverse()
        return r

    def reverse_ft(self) -> None:
        """Reverse the orientation of this face in place, keeping the first vertex fixed.

        The order of all vertex indices except the first is reversed.
        Has no effect if the face has fewer than three vertices.
        """
        if len(self.vertex_index_list) > 2:
            first = self.vertex_index_list[0]
            rest = list(reversed(self.vertex_index_list[1:]))
            self.vertex_index_list = [first] + rest

    def reversed_ft(self) -> Sp3dFace:
        """Return a new face with orientation reversed, keeping the first vertex fixed.

        Returns
        -------
        Sp3dFace
            A new face with the first vertex unchanged and the remaining
            vertices in reversed order.
        """
        r = self.deep_copy()
        r.reverse_ft()
        return r

    def move(self, parent: Sp3dObj, v: Sp3dV3D) -> Sp3dFace:
        """Add *v* to all vertices of this face and return self.

        Parameters
        ----------
        parent : Sp3dObj
            The parent object that owns the vertex list.
        v : Sp3dV3D
            The translation vector.

        Returns
        -------
        Sp3dFace
            This face after the translation.
        """
        for i in self.vertex_index_list:
            parent.vertices[i].add(v)
        return self

    def rotate(self, parent: Sp3dObj, nor_axis: Sp3dV3D, radian: float) -> Sp3dFace:
        """Rotate all vertices of this face around *nor_axis* and return self.

        Parameters
        ----------
        parent : Sp3dObj
            The parent object that owns the vertex list.
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dFace
            This face after rotation.
        """
        for i in self.vertex_index_list:
            parent.vertices[i].rotate(nor_axis, radian)
        return self

    def rotate_in_place(self, parent: Sp3dObj, nor_axis: Sp3dV3D, radian: float) -> Sp3dFace:
        """Rotate all vertices of this face around its own center and return self.

        Unlike :meth:`rotate`, this method uses the mean coordinate of this
        face as the origin of rotation.

        Parameters
        ----------
        parent : Sp3dObj
            The parent object that owns the vertex list.
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dFace
            This face after rotation.
        """
        from .sp3d_v3d import Sp3dV3D as _V3D

        center = self.get_center(parent)
        diff = _V3D(0.0, 0.0, 0.0) - center
        self.move(parent, diff)
        self.rotate(parent, nor_axis, radian)
        self.move(parent, diff * -1)
        return self

    def rotate_by(
        self,
        center: Sp3dV3D,
        parent: Sp3dObj,
        nor_axis: Sp3dV3D,
        radian: float,
    ) -> Sp3dFace:
        """Rotate all vertices of this face around an arbitrary *center* and return self.

        Parameters
        ----------
        center : Sp3dV3D
            The center of rotation.
        parent : Sp3dObj
            The parent object that owns the vertex list.
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dFace
            This face after rotation.
        """
        from .sp3d_v3d import Sp3dV3D as _V3D

        diff = _V3D(0.0, 0.0, 0.0) - center
        self.move(parent, diff)
        self.rotate(parent, nor_axis, radian)
        self.move(parent, diff * -1)
        return self

    def get_center(self, parent: Sp3dObj) -> Sp3dV3D:
        """Return the average coordinate (centroid) of this face's vertices.

        Parameters
        ----------
        parent : Sp3dObj
            The parent object that owns the vertex list.

        Returns
        -------
        Sp3dV3D
            The centroid of this face.
        """
        from .sp3d_v3d import Sp3dV3D as _V3D

        return _V3D.ave(self.get_vertices(parent))

    def update_vertices_indexes(self, update_map: dict[int, int]) -> None:
        """Update vertex indices according to *update_map*.

        Parameters
        ----------
        update_map : dict of {int: int}
            Maps old vertex indices to new vertex indices.  Indices not
            present in the map are left unchanged.
        """
        self.vertex_index_list = [update_map.get(i, i) for i in self.vertex_index_list]

    def update_material_indexes(self, update_map: dict[int, int]) -> None:
        """Update the material index according to *update_map*.

        Parameters
        ----------
        update_map : dict of {int: int}
            Maps old material indices to new material indices.  If
            ``material_index`` is ``None`` or not in the map, it is left
            unchanged.
        """
        if self.material_index is not None and self.material_index in update_map:
            self.material_index = update_map[self.material_index]
