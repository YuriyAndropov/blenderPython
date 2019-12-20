import bpy


class QuickDragIsland(bpy.types.Operator):
    bl_idname = "uv.toolkit_quick_drag_island"
    bl_label = "Quick Drag Island (UVToolkit)"
    bl_description = "Quick drag island"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        if context.scene.tool_settings.use_uv_select_sync is True:
            current_mode = tuple(context.tool_settings.mesh_select_mode)
            context.tool_settings.mesh_select_mode = (False, False, True)  # Face
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            context.tool_settings.mesh_select_mode = current_mode
            return {'FINISHED'}
        else:
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            return {'FINISHED'}
