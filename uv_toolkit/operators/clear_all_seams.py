import bpy


class ClearAllSeams(bpy.types.Operator):
    bl_idname = "uv.toolkit_clear_all_seams"
    bl_label = "Clear All Seams"
    bl_description = "Clear all seams"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        return {'FINISHED'}
