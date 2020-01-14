import bpy


class RemoveAllCheckerMaps(bpy.types.Operator):
    bl_idname = "uv.toolkit_remove_all_checker_maps"
    bl_label = "Remove All Checker Maps (UVToolkit)"
    bl_description = "Completely remove all checker materials and textures"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for image in bpy.data.images:
            if image.name.startswith("checker_image"):
                bpy.data.images.remove(image)

        for mat in bpy.data.materials:
            if mat.name.startswith("checker_material"):
                bpy.data.materials.remove(mat)
        return {'FINISHED'}
