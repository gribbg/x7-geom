from math import cos, sin, radians, tau, sqrt
from typing import Union

from matplotlib.axes import Axes
from x7.lib.iters import t_range
from x7.geom.geom import BasePoint, Point, Vector, XYList, PointList, PointUnionList
from x7.geom.plot_utils import plot
from x7.geom.plot_viewer import PlotViewer
from x7.geom.transform import Transform

__all__ = ['arc', 'arc2p', 'check_point_list', 'circle', 'cross', 'plus',
           'min_rotation', 'path_rotate', 'path_rotate_ccw', 'path_translate', 'path_to_xy', 'path_from_xy']


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
    # TODO-replace all calls to path_rotate with path_rotate_ccw, then make path_rotate_ccw primary
    t = Transform().rotate(angle)
    return [t.transform_pt(pt, as_pt) for pt in path]


def path_rotate_ccw(path: PointList, angle, as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) CCW about 0,0"""
    t = Transform().rotate_ccw(angle)
    return [t.transform_pt(pt, as_pt) for pt in path]


def path_translate(path: PointList, dxy: Union[Point, Vector], as_pt=False) -> PointUnionList:
    """Rotate all points by angle (in degrees) about 0,0"""
    dxy = Vector(*dxy.xy())
    if as_pt:
        return [p + dxy for p in path]
    else:
        return [(p + dxy).xy() for p in path]


def path_to_xy(path: PointList) -> XYList:
    """Convert PointList to XYList"""
    return [p.xy() for p in path]


def path_from_xy(xy: XYList) -> PointList:
    """Convert XYList to PointList"""
    return [Point(*p) for p in xy]


def arc(r: float, sa: float, ea: float, c=Point(0, 0), steps=-1, direction='ccw') -> XYList:
    """
        Generate an arc of radius r about c as a list of x,y pairs
        :param r:   Radius of arc
        :param sa:  Start angle in degrees
        :param ea:  End angle in degrees
        :param c:   Center of arc
        :param steps: steps (defaults to 1 step per degree)
        :param direction: direction to travel around circle: ccw, cw, or none (no adjustments to angles)
        :return:    List of (x, y)
    """
    if direction == 'ccw':
        sa = sa % 360
        ea = ea % 360
        if ea < sa:
            ea += 360
    elif direction == 'cw':
        sa = sa % 360
        ea = ea % 360
        if sa < ea:
            sa += 360

    steps = int(abs(ea-sa)+1) if steps < 0 else steps
    return [(r * cos(t) + c.x, r * sin(t) + c.y) for t in t_range(steps, radians(sa), radians(ea))]


def arc2p(r: float, s: Point, e: Point, steps=-1, side=1) -> XYList:
    """
        Generate an arc of radius r about c as a list of x,y pairs
        :param r:   Radius of arc
        :param s:   Start point
        :param e:   End point
        :param steps: steps (defaults to 1 step per degree)
        :param side: positive or negative value to determine arc side
        :return:    List of (x, y)
    """
    v: Vector = e-s
    vl = v.length() / 2
    if vl > r:
        raise ValueError('s-e too far apart for r: %s > 2*%s' % (v.length(), r))
    elif vl == 0:
        raise ValueError('s == e, cannot compute arc')
    mp = s + v * 0.5
    clv = (v.normal()*side).unit()
    cll = sqrt(r*r - vl*vl)
    c = mp + clv * cll
    sv = s-c
    ev = e-c
    # return arc(r, sv.angle(), ev.angle(), c=c, steps=steps)
    return path_to_xy([e, c, s]) + arc(r, sv.angle(), ev.angle(), c=c, steps=steps)


def circle(r, c=Point(0, 0)) -> XYList:
    """Generate a circle of radius r about c as a list of x,y pairs"""
    steps = 360
    return [(r * cos(t) + c.x, r * sin(t) + c.y) for t in t_range(steps, 0, tau)]


def cross(r, c=Point(0, 0)) -> XYList:
    """Generate a cross of radius r about c as a list of x,y pairs"""
    r *= sqrt(2)/2
    vx = Vector(r, r)
    vy = Vector(-r, r)
    return [p.xy() for p in [c-vx, c+vx, c, c-vy, c+vy]]


def plus(r, c=Point(0, 0)) -> XYList:
    """Generate a plus sign of radius r about c as a list of x,y pairs"""
    vx = Vector(r, 0)
    vy = Vector(0, r)
    return [p.xy() for p in [c-vx, c+vx, c, c-vy, c+vy]]


def arc_animate():
    def update_example():
        rotate = [3]

        def arc_fun(ax: Axes):
            angle = rotate[0]
            rotate[0] = (rotate[0] + 3) % 360
            if rotate[0] == 0:
                rotate[0] += 3

            # plot(circle(2, Point(0, 0)), 'lightgrey', plotter=ax)
            plot(circle(0.1, Point(-4, 4)), 'lightgrey', plotter=ax)
            plot(circle(0.1, Point(4, -4)), 'lightgrey', plotter=ax)

            for side, color, offset in [(1, 'blue', -1), (-1, 'red', 1)]: #[:1]:
                yv = Vector(0, -1).rotate(0)
                p1 = yv.p
                p2 = yv.rotate(angle).p
                ov = Vector(offset, offset)
                p1 = p1 + ov
                p2 = p2 + ov
                #plot(arc2p(1+1e-8, p1, p2, side=1 if angle > 180 else -1), color, plotter=ax)
                #plot(arc2p(1+1e-8, p1, p2, side=1 if angle < 180 else -1), 'lightblue', plotter=ax)
                a1 = arc2p(1+1e-8, p1, p2, side=side)
                a2 = arc2p(1+1e-8, p1, p2, side=-side)
                c1 = a1[1]
                c2 = a2[1]
                plot(a1, 'lightblue', plotter=ax)
                plot(a2, color, plotter=ax)
                # plot(arc2p(1+1e-8, p1, p2, side=-1), 'lightblue', plotter=ax)
                plot([p1, p2], color, linestyle=':', plotter=ax)
                mid = p1.mid(p2)
                plot([mid, mid+(p2-p1).unit().normal()], 'cyan', plotter=ax)
                # plot(arc2p(1, Point(0, -1), yv.rotate(rotate[0]).p, side=side), color, plotter=ax)

            ax.axis('equal')

        return arc_fun

    app = PlotViewer(update_example())
    app.mainloop()


def arc_test():
    from x7.geom.plot_utils import plot, plot_show
    import matplotlib.pyplot as plt

    if False:
        for side, color in [(1, 'blue'), (-1, 'red')]:
            p1 = Point(1, 1)
            p2 = Point(1, 2)
            if side < 0:
                # p1, p2 = p2, p1
                pass
            plot(arc2p(3, p1, p2, side=side)[3:], color)
            #plot(arc2p(2, p1, p2, side=side), color)
            #plot(arc2p(1, p1, p2, side=side), color)
            #plot(arc2p(0.6, p1, p2, side=side), color)
            #plot(arc2p(0.5, p1, p2, side=side), color)
        plot(circle(5), 'grey')
        plt.axis('equal')
        plot_show()
        return

    colors = plt.cycler(color='red orange yellow green cyan blue purple'.split())
    cc = colors()
    off = 5
    centers = [Point(-off, off), Point(-off, -off), Point(off, off), Point(off, -off)]
    angles = [0, 85, 90, 95]
    centers = [Point(10*n, 0) for n in range(20)]
    angles = [n for n in t_range(20, 45, 45+360, closed=False)]
    for y in t_range(10, -3, 3):
        if y != 0:
            color = next(cc)
            for c, ang in zip(centers, angles):
                v = Vector(y, 0).rotate(ang)
                center = c + Vector(y-3, 0).rotate(ang)
                # a = arc2p(3.1, center + v.normal(), center - v.normal(), side=y)
                a = arc2p(3.1, center + v.normal(), center - v.normal(), side=y)
                plot(a[1:3], 'green', linestyle=':')
                plot(a[:2], 'red', linestyle=':')
                plot(a[3:], **color)
    # plot(circle(5), 'grey')
    plt.axis('equal')
    plot_show()


if __name__ == '__main__':
    arc_animate(); exit(0)
    arc_test()
