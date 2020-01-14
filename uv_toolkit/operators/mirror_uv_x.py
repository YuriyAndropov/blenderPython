import bpy


class MirrorUvX(bpy.types.Operator):
    bl_idname = "uv.toolkit_mirror_uv_x"
    bl_label = "Mirror selected UV X axis"
    bl_description = "Mirror UV X axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))
        return {'FINISHED'}
