import cadquery as cq
from cq_server.ui import ui, show_object


corner_length = 30
panel_height = 10
thickness = 4
frame_width = 8

result = (
  cq.Workplane()
	.box(corner_length, corner_length, panel_height+thickness)
	.faces("<Z")
	.vertices(">XY")
	.circle(10)
	.extrude(panel_height+thickness)
	.faces("<Z")
	.vertices("<XY")
	.rect(corner_length-thickness, corner_length-thickness, centered=[0,0])
	.cutBlind(panel_height)
	.faces(">Z")
	.vertices("<XY")
	.rect(corner_length-thickness-frame_width, corner_length-thickness-frame_width, centered=[0,0])
	.cutThruAll()
)

show_object(result)
