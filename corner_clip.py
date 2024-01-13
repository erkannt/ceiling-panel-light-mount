# %%
from build123d import *
from ocp_vscode import *
from copy import copy

reset_show()

length = 30
panel_thickness = 9
edge_width = 12
side_thick = 3
top_thick = 4
total_height = panel_thickness + top_thick

screw_diam = 4
screw_head_diam = 7
screw_tol = 0.6
countersink_depth = top_thick - 1.5

layer = 0.16


def screw_cyl_fillet(total_height, corner_clip):
    fillet(
        corner_clip.edges()
        .filter_by(Axis.Z)
        .filter_by(lambda e: e.bounding_box().max.Z == total_height)
        .sort_by_distance((0, 0, 0))[0:2],
        radius=10,
    )


def vert_fillet(total_height, corner_clip):
    fillet(
        corner_clip.edges()
        .filter_by(Axis.Z)
        .filter_by(lambda e: e.bounding_box().max.Z == total_height),
        radius=2,
    )


def printable_top_edge_fillet(panel_thickness, total_height, corner_clip):
    chamfer(corner_clip.faces().sort_by(Axis.Z)[-1].edges(), 1, angle=50)

    fillet(
        corner_clip.edges()
        .filter_by_position(
            axis=Axis.Z,
            minimum=panel_thickness + 1,
            maximum=total_height - 1,
        )
        .filter_by(Axis.Z, reverse=True),
        2,
    )


with BuildPart(Plane.XY) as corner_clip:
    with BuildSketch(Plane.XY) as base_shape:
        Rectangle(length, length, align=[Align.MIN, Align.MIN])
        Circle(screw_diam / 2 + side_thick * 2)
    extrude(amount=total_height)

    with BuildSketch(Plane.XY) as panel:
        with Locations((side_thick, side_thick)):
            Rectangle(length, length, align=[Align.MIN, Align.MIN])
    extrude(amount=panel_thickness, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY) as cutout:
        with Locations((side_thick + edge_width, side_thick + edge_width)):
            Rectangle(length, length, align=[Align.MIN, Align.MIN])
    extrude(amount=total_height, mode=Mode.SUBTRACT)

    screw_cyl_fillet(total_height, corner_clip)
    vert_fillet(total_height, corner_clip)
    printable_top_edge_fillet(panel_thickness, total_height, corner_clip)

    hole_loc = (0, 0, total_height)
    with Locations(hole_loc):
        Hole(
            radius=(screw_head_diam + screw_tol) / 2,
            depth=countersink_depth,
        )
    with Locations(hole_loc):
        Hole(
            radius=(screw_diam + screw_tol) / 2,
        )
    with BuildSketch(Plane(hole_loc).offset(-countersink_depth)):
        Rectangle(screw_diam + screw_tol, screw_diam + screw_tol)
    extrude(amount=-layer * 2, mode=Mode.SUBTRACT)
    with BuildSketch(Plane(hole_loc).offset(-countersink_depth)):
        Circle((screw_head_diam + screw_tol) / 2),
        Rectangle(
            screw_diam + screw_tol, screw_head_diam + screw_tol, mode=Mode.INTERSECT
        )
    extrude(amount=-layer * 1, mode=Mode.SUBTRACT)

lcl = copy(locals())
for i in lcl.keys():
    if isinstance(lcl[i], (BuildPart, BuildSketch, BuildLine)):
        show_object(lcl[i])


# %%
show(corner_clip)
corner_clip.part.export_stl("corner_clip.stl")
# %%
