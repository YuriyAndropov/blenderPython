import bpy
import rna_keymap_ui
from bpy.props import EnumProperty


def get_hotkey_entry_item(km, kmi_name, kmi_value):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            print(i, km.keymap_items.keys()[i])
            if km.keymap_items[i].properties.name == kmi_value:
                print(km.keymap_items[i].properties.name)
                return km_item
    return None


class UvToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    checker_type: EnumProperty(
        items=[
            ("UV_GRID", "Checker Grid", "", "", 0),
            ("COLOR_GRID", "Color Grid", "", "", 1)
        ],
        default="UV_GRID"
    )

    assign_image: EnumProperty(
        items=[
            ("enable", "Enable", "", "", 0),
            ("disable", "Disable", "", "", 1)
        ],
        default="enable"
    )

    # use_pie_menu: EnumProperty(
    #     items=[
    #         ("enable", "Enable", "", "", 0),
    #         ("disable", "Disable", "", "", 1)
    #     ],
    #     default="enable"
    # )

    uv_sync_auto_select: EnumProperty(
        items=[
            ("enable", "Enable", "", "", 0),
            ("disable", "Disable", "", "", 1)
        ],
        default="enable"
    )

    uv_sync_selection_mode: EnumProperty(
        items=[
            ("enable", "Enable", "", "", 0),
            ("disable", "Disable", "", "", 1)
        ],
        default="enable"
    )

    boundary_loop_unwrap: EnumProperty(
        items=[
            ("enable", "Enable", "", "", 0),
            ("disable", "Disable", "", "", 1)
        ],
        default="disable"
    )

    boundary_loop_enable_uv_sync: EnumProperty(
        items=[
            ("enable", "Enable", "", "", 0),
            ("disable", "Disable", "", "", 1)
        ],
        default="disable"
    )

    boundary_loop_enable_live_unwrap: EnumProperty(
        items=[
            ("enable", "Enable", "", "", 0),
            ("disable", "Disable", "", "", 1)
        ],
        default="disable"
    )

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager

        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text='UV Toolkit Pie menu Hotkey')
        col.separator()
        kc = wm.keyconfigs.user
        km = kc.keymaps['3D View']
        kmi = get_hotkey_entry_item(km, 'wm.call_menu_pie', 'UVTOOLKIT_MT_pie')
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

        # box = layout.box()
        # row = box.row()
        # row.label(text="UV Toolkit Pie menu: (Shift+F)")
        # row.prop(self, "use_pie_menu", expand=True)

        layout.label(text="Checker image settings:")
        box = layout.box()
        row = box.row()
        row.label(text="Default checker style")
        row.prop(self, "checker_type", expand=True)
        row = box.row()
        row.label(text="Auto assign texture in UV Editor")
        row.prop(self, "assign_image", expand=True)

        layout.label(text="UV Sync settings:")
        box = layout.box()
        row = box.row()
        row.label(text="Auto select mesh")
        row.prop(self, "uv_sync_auto_select", expand=True)
        row = box.row()
        row.label(text="Sync selection mode")
        row.prop(self, "uv_sync_selection_mode", expand=True)

        layout.label(text="Boundary Seam settings:")
        box = layout.box()
        row = box.row()
        row.label(text="Regular Unwrap after Boundary seam")
        row.prop(self, "boundary_loop_unwrap", expand=True)
        row = box.row()
        row.label(text="Alternative Unwrap after Boundary seam")
        row.prop(self, "boundary_loop_enable_live_unwrap", expand=True)
        row = box.row()
        row.label(text="Enable UV Sync")
        row.prop(self, "boundary_loop_enable_uv_sync", expand=True)

        layout.label(text="Support Me on:")
        box = layout.box()
        row = box.row()
        row.operator("wm.url_open", text="Gumroad").url = "https://gumroad.com/alexbel"
        row.operator("wm.url_open", text="PayPal").url = "https://paypal.me/belyakovalexander"
        # row.operator("wm.url_open", text="Blender Market").url = ""
