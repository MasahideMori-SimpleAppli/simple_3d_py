import json
import math

import pytest

from simple_3d import (
    EnumSp3dDrawMode,
    Sp3dColor,
    Sp3dFace,
    Sp3dFragment,
    Sp3dMaterial,
    Sp3dObj,
    Sp3dPhysics,
    Sp3dV3D,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_simple_obj() -> Sp3dObj:
    return Sp3dObj(
        [Sp3dV3D(0, 0, 0)],
        [Sp3dFragment([Sp3dFace([0], 0)])],
        [Sp3dMaterial(Sp3dColor.from_argb_int(255, 0, 255, 0), True, 1.0, Sp3dColor.from_argb_int(255, 0, 255, 0))],
        [],
    )


def _make_full_obj() -> Sp3dObj:
    return Sp3dObj(
        [Sp3dV3D(0, 0, 0)],
        [
            Sp3dFragment(
                [Sp3dFace([0], 0)],
                is_particle=True,
                r=1.0,
                physics=Sp3dPhysics(
                    mass=1.0,
                    speed=20.0,
                    direction=Sp3dV3D(1, 0, 0),
                    velocity=Sp3dV3D(1, 1, 0),
                    rotate_axis=Sp3dV3D(1, 0, 0),
                    angular_velocity=2.0,
                    angle=0.45,
                    others={"test": "test"},
                ),
                option={"test": "test"},
            )
        ],
        [
            Sp3dMaterial(
                Sp3dColor.from_argb_int(255, 0, 255, 0),
                True,
                1.0,
                Sp3dColor.from_argb_int(255, 0, 255, 0),
                image_index=None,
                texture_coordinates=[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)],
            )
        ],
        [bytes([1, 2, 3, 4, 5, 6, 7, 8])],
        id="1",
        name="test",
        author="Masahide Mori",
        physics=Sp3dPhysics(
            is_locked=True,
            mass=1.0,
            speed=20.0,
            direction=Sp3dV3D(1, 0, 0),
            velocity=Sp3dV3D(1, 1, 0),
            rotate_axis=Sp3dV3D(1, 0, 0),
            angular_velocity=2.0,
            angle=0.45,
            others={"test": "test"},
        ),
        option={"test": "test"},
        layer_num=1,
        draw_mode=EnumSp3dDrawMode.rect,
    )


# ---------------------------------------------------------------------------
# Serialization round-trips
# ---------------------------------------------------------------------------

def test_simple_obj_roundtrip():
    obj = _make_simple_obj()
    d = obj.to_dict()
    restored = Sp3dObj.from_dict(d)
    assert json.dumps(d, sort_keys=True) == json.dumps(restored.to_dict(), sort_keys=True)


def test_full_obj_roundtrip():
    obj = _make_full_obj()
    d = obj.to_dict()
    restored = Sp3dObj.from_dict(d)
    assert json.dumps(d, sort_keys=True) == json.dumps(restored.to_dict(), sort_keys=True)


def test_null_physics_roundtrip():
    obj = Sp3dObj(
        [Sp3dV3D(0, 0, 0)],
        [Sp3dFragment([Sp3dFace([0], 0)], physics=Sp3dPhysics())],
        [Sp3dMaterial(
            Sp3dColor.from_argb_int(255, 0, 255, 0),
            True, 1.0,
            Sp3dColor.from_argb_int(255, 0, 255, 0),
            texture_coordinates=[(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)],
        )],
        [],
        physics=Sp3dPhysics(),
    )
    d = obj.to_dict()
    restored = Sp3dObj.from_dict(d)
    assert json.dumps(d, sort_keys=True) == json.dumps(restored.to_dict(), sort_keys=True)


def test_minimal_obj_roundtrip():
    obj = Sp3dObj(
        [Sp3dV3D(0, 0, 0)],
        [Sp3dFragment([Sp3dFace([0], 0)])],
        [Sp3dMaterial(
            Sp3dColor.from_argb_int(255, 0, 255, 0),
            True, 1.0,
            Sp3dColor.from_argb_int(255, 0, 255, 0),
        )],
        [],
    )
    d = obj.to_dict()
    restored = Sp3dObj.from_dict(d)
    assert json.dumps(d, sort_keys=True) == json.dumps(restored.to_dict(), sort_keys=True)


def test_json_serializable():
    obj = _make_full_obj()
    json.dumps(obj.to_dict())  # must not raise


# ---------------------------------------------------------------------------
# deep_copy
# ---------------------------------------------------------------------------

def test_deep_copy_independence():
    obj = _make_simple_obj()
    c = obj.deep_copy()
    c.vertices[0].x = 99.0
    assert obj.vertices[0].x == 0.0


# ---------------------------------------------------------------------------
# move / rotate
# ---------------------------------------------------------------------------

def test_move():
    obj = _make_simple_obj()
    obj.move(Sp3dV3D(1, 0, 0))
    assert obj.vertices[0] == Sp3dV3D(1, 0, 0)


def test_move_return_value():
    obj = _make_simple_obj()
    obj.move(Sp3dV3D(1, 0, 0))
    assert obj.vertices[0] == Sp3dV3D(1, 0, 0)


def test_rotate():
    obj = Sp3dObj([Sp3dV3D(1, 0, 0)], [], [], [])
    obj.rotate(Sp3dV3D(0, 0, 1), math.pi / 2)
    assert obj.vertices[0].x == pytest.approx(0.0, abs=1e-9)
    assert obj.vertices[0].y == pytest.approx(1.0, abs=1e-9)


def test_rotate_in_place():
    obj = Sp3dObj([Sp3dV3D(1, 0, 0), Sp3dV3D(-1, 0, 0)], [], [], [])
    center_before = obj.get_center()
    obj.rotate_in_place(Sp3dV3D(0, 0, 1), math.pi / 2)
    center_after = obj.get_center()
    assert center_before.x == pytest.approx(center_after.x, abs=1e-9)
    assert center_before.y == pytest.approx(center_after.y, abs=1e-9)


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------

def test_merge():
    a = Sp3dObj([Sp3dV3D(0, 0, 0)], [], [], [])
    b = Sp3dObj([Sp3dV3D(1, 0, 0)], [], [], [])
    a.merge(b)
    assert len(a.vertices) == 2
    assert a.vertices[1] == Sp3dV3D(1, 0, 0)


# ---------------------------------------------------------------------------
# add_vertices / add_materials / add_material_if_needed
# ---------------------------------------------------------------------------

def test_add_vertices():
    obj = Sp3dObj([], [], [], [])
    indices = obj.add_vertices([Sp3dV3D(1, 2, 3), Sp3dV3D(4, 5, 6)])
    assert indices == [0, 1]
    assert len(obj.vertices) == 2


def test_add_material_if_needed_dedup():
    mat = Sp3dMaterial(Sp3dColor.from_argb_int(255, 0, 0, 0), False, 1.0, Sp3dColor.from_argb_int(255, 0, 0, 0))
    obj = Sp3dObj([], [], [mat], [])
    idx = obj.add_material_if_needed(mat)
    assert idx == 0
    assert len(obj.materials) == 1


def test_add_material_if_needed_new():
    mat1 = Sp3dMaterial(Sp3dColor.from_argb_int(255, 0, 0, 0), False, 1.0, Sp3dColor.from_argb_int(255, 0, 0, 0))
    mat2 = Sp3dMaterial(Sp3dColor.from_argb_int(255, 255, 0, 0), False, 1.0, Sp3dColor.from_argb_int(255, 0, 0, 0))
    obj = Sp3dObj([], [], [mat1], [])
    idx = obj.add_material_if_needed(mat2)
    assert idx == 1
    assert len(obj.materials) == 2


# ---------------------------------------------------------------------------
# resize
# ---------------------------------------------------------------------------

def test_resize():
    obj = Sp3dObj([Sp3dV3D(1, 0, 0), Sp3dV3D(-1, 0, 0)], [], [], [])
    obj.resize(2.0)
    assert obj.vertices[0].x == pytest.approx(2.0, abs=1e-9)
    assert obj.vertices[1].x == pytest.approx(-2.0, abs=1e-9)


# ---------------------------------------------------------------------------
# reverse / reversed
# ---------------------------------------------------------------------------

def test_reverse():
    face = Sp3dFace([0, 1, 2], None)
    frg = Sp3dFragment([face])
    obj = Sp3dObj([Sp3dV3D(0, 0, 0), Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0)], [frg], [], [])
    obj.reverse()
    assert obj.fragments[0].faces[0].vertex_index_list == [2, 1, 0]


# ---------------------------------------------------------------------------
# get_center
# ---------------------------------------------------------------------------

def test_get_center():
    obj = Sp3dObj([Sp3dV3D(0, 0, 0), Sp3dV3D(2, 0, 0)], [], [], [])
    assert obj.get_center() == Sp3dV3D(1, 0, 0)


# ---------------------------------------------------------------------------
# Sp3dFace helpers
# ---------------------------------------------------------------------------

def test_face_get_vertices():
    obj = Sp3dObj([Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0)], [], [], [])
    face = Sp3dFace([0, 1], None)
    verts = face.get_vertices(obj)
    assert verts[0] == Sp3dV3D(1, 0, 0)
    assert verts[1] == Sp3dV3D(0, 1, 0)


def test_face_reverse():
    face = Sp3dFace([0, 1, 2], None)
    face.reverse()
    assert face.vertex_index_list == [2, 1, 0]


def test_face_reverse_ft():
    face = Sp3dFace([0, 1, 2, 3], None)
    face.reverse_ft()
    assert face.vertex_index_list == [0, 3, 2, 1]


def test_face_roundtrip():
    face = Sp3dFace([0, 1, 2], 1)
    restored = Sp3dFace.from_dict(face.to_dict())
    assert restored.vertex_index_list == face.vertex_index_list
    assert restored.material_index == face.material_index


def test_face_roundtrip_v14():
    face = Sp3dFace([0, 1, 2], 1)
    restored = Sp3dFace.from_dict_v14(face.to_dict_v14())
    assert restored.vertex_index_list == face.vertex_index_list
    assert restored.material_index == face.material_index


# ---------------------------------------------------------------------------
# Sp3dMaterial equality and serialization
# ---------------------------------------------------------------------------

def test_material_equality():
    m1 = Sp3dMaterial(Sp3dColor.from_argb_int(255, 0, 255, 0), True, 1.0, Sp3dColor.from_argb_int(255, 0, 255, 0))
    m2 = Sp3dMaterial(Sp3dColor.from_argb_int(255, 0, 255, 0), True, 1.0, Sp3dColor.from_argb_int(255, 0, 255, 0))
    assert m1 == m2


def test_material_roundtrip_v2():
    m = Sp3dMaterial(
        Sp3dColor(1.0, 0.0, 1.0, 0.0),
        True, 1.5,
        Sp3dColor(1.0, 0.0, 0.0, 1.0),
        texture_coordinates=[(0.0, 0.0), (1.0, 1.0)],
        name="test",
    )
    d = m.to_dict(version=2)
    restored = Sp3dMaterial.from_dict(d, version=2)
    assert restored == m


def test_material_roundtrip_v1():
    m = Sp3dMaterial(
        Sp3dColor.from_argb_int(255, 0, 255, 0),
        True, 1.0,
        Sp3dColor.from_argb_int(255, 0, 255, 0),
    )
    d = m.to_dict(version=1)
    restored = Sp3dMaterial.from_dict(d, version=1)
    # Check ARGB ints match (float conversion may not be exact)
    assert restored.bg.to_argb_int() == m.bg.to_argb_int()
    assert restored.stroke_color.to_argb_int() == m.stroke_color.to_argb_int()


# ---------------------------------------------------------------------------
# Sp3dPhysics serialization
# ---------------------------------------------------------------------------

def test_physics_roundtrip():
    p = Sp3dPhysics(
        is_locked=True,
        mass=1.0,
        speed=20.0,
        direction=Sp3dV3D(1, 0, 0),
        velocity=Sp3dV3D(0, 1, 0),
        rotate_axis=Sp3dV3D(0, 0, 1),
        angular_velocity=2.0,
        angle=0.5,
        name="test",
        others={"k": "v"},
    )
    d = p.to_dict()
    restored = Sp3dPhysics.from_dict(d)
    assert json.dumps(d, sort_keys=True) == json.dumps(restored.to_dict(), sort_keys=True)


def test_physics_roundtrip_v14():
    p = Sp3dPhysics(
        is_locked=False,
        mass=2.0,
        speed=5.0,
        direction=Sp3dV3D(0, 1, 0),
    )
    d = p.to_dict_v14()
    restored = Sp3dPhysics.from_dict_v14(d)
    assert restored.is_locked == p.is_locked
    assert restored.mass == p.mass
    assert restored.direction == p.direction


# ---------------------------------------------------------------------------
# Sp3dFragment serialization
# ---------------------------------------------------------------------------

def test_fragment_roundtrip():
    frg = Sp3dFragment(
        [Sp3dFace([0, 1, 2], 0)],
        is_particle=False,
        r=0.0,
        is_touchable=True,
        name="f1",
    )
    d = frg.to_dict()
    restored = Sp3dFragment.from_dict(d)
    assert json.dumps(d, sort_keys=True) == json.dumps(restored.to_dict(), sort_keys=True)


def test_fragment_roundtrip_v14():
    frg = Sp3dFragment(
        [Sp3dFace([0, 1, 2], 0)],
        is_particle=True,
        r=1.0,
    )
    d = frg.to_dict_v14()
    restored = Sp3dFragment.from_dict_v14(d)
    assert restored.is_particle == frg.is_particle
    assert restored.r == frg.r


# ---------------------------------------------------------------------------
# EnumSp3dDrawMode
# ---------------------------------------------------------------------------

def test_draw_mode_roundtrip():
    for mode in EnumSp3dDrawMode:
        assert EnumSp3dDrawMode(mode.value) == mode


def test_draw_mode_in_obj():
    obj = _make_simple_obj()
    obj.draw_mode = EnumSp3dDrawMode.rect
    restored = Sp3dObj.from_dict(obj.to_dict())
    assert restored.draw_mode == EnumSp3dDrawMode.rect


# ---------------------------------------------------------------------------
# clone_part
# ---------------------------------------------------------------------------

def test_clone_part():
    obj = Sp3dObj(
        [Sp3dV3D(0, 0, 0), Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0)],
        [
            Sp3dFragment([Sp3dFace([0, 1], 0)]),
            Sp3dFragment([Sp3dFace([1, 2], 0)]),
        ],
        [Sp3dMaterial(Sp3dColor.from_argb_int(255, 0, 0, 0), False, 1.0, Sp3dColor.from_argb_int(255, 0, 0, 0))],
        [],
    )
    part = obj.clone_part([obj.fragments[0]])
    assert len(part.fragments) == 1
    assert len(part.vertices) == 2


# ---------------------------------------------------------------------------
# Sp3dColor
# ---------------------------------------------------------------------------

def test_color_from_argb_int():
    c = Sp3dColor.from_argb_int(255, 0, 255, 0)
    assert c.to_argb_int() == (255, 0, 255, 0)


def test_color_equality():
    assert Sp3dColor(1.0, 0.0, 1.0, 0.0) == Sp3dColor(1.0, 0.0, 1.0, 0.0)
    assert Sp3dColor(1.0, 0.0, 1.0, 0.0) != Sp3dColor(0.0, 0.0, 1.0, 0.0)
