# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "UV Toolkit",
    "author": "Alexander Belyakov",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "UV",
}

import bpy
from .operators.boundary_seam_settings import BoundarySeamSettings
from .operators.boundary_seam import BoundarySeam
from .operators.checker_grid_type import CheckerGridType
from .operators.clear_all_seams import ClearAllSeams
from .operators.create_checker_map import CheckerMap
from .operators.custom_sizes_checker_map import CustomSizesCheckerMap
from .operators.mirror_uv_x import MirrorUvX
from .operators.mirror_uv_y import MirrorUvY
from .operators.move_islands_down import MoveIslandsDown
from .operators.move_islands_left import MoveIslandsLeft
from .operators.move_islands_right import MoveIslandsRight
from .operators.move_islands_up import MoveIslandsUp
from .operators.quick_drag_island import QuickDragIsland
from .operators.remove_all_checker_maps import RemoveAllCheckerMaps
from .operators.disable_selected_checker_maps import DisableSelectedCheckerMaps
from .operators.hotkeys import Hotkeys
from .operators.mirror_seam import MirrorSeam
from .operators.rotate_selected_uv_islands import RotateUVIslands
from .operators.scale_individual_origins import ScaleIndividualOrigins
from .operators.sharp_edges_from_uv_islands import SharpEdgesFromUvIslands
from .operators.toggle_texture import TextureMode
from .operators.unwrap_selected import UnwrapSelected
from .operators.uv_sync_mode import UvSyncMode
from .operators.view_all_uv import ViewAllUv
from .ui.panel import (UVTOOLKIT_PT_uv_sync,
                       UVTOOLKIT_PT_uv_sync_settings,
                       UVTOOLKIT_PT_tools,
                       UVTOOLKIT_PT_display,
                       UVTOOLKIT_PT_checker_map,
                       UVTOOLKIT_PT_settings,
                       UVTOOLKIT_PT_square,
                       UVTOOLKIT_PT_horizontal_rectangle,
                       UVTOOLKIT_PT_vertical_rectangle,
                       UVTOOLKIT_PT_help,
                       )
from .ui.pie_menu import PieUvToolkit
from .preferences import UvToolkitPreferences


classes = (
    BoundarySeamSettings,
    BoundarySeam,
    CheckerGridType,
    ClearAllSeams,
    CheckerMap,
    CustomSizesCheckerMap,
    MirrorUvX,
    MirrorUvY,
    MoveIslandsDown,
    MoveIslandsLeft,
    MoveIslandsRight,
    MoveIslandsUp,
    QuickDragIsland,
    RemoveAllCheckerMaps,
    DisableSelectedCheckerMaps,
    Hotkeys,
    MirrorSeam,
    RotateUVIslands,
    ScaleIndividualOrigins,
    SharpEdgesFromUvIslands,
    TextureMode,
    UnwrapSelected,
    UvSyncMode,
    ViewAllUv,
    UVTOOLKIT_PT_uv_sync,
    UVTOOLKIT_PT_uv_sync_settings,
    UVTOOLKIT_PT_tools,
    UVTOOLKIT_PT_display,
    UVTOOLKIT_PT_checker_map,
    UVTOOLKIT_PT_settings,
    UVTOOLKIT_PT_square,
    UVTOOLKIT_PT_horizontal_rectangle,
    UVTOOLKIT_PT_vertical_rectangle,
    UVTOOLKIT_PT_help,
    PieUvToolkit,
    UvToolkitPreferences,
)


addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_quick_drag_island', 'F', 'PRESS')
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_scale_individual_origins', 'S', 'PRESS', alt=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_sync_mode', 'TAB', 'PRESS')
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_move_islands_right', 'RIGHT_ARROW', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_move_islands_left', 'LEFT_ARROW', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_move_islands_up', 'UP_ARROW', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_move_islands_down', 'DOWN_ARROW', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_unwrap_selected', 'E', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
        kmi = km.keymap_items.new('uv.toolkit_view_all_uv', 'C', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))

        # if bpy.context.preferences.addons["uv_toolkit"].preferences.use_pie_menu == "enable":
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS', shift=True)
        kmi.properties.name = "UVTOOLKIT_MT_pie"
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
