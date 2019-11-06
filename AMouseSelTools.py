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
    "name": "A* Mouse Selection Tools",
    "description": "A* Mouse Selection Tools ",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Mesh",
    "wiki_url": "",
    "category": "Mesh"
}

import bpy
from bpy_extras import view3d_utils
import numpy
import bmesh

addon_keymaps = []

class AddonPreferences(bpy.types.AddonPreferences): 
    bl_idname = __name__

    vRayTolerance:bpy.props.FloatProperty(name='Vertex Raycast Tolerance',default=0.1)
    eRayTolerance:bpy.props.FloatProperty(name='Edge Raycat Tolerance',default=0.1)
    vLinkTolerance:bpy.props.FloatProperty(name='Vertex Linked Tolerance',default=0.2)
    eLinkTolerance:bpy.props.FloatProperty(name='Edge Linked Tolerance',default=0.2)
    deselectSelected:bpy.props.BoolProperty(name='Deselect Selected Linked Only',default=True)

    def draw(self, context):
        layout = self.layout
        vRayRow = layout.row()
        eRayRow = layout.row()
        vLinkRow = layout.row()
        eLinkRow = layout.row()
        dSelRow = layout.row()

        vRayRow.prop(self,'vRayTolerance')
        eRayRow.prop(self,'eRayTolerance')
        vLinkRow.prop(self,'vLinkTolerance')
        eLinkRow.prop(self,'eLinkTolerance')
        dSelRow.prop(self,'deselectSelected')
def getValue(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

def ray(coords):
    view_layer = bpy.context.view_layer
    region = bpy.context.region
    region3d = bpy.context.space_data.region_3d
    origin = view3d_utils.region_2d_to_origin_3d(region,region3d,coords )
    direction = view3d_utils.region_2d_to_vector_3d(region,region3d,coords)
    return bpy.context.scene.ray_cast(view_layer,origin,direction)

def t(l1,l2,p):
        x = l1-l2
        return numpy.dot(p-l2,x)/numpy.dot(x,x)

def distToLine(l1,l2,p):
    return numpy.linalg.norm(t(l1,l2,p)*(l1-l2)+l2-p)

class ASelection_Linked(bpy.types.Operator):
    bl_idname = "object.aselection_link"
    bl_label = "A*Selection Connected"
    bl_options = {'REGISTER', 'UNDO'}
    #############There is an operator in 3dView called select. It is mapped in Ctrl LClick and it is breaking the script.Should be disabled
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
            if hitResult[0] and hitResult[4] in bpy.context.selected_objects:
                for obj in bpy.context.selected_objects:
                    if obj.type == 'MESH':
                        obj.update_from_editmode()
                        bm = bmesh.new()
                        bm.from_mesh(obj.data)
                        if self.toggle:
                            bm.select_flush(False)
                        if hitResult[4] == obj:
                            distances = {}
                            linked = []
                            select = []
                        #face link
                            if bpy.context.scene.tool_settings.mesh_select_mode[2]:
                                bm.faces.ensure_lookup_table()
                                linked.append(bm.faces[hitResult[3]])
                                while len(linked) != 0:
                                    select.append(linked.pop())
                                    for edge in select[len(select)-1].edges:
                                        for face in edge.link_faces:
                                            if face not in select :
                                                linked.append(face)
                                if self.deselect:
                                    if getValue('deselectSelected'):
                                        del select[:]
                                        linked.append(bm.faces[hitResult[3]])
                                        while len(linked) != 0:
                                            select.append(linked.pop())
                                            for edge in select[len(select)-1].edges:
                                                for face in edge.link_faces:
                                                    if face not in select and select[len(select)-1].select and face.select:
                                                        linked.append(face)
                                    for face in select:
                                        face.select = False
                                else:
                                    for face in select:
                                        face.select = True
                            #vert link
                            elif bpy.context.scene.tool_settings.mesh_select_mode[0]:
                                for face in bm.faces:
                                    if face.index == hitResult[3]:
                                        for vert in face.verts:
                                            wCo = hitResult[4].matrix_world @ vert.co
                                            l1 = numpy.array(wCo)
                                            l2 = numpy.array(hitResult[1])
                                            distances[numpy.linalg.norm(l1 - l2)] = vert
                                        break
                                if min(distances) <= getValue('vLinkTolerance'):
                                    closest = distances.get(min(distances))
                                    linked.append(closest)
                                    while len(linked) != 0:
                                        select.append(linked.pop())
                                        for edge in select[len(select)-1].link_edges:
                                            for vert in edge.verts:
                                                if vert not in select:
                                                    linked.append(vert)
                                    if self.deselect:
                                        if getValue('deselectSelected'):
                                            linked.append(closest)
                                            del select[:]
                                            while len(linked) != 0:
                                                select.append(linked.pop())
                                                for edge in select[len(select)-1].link_edges:
                                                    for vert in edge.verts:
                                                        if select[len(select)-1].select and vert.select and vert not in select:
                                                            linked.append(vert)
                                        for vert in select:
                                            for face in vert.link_faces:
                                                face.select = False
                                    else:
                                        for vert in select:
                                            vert.select = True
                            #edge link
                            elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
                                for face in bm.faces:
                                    if face.index == hitResult[3]:
                                        for edge in face.edges:
                                            l1 = numpy.array(hitResult[4].matrix_world @ edge.verts[0].co)
                                            l2 = numpy.array(hitResult[4].matrix_world @ edge.verts[1].co)
                                            p = numpy.array(hitResult[1])
                                            distances[distToLine(l1,l2,p)] = edge
                                if min(distances)<= getValue('eRayTolerance'):
                                    closest = distances.get(min(distances))
                                    linked.append(closest)
                                    while len(linked) != 0:
                                        select.append(linked.pop())
                                        for loop in select[len(select)-1].link_loops:
                                            if len(loop.face.verts)==4:
                                                if not self.alt:
                                                    if loop.link_loop_prev.link_loop_radial_next.link_loop_prev.edge not in select:
                                                        linked.append(loop.link_loop_prev.link_loop_radial_next.link_loop_prev.edge)
                                                else:
                                                    if loop.link_loop_radial_next.link_loop_next.link_loop_next.edge not in select:
                                                        linked.append(loop.link_loop_radial_next.link_loop_next.link_loop_next.edge)
                                    if self.deselect:
                                            for edge in select:
                                                edge.select = False    
                                    else:
                                        for edge in select:
                                                edge.select = True    
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                        bm.to_mesh(obj.data)
                        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        bm.free()
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
            if bpy.context.mode == 'OBJECT':
                if hitResult[0]:
                    if self.toggle:
                        bpy.ops.object.select_all(action='DESELECT')
                    if self.deselect:
                        hitResult[4].select_set(False)
                    else:
                        hitResult[4].select_set(True)
            elif bpy.context.mode == 'EDIT_MESH':
                distances = []
                #vert raycast
                if hitResult[0]:
                    hitResult[4].update_from_editmode()           
                if hitResult[0] and hitResult[4].select_get() and bpy.context.scene.tool_settings.mesh_select_mode[0]:
                    for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                        wCo = hitResult[4].matrix_world @ hitResult[4].data.vertices[hitResult[4].data.loops[loop].vertex_index].co
                        l1 = numpy.array(wCo)
                        l2 = numpy.array(hitResult[1])
                        distances.append(numpy.linalg.norm(l1 - l2))
                    if distances:
                        lowest = distances.index(min(distances))
                        if distances[lowest]<= getValue('vRayTolerance'):
                            index  = hitResult[4].data.loops[hitResult[4].data.polygons[hitResult[3]].loop_indices[0] + lowest].vertex_index
                            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                            if self.deselect:
                                bm = bmesh.new()
                                bm.from_mesh(hitResult[4].data)
                                bm.verts.ensure_lookup_table()
                                bm.faces.ensure_lookup_table()
                                bm.edges.ensure_lookup_table()
                                if bm.verts[index].select:
                                    bm.verts[index].select_set(False)
                                    for loop in bm.verts[index].link_loops:
                                        if loop.edge.select:
                                            loop.edge.select_set(False)
                                            #selecting back verts of the edge that are not raycasted
                                            for vert in loop.edge.verts:
                                                if bm.verts[index]!=bm.verts[vert.index]:
                                                    bm.verts[vert.index].select_set(True)
                                            #selecting back verts of the face that are not raycasted
                                            if loop.face.select:
                                                loop.face.select_set(False)
                                                for vert in loop.face.verts:
                                                    if bm.verts[index]!=bm.verts[vert.index]:
                                                        bm.verts[vert.index].select_set(True)
                                bm.to_mesh(hitResult[4].data)
                                bm.free()
                            else:
                                hitResult[4].data.vertices[index].select = True
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
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
                    for loop in hitResult[4].data.polygons[hitResult[3]].loop_indices:
                        edge = hitResult[4].data.edges[hitResult[4].data.loops[loop].edge_index]
                        l1 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[0]].co)
                        l2 = numpy.array(hitResult[4].matrix_world @ hitResult[4].data.vertices[edge.vertices[1]].co)
                        p = numpy.array(hitResult[1])
                        distances.append(distToLine(l1,l2,p))
                    lowest = distances.index(min(distances))
                    if distances[lowest]<= getValue('eRayTolerance'):
                        index = hitResult[4].data.loops[hitResult[4].data.polygons[hitResult[3]].loop_indices[0] + lowest].edge_index
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                        if self.deselect:
                            bm = bmesh.new()
                            bm.from_mesh(hitResult[4].data)
                            bm.faces.ensure_lookup_table()
                            bm.edges.ensure_lookup_table()
                            for face in bm.edges[index].link_faces:
                                if face.select:
                                    face.select_set(False)
                                    for edge in face.edges:
                                        if edge != bm.edges[index]:
                                            edge.select_set(True)
                            bm.edges[index].select_set(False)
                            bm.to_mesh(hitResult[4].data)
                            bm.free()
                        else:
                                hitResult[4].data.edges[index].select = True
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
    bpy.utils.register_class(ASelection_Linked)
    bpy.utils.register_class(ASelection_Ray)
    wm = bpy.context.window_manager
    #mesh keys
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    #click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #alt click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=False,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #ctrl click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=True,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #shift click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=True,head=True)
    addon_keymaps.append((km, kmi))
    #ctrl shift click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=True,shift=True,head=True)
    addon_keymaps.append((km, kmi))
    #alt shift click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=False,shift=True,head=True)
    addon_keymaps.append((km, kmi))
    #alt ctrl click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=True,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #press
    kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #ctrl press
    kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #shift press
    kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
    addon_keymaps.append((km, kmi)) 
    #obj keys
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    #click
    kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=False,head=True)
    addon_keymaps.append((km, kmi)) 
    #press
    kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
    addon_keymaps.append((km, kmi))
    #shift press
    kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
    addon_keymaps.append((km, kmi))
    #ctrl press
    kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
    addon_keymaps.append((km, kmi))
        
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(AddonPreferences)
    bpy.utils.unregister_class(ASelection_Linked)
    bpy.utils.unregister_class(ASelection_Ray)
        