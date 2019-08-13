'''
Copyright (C) 2019
yuriy.andropov@live.com

Created by Yurii Andropov

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "A* Selection",
    "description": "A* Selection Modes ",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Mesh",
    "wiki_url": "",
    "category": "Mesh"
}

import bpy
from bpy_extras import view3d_utils


def ray(coords):
    view_layer = bpy.context.view_layer
    region = bpy.context.region
    region3d = bpy.context.space_data.region_3d
    origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region,region3d,coords )
    direction = bpy_extras.view3d_utils.region_2d_to_vector_3d(region,region3d,coords)
    return bpy.context.scene.ray_cast(view_layer,origin,direction)

class ASelection_Conn(bpy.types.Operator):
    bl_idname = "object.aselection_conn"
    bl_label = "A*Selection Connected"
    bl_options = {'REGISTER', 'UNDO'}

    coords = [0,0]
    extend = False
    deselect = False
    toggle = True
    ring = False

    def execute(self,context):
        if bpy.context.mode == 'OBJECT':
            if ray(self.coords)[0]:
                for obj in bpy.context.visible_objects:
                    if obj.type == ray(self.coords)[4].type :
                        obj.select_set(True)
        if bpy.context.mode == 'EDIT_MESH':
            if bpy.context.scene.tool_settings.mesh_select_mode[2] :
                if ray(self.coords)[0]:
                    if self.toggle:
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)    
                        #bpy.ops.mesh.select_all(action='DESELECT')
                        ray(self.coords)[4].data.polygons[ray(self.coords)[3]].select = True
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        bpy.ops.mesh.select_linked(delimit={'SEAM'})
            if bpy.context.scene.tool_settings.mesh_select_mode[1]:
                bpy.ops.mesh.loop_select('INVOKE_DEFAULT')
        return {'FINISHED'}
    def invoke(self,context,event):
        self.coords = [event.mouse_region_x,event.mouse_region_y]
        if event.ctrl:
            print(event.ctrl)
        if event.alt:
            print(event.alt)
        if event.shift:
            print(event.shift)
        return self.execute(context)

class ASelection_Ray(bpy.types.Operator):
    bl_idname = "object.aselection_ray"
    bl_label = "A*Selection Connected"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self,context,event):
        #if event != 'RIGHTMOUSE':
            #return {'PASS_THROUGH'}
        #if event == 'RIGHTMOUSE' and event.value == 'RELEASE':
            #return {'FINISHED'}
        if bpy.context.mode == 'OBJECT':
            ray[4].select_set(True)
        print('modal')
        return {'RUNNING_MODAL'}

    def invoke(self,context,event):
        return {'RUNNING_MODAL'}



def register():
    bpy.utils.register_class(ASelection_Conn)
    bpy.utils.register_class(ASelection_Ray)
        
        
        
def unregister():
    bpy.utils.unregister_class(ASelection_Conn)
    bpy.utils.unregister_class(ASelection_Ray)
        