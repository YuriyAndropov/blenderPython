from bpy.types import Menu


class PieUvToolkit(Menu):
    bl_idname = "UVTOOLKIT_MT_pie"
    bl_label = "UV Toolkit Pie"

    def draw(self, context):
        tool_settings = context.tool_settings
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("mesh.mark_seam", text="Clear Seam").clear = True
        # 6 - RIGHT
        pie.operator("mesh.mark_seam", text="Mark Seam   ").clear = False
        # 2 - BOTTOM
        split = pie.split()
        box = split.box().column()
        box.prop(tool_settings, "use_edge_path_live_unwrap")
        box.operator("uv.smart_project")
        box.operator("uv.project_from_view")
        box.operator("uv.lightmap_pack")
        box.operator("uv.follow_active_quads")
        box.operator("uv.cube_project")
        box.operator("uv.cylinder_project")
        box.operator("uv.sphere_project")
        box.operator("uv.project_from_view")
        prop = box.operator("uv.project_from_view", text="Project from View (Bounds)")
        prop.camera_bounds, prop.correct_aspect, prop.scale_to_bounds = False, True, True
        box.operator("uv.reset")
        # 8 - TOP
        pie.operator("uv.unwrap", text="Unwrap")
        # 7 - TOP - LEFT
        pie.operator("uv.toolkit_clear_all_seams")
        # 9 - TOP - RIGHT
        pie.operator("uv.toolkit_boundary_seam")
        # 1 - BOTTOM - LEFT
        pie.operator("uv.toolkit_sharp_edges_from_uv_islands", text="Sharp Edges From Islands")
        # 3 - BOTTOM - RIGHT
        pie.operator("uv.toolkit_toggle_texture_mode", text="Show Texture in Viewport")
