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
import numpy


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    vRayTolerance:bpy.props.FloatProperty(name='Vertex Raycast Tolerance',default=0.1)
    eRayTolerance:bpy.props.FloatProperty(name='Edge Raycat Tolerance',default=0.1)
    vLinkTolerance:bpy.props.FloatProperty(name='Vertex Linked Tolerance',default=0.2)
    eLinkTolerance:bpy.props.FloatProperty(name='Edge Linked Tolerance',default=0.2)

    def draw(self, context):
        layout = self.layout
        vRayRow = layout.row()
        eRayRow = layout.row()
        vLinkRow = layout.row()
        eLinkRow = layout.row()

        vRayRow.prop(self,'vRayTolerance')
        eRayRow.prop(self,'eRayTolerance')
        vLinkRow.prop(self,'vLinkTolerance')
        eLinkRow.prop(self,'eLinkTolerance')

def getValue(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

def ray(coords):
    view_layer = bpy.context.view_layer
    region = bpy.context.region
    region3d = bpy.context.space_data.region_3d
    origin = view3d_utils.region_2d_to_origin_3d(region,region3d,coords )
    direction = view3d_utils.region_2d_to_vector_3d(region,region3d,coords)
    return bpy.context.scene.ray_cast(view_layer,origin,direction)

def traceEdge(hitResult,tolerance):
    for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
        edge = hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index]
        l1 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[0]].co)
        l2 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[1]].co)
        p = numpy.array(hitResult[1])
        if distToLine(l1,l2,p) < getValue(tolerance):
            return edge
    return None

def t(l1,l2,p):
        x = l1-l2
        return numpy.dot(p-l2,x)/numpy.dot(x,x)

def distToLine(l1,l2,p):
    return numpy.linalg.norm(t(l1,l2,p)*(l1-l2)+l2-p)

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
            if hitResult[0] and hitResult[4].select_get():
                #face link
                if bpy.context.scene.tool_settings.mesh_select_mode[2] :
                    if self.toggle:
                        bpy.ops.mesh.select_all(action='DESELECT')
                    if self.deselect:
                        if self.alt:
                            bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=False, deselect=True, toggle=False, ring=True)
                        else:
                            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                            hitResult[4].data.polygons[hitResult[3]].select = False
                            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                            bpy.ops.mesh.select_all(action='INVERT')
                            bpy.ops.mesh.select_linked(delimit={'SEAM'})
                            bpy.ops.mesh.select_all(action='INVERT')
                    else:
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                        hitResult[4].data.polygons[hitResult[3]].select = True
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        if self.alt:
                            bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=True, deselect=False, toggle=False, ring=True)
                        else:
                            bpy.ops.mesh.select_linked(delimit={'SEAM'})
                #vert link
                elif bpy.context.scene.tool_settings.mesh_select_mode[0]:
                    if self.toggle:
                        bpy.ops.mesh.select_all(action='DESELECT')
                    
                    for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                        wCo = hitResult[4].matrix_world @ hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].co
                        l1 = numpy.array(wCo)
                        l2 = numpy.array(hitResult[1])
                        dist = numpy.linalg.norm(l1 - l2)
                        
                        if dist < getValue('vLinkTolerance'):
                            if self.deselect:
                                if hitResult[4].data.polygons[hitResult].select:
                                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                                    hitResult[4].data.polygons[hitResult].select = False
                                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

                                if self.alt:
                                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=False, deselect=True, toggle=False, ring=False)
                                else:
                                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                                    hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].select = False
                                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                                    bpy.ops.mesh.select_all(action='INVERT')
                                    bpy.ops.mesh.select_linked(delimit={'SEAM'})
                                    bpy.ops.mesh.select_all(action='INVERT')
                            else:
                                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                                hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].select = True
                                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                                if self.alt:
                                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=True, deselect=False, toggle=False, ring=False)
                                else:
                                    bpy.ops.mesh.select_linked(delimit={'SEAM'})
                            break
                #edge link
                elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
                    if self.toggle:
                        bpy.ops.mesh.select_all(action='DESELECT')
                    for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                        edge = hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index]
                        l1 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[0]].co)
                        l2 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[1]].co)
                        p = numpy.array(hitResult[1])
                        if distToLine(l1,l2,p) < getValue('eLinkTolerance'):
                            if self.deselect:
                                if self.alt:
                                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=False, deselect=True, toggle=False, ring=True)
                                else:
                                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=False, deselect=True, toggle=False, ring=False)
                            else:
                                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                                edge.select = True
                                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                                if not self.alt:
                                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=True, deselect=False, toggle=False, ring=False)
                                else:
                                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT',extend=True, deselect=False, toggle=False, ring=True)
                            break
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
    extend = False
    deselect = False
    toggle = True
    
    coords = [0,0]
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
            context.area.tag_redraw()
            self.coords = [event.mouse_region_x,event.mouse_region_y]
            hitResult = ray(self.coords)
            #vert raycast
            if hitResult[0] and hitResult[4].select_get() and bpy.context.scene.tool_settings.mesh_select_mode[0]:
                for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                    wCo = hitResult[4].matrix_world @ hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].co
                    l1 = numpy.array(wCo)
                    l2 = numpy.array(hitResult[1])
                    dist = numpy.linalg.norm(l1 - l2)
                    if dist < getValue('vRayTolerance'):
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                        if self.deselect:
                            for pLoop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                                hitResult[4].data.edges[hitResult[4].data.loops[pLoop].edge_index].select = False
                            hitResult[4].data.polygons[hitResult[3]].select = False
                            hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].select = False
                        else:
                            hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].select = True
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        break
            #face raycast
            elif hitResult[0] and hitResult[4].select_get() and bpy.context.scene.tool_settings.mesh_select_mode[2]:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                if self.deselect:
                    hitResult[4].data.polygons[hitResult[3]].select = False
                    for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                        hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index].select = False
                        hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].select = False
                else:
                    hitResult[4].data.polygons[hitResult[3]].select = True
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            #edge raycast
            elif hitResult[0] and hitResult[4].select_get() and bpy.context.scene.tool_settings.mesh_select_mode[1]:
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                edge = traceEdge(hitResult,'eRayTolerance')
                for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                    edge = hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index]
                    l1 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[0]].co)
                    l2 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[1]].co)
                    p = numpy.array(hitResult[1])
                    if distToLine(l1,l2,p) < getValue('eRayTolerance'):
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                        if self.deselect:
                            hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index].select = False
                            for index in hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index].vertices:
                                hitResult[4].data.vertices[index].select = False    
                            hitResult[4].data.polygons[hitResult[3]].select = False
                        else:
                            hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index].select = True
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        break
                    
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
        if event.ctrl:
            self.deselect = True
        elif not event.ctrl:
            self.deselect = False
        if event.shift:
            self.extend = True
        elif not event.shift:
            self.extend = False
        if not event.ctrl and not event.shift and bpy.context.mode == 'EDIT_MESH':
            self.toggle = True
            bpy.ops.mesh.select_all(action='DESELECT')
        else:
            self.toggle = False    
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        





def register():
    bpy.utils.register_class(AddonPreferences)
    bpy.utils.register_class(ASelection_Conn)
    bpy.utils.register_class(ASelection_Ray)
        
        
        
def unregister():
    bpy.utils.unregister_class(AddonPreferences)
    bpy.utils.unregister_class(ASelection_Conn)
    bpy.utils.unregister_class(ASelection_Ray)
        