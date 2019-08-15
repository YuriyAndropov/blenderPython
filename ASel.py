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
import mathutils


def ray(coords):
    view_layer = bpy.context.view_layer
    region = bpy.context.region
    region3d = bpy.context.space_data.region_3d
    origin = view3d_utils.region_2d_to_origin_3d(region,region3d,coords )
    direction = view3d_utils.region_2d_to_vector_3d(region,region3d,coords)
    return bpy.context.scene.ray_cast(view_layer,origin,direction)

class ASelection_Conn(bpy.types.Operator):
    bl_idname = "object.aselection_conn"
    bl_label = "A*Selection Connected"
    bl_options = {'REGISTER', 'UNDO'}

    coords = [0,0]
    extend = False
    deselect = False
    toggle = True
    alt = False

    def execute(self,context):
        hitResult = ray(self.coords)
        if bpy.context.mode == 'OBJECT':
            if hitResult[0]:
                for obj in bpy.context.visible_objects:
                    if obj.type == hitResult[4].type :
                        obj.select_set(True)
        if bpy.context.mode == 'EDIT_MESH':
            if hitResult[0]:
                if self.toggle:
                    if bpy.context.scene.tool_settings.mesh_select_mode[2] :
                        bpy.ops.mesh.select_all(action='DESELECT')
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)    
                        hitResult[4].data.polygons[hitResult[3]].select = True
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        if not self.alt:
                            
                            bpy.ops.mesh.select_linked(delimit={'SEAM'})
                        else:
                            bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=False, deselect=False, toggle=False, ring=True)
                elif self.extend:
                    if bpy.context.scene.tool_settings.mesh_select_mode[2] :
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)    
                        hitResult[4].data.polygons[hitResult[3]].select = True
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        if not self.alt:
                            bpy.ops.mesh.select_linked(delimit={'SEAM'})
                        else:
                            bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=True, deselect=False, toggle=False, ring=True)
                elif self.deselect:
                    if bpy.context.scene.tool_settings.mesh_select_mode[2] :
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)   
                        hitResult[4].data.polygons[hitResult[3]].select = False
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        if not self.alt:
                            bpy.ops.mesh.select_all(action='INVERT')
                            bpy.ops.mesh.select_linked(delimit={'SEAM'})
                            bpy.ops.mesh.select_all(action='INVERT')
                        else:
                            bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=False, deselect=True, toggle=False, ring=True)
                
        return {'FINISHED'}
    def invoke(self,context,event):
        self.coords = [event.mouse_region_x,event.mouse_region_y]
        
        if event.ctrl:
            self.deselect = True
        elif not event.ctrl:
            self.deselect = False
        if event.alt:
            self.alt = True
        elif not event.alt:
            self.alt = False
        if event.shift:
            self.extend = True
        elif not event.shift:
            self.extend = False
        if not event.ctrl and not event.shift:
            self.toggle = True
        else:
            self.toggle = False
        return self.execute(context)

class ASelection_Ray(bpy.types.Operator):
    bl_idname = "object.aselection_ray"
    bl_label = "A*Selection Ray"
    bl_options = {'REGISTER', 'UNDO'}
    
    coords = [0,0]
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
            context.area.tag_redraw()
            self.coords = [event.mouse_region_x,event.mouse_region_y]
            hitResult = ray(self.coords)
            #vert raycast
            if hitResult[0] and hitResult[4].select_get() and bpy.context.scene.tool_settings.mesh_select_mode[0]:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                for vIndex in hitResult[4].data.polygons[hitResult[3]].vertices:
                    wMat = hitResult[4].matrix_world @ hitResult[4].data.vertices[vIndex].co
                    tolerance =  mathutils.Vector((0.005,0.005,0.005))
                    #TODO change max and min to distance 
                    max = wMat + tolerance
                    min = wMat - tolerance
                    if hitResult[1]<max and hitResult[1]>min:
                        hitResult[4].data.vertices[vIndex].select = True
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            #face raycast
            elif hitResult[0] and hitResult[4].select_get() and bpy.context.scene.tool_settings.mesh_select_mode[2]:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                hitResult[4].data.polygons[hitResult[3]].select = True
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if event.value == 'RELEASE': 
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        self.coords = [event.mouse_region_x,event.mouse_region_y]
        hitResult = ray(self.coords)
        if hitResult[0] == False:
            if bpy.context.mode == 'OBJECT':
                return bpy.ops.wm.call_menu(name='VIEW3D_MT_object_context_menu')
            elif bpy.context.mode == 'EDIT_MESH':
                return bpy.ops.wm.call_menu(name='VIEW3D_MT_edit_mesh_context_menu')
            
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        





def register():
    bpy.utils.register_class(ASelection_Conn)
    bpy.utils.register_class(ASelection_Ray)
        
        
        
def unregister():
    bpy.utils.unregister_class(ASelection_Conn)
    bpy.utils.unregister_class(ASelection_Ray)
        