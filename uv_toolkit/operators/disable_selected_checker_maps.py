import bpy


class DisableSelectedCheckerMaps(bpy.types.Operator):
    bl_idname = "uv.toolkit_disable_selected_checker_materials"
    bl_label = "Disable selected Materials (UVToolkit)"
    bl_description = "Disable selected checker materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.selected_objects == []:
            self.report({'WARNING'}, 'No Objects Selected')
            return {'FINISHED'}
        else:
            active_object = context.view_layer.objects.active  # Store active object
            for obj in context.selected_objects:
                context.view_layer.objects.active = obj
                current_mode = context.object.mode  # Store object mode
                if bpy.data.materials[0].name.startswith("checker_material"):
                    context.object.active_material_index = 0
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.material_slot_remove()
                bpy.ops.object.mode_set(mode=current_mode)  # Restore object mode
            context.view_layer.objects.active = active_object  # Restore active object
            # Disable active image in Image Editor
            for area in bpy.context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = None
            return{'FINISHED'}
