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

from bpy.props import (IntProperty, EnumProperty, BoolProperty)
from bpy.types import (AddonPreferences, GizmoGroup, Operator)

class GizmoButton2D(GizmoGroup):
    """ test gizmo button 2d """
    bl_idname = "view3d.gizmo_button_2d"
    bl_label = "Test button 2d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}
    
    @classmethod
    def poll(cls, context):
        return True
    
    def draw_prepare(self, context):
        #x
        self.foo_gizmo.matrix_basis[0][3] = 100
        #y
        self.foo_gizmo.matrix_basis[1][3] = 200

    def setup(self, context):
        gizmoGroup = self.gizmos.new("GIZMO_GT_button_2d")
       
        gizmoGroup.icon = 'INFO'
        gizmoGroup.draw_options = {'BACKDROP', 'OUTLINE'}
        gizmoGroup.alpha = 0.0
        gizmoGroup.color = 0,0,0
        gizmoGroup.color_highlight = 1, 0, 0
        gizmoGroup.alpha_highlight = 0.2
        gizmoGroup.scale_basis = (80 * 0.35) / 2 
        gizmoGroup.target_set_operator("object.amaas_menu")
        gizmoGroup.use_grab_cursor = True
        self.foo_gizmo = gizmoGroup
    def invoke(context,event):
        if event.type == "RIGHTMOUSE" and event.value == "PRESS":
            print('right mouse')
        if event.ctrl:
            print("ctrl")

def register():
    bpy.utils.register_class(GizmoButton2D)

def unregister():
    bpy.utils.unregister_class(GizmoButton2D)