import numpy as np

import pygmsh
from helpers import compute_volume


def test_builtin_duplicate():
    """Translation and duplication of a surface object with built_in kernel"""
    geom = pygmsh.built_in.Geometry()
    geom.add_raw_code("Geometry.CopyMeshingMethod = 1;")

    # built-in square
    p0 = geom.add_point([0.0, 0.0, 0], 0.01)
    p1 = geom.add_point([1.0, 0.0, 0], 0.01)
    p2 = geom.add_point([1.0, 1.0, 0], 0.01)
    p3 = geom.add_point([0.0, 1.0, 0], 0.01)
    l0 = geom.add_line(p0, p1)
    l1 = geom.add_line(p1, p2)
    l2 = geom.add_line(p2, p3)
    l3 = geom.add_line(p3, p0)
    ll0 = geom.add_line_loop([l0, l1, l2, l3])
    square_builtin = geom.add_plane_surface(ll0)
    geom.set_transfinite_surface(square_builtin, size=[11, 11])

    duplicate = geom.translate(square_builtin, [1.0, 0.0, 0.0], duplicate=True)

    mesh = pygmsh.generate_mesh(geom)
    area = 2.0
    assert np.abs(compute_volume(mesh) - area) < 1e-3 * area
    assert len(mesh.get_cells_type("triangle")) == 400
    return


def test_translate_duplicate2d():
    """Translation and duplication of a surface object"""
    geom = pygmsh.opencascade.Geometry(0.1, 0.1)
    square = geom.add_rectangle([0.0, 0.0, 0.0], 1.0, 1.0)
    other = geom.translate(square, [1.0, 0.0, 0.0], duplicate=True)
    another = geom.translate(square, [0.0, 1.0, 0.0], duplicate=True)
    and_another = geom.translate(square, [1.0, 1.0, 0.0], duplicate=True)
    geom.boolean_union([square, other, another, and_another])

    mesh = pygmsh.generate_mesh(geom)
    area = 4.0
    assert np.abs(compute_volume(mesh) - area) < 1e-3 * area
    return


def test_translate_duplicate3d():
    """Translation and duplciation of a volume object"""
    geom = pygmsh.opencascade.Geometry(0.1, 0.1)
    cube = geom.add_box([0, 0, 0], [1, 1, 1])
    other = geom.translate(cube, [1.0, 0, 0], duplicate=True)
    geom.boolean_union([cube, other])

    mesh = pygmsh.generate_mesh(geom)
    vol = 2
    assert np.abs(compute_volume(mesh) - vol) < 1e-3 * vol
    return


if __name__ == "__main__":
    test_builtin_duplicate()
    test_translate_duplicate2d()
    test_translate_duplicate3d()
