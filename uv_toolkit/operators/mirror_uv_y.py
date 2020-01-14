import bpy


class MirrorUvY(bpy.types.Operator):
    bl_idname = "uv.toolkit_mirror_uv_y"
    bl_label = "Mirror selected UV Y axis"
    bl_description = "Mirror UV Y axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))
        return {'FINISHED'}
