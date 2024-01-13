# %%
from build123d import *
from ocp_vscode import *
from copy import copy

length = 30
panel_thickness = 10
edge_width = 10
thickness = 3
screw_diam = 4

with BuildPart(Plane.XY) as corner_clip:
	with BuildSketch(Plane.XY) as clip_edges:
		Rectangle(length, length, align=[Align.MIN, Align.MIN])
		Circle(screw_diam/2+thickness*2)
	extrude(amount=panel_thickness + thickness)

	with BuildSketch(Plane.XY) as panel:
		with Locations((thickness, thickness)):
			Rectangle(length, length, align=[Align.MIN, Align.MIN])
	extrude(amount=panel_thickness, mode=Mode.SUBTRACT)

	with BuildSketch(Plane.XY) as panel_light:
		with Locations((thickness + edge_width, thickness + edge_width)):
			Rectangle(length, length, align=[Align.MIN, Align.MIN])
	extrude(amount=panel_thickness + thickness, mode=Mode.SUBTRACT)

	with Locations((0,0, panel_thickness, thickness)):
		CounterBoreHole(radius=(screw_diam+0.6)/2, counter_bore_radius=(7+0.6)/2, counter_bore_depth=thickness)

reset_show()
lcl = copy(locals())
for i in lcl.keys():
	if isinstance(lcl[i], (BuildPart, BuildSketch, BuildLine)):
		show_object(lcl[i])


# %%
show(corner_clip)
corner_clip.part.export_stl("corner_clip.stl")
# %%
