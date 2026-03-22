from __future__ import annotations

import base64
from typing import Any

from .enum_sp3d_draw_mode import EnumSp3dDrawMode
from .sp3d_fragment import Sp3dFragment
from .sp3d_material import Sp3dMaterial
from .sp3d_v3d import Sp3dV3D


class Sp3dObj:
    """Main 3D object class for Simple 3D Format.

    All data describing a single 3D object — vertices, fragments, materials,
    and images — is contained in one instance.  The object can be serialized
    to a JSON-compatible dictionary and restored from it, with full
    compatibility with the Dart ``Sp3dObj`` class.

    The ``option`` fields of this object and its internal elements can be
    freely extended for each application.  Only JSON-serializable values may
    be placed in ``option``.

    Parameters
    ----------
    vertices : list of Sp3dV3D
        The 3D vertex list.
    fragments : list of Sp3dFragment
        The fragment list.  Each fragment contains face and physics
        information.
    materials : list of Sp3dMaterial
        The material list.  Each material contains color and texture
        information.
    images : list of bytes
        The image data list (PNG bytes).  Referenced by materials via
        ``image_index``.
    id : str or None, optional
        Object ID.  Defaults to ``None``.
    name : str or None, optional
        Object name.  Defaults to ``None``.
    author : str or None, optional
        Object author name.  Mainly for distribution; ``None`` is preferred
        during calculations.  Defaults to ``None``.
    physics : Sp3dPhysics or None, optional
        Physics parameters for the entire object.  Defaults to ``None``.
    option : dict or None, optional
        Optional attributes that may be added for each application.  Only
        JSON-serializable values are accepted.  Defaults to ``None``.
    layer_num : int, optional
        Drawing priority in the depth direction.  When enabled by the
        renderer, objects are drawn in ascending order of this value.
        Defaults to ``0``.
    draw_mode : EnumSp3dDrawMode, optional
        Drawing mode for the renderer.  Use ``rect`` when speed is required
        but 3D structure is not, such as scatter plots.
        Defaults to :attr:`EnumSp3dDrawMode.normal`.
    """

    CLASS_NAME = "Sp3dObj"
    VERSION = "22"

    def __init__(
        self,
        vertices: list[Sp3dV3D],
        fragments: list[Sp3dFragment],
        materials: list[Sp3dMaterial],
        images: list[bytes],
        id: str | None = None,
        name: str | None = None,
        author: str | None = None,
        physics=None,
        option: dict[str, Any] | None = None,
        layer_num: int = 0,
        draw_mode: EnumSp3dDrawMode = EnumSp3dDrawMode.normal,
    ) -> None:
        self.vertices = vertices
        self.fragments = fragments
        self.materials = materials
        self.images = images
        self.id = id
        self.name = name
        self.author = author
        self.physics = physics
        self.option = option
        self.layer_num = layer_num
        self.draw_mode = draw_mode

    def deep_copy(self) -> Sp3dObj:
        """Return a deep copy of this object.

        Returns
        -------
        Sp3dObj
            A new ``Sp3dObj`` with all fields deep-copied.
        """
        from .sp3d_physics import Sp3dPhysics  # noqa: F401

        return Sp3dObj(
            [v.deep_copy() for v in self.vertices],
            [f.deep_copy() for f in self.fragments],
            [m.deep_copy() for m in self.materials],
            [bytes(img) for img in self.images],
            id=self.id,
            name=self.name,
            author=self.author,
            physics=self.physics.deep_copy() if self.physics is not None else None,
            option=dict(self.option) if self.option is not None else None,
            layer_num=self.layer_num,
            draw_mode=self.draw_mode,
        )

    def clone(self) -> Sp3dObj:
        """Return a deep copy of this object (alias for :meth:`deep_copy`).

        Returns
        -------
        Sp3dObj
            A new ``Sp3dObj`` with all fields deep-copied.
        """
        return self.deep_copy()

    # ------------------------------------------------------------------
    # Serialization (current format, version >= 21)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert this object to a dictionary (current camelCase format).

        The output is compatible with Dart ``Sp3dObj`` version 21 and later.
        Vertices, fragments, and materials are wrapped in internal list
        container dictionaries (``Sp3dV3DList``, ``Sp3dFragmentList``,
        ``Sp3dMaterialList``).  Images are encoded as base64 strings.

        Returns
        -------
        dict
            A JSON-serializable dictionary representing this object.
        """
        from .sp3d_physics import Sp3dPhysics  # noqa: F401

        vertices_dict: dict[str, Any] = {
            "className": "Sp3dV3DList",
            "version": "1",
            "v": [v.to_dict() for v in self.vertices],
        }

        fragments_dict: dict[str, Any] = {
            "className": "Sp3dFragmentList",
            "version": "1",
            "fragment": [f.to_dict() for f in self.fragments],
        }

        materials_dict: dict[str, Any] = {
            "className": "Sp3dMaterialList",
            "version": "2",
            "material": [m.to_dict(version=2) for m in self.materials],
        }

        return {
            "className": self.CLASS_NAME,
            "version": self.VERSION,
            "vertices": vertices_dict,
            "fragments": fragments_dict,
            "materials": materials_dict,
            "images": [base64.b64encode(img).decode("ascii") for img in self.images],
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "physics": self.physics.to_dict() if self.physics is not None else None,
            "option": self.option,
            "layerNum": self.layer_num,
            "drawMode": self.draw_mode.value,
        }

    @classmethod
    def from_dict(cls, src: dict[str, Any]) -> Sp3dObj:
        """Restore an object from a dictionary produced by :meth:`to_dict`.

        Automatically detects the version of the source dictionary and calls
        the appropriate loader.  Dictionaries with version <= 20 are loaded
        via the v14-compatible path.

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict` or :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dObj
            The restored object.
        """
        version_num = int(src.get("version", 0))
        if version_num <= 20:
            return cls._from_dict_v14(src)

        from .sp3d_physics import Sp3dPhysics

        vertices = [Sp3dV3D.from_dict(v) for v in src["vertices"]["v"]]

        fragments = [Sp3dFragment.from_dict(f) for f in src["fragments"]["fragment"]]

        mat_version = int(src["materials"].get("version", 2))
        materials = [
            Sp3dMaterial.from_dict(m, mat_version)
            for m in src["materials"]["material"]
        ]

        images = [base64.b64decode(i) for i in src["images"]]

        return cls(
            vertices,
            fragments,
            materials,
            images,
            id=src.get("id"),
            name=src.get("name"),
            author=src.get("author"),
            physics=Sp3dPhysics.from_dict(src["physics"]) if src.get("physics") is not None else None,
            option=src.get("option"),
            layer_num=src.get("layerNum", 0),
            draw_mode=EnumSp3dDrawMode(src.get("drawMode", "normal")),
        )

    def to_dict_v14(self) -> dict[str, Any]:
        """Convert this object to a dictionary (compatibility format for version <= 14).

        Returns
        -------
        dict
            A dictionary including ``"class_name"`` and ``"version"`` keys,
            using the older snake_case format.  Vertices, fragments, and
            materials are stored as plain lists rather than wrapped
            container dictionaries.
        """
        return {
            "class_name": self.CLASS_NAME,
            "version": "20",
            "vertices": [v.to_dict_v14() for v in self.vertices],
            "fragments": [f.to_dict_v14() for f in self.fragments],
            "materials": [m.to_dict_v14() for m in self.materials],
            "images": [base64.b64encode(img).decode("ascii") for img in self.images],
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "physics": self.physics.to_dict_v14() if self.physics is not None else None,
            "option": self.option,
            "layer_num": self.layer_num,
            "draw_mode": self.draw_mode.value,
        }

    @classmethod
    def _from_dict_v14(cls, src: dict[str, Any]) -> Sp3dObj:
        """Restore an object from an older-format dictionary (version <= 14).

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dObj
            The restored object.
        """
        from .sp3d_physics import Sp3dPhysics

        vertices = [Sp3dV3D.from_dict_v14(v) for v in src["vertices"]]
        fragments = [Sp3dFragment.from_dict_v14(f) for f in src["fragments"]]
        materials = [Sp3dMaterial.from_dict_v14(m) for m in src["materials"]]

        version_str = str(src.get("version", "0"))
        try:
            ver_float = float(version_str)
        except ValueError:
            ver_float = 0.0

        if ver_float >= 9:
            images = [base64.b64decode(i) for i in src["images"]]
        else:
            images = [bytes(list(i)) for i in src["images"]]

        physics = None
        if src.get("physics") is not None:
            physics = Sp3dPhysics.from_dict_v14(src["physics"])

        layer_num = src.get("layer_num", 0)
        draw_mode = EnumSp3dDrawMode.normal
        if "draw_mode" in src:
            raw = src["draw_mode"]
            if version_str == "10":
                draw_mode = EnumSp3dDrawMode.normal if raw == 0 else EnumSp3dDrawMode.rect
            else:
                draw_mode = EnumSp3dDrawMode(raw)

        return cls(
            vertices,
            fragments,
            materials,
            images,
            id=src.get("id"),
            name=src.get("name"),
            author=src.get("author"),
            physics=physics,
            option=src.get("option"),
            layer_num=layer_num,
            draw_mode=draw_mode,
        )

    # ------------------------------------------------------------------
    # Geometry operations
    # ------------------------------------------------------------------

    def move(self, v: Sp3dV3D) -> Sp3dObj:
        """Add *v* to all vertices of this object and return self.

        Parameters
        ----------
        v : Sp3dV3D
            The translation vector.

        Returns
        -------
        Sp3dObj
            This object after the translation.
        """
        for vtx in self.vertices:
            vtx.add(v)
        return self

    def rotate(self, nor_axis: Sp3dV3D, radian: float) -> Sp3dObj:
        """Rotate all vertices of this object around *nor_axis* and return self.

        Parameters
        ----------
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dObj
            This object after rotation.
        """
        for vtx in self.vertices:
            vtx.rotate(nor_axis, radian)
        return self

    def rotate_in_place(self, nor_axis: Sp3dV3D, radian: float) -> Sp3dObj:
        """Rotate all vertices of this object around its own centroid and return self.

        Unlike :meth:`rotate`, this method uses the mean coordinate of the
        object as the origin of rotation.

        Parameters
        ----------
        nor_axis : Sp3dV3D
            Normalized rotation axis vector.
        radian : float
            Rotation angle in radians. To convert from degrees:
            ``radian = degree * pi / 180``.

        Returns
        -------
        Sp3dObj
            This object after rotation.
        """
        center = self.get_center()
        diff = Sp3dV3D(0.0, 0.0, 0.0) - center
        self.move(diff)
        self.rotate(nor_axis, radian)
        self.move(diff * -1)
        return self

    def rotate_by(self, center: Sp3dV3D, nor_axis: Sp3dV3D, radian: float) -> Sp3dObj:
        """Rotate all vertices of this object around an arbitrary *center* and return self.

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
        Sp3dObj
            This object after rotation.
        """
        diff = Sp3dV3D(0.0, 0.0, 0.0) - center
        self.move(diff)
        self.rotate(nor_axis, radian)
        self.move(diff * -1)
        return self

    def get_center(self) -> Sp3dV3D:
        """Return the average coordinate (centroid) of all vertices.

        Returns
        -------
        Sp3dV3D
            The centroid of this object.
        """
        return Sp3dV3D.ave(self.vertices)

    def merge(self, other: Sp3dObj) -> Sp3dObj:
        """Merge *other* into this object in place and return self.

        This operation is high-cost.  The ``id``, ``name``, ``author``,
        ``physics``, ``option``, ``layer_num``, and ``draw_mode`` of this
        object are preserved unchanged.

        Parameters
        ----------
        other : Sp3dObj
            The object to merge into this one.  A deep copy is made
            internally so *other* is not modified.

        Returns
        -------
        Sp3dObj
            This object after merging.
        """
        copy_other = other.deep_copy()
        my_vertices_len = len(self.vertices)
        my_material_len = len(self.materials)
        my_image_len = len(self.images)

        for mat in copy_other.materials:
            if mat.image_index is not None:
                mat.image_index += my_image_len

        from .sp3d_face import Sp3dFace  # noqa: F401

        for frg in copy_other.fragments:
            for face in frg.faces:
                if face.material_index is not None:
                    face.material_index += my_material_len
                face.vertex_index_list = [idx + my_vertices_len for idx in face.vertex_index_list]

        self.images.extend(copy_other.images)
        self.materials.extend(copy_other.materials)
        self.vertices.extend(copy_other.vertices)
        self.fragments.extend(copy_other.fragments)
        return self

    def reverse(self) -> None:
        """Reverse the orientation of all faces in all fragments in place."""
        for frg in self.fragments:
            frg.reverse()

    def reversed(self) -> Sp3dObj:
        """Return a new object with all faces' orientations reversed.

        Returns
        -------
        Sp3dObj
            A deep copy of this object with all faces reversed.
        """
        r = self.deep_copy()
        r.reverse()
        return r

    def set_is_touchable_flags(self, is_touchable: bool) -> Sp3dObj:
        """Set the ``is_touchable`` flag of all fragments and return self.

        Parameters
        ----------
        is_touchable : bool
            If ``False``, all rendered fragments will be excluded from
            touch calculations.

        Returns
        -------
        Sp3dObj
            This object after updating all flags.
        """
        for frg in self.fragments:
            frg.is_touchable = is_touchable
        return self

    def add_vertices(self, v: list[Sp3dV3D]) -> list[int]:
        """Append vertices to this object and return their new indices.

        Parameters
        ----------
        v : list of Sp3dV3D
            The vertices to add.

        Returns
        -------
        list of int
            The indices of the newly added vertices in the ``vertices`` list.
        """
        now_len = len(self.vertices)
        result = []
        for i, vtx in enumerate(v):
            self.vertices.append(vtx)
            result.append(now_len + i)
        return result

    def add_materials(self, m: list[Sp3dMaterial]) -> list[int]:
        """Append materials to this object and return their new indices.

        This method adds each material as-is, even if it already exists in
        the list.

        Parameters
        ----------
        m : list of Sp3dMaterial
            The materials to add.

        Returns
        -------
        list of int
            The indices of the newly added materials in the ``materials`` list.
        """
        now_len = len(self.materials)
        result = []
        for i, mat in enumerate(m):
            self.materials.append(mat)
            result.append(now_len + i)
        return result

    def add_material_if_needed(self, m: Sp3dMaterial) -> int:
        """Add *m* to the material list if it does not already exist, and return its index.

        Materials are compared by content equality.  If *m* already exists,
        its existing index is returned without adding a duplicate.

        Parameters
        ----------
        m : Sp3dMaterial
            The material to add if not already present.

        Returns
        -------
        int
            The index of *m* in the ``materials`` list.
        """
        try:
            return self.materials.index(m)
        except ValueError:
            idx = len(self.materials)
            self.materials.append(m)
            return idx

    def add_images(self, images: list[bytes]) -> list[int]:
        """Append image data to this object and return their new indices.

        This method adds each image as-is, even if it already exists in
        the list.

        Parameters
        ----------
        images : list of bytes
            The image data (PNG bytes) to add.

        Returns
        -------
        list of int
            The indices of the newly added images in the ``images`` list.
        """
        now_len = len(self.images)
        result = []
        for i, img in enumerate(images):
            self.images.append(img)
            result.append(now_len + i)
        return result

    def resize(self, mag: float) -> Sp3dObj:
        """Resize this object by *mag* relative to its centroid and return self.

        Parameters
        ----------
        mag : float
            The scale factor.  Values greater than 1 enlarge the object;
            values less than 1 shrink it.

        Returns
        -------
        Sp3dObj
            This object after resizing.
        """
        c = self.get_center()
        for vtx in self.vertices:
            vtx.set(c + (vtx - c) * mag)
        return self

    def cleaning(self) -> Sp3dObj:
        """Remove unused vertices, materials, and images, and adjust internal indices.

        This method is processing-intensive.  After calling it, the vertex
        and material indices stored in ``Sp3dFace``, and the image index
        stored in ``Sp3dMaterial``, may have changed.

        Returns
        -------
        Sp3dObj
            This object after cleaning.
        """
        from .sp3d_face import Sp3dFace  # noqa: F401

        all_faces: list[Sp3dFace] = []
        for frg in self.fragments:
            all_faces.extend(frg.faces)

        # --- remove unused images ---
        image_uses = [False] * len(self.images)
        image_index_targets: list[Sp3dFace] = []
        material_index_targets: list[Sp3dFace] = []

        for face in all_faces:
            if face.material_index is not None:
                material_index_targets.append(face)
                img_idx = self.materials[face.material_index].image_index
                if img_idx is not None:
                    image_uses[img_idx] = True
                    image_index_targets.append(face)

        for i in range(len(image_uses) - 1, -1, -1):
            if not image_uses[i]:
                self.images.pop(i)
                for face in image_index_targets:
                    mat = self.materials[face.material_index]  # type: ignore[index]
                    if mat.image_index is not None and mat.image_index > i:
                        mat.image_index -= 1

        # --- remove unused materials ---
        material_uses = [False] * len(self.materials)
        for face in material_index_targets:
            material_uses[face.material_index] = True  # type: ignore[index]

        for i in range(len(material_uses) - 1, -1, -1):
            if not material_uses[i]:
                self.materials.pop(i)
                for face in material_index_targets:
                    if face.material_index is not None and face.material_index > i:
                        face.material_index -= 1

        # --- remove unused vertices ---
        vertices_uses = [False] * len(self.vertices)
        for face in all_faces:
            for idx in face.vertex_index_list:
                vertices_uses[idx] = True

        for i in range(len(vertices_uses) - 1, -1, -1):
            if not vertices_uses[i]:
                self.vertices.pop(i)
                for face in all_faces:
                    face.vertex_index_list = [
                        idx - 1 if idx > i else idx
                        for idx in face.vertex_index_list
                    ]

        return self

    def clone_part(self, targets: list[Sp3dFragment]) -> Sp3dObj:
        """Return a new ``Sp3dObj`` consisting of copies of the specified fragments.

        Only vertices, materials, and images actually referenced by *targets*
        are included.  All internal indices are remapped accordingly.

        Parameters
        ----------
        targets : list of Sp3dFragment
            The fragments to copy into the new object.  These must belong to
            this object.

        Returns
        -------
        Sp3dObj
            A new ``Sp3dObj`` containing only the specified fragments and their
            dependencies.
        """
        vertices_map: dict[int, int] = {}
        material_map: dict[int, int] = {}
        image_map: dict[int, int] = {}
        result = Sp3dObj([], [], [], [])

        for frg in targets:
            result.fragments.append(frg.deep_copy())
            for pre_index in frg.get_unique_vertices_indexes():
                if pre_index not in vertices_map:
                    new_index = len(result.vertices)
                    result.vertices.append(self.vertices[pre_index].deep_copy())
                    vertices_map[pre_index] = new_index

            for pre_index in frg.get_unique_material_indexes():
                if pre_index not in material_map:
                    new_index = len(result.materials)
                    result.materials.append(self.materials[pre_index].deep_copy())
                    material_map[pre_index] = new_index

                pre_img_index = self.materials[pre_index].image_index
                if pre_img_index is not None and pre_img_index not in image_map:
                    new_index = len(result.images)
                    result.images.append(bytes(self.images[pre_img_index]))
                    image_map[pre_img_index] = new_index

        for frg in result.fragments:
            frg.update_vertices_indexes(vertices_map)
            frg.update_material_indexes(material_map)

        for mat in result.materials:
            mat.update_image_indexes(image_map)

        return result
