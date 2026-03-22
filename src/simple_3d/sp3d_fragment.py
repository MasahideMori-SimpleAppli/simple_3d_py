from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .sp3d_face import Sp3dFace

if TYPE_CHECKING:
    from .sp3d_obj import Sp3dObj
    from .sp3d_physics import Sp3dPhysics
    from .sp3d_v3d import Sp3dV3D


class Sp3dFragment:
    """Fragment (part) class used inside ``Sp3dObj``.

    A fragment groups one or more faces and carries per-part physics and
    rendering attributes.  Mirrors the Dart ``Sp3dFragment`` class.

    Parameters
    ----------
    faces : list of Sp3dFace
        The list of faces belonging to this fragment.
    is_particle : bool, optional
        If ``True``, this fragment represents a particle.  Defaults to
        ``False``.
    r : float, optional
        Particle radius.  Used when ``is_particle`` is ``True``.
        Defaults to ``0.0``.
    physics : Sp3dPhysics or None, optional
        Physics parameters for this fragment.  Defines the behavior of
        the fragment, not the entire object.  Defaults to ``None``.
    is_touchable : bool, optional
        If ``False``, the rendered fragment is excluded from touch
        calculations.  Defaults to ``True``.
    name : str or None, optional
        The fragment name.  Defaults to ``None``.
    option : dict or None, optional
        Optional attributes that may be added for each application.  Only
        JSON-serializable values are accepted.  Defaults to ``None``.
    """

    CLASS_NAME = "Sp3dFragment"
    VERSION = "12"

    def __init__(
        self,
        faces: list[Sp3dFace],
        is_particle: bool = False,
        r: float = 0.0,
        physics: Sp3dPhysics | None = None,
        is_touchable: bool = True,
        name: str | None = None,
        option: dict[str, Any] | None = None,
    ) -> None:
        self.faces = faces
        self.is_particle = is_particle
        self.r = float(r)
        self.physics = physics
        self.is_touchable = is_touchable
        self.name = name
        self.option = option

    def deep_copy(self) -> Sp3dFragment:
        """Return a deep copy of this fragment.

        Returns
        -------
        Sp3dFragment
            A new ``Sp3dFragment`` with all fields deep-copied.
        """
        from .sp3d_physics import Sp3dPhysics  # noqa: F401

        return Sp3dFragment(
            [f.deep_copy() for f in self.faces],
            is_particle=self.is_particle,
            r=self.r,
            physics=self.physics.deep_copy() if self.physics is not None else None,
            is_touchable=self.is_touchable,
            name=self.name,
            option=dict(self.option) if self.option is not None else None,
        )

    # ------------------------------------------------------------------
    # Serialization helpers (internal list wrappers)
    # ------------------------------------------------------------------

    def _faces_to_dict(self) -> dict[str, Any]:
        return {
            "className": "Sp3dFaceList",
            "version": "1",
            "face": [f.to_dict() for f in self.faces],
        }

    @staticmethod
    def _faces_from_dict(src: dict[str, Any]) -> list[Sp3dFace]:
        return [Sp3dFace.from_dict(f) for f in src["faces"]["face"]]

    def _faces_to_dict_v14(self) -> list[dict[str, Any]]:
        return [f.to_dict_v14() for f in self.faces]

    @staticmethod
    def _faces_from_dict_v14(src: dict[str, Any]) -> list[Sp3dFace]:
        return [Sp3dFace.from_dict_v14(f) for f in src["faces"]]

    # ------------------------------------------------------------------
    # Serialization (current format)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert this fragment to a dictionary (current camelCase format).

        Starting with simple_3d version 15, class name and version information
        are excluded from the output.

        Returns
        -------
        dict
            A dictionary representing this fragment, with faces serialized
            via the internal ``Sp3dFaceList`` wrapper.
        """
        from .sp3d_physics import Sp3dPhysics  # noqa: F401

        return {
            "faces": self._faces_to_dict(),
            "isParticle": self.is_particle,
            "r": self.r,
            "physics": self.physics.to_dict() if self.physics is not None else None,
            "isTouchable": self.is_touchable,
            "name": self.name,
            "option": self.option,
        }

    @classmethod
    def from_dict(cls, src: dict[str, Any]) -> Sp3dFragment:
        """Restore a fragment from a dictionary produced by :meth:`to_dict`.

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict`.

        Returns
        -------
        Sp3dFragment
            The restored fragment.
        """
        from .sp3d_physics import Sp3dPhysics

        return cls(
            cls._faces_from_dict(src),
            is_particle=src["isParticle"],
            r=src["r"],
            physics=Sp3dPhysics.from_dict(src["physics"]) if src.get("physics") is not None else None,
            is_touchable=src["isTouchable"],
            name=src.get("name"),
            option=src.get("option"),
        )

    def to_dict_v14(self) -> dict[str, Any]:
        """Convert this fragment to a dictionary (compatibility format for version <= 14).

        Returns
        -------
        dict
            A dictionary including ``"class_name"`` and ``"version"`` keys,
            using the older snake_case format.
        """
        return {
            "class_name": self.CLASS_NAME,
            "version": "11",
            "faces": self._faces_to_dict_v14(),
            "is_particle": self.is_particle,
            "r": self.r,
            "physics": self.physics.to_dict_v14() if self.physics is not None else None,
            "is_touchable": self.is_touchable,
            "name": self.name,
            "option": self.option,
        }

    @classmethod
    def from_dict_v14(cls, src: dict[str, Any]) -> Sp3dFragment:
        """Restore a fragment from an older-format dictionary (version <= 14).

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dFragment
            The restored fragment.
        """
        from .sp3d_physics import Sp3dPhysics

        return cls(
            cls._faces_from_dict_v14(src),
            is_particle=src["is_particle"],
            r=src["r"],
            physics=Sp3dPhysics.from_dict_v14(src["physics"]) if src.get("physics") is not None else None,
            is_touchable=src.get("is_touchable", True),
            name=src.get("name"),
            option=src.get("option"),
        )

    # ------------------------------------------------------------------
    # Geometry operations
    # ------------------------------------------------------------------

    def move(self, parent: Sp3dObj, v: Sp3dV3D) -> Sp3dFragment:
        """Add *v* to all vertices of this fragment and return self.

        Parameters
        ----------
        parent : Sp3dObj
            The parent object that owns the vertex list.
        v : Sp3dV3D
            The translation vector.

        Returns
        -------
        Sp3dFragment
            This fragment after the translation.
        """
        for face in self.faces:
            face.move(parent, v)
        return self

    def rotate(self, parent: Sp3dObj, nor_axis: Sp3dV3D, radian: float) -> Sp3dFragment:
        """Rotate all vertices of this fragment around *nor_axis* and return self.

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
        Sp3dFragment
            This fragment after rotation.
        """
        for face in self.faces:
            face.rotate(parent, nor_axis, radian)
        return self

    def rotate_in_place(self, parent: Sp3dObj, nor_axis: Sp3dV3D, radian: float) -> Sp3dFragment:
        """Rotate all vertices of this fragment around its own centroid and return self.

        Unlike :meth:`rotate`, this method uses the mean coordinate of this
        fragment as the origin of rotation.

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
        Sp3dFragment
            This fragment after rotation.
        """
        from .sp3d_v3d import Sp3dV3D as _V3D

        frag_vertices: list[Sp3dV3D] = []
        for face in self.faces:
            frag_vertices.extend(face.get_vertices(parent))
        center = _V3D.ave(frag_vertices)
        diff = _V3D(0.0, 0.0, 0.0) - center
        for vtx in frag_vertices:
            vtx.add(diff)
        for vtx in frag_vertices:
            vtx.rotate(nor_axis, radian)
        neg_diff = diff * -1
        for vtx in frag_vertices:
            vtx.add(neg_diff)
        return self

    def rotate_by(
        self,
        center: Sp3dV3D,
        parent: Sp3dObj,
        nor_axis: Sp3dV3D,
        radian: float,
    ) -> Sp3dFragment:
        """Rotate all vertices of this fragment around an arbitrary *center* and return self.

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
        Sp3dFragment
            This fragment after rotation.
        """
        from .sp3d_v3d import Sp3dV3D as _V3D

        frag_vertices: list[Sp3dV3D] = []
        for face in self.faces:
            frag_vertices.extend(face.get_vertices(parent))
        diff = _V3D(0.0, 0.0, 0.0) - center
        for vtx in frag_vertices:
            vtx.add(diff)
        for vtx in frag_vertices:
            vtx.rotate(nor_axis, radian)
        neg_diff = diff * -1
        for vtx in frag_vertices:
            vtx.add(neg_diff)
        return self

    def scale(self, bp: Sp3dV3D, parent: Sp3dObj, mag: float) -> Sp3dFragment:
        """Scale all vertices of this fragment relative to *bp* and return self.

        All vertices are moved so that their distance from *bp* is multiplied
        by *mag*.  This method allows you to resize this fragment relative to
        any point.

        Parameters
        ----------
        bp : Sp3dV3D
            The base point for scaling.
        parent : Sp3dObj
            The parent object that owns the vertex list.
        mag : float
            The scale factor.

        Returns
        -------
        Sp3dFragment
            This fragment after scaling.
        """
        frag_vertices: list[Sp3dV3D] = []
        for face in self.faces:
            frag_vertices.extend(face.get_vertices(parent))
        for vtx in frag_vertices:
            vtx.set(bp + (vtx - bp) * mag)
        return self

    def get_center(self, parent: Sp3dObj) -> Sp3dV3D:
        """Return the average coordinate (centroid) of all vertices in this fragment.

        Parameters
        ----------
        parent : Sp3dObj
            The parent object that owns the vertex list.

        Returns
        -------
        Sp3dV3D
            The centroid of this fragment.
        """
        from .sp3d_v3d import Sp3dV3D as _V3D

        all_v: list[Sp3dV3D] = []
        for face in self.faces:
            all_v.extend(face.get_vertices(parent))
        return _V3D.ave(all_v)

    def reverse(self) -> None:
        """Reverse the orientation of all faces in this fragment in place."""
        for face in self.faces:
            face.reverse()

    def reversed(self) -> Sp3dFragment:
        """Return a new fragment with all faces' orientations reversed.

        Returns
        -------
        Sp3dFragment
            A deep copy of this fragment with all faces reversed.
        """
        r = self.deep_copy()
        r.reverse()
        return r

    def get_unique_vertices_indexes(self) -> list[int]:
        """Return a deduplicated list of all vertex indices used by this fragment.

        Returns
        -------
        list of int
            Unique vertex indices referenced by all faces in this fragment.
        """
        seen: set[int] = set()
        for face in self.faces:
            seen.update(face.vertex_index_list)
        return list(seen)

    def get_unique_material_indexes(self) -> list[int]:
        """Return a deduplicated list of all material indices used by this fragment.

        Returns
        -------
        list of int
            Unique material indices referenced by all faces in this fragment.
            Faces with ``material_index`` of ``None`` are excluded.
        """
        seen: set[int] = set()
        for face in self.faces:
            if face.material_index is not None:
                seen.add(face.material_index)
        return list(seen)

    def update_vertices_indexes(self, update_map: dict[int, int]) -> None:
        """Update vertex indices in all faces according to *update_map*.

        Parameters
        ----------
        update_map : dict of {int: int}
            Maps old vertex indices to new vertex indices.
        """
        for face in self.faces:
            face.update_vertices_indexes(update_map)

    def update_material_indexes(self, update_map: dict[int, int]) -> None:
        """Update material indices in all faces according to *update_map*.

        Parameters
        ----------
        update_map : dict of {int: int}
            Maps old material indices to new material indices.
        """
        for face in self.faces:
            face.update_material_indexes(update_map)
