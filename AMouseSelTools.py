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
    "blender": (2, 91, 0),
    "location": "Generic",
    "wiki_url": "https://youtu.be/r9TZU51CHXc",
    "category": "Generic"
}

import bpy
from bpy_extras import view3d_utils
import numpy
import bmesh
addon_keymaps = []
raycast_keys = []
linked_keys = []
class AddonPreferences(bpy.types.AddonPreferences): 
    bl_idname = __name__

    def updateLinkedKeys(self,context):
        if getValue('enableSelectLinked'):
            for km, kmi in linked_keys:
                km.keymap_items.remove(kmi)
            linked_keys.clear()
            wm = bpy.context.window_manager
            #mesh keys
            km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
            #click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=False,head=True)
            linked_keys.append((km, kmi))
            #alt click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=False,shift=False,head=True)
            linked_keys.append((km, kmi))
            #ctrl click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=True,shift=False,head=True)
            linked_keys.append((km, kmi))
            #shift click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=True,head=True)
            linked_keys.append((km, kmi))
            #ctrl shift click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=True,shift=True,head=True)
            linked_keys.append((km, kmi))
            #alt shift click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=False,shift=True,head=True)
            linked_keys.append((km, kmi))
            #alt ctrl click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=True,shift=False,head=True)
            linked_keys.append((km, kmi))
            #obj keys
            km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
            #click
            kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=False,head=True)
            linked_keys.append((km, kmi)) 
        else:
            for km, kmi in linked_keys:
                km.keymap_items.remove(kmi)
            linked_keys.clear()
        return None
        
    def updateRaycastKeys(self,context):
        if getValue('enableRaycast'):
            for km, kmi in raycast_keys:
                km.keymap_items.remove(kmi)
            raycast_keys.clear()
            wm = bpy.context.window_manager
            #mesh keys
            km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
            #press
            kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
            raycast_keys.append((km, kmi))
            #ctrl press
            kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
            raycast_keys.append((km, kmi))
            #shift press
            kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
            raycast_keys.append((km, kmi)) 
            #obj keys
            km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
            #click
            #press
            kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
            raycast_keys.append((km, kmi))
            #shift press
            kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
            raycast_keys.append((km, kmi))
            #ctrl press
            kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
            raycast_keys.append((km, kmi))
        else:
            for km, kmi in raycast_keys:
                km.keymap_items.remove(kmi)
            raycast_keys.clear()
        return None

    RayTolerance:bpy.props.FloatProperty(name='Vertex Raycast Tolerance',default=25)
    vLinkTolerance:bpy.props.FloatProperty(name='Vertex Linked Tolerance',default=0.2)
    eLinkTolerance:bpy.props.FloatProperty(name='Edge Linked Tolerance',default=0.2)
    deselectSelected:bpy.props.BoolProperty(name='Deselect Selected Linked Only',default=True)
    bringMenuOnFail:bpy.props.BoolProperty(name='Bring Menu On Raycast Fail',default=False)
    enableRaycast:bpy.props.BoolProperty(name='Right Click Raycast Tool',default=True,update=updateRaycastKeys)
    enableSelectLinked:bpy.props.BoolProperty(name='Double Click Select Linked Tool',default=True,update=updateLinkedKeys)

    def draw(self, context):
        layout = self.layout
        warningBox = layout.box()
        warningBox.label(text='To work properly, disable the hotkey for 3dView->Select(The one that is mapped on Ctrl-Left Click)',icon='ERROR')
        mainBox = layout.box()
        mainBox.label(text='Selection Tools')
        mainOp = layout.box()
        mainOp.label(text='Additional Options')
        tolOp = layout.box()
        tolOp.label(text='Tolerance Distances')
        enableRaycast = mainBox.row()
        enableLinked = mainBox.row()
        vRayRow = tolOp.row()
        eRayRow = tolOp.row()
        vLinkRow = tolOp.row()
        eLinkRow = tolOp.row()
        dSelRow = mainOp.row()
        mFailRow = mainOp.row()

        enableRaycast.prop(self,'enableRaycast')
        enableLinked.prop(self,'enableSelectLinked')
        vRayRow.prop(self,'RayTolerance')
        vLinkRow.prop(self,'vLinkTolerance')
        eLinkRow.prop(self,'eLinkTolerance')
        dSelRow.prop(self,'deselectSelected')
        mFailRow.prop(self,'bringMenuOnFail')

def getValue(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

def ray(coords):
    depthGraph = bpy.context.evaluated_depsgraph_get()
    region = bpy.context.region
    region3d = bpy.context.space_data.region_3d
    origin = view3d_utils.region_2d_to_origin_3d(region,region3d,coords )
    direction = view3d_utils.region_2d_to_vector_3d(region,region3d,coords)
    return bpy.context.scene.ray_cast(depthGraph,origin,direction)

def t(l1,l2,p):
        x = l1-l2
        return numpy.dot(p-l2,x)/numpy.dot(x,x)

def distToLine(l1,l2,p):
    return numpy.linalg.norm(t(l1,l2,p)*(l1-l2)+l2-p)

class ASelection_Linked(bpy.types.Operator):
    bl_idname = "object.aselection_link"
    bl_label = "A*Selection Connected"
    bl_options = {'REGISTER', 'UNDO'}
    coords = [0,0]
    extend = False
    deselect = False
    toggle = True
    alt = False
    #custom flush. Built-in function not working properly all the time
    def flushSelection(self,bm):
        for face in bm.faces:
            face.select_set(False)
        for edge in bm.edges:
            edge.select_set(False)
        for vert in bm.verts:
            vert.select_set(False)

    def execute(self,context):
        hitResult = ray(self.coords)
        subSurfList = {}
        if bpy.context.mode == 'OBJECT':
            if hitResult[0]:
                for obj in bpy.context.visible_objects:
                    if obj.type == hitResult[4].type :
                        obj.select_set(True)
        if bpy.context.mode == 'EDIT_MESH':
            if hitResult[0] and hitResult[4] in bpy.context.selected_objects:
                objects  = bpy.context.selected_objects
                for obj in objects:
                    if obj.type == 'MESH':
                        for mod in obj.modifiers:
                            if mod.type == 'SUBSURF':
                                subSurfList[mod] = mod.levels
                        if len(subSurfList)!=0:
                            for mod,lvl in subSurfList.items():
                                if mod.levels > 0 :
                                    mod.levels = 0
                        #scene update after switching subsurf levels
                        dg = bpy.context.evaluated_depsgraph_get()
                        dg.update()
                        #---------#
                        hitResult = ray(self.coords)
                        obj.update_from_editmode()
                        bm = bmesh.new()
                        bm.from_mesh(obj.data)
                        bm.faces.ensure_lookup_table()
                        if hitResult[4] == obj:
                            distances = {}
                            linked = []
                            select = []
                            if self.toggle:
                                self.flushSelection(bm)
                        #face link
                            if bpy.context.scene.tool_settings.mesh_select_mode[2]:
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
                                        face.select_set(False)
                                else:
                                    for face in select:
                                        face.select_set(True)
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
                                                face.select_set(False)
                                    else:
                                        for vert in select:
                                            vert.select_set(True)
                            #edge link
                            elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
                                for face in bm.faces:
                                    if face.index == hitResult[3]:
                                        for edge in face.edges:
                                            l1 = numpy.array(hitResult[4].matrix_world @ edge.verts[0].co)
                                            l2 = numpy.array(hitResult[4].matrix_world @ edge.verts[1].co)
                                            p = numpy.array(hitResult[1])
                                            distances[distToLine(l1,l2,p)] = edge
                                if min(distances)<= getValue('RayTolerance'):
                                    del select[:]
                                    closest = distances.get(min(distances))
                                    linked.append(closest)
                                    while len(linked) != 0:
                                        select.append(linked.pop())
                                        for loop in select[len(select)-1].link_loops:
                                            if self.alt:
                                                if len(loop.face.verts)==4:
                                                    ring = loop.link_loop_radial_next.link_loop_next.link_loop_next.edge
                                                    rLoop = loop.link_loop_radial_next.link_loop_next.link_loop_next
                                                    if ring not in select and len(rLoop.face.verts)==4 :
                                                        linked.append(loop.link_loop_radial_next.link_loop_next.link_loop_next.edge)
                                            else:
                                                if len(loop.vert.link_edges)==4:
                                                    if not self.alt:
                                                        if loop.link_loop_prev.link_loop_radial_next.link_loop_prev.edge not in select:
                                                            linked.append(loop.link_loop_prev.link_loop_radial_next.link_loop_prev.edge)
                                    if self.deselect:
                                        for edge in select:
                                            edge.select_set(False)    
                                    else:
                                        for edge in select:
                                            edge.select_set(True)
                    for mod,lvl in subSurfList.items():
                        mod.levels = lvl
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
                    bm.to_mesh(obj.data)
                    bpy.ops.object.mode_set(mode='EDIT', toggle=True)
                    bm.free()
        return {'FINISHED'}
    def invoke(self,context,event):
        self.coords = [event.mouse_region_x,event.mouse_region_y]
        if event.ctrl:
            self.deselect = True
        else:
            self.deselect = False
        if event.alt:
            self.alt = True
        elif not event.alt:
            self.alt = False
        if event.shift:
            self.extend = True
        elif not event.shift:
            self.extend = False
        if not event.ctrl and not event.shift :
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
    subSurfList = {}
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
                if hitResult[0]:
                    if self.toggle:
                        bpy.ops.view3d.select_circle(x=event.mouse_region_x, y=event.mouse_region_y, radius=getValue('RayTolerance'), wait_for_input=True, mode='ADD')
                    if self.deselect:
                        bpy.ops.view3d.select_circle(x=event.mouse_region_x, y=event.mouse_region_y, radius=getValue('RayTolerance'), wait_for_input=False, mode='SUB')
                    else:
                        bpy.ops.view3d.select_circle(x=event.mouse_region_x, y=event.mouse_region_y, radius=getValue('RayTolerance'), wait_for_input=False, mode='ADD')
                else:
                    if getValue('bringMenuOnFail'):
                        return bpy.ops.wm.call_menu(name='VIEW3D_MT_edit_mesh_context_menu')
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if event.value == 'RELEASE':
            for mod,lvl in self.subSurfList.items():
                        mod.levels = lvl 
            return {'FINISHED'}
        return {'RUNNING_MODAL'}
    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        self.coords = [event.mouse_region_x,event.mouse_region_y]
        hitResult = ray(self.coords)
        if bpy.context.mode == 'OBJECT':
            if hitResult[0] == False:
                return bpy.ops.wm.call_menu(name='VIEW3D_MT_object_context_menu')
        elif bpy.context.mode == 'EDIT_MESH':
            if hitResult[0] == False or (hitResult[0] and hitResult[4] not in bpy.context.selected_objects):
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
    if getValue('enableSelectLinked'):
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=False,head=True)
        linked_keys.append((km, kmi))
        #alt click
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=False,shift=False,head=True)
        linked_keys.append((km, kmi))
        #ctrl click
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=True,shift=False,head=True)
        linked_keys.append((km, kmi))
        #shift click
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=True,head=True)
        linked_keys.append((km, kmi))
        #alt shift click
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=False,shift=True,head=True)
        linked_keys.append((km, kmi))
        #alt ctrl click
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=True,ctrl=True,shift=False,head=True)
        linked_keys.append((km, kmi))
    #press
    if getValue('enableRaycast'):
        kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
        raycast_keys.append((km, kmi))
        #ctrl press
        kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
        raycast_keys.append((km, kmi))
        #shift press
        kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
        raycast_keys.append((km, kmi)) 
    #obj keys
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    #click
    if getValue('enableSelectLinked'):
        kmi = km.keymap_items.new("object.aselection_link",'LEFTMOUSE',value='DOUBLE_CLICK',any=False,alt=False,ctrl=False,shift=False,head=True)
        linked_keys.append((km, kmi)) 
    #press
    if getValue('enableRaycast'):
        kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
        raycast_keys.append((km, kmi))
        #shift press
        kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
        raycast_keys.append((km, kmi))
        #ctrl press
        kmi = km.keymap_items.new("object.aselection_ray",'RIGHTMOUSE',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
        raycast_keys.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    
def unregister():
    for km, kmi in linked_keys:
        km.keymap_items.remove(kmi)
    for km, kmi in raycast_keys:
        km.keymap_items.remove(kmi)
    linked_keys.clear()
    raycast_keys.clear()
    bpy.utils.unregister_class(AddonPreferences)
    bpy.utils.unregister_class(ASelection_Linked)
    bpy.utils.unregister_class(ASelection_Ray)
        