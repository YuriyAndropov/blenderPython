import bpy
from bpy.props import StringProperty


class CheckerGridType(bpy.types.Operator):
    bl_idname = "uv.toolkit_change_checker_grid"
    bl_label = "Checker Grid Type (UVToolkit)"
    bl_description = "Checker grid type"
    bl_options = {'REGISTER', 'UNDO'}

    checker_grid_type: StringProperty(options={'HIDDEN'})

    def execute(self, context):
        for image in bpy.data.images:
            if image.name.startswith("checker_image"):
                image.generated_type = self.checker_grid_type
        return{'FINISHED'}
