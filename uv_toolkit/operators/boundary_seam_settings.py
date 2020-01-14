import bpy


class BoundarySeamSettings(bpy.types.Operator):
    bl_idname = "uv.toolkit_boundary_seam_settings"
    bl_label = "Boundary Seam Settings"
    bl_description = "Boundary Seam Settings"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=230)

    def draw(self, context):
        addon_prefs = context.preferences.addons["uv_toolkit"].preferences

        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Regular Unwrap after Boundary seam")
        row = box.row()
        row.prop(addon_prefs, "boundary_loop_unwrap", expand=True)
        box = layout.box()
        row = box.row()
        row.label(text="Alternative Unwrap after Boundary seam")
        row = box.row()
        row.prop(addon_prefs, "boundary_loop_enable_live_unwrap", expand=True)
        box = layout.box()
        row = box.row()
        row.label(text="Enable UV Sync")
        row = box.row()
        row.prop(addon_prefs, "boundary_loop_enable_uv_sync", expand=True)
