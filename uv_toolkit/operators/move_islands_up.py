import bpy


class MoveIslandsUp(bpy.types.Operator):
    bl_idname = "uv.toolkit_move_islands_up"
    bl_label = "Move islands up (UVToolkit)"
    bl_description = "Move islands up"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.transform.translate(value=(0, 1, 0))
        return {'FINISHED'}
