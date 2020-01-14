import bpy


class MoveIslandsLeft(bpy.types.Operator):
    bl_idname = "uv.toolkit_move_islands_left"
    bl_label = "Move islands left (UVToolkit)"
    bl_description = "Move islands left"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.transform.translate(value=(-1, 0, 0))
        return {'FINISHED'}
