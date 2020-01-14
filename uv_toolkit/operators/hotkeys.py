import bpy


class Hotkeys(bpy.types.Operator):
    bl_idname = "uv.toolkit_hotkeys"
    bl_label = "Hotkeys"
    bl_description = "Hotkeys"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=230)

    def draw(self, context):
        layout = self.layout
        layout = layout.box()
        layout.label(text="Shift+F: UV Toolkit Pie menu")
        layout.label(text="Tab: UV Sync mode")
        layout.label(text="Shift+E: Unwrap Selected")
        layout.label(text="Shift+C: View All")
        layout.label(text="Alt+S: Scale Individual Origins")
        layout.label(text="F: Quick Drag Island")
        layout.label(text="Ctrl+Up Arrow: Move islands up")
        layout.label(text="Ctrl+Left Arrow: Move islands left")
        layout.label(text="Ctrl+Right Arrow: Move islands right")
        layout.label(text="Ctrl+Down Arrow: Move islands down")
