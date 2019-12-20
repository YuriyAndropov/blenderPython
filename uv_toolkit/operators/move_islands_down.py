import bpy


class MoveIslandsDown(bpy.types.Operator):
    bl_idname = "uv.toolkit_move_islands_down"
    bl_label = "Move islands down (UVToolkit)"
    bl_description = "Move islands down"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.transform.translate(value=(0, -1, 0))
        return {'FINISHED'}
