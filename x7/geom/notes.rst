Coordinate Spaces
=================

**Internal Shape Space**
    The space used to specify raw data in a file,
    for example, ``Rectangle(Point(1, 2), Point(3, 4)``.

**External Shape Space**
    Internal Space transformed by a shape or
    elem's own transformation matrix.  A composite
    shape's Internal Space is the sub-shape's
    External Space.  This is sometimes called
    Modeling Space.

**Drawing Space**
    External Shape Space transformed by a
    DrawingContext transformation matrix.  This could
    also be called Screen Space.

Internal Space methods:

*   constructor
*   bbox_int, bbox_int_update
*   control_path
*   copy, restore
*   display
*   dump
*   iter_elems (but it tracks hierarchical
    transformations)

External Space,
decorated with ``@shape_transformer``,
accessed via ``self.xform``:

*   as_digi_points,
*   bbox, center
*   transform (starts in shape space, but
    adds an additional transform)

Drawing Space,
decorated with ``@draw_transformer``,

*   draw
*   path







accessed via ``draw.matrix.compose(self.xform)``:

*   draw
*   path

Shape space is