import bpy


class TextureMode(bpy.types.Operator):
    bl_idname = "uv.toolkit_toggle_texture_mode"
    bl_label = "Show Texture in Viewport (UVToolkit)"
    bl_description = "Show texture in viewport (Toggle)"

    def execute(self, context):
        for area in bpy.context.workspace.screens[0].areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.shading.type != 'SOLID':
                        self.report({'WARNING'}, 'Works only Solid mode')
                    else:
                        if space.shading.light == 'MATCAP':
                            space.shading.light = 'STUDIO'
                        if space.shading.light == 'STUDIO' or space.shading.light == 'FLAT':
                            if space.shading.color_type == 'TEXTURE':
                                space.shading.color_type = 'MATERIAL'
                            else:
                                space.shading.color_type = 'TEXTURE'
        return {'FINISHED'}
