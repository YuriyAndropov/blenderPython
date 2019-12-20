import bpy
from bpy.props import IntProperty


class CheckerMap(bpy.types.Operator):
    bl_idname = "uv.toolkit_create_checker_map"
    bl_label = "Create Checker Map"
    bl_description = "Create checker map (UVToolkit)"
    bl_options = {'REGISTER', 'UNDO'}

    width: IntProperty(options={'HIDDEN'})
    height: IntProperty(options={'HIDDEN'})

    def execute(self, context):
        addon_prefs = context.preferences.addons["uv_toolkit"].preferences
        if context.selected_objects == []:
            self.report({'WARNING'}, 'No Objects Selected')
            return {'FINISHED'}
        else:
            if addon_prefs.checker_type == "UV_GRID":
                gird_type = "UV_GRID"
            else:
                gird_type = "COLOR_GRID"
            #  Set Texture mode in Viewport
            for area in bpy.context.workspace.screens[0].areas:
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.shading.type == 'MATERIAL' or space.shading.type == 'RENDERED':
                            pass
                        else:
                            if space.shading.type == 'WIREFRAME':
                                space.shading.type = 'SOLID'
                            if space.shading.light == 'MATCAP':
                                space.shading.light = 'STUDIO'
                            if space.shading.light == 'STUDIO' or space.shading.light == 'FLAT':
                                space.shading.color_type = 'TEXTURE'

            #  Create checker material
            image_size = str(self.width) + "x" + str(self.height)
            if bpy.data.materials.get("checker_material_" + image_size) is None:
                mat = bpy.data.materials.new("checker_material_" + image_size)
                mat.use_nodes = True

                nodes = mat.node_tree.nodes
                nodes.remove(nodes["Principled BSDF"])
                # Create Checker Image
                bpy.ops.image.new(name="checker_image_" + image_size, width=self.width,
                                  height=self.height, generated_type=gird_type)

                node_texture = nodes.new(type="ShaderNodeTexImage")
                node_texture.image = bpy.data.images['checker_image_' + image_size]
                node_texture.location = -20, 300

                links = mat.node_tree.links
                links.new(node_texture.outputs[0], nodes.get("Material Output").inputs[0])
            # Сheck if image is deleted
            if bpy.data.images.get("checker_image_" + image_size) is None:
                mat = bpy.data.materials.get("checker_material_" + image_size)
                bpy.ops.image.new(name="checker_image_" + image_size, width=self.width,
                                  height=self.height, generated_type=gird_type)
                nodes = mat.node_tree.nodes
                nodes["Image Texture"].image = bpy.data.images['checker_image_' + image_size]
            # Set active image in UV Editor
            if addon_prefs.assign_image == "enable":
                for area in bpy.context.screen.areas:
                    if area.type == 'IMAGE_EDITOR':
                        area.spaces.active.image = bpy.data.images['checker_image_' + image_size]
            else:
                for area in bpy.context.screen.areas:
                    if area.type == 'IMAGE_EDITOR':
                        area.spaces.active.image = None
            # Assign checker material
            active_object = context.view_layer.objects.active  # Store active object
            material = bpy.data.materials['checker_material_' + image_size]

            for obj in context.selected_objects:
                if obj.type == 'MESH':
                    context.view_layer.objects.active = obj
                    if len(obj.data.materials) == 0:
                        obj.data.materials.append(material)
                    else:
                        obj.data.materials[0] = material
                context.view_layer.objects.active = active_object  # Restore active object
            return {'FINISHED'}
