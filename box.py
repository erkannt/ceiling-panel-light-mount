# %%
from build123d import *
from ocp_vscode import *
from copy import copy

reset_show()

length = 200
width = 170
depth = 40
thick = 2

screw_diam = 4
screw_head_diam = 7
screw_tol = 0.6
countersink_depth = depth-5
layer = 0.16


def printable_top_edge_fillet(edges):
    fillet(edges, 1)


def printable_top_fillet(box, top_edge):
    size = 5
    chamfer(top_edge, size, angle=50)
    fillet_z = top_edge.bounding_box().center().Z - size
    fillet(
        box.edges().filter_by_position(
            axis=Axis.Z, minimum=fillet_z - 0.1, maximum=fillet_z + 0.1
        ),
        8,
    )


with BuildPart(Plane.XY) as box:
    with BuildSketch(Plane.XY) as base_shape:
        Rectangle(length, width)
    extrude(amount=depth + thick, taper=5)
    fillet(
        box.edges().filter_by(Axis.X, reverse=True).filter_by(Axis.Y, reverse=True), 10
    )
    top_edge = box.edges().sort_by(Axis.Z)[-1]
    printable_top_fillet(box, top_edge)
    body_of_box = copy(box)
    offset(amount=thick, openings=box.faces().sort_by(Axis.Z)[0])

    with BuildPart(Plane.XY) as posts:
        add(body_of_box)
        with BuildSketch(Plane.XY) as screw_post:
            post_diam = screw_diam + thick * 2
            with GridLocations(
                x_spacing=length - post_diam,
                y_spacing=width - post_diam,
                x_count=2,
                y_count=2,
            ) as corners:
                Circle(post_diam)
        extrude(amount=80, mode=Mode.INTERSECT)
    fillet(edges(Select.LAST).filter_by(Plane.XY, reverse=True), 2)

    hole_offset = post_diam + 3
    with Locations(box.faces().sort_by(Axis.Z)[-1]):
        with GridLocations(
            x_spacing=length - hole_offset,
            y_spacing=width - hole_offset,
            x_count=2,
            y_count=2,
        ) as corners:
            Hole(
                radius=(screw_head_diam + screw_tol) / 2,
                depth=countersink_depth,
            )
            Hole(
                radius=(screw_diam + screw_tol) / 2,
            )
    with BuildSketch(box.faces().sort_by(Axis.Z)[-1].offset(-countersink_depth)):
        with GridLocations(
            x_spacing=length - hole_offset,
            y_spacing=width - hole_offset,
            x_count=2,
            y_count=2,
        ) as corners:
            Rectangle(screw_diam + screw_tol, screw_diam + screw_tol)
    extrude(amount=-layer * 2, mode=Mode.SUBTRACT)
    with BuildSketch(box.faces().sort_by(Axis.Z)[-1].offset(-countersink_depth)):
        with GridLocations(
            x_spacing=length - hole_offset,
            y_spacing=width - hole_offset,
            x_count=2,
            y_count=2,
        ) as corners:
            Circle((screw_head_diam + screw_tol) / 2),
            Rectangle(
                screw_diam + screw_tol, screw_head_diam + screw_tol, mode=Mode.INTERSECT
            )
    extrude(amount=-layer * 1, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ):
        Circle(8)
    extrude(until=Until.LAST,  mode=Mode.SUBTRACT)

# lcl = copy(locals())
# for i in lcl.keys():
#     if isinstance(lcl[i], (BuildPart, BuildSketch, BuildLine)):
#         show_object(lcl[i])


show_object(box)
box.part.export_stl("box.stl")
# %%
