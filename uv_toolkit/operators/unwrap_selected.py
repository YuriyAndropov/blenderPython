import bpy


class UnwrapSelected(bpy.types.Operator):
    bl_idname = "uv.toolkit_unwrap_selected"
    bl_label = "Unwrap Selected (UVToolkit)"
    bl_description = "Unwrap selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.mode == 'EDIT'

    def check_seams(self, context):
        for edge in context.object.data.edges:
            if edge.use_seam:
                return True

    def invoke(self, context, event):
        if event.alt:
            if context.scene.tool_settings.use_uv_select_sync is False:
                bpy.ops.uv.pin(clear=True)
                bpy.ops.uv.select_all(action='INVERT')
                bpy.ops.uv.pin(clear=False)
                bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True, margin=0)
                bpy.ops.uv.pin(clear=True)
                bpy.ops.uv.select_all(action='INVERT')
                return {'FINISHED'}
            else:
                self.report({'INFO'}, 'Need to disable UV Sync')
                return {'CANCELLED'}
        if context.scene.tool_settings.use_uv_select_sync is False:
            if self.check_seams(context) is not True:
                bpy.ops.uv.seams_from_islands()
            bpy.ops.uv.pin(clear=True)
            bpy.ops.uv.select_all(action='INVERT')
            bpy.ops.uv.pin(clear=False)
            bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True, margin=0)
            bpy.ops.uv.pin(clear=True)
            bpy.ops.uv.select_all(action='INVERT')
            return {'FINISHED'}
        else:
            self.report({'INFO'}, 'Need to disable UV Sync')
            return {'CANCELLED'}
