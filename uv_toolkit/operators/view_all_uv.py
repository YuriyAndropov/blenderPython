import bpy


class ViewAllUv(bpy.types.Operator):
    bl_idname = "uv.toolkit_view_all_uv"
    bl_label = "View All UV (UVToolkit)"
    bl_description = "View All UV"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.space_data.cursor_location[1] = 0
        context.space_data.cursor_location[0] = 0
        bpy.ops.image.view_all(fit_view=True)
        return {'FINISHED'}
