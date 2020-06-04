"""Test translation for all dimensions."""
import numpy as np

import pygmsh
from helpers import compute_volume

# def test_translation1d():
#     """Translation of a line."""
#     geom = pygmsh.built_in.Geometry()
#     points = []
#     for array in [[1, 0, 0], [0, 0, 0], [0, 1, 0]]:
#         points.append(geom.add_point(array, 0.5))
#     circle = geom.add_circle_arc(*points)
#     # mesh = pygmsh.generate_mesh(geom)
#     geom.translate(circle, [1.5, 0, 0])
#     translated_mesh = pygmsh.generate_mesh(geom)
#     points[:, 0] = points[:, 0] + 1.5
#     assert np.allclose(points, translated_mesh.points)
#     return


def test_translation2d():
    """Translation of a surface object."""
    geom = pygmsh.opencascade.Geometry(0.05, 0.05)
    disk = geom.add_disk([0, 0, 0], 1)
    disk2 = geom.add_disk([1.5, 0, 0], 1)
    geom.translate(disk, [1.5, 0, 0])
    geom.boolean_union([disk2, disk])

    mesh = pygmsh.generate_mesh(geom)
    surf = np.pi
    assert np.abs(compute_volume(mesh) - surf) < 1e-3 * surf
    return

def test_translate_duplicate2d():
    """Translation and duplication of a surface object"""
    geom = pygmsh.opencascade.Geometry(0.1, 0.1)
    geom.add_raw_code("Geometry.CopyMeshingMethod=1;")
    square = geom.add_rectangle([0.0, 0.0, 0.0], 1.0, 1.0)
    other = geom.translate(square, [1.0, 0.0, 0.0], duplicate=True)
    another = geom.translate(square, [0.0, 1.0, 0.0], duplicate=True)
    and_another = geom.translate(square, [1.0, 1.0, 0.0], duplicate=True)
    geom.boolean_union([square, other, another, and_another])

    mesh = pygmsh.generate_mesh(geom)
    area = 4.0
    assert np.abs(compute_volume(mesh) - area) < 1e-3 * area
    return


def test_translation3d():
    """Translation of a volume object."""
    geom = pygmsh.opencascade.Geometry(0.2, 0.2)
    ball = geom.add_ball([0, 0, 0], 1)
    ball2 = geom.add_ball([1.5, 0, 0], 1)
    geom.translate(ball, [1.5, 0, 0])
    geom.boolean_union([ball2, ball])

    mesh = pygmsh.generate_mesh(geom)
    surf = 4 / 3 * np.pi
    assert isinstance(ball, pygmsh.opencascade.volume_base.VolumeBase)
    assert isinstance(ball, pygmsh.built_in.volume_base.VolumeBase)

    assert np.abs(compute_volume(mesh) - surf) < 2e-2 * surf
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
    # test_translation1d()
    test_translation2d()
    test_translate_duplicate2d()
    test_translation3d()
    test_translate_duplicate3d()
