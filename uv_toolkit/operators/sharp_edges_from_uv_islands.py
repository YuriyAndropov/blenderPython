import bpy


class SharpEdgesFromUvIslands(bpy.types.Operator):
    bl_idname = "uv.toolkit_sharp_edges_from_uv_islands"
    bl_label = "Sharp Edges From UV Islands (UVToolkit)"
    bl_description = "Sharp Edges From UV Islands"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if context.selected_objects != []:
            active_object = context.view_layer.objects.active  # Store active object
            current_mode = context.object.mode  # Store object mode
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.shade_smooth()
            for obj in context.selected_objects:
                context.view_layer.objects.active = obj
                context.object.data.use_auto_smooth = True
                context.object.data.auto_smooth_angle = 3.14159
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.seams_from_islands(mark_seams=False, mark_sharp=True)
            context.view_layer.objects.active = active_object  # restore active object
            bpy.ops.object.mode_set(mode=current_mode)  # Restore object mode
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
