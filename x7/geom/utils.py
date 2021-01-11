from math import cos, sin, radians, tau
from typing import Union

from x7.lib.iters import t_range
from x7.geom.geom import BasePoint, Point, Vector, XYList, PointList, PointUnionList
from x7.geom.transform import Transform

__all__ = ['arc', 'check_point_list', 'circle', 'min_rotation', 'path_rotate', 'path_translate', 'plot', 'plot_show']


def check_point_list(lst: PointList):
    """Validate that lst is List[BasePoint]"""
    for elem in lst:
        if not isinstance(elem, BasePoint):
            raise ValueError('%s of lst is not a BasePoint' % repr(elem))


def min_rotation(target_degrees, source_degrees):
    """
        Return the smallest rotation required to move
        from source angle to target angle::

            min_rotation(20, 10) => 10
            min_rotation(-340, 10) => 10
            min_rotation(20, 370) => 10
    """
    return (target_degrees - source_degrees + 180) % 360 - 180


def path_rotate(path: PointList, angle, as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) about 0,0"""
    t = Transform().rotate(angle)
    return [t.transform_pt(pt, as_pt) for pt in path]


def path_translate(path: PointList, dxy: Union[Point, Vector], as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) about 0,0"""
    dxy = Vector(*dxy.xy())
    if as_pt:
        return [p + dxy for p in path]
    else:
        return [(p + dxy).xy() for p in path]


def arc(r, sa, ea, c=Point(0, 0), steps=-1) -> XYList:
    """Generate an arc of radius r about c as a list of x,y pairs"""
    steps = int(abs(ea-sa)+1) if steps < 0 else steps
    return [(r * cos(t) + c.x, r * sin(t) + c.y) for t in t_range(steps, radians(sa), radians(ea))]


def circle(r, c=Point(0, 0)) -> XYList:
    """Generate a circle of radius r about c as a list of x,y pairs"""
    steps = 360
    return [(r * cos(t) + c.x, r * sin(t) + c.y) for t in t_range(steps, 0, tau)]


def plot(xy: PointUnionList, color='black', label=None, plotter=None):
    """Quick entry to pyplot.plot() for List[Point]"""
    import matplotlib.pyplot as plt

    plotter = plotter or plt
    artists = plotter.plot(*zip(*xy), color)
    if label:
        for artist in artists:
            artist.set_label(label)


def plot_show():
    """Quick entry to pyplot.show()"""
    import matplotlib.pyplot as plt

    plt.show()
