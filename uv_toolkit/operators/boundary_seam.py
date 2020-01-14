import bpy


class BoundarySeam(bpy.types.Operator):
    bl_idname = "uv.toolkit_boundary_seam"
    bl_label = "Boundary Seam"
    bl_description = "Boundary seam"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def invoke(self, context, event):
        if event.alt:
            bpy.ops.uv.toolkit_boundary_seam_settings('INVOKE_DEFAULT')
            return {'FINISHED'}
        else:
            current_select_mode = tuple(context.tool_settings.mesh_select_mode)
            addon_prefs = context.preferences.addons["uv_toolkit"].preferences
            tool_settings = context.scene.tool_settings
            live_unwrap_current_state = tool_settings.use_edge_path_live_unwrap

            if addon_prefs.boundary_loop_unwrap == "enable":
                bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

            if addon_prefs.boundary_loop_enable_live_unwrap == "enable":
                if tool_settings.use_edge_path_live_unwrap is not True:
                    tool_settings.use_edge_path_live_unwrap = True

            if addon_prefs.boundary_loop_enable_uv_sync == "enable":
                tool_settings.use_uv_select_sync = True

            bpy.ops.mesh.region_to_loop()
            bpy.ops.mesh.mark_seam(clear=False)
            context.tool_settings.mesh_select_mode = current_select_mode
            tool_settings.use_edge_path_live_unwrap = live_unwrap_current_state
            return {'FINISHED'}
