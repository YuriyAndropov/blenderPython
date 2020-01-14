import bpy


class ScaleIndividualOrigins(bpy.types.Operator):
    bl_idname = "uv.toolkit_scale_individual_origins"
    bl_label = "Scale Individual Origins (UVToolkit)"
    bl_description = "Scale individual origins"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        current_pivot_point = context.space_data.pivot_point
        context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        bpy.ops.transform.resize('INVOKE_DEFAULT')
        context.space_data.pivot_point = current_pivot_point
        return {'FINISHED'}
