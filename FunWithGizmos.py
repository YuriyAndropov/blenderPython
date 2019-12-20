bl_info = {
    "name": "Gizmo button 2d test",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "description": "",
    "location": "View3D",
    "warning": "",
    "category": "3D View"
}
import bpy
import mathutils

from bpy.types import (
    GizmoGroup,
)

from bpy.props import (IntProperty, EnumProperty, BoolProperty)
from bpy.types import (AddonPreferences, GizmoGroup, Operator)

class GizmoButton2D(GizmoGroup):
    """ test gizmo button 2d """
    bl_idname = "view3d.gizmo_button_2d"
    bl_label = "Test button 2d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}
    
        
    
    
    def setup(self, context):
        # Arrow gizmo has one 'offset' property we can assign to the light energy.
        mpr = self.gizmos.new("GIZMO_GT_arrow_3d")
        mpr.matrix_basis = mathutils.Matrix.Translation((0,0,0))
        

        mpr.color = 1.0, 0.5, 0.0
        #mpr.alpha = 0.5

        #mpr.color_highlight = 1.0, 0.5, 1.0
        #mpr.alpha_highlight = 0.5

        #self.energy_widget = mpr
    def invoke(context,event):
        if event.type == "RIGHTMOUSE" and event.value == "PRESS":
            print('right mouse')
        if event.ctrl:
            print("ctrl")
    

def register():
    bpy.utils.register_class(GizmoButton2D)

def unregister():
    bpy.utils.unregister_class(GizmoButton2D)