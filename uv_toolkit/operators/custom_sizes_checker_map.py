import bpy
from bpy.props import IntProperty


class CustomSizesCheckerMap(bpy.types.Operator):
    bl_idname = "uv.toolkit_custom_sizes_checker_map"
    bl_label = "Create Checker Map"
    bl_description = "Create checker map"
    bl_options = {'REGISTER', 'UNDO'}

    width: IntProperty(name="Width")
    height: IntProperty(name="Height")

    def execute(self, context):
        bpy.ops.uv.toolkit_create_checker_map(width=self.width, height=self.height)
        return {'FINISHED'}

    def invoke(self, context, event):
        if context.selected_objects == []:
            self.report({'WARNING'}, 'No Objects Selected')
            return {'FINISHED'}
        else:
            return context.window_manager.invoke_props_dialog(self, width=150)
