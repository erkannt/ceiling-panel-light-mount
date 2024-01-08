import cadquery as cq
from cq_server.ui import ui, show_object

height = 60.0
width = 80.0
thickness = 10.0
diameter = 22.0
padding = 12.0

result = (
    cq.Workplane("XY")
    .box(height, width, thickness)
		.edges("|Z")
		.fillet(5.0)
		.faces(">Z or <Z")
		.edges()
		.fillet(2)
    .faces(">Z")
    .workplane()
    .hole(diameter)
    .faces(">Z")
    .workplane()
    .rect(height - padding, width - padding, forConstruction=True)
		.vertices()
		.cboreHole(2.4, 4.4, 2.1)
		.faces(">Z")
		.workplane()
		.hole(diameter+padding, thickness/2)
)

show_object(result)
