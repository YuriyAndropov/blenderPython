import bpy
from bpy.props import FloatProperty


class RotateUVIslands(bpy.types.Operator):
    bl_idname = "uv.toolkit_rotate_uv_islands"
    bl_label = "Rotate selected UV islands (UVToolkit)"
    bl_description = "Rotate selected UV islands"
    bl_options = {'REGISTER', 'UNDO'}

    angle: FloatProperty(options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.transform.rotate(value=self.angle)
        return {'FINISHED'}
