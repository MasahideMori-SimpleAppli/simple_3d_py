import json
import math

import pytest

from simple_3d import Sp3dV3D


# ---------------------------------------------------------------------------
# Basic construction and equality
# ---------------------------------------------------------------------------

def test_zero():
    v = Sp3dV3D.zero()
    assert v.x == 0.0 and v.y == 0.0 and v.z == 0.0


def test_equality():
    assert Sp3dV3D(1, 2, 3) == Sp3dV3D(1, 2, 3)
    assert Sp3dV3D(1, 2, 3) != Sp3dV3D(1, 2, 4)


def test_hash():
    assert hash(Sp3dV3D(1, 2, 3)) == hash(Sp3dV3D(1, 2, 3))


def test_repr():
    assert repr(Sp3dV3D(1, 2, 3)) == "[1.0,2.0,3.0]"


# ---------------------------------------------------------------------------
# Arithmetic operators
# ---------------------------------------------------------------------------

def test_add():
    assert Sp3dV3D(1, 1, 1) + Sp3dV3D(2, 2, 2) == Sp3dV3D(3, 3, 3)


def test_sub():
    assert Sp3dV3D(2, 2, 2) - Sp3dV3D(1, 1, 1) == Sp3dV3D(1, 1, 1)


def test_mul():
    assert Sp3dV3D(1, 1, 1) * 3 == Sp3dV3D(3, 3, 3)


def test_div():
    assert Sp3dV3D(3, 3, 3) / 3 == Sp3dV3D(1, 1, 1)


# ---------------------------------------------------------------------------
# In-place mutating methods
# ---------------------------------------------------------------------------

def test_add_inplace():
    v1 = Sp3dV3D(1, 1, 1)
    v1.add(Sp3dV3D(2, 2, 2))
    assert v1 == Sp3dV3D(3, 3, 3)


def test_sub_inplace():
    v2 = Sp3dV3D(2, 2, 2)
    v2.sub(Sp3dV3D(1, 1, 1))
    assert v2 == Sp3dV3D(1, 1, 1)


def test_mul_inplace():
    v = Sp3dV3D(1, 1, 1)
    v.mul(3)
    assert v == Sp3dV3D(3, 3, 3)


def test_div_inplace():
    v = Sp3dV3D(3, 3, 3)
    v.div(3)
    assert v == Sp3dV3D(1, 1, 1)


def test_set():
    v = Sp3dV3D(0, 0, 0)
    v.set(Sp3dV3D(1, 2, 3))
    assert v == Sp3dV3D(1, 2, 3)


# ---------------------------------------------------------------------------
# Vector operations
# ---------------------------------------------------------------------------

def test_len():
    assert Sp3dV3D(3, 4, 0).len() == pytest.approx(5.0)


def test_nor():
    v = Sp3dV3D(3, 0, 0).nor()
    assert v == Sp3dV3D(1, 0, 0)


def test_nor_zero_returns_copy():
    v = Sp3dV3D.zero().nor()
    assert v == Sp3dV3D.zero()


def test_nor_safe():
    v = Sp3dV3D(0, 0, 1e-7).nor_safe()
    assert v == Sp3dV3D.zero()


def test_dot():
    assert Sp3dV3D.dot(Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0)) == 0.0
    assert Sp3dV3D.dot(Sp3dV3D(1, 0, 0), Sp3dV3D(1, 0, 0)) == 1.0


def test_cross():
    c = Sp3dV3D.cross(Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0))
    assert c == Sp3dV3D(0, 0, 1)


def test_angle():
    a = Sp3dV3D.angle(Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0))
    assert a == pytest.approx(math.pi / 2)


def test_dist():
    assert Sp3dV3D.dist(Sp3dV3D(0, 0, 0), Sp3dV3D(3, 4, 0)) == pytest.approx(5.0)


def test_equals_with_range():
    v1 = Sp3dV3D(1, 1, 1)
    v2 = Sp3dV3D(2, 2, 2)
    assert (v1 * 2.5).equals(v2, 0.6)
    assert (v1 * 1.5).equals(v2, 0.6)
    assert not (v1 * 2.7).equals(v2, 0.6)


def test_deep_copy():
    v = Sp3dV3D(1, 2, 3)
    c = v.deep_copy()
    c.x = 99
    assert v.x == 1.0


def test_copy_with():
    v = Sp3dV3D(1, 2, 3)
    c = v.copy_with(y=9)
    assert c == Sp3dV3D(1, 9, 3)
    assert v == Sp3dV3D(1, 2, 3)


def test_is_zero():
    assert Sp3dV3D.zero().is_zero()
    assert not Sp3dV3D(0, 0, 1).is_zero()


def test_ave():
    avg = Sp3dV3D.ave([Sp3dV3D(0, 0, 0), Sp3dV3D(2, 2, 2)])
    assert avg == Sp3dV3D(1, 1, 1)


# ---------------------------------------------------------------------------
# Rotation
# ---------------------------------------------------------------------------

def test_rotated_90_deg_around_z():
    x = Sp3dV3D(1, 0, 0)
    z = Sp3dV3D(0, 0, 1)
    r = x.rotated(z, math.pi / 2)
    assert r.x == pytest.approx(0.0, abs=1e-9)
    assert r.y == pytest.approx(1.0, abs=1e-9)
    assert r.z == pytest.approx(0.0, abs=1e-9)


def test_rotate_mutates():
    v = Sp3dV3D(1, 0, 0)
    z = Sp3dV3D(0, 0, 1)
    v.rotate(z, math.pi / 2)
    assert v.y == pytest.approx(1.0, abs=1e-9)


# ---------------------------------------------------------------------------
# signed_angle
# ---------------------------------------------------------------------------

def test_signed_angle_ccw():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    assert Sp3dV3D.signed_angle(x, y, z) == pytest.approx(math.pi / 2, abs=1e-9)


def test_signed_angle_cw():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    assert Sp3dV3D.signed_angle(y, x, z) == pytest.approx(-math.pi / 2, abs=1e-9)


def test_signed_angle_zero_input():
    zero = Sp3dV3D.zero()
    x = Sp3dV3D(1, 0, 0)
    z = Sp3dV3D(0, 0, 1)
    assert Sp3dV3D.signed_angle(zero, x, z) == 0.0
    assert Sp3dV3D.signed_angle(x, x, zero) == 0.0


def test_signed_angle_normal_flip():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    a1 = Sp3dV3D.signed_angle(x, y, z)
    a2 = Sp3dV3D.signed_angle(x, y, z * -1.0)
    assert a1 == pytest.approx(-a2, abs=1e-9)


def test_signed_angle_scale_invariant():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    assert Sp3dV3D.signed_angle(x, y, z * 10.0) == pytest.approx(math.pi / 2, abs=1e-9)


# ---------------------------------------------------------------------------
# signed_angle_on_plane
# ---------------------------------------------------------------------------

def test_signed_angle_on_plane_basic():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    a = Sp3dV3D(1, 0, 10)
    b = Sp3dV3D(0, 1, 20)
    assert Sp3dV3D.signed_angle_on_plane(a, b, z) == pytest.approx(math.pi / 2, abs=1e-9)


def test_signed_angle_on_plane_zero_projection():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    zero = Sp3dV3D.zero()
    parallel = Sp3dV3D(0, 0, 5)
    assert Sp3dV3D.signed_angle_on_plane(parallel, x, z) == 0.0
    assert Sp3dV3D.signed_angle_on_plane(x, y, zero) == 0.0


# ---------------------------------------------------------------------------
# angle_on_plane
# ---------------------------------------------------------------------------

def test_angle_on_plane_unsigned():
    x = Sp3dV3D(1, 0, 0)
    y = Sp3dV3D(0, 1, 0)
    z = Sp3dV3D(0, 0, 1)
    assert Sp3dV3D.angle_on_plane(x, y, z) == pytest.approx(math.pi / 2, abs=1e-9)
    assert Sp3dV3D.angle_on_plane(y, x, z) == pytest.approx(math.pi / 2, abs=1e-9)


# ---------------------------------------------------------------------------
# project_on_plane / direction_on_plane
# ---------------------------------------------------------------------------

def test_project_on_plane():
    v = Sp3dV3D(1, 1, 1)
    y = Sp3dV3D(0, 1, 0)
    p = v.project_on_plane(y)
    assert p.x == pytest.approx(1.0)
    assert p.y == pytest.approx(0.0)
    assert p.z == pytest.approx(1.0)


def test_project_on_plane_zero_normal():
    v = Sp3dV3D(1, 2, 3)
    p = v.project_on_plane(Sp3dV3D.zero())
    assert p == v


def test_direction_on_plane():
    v = Sp3dV3D(10, 10, 0)
    z = Sp3dV3D(0, 0, 1)
    d = v.direction_on_plane(z)
    assert d.len() == pytest.approx(1.0, abs=1e-9)
    assert d.x == pytest.approx(math.cos(math.pi / 4), abs=1e-9)


def test_direction_on_plane_parallel_returns_zero():
    v = Sp3dV3D(0, 0, 5)
    z = Sp3dV3D(0, 0, 1)
    assert v.direction_on_plane(z) == Sp3dV3D.zero()


# ---------------------------------------------------------------------------
# surface_normal
# ---------------------------------------------------------------------------

def test_surface_normal_triangle():
    # Dart computes cross(face[1]-face[0], face[1]-face[2]) for triangles,
    # which for this CCW face in XY-plane gives (0,0,-1).
    face = [Sp3dV3D(0, 0, 0), Sp3dV3D(1, 0, 0), Sp3dV3D(0, 1, 0)]
    n = Sp3dV3D.surface_normal(face).nor()
    assert n.z == pytest.approx(-1.0, abs=1e-9)
    assert n.x == pytest.approx(0.0, abs=1e-9)
    assert n.y == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Serialization round-trip
# ---------------------------------------------------------------------------

def test_to_dict_from_dict():
    v = Sp3dV3D(1.5, -2.0, 3.0)
    assert Sp3dV3D.from_dict(v.to_dict()) == v


def test_to_dict_v14_from_dict_v14():
    v = Sp3dV3D(1.5, -2.0, 3.0)
    assert Sp3dV3D.from_dict_v14(v.to_dict_v14()) == v


def test_json_serializable():
    v = Sp3dV3D(1.0, 2.0, 3.0)
    json.dumps(v.to_dict())  # must not raise
