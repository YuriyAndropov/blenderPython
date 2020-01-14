import bpy


class UvSyncMode(bpy.types.Operator):
    bl_idname = "uv.toolkit_sync_mode"
    bl_label = "UV Sync mode (UVToolkit)"
    bl_description = "UV sync mode"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.mode == 'EDIT'

    def execute(self, context):
        tool_settings = context.scene.tool_settings
        addon_prefs = context.preferences.addons["uv_toolkit"].preferences

        tool_settings.use_uv_select_sync = not tool_settings.use_uv_select_sync

        if tool_settings.use_uv_select_sync is True:
            if addon_prefs.uv_sync_selection_mode == "enable":
                # Sync selection mode UV Sync Active
                if context.scene.tool_settings.uv_select_mode == 'VERTEX':
                    context.tool_settings.mesh_select_mode = (True, False, False)  # Vertex
                elif context.scene.tool_settings.uv_select_mode == 'EDGE':
                    context.tool_settings.mesh_select_mode = (False, True, False)  # Edge
                elif context.scene.tool_settings.uv_select_mode == 'FACE':
                    context.tool_settings.mesh_select_mode = (False, False, True)  # Face

            self.report({'WARNING'}, 'UV Sync Active')
            if addon_prefs.uv_sync_auto_select == "enable":
                bpy.ops.mesh.select_all(action='DESELECT')
            return {'FINISHED'}
        else:
            if addon_prefs.uv_sync_selection_mode == "enable":
                # Sync selection mode UV Sync Disabled
                if tuple(context.tool_settings.mesh_select_mode) == (True, False, False):  # Vertex
                    context.scene.tool_settings.uv_select_mode = 'VERTEX'
                elif tuple(context.tool_settings.mesh_select_mode) == (False, True, False):  # Edge
                    context.scene.tool_settings.uv_select_mode = 'EDGE'
                elif tuple(context.tool_settings.mesh_select_mode) == (False, False, True):  # Face
                    context.scene.tool_settings.uv_select_mode = 'FACE'

            self.report({'INFO'}, 'UV Sync Disabled')
            if addon_prefs.uv_sync_auto_select == "enable":
                bpy.ops.mesh.select_all(action='SELECT')
            return {'FINISHED'}
