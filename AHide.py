'''
Copyright (C) 2020
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
    "name": "A* Hide/Unhide ",
    "description": "A* Hide Unhide",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Generic",
    "wiki_url": 'https://youtu.be/C-QVVQ8_1bE',
    "category": "Genric"
}
import bpy
import bmesh
keys = []

class ObjectListProperty(bpy.types.PropertyGroup):
    def updateHide(self,context):
        for obj in bpy.context.blend_data.objects:
            if self.name == obj.name:
                if self.hidden:
                    obj.hide_set(True)
                else:
                    obj.hide_set(False)

    hidden : bpy.props.BoolProperty(update=updateHide)
    name : bpy.props.StringProperty()
    icon : bpy.props.StringProperty()

class AUnhideByName(bpy.types.Operator):
    bl_idname = "object.aunhide_name"
    bl_label = "A* Unhide by Name"
    bl_options = {'REGISTER', 'UNDO'}
    objlist = []
    props = []
    def draw(self,context):
        self.objlist = bpy.context.blend_data.objects
        layout = self.layout
        objBox = layout.box()
        objBox.label(text='Objects List')
        for i in range(len(bpy.context.scene.objProp)):
            row = objBox.row()
            nameColumn = row.column()
            nameColumn.prop(bpy.context.scene.objProp[i],'name',text='',icon=bpy.context.scene.objProp[i].icon)
            nameColumn.enabled = False
            nameColumn.ui_units_x = 0.2
            hideColumn = row.column()
            hideColumn.prop(bpy.context.scene.objProp[i],'hidden',text='',invert_checkbox=True)
    def execute(self,context):
        bpy.context.scene.objProp.clear()
        return {'FINISHED'}
    def invoke(self,context,event):
        bpy.context.scene.objProp.clear()
        for obj in bpy.context.blend_data.objects:
            newProp = bpy.context.scene.objProp.add()
            newProp.hidden = obj.hide_get()
            newProp.name = obj.name
            if obj.type == 'MESH':
                newProp.icon = "OUTLINER_OB_MESH"
            elif obj.type == 'CURVE':
                newProp.icon = "OUTLINER_OB_CURVE"
            elif obj.type == 'SURFACE':
                newProp.icon = "OUTLINER_OB_SURFACE"
            elif obj.type == 'META':
                newProp.icon = "OUTLINER_OB_META"
            elif obj.type == 'FONT':
                newProp.icon = "OUTLINER_OB_FONT"
            elif obj.type == 'ARMATURE':
                newProp.icon = "OUTLINER_OB_ARMATURE"
            elif obj.type == 'LATTICE':
                newProp.icon = "OUTLINER_OB_LATTICE"
            elif obj.type == 'GPENCIL':
                newProp.icon = "OUTLINER_OB_GREASEPENCIL"
            elif obj.type == 'CAMERA':
                newProp.icon = "OUTLINER_OB_CAMERA"
            elif obj.type == 'LIGHT':
                newProp.icon = "OUTLINER_OB_LIGHT"
            elif obj.type == 'SPEAKER':
                newProp.icon = "OUTLINER_OB_SPEAKER"
            elif obj.type == 'LIGHT_PROBE':
                newProp.icon = "OUTLINER_OB_LIGHTPROBE"
            else:
                newProp.icon = "OUTLINER_OB_EMPTY"
        return context.window_manager.invoke_props_dialog(self, width=200)

class AHideUnhide(bpy.types.Operator):
    bl_idname = "object.ahide_unhide"
    bl_label = "A* Hide Unhide"
    bl_options = {'REGISTER', 'UNDO'}
    select = False
    hide = False
    nonSelected = False
    def getComps(self,bm):
        if bpy.context.mode == 'EDIT_MESH':
            #vert
            if bpy.context.scene.tool_settings.mesh_select_mode[0]:
                return bm.verts
            #edge
            elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
                return bm.edges
            #face
            elif bpy.context.scene.tool_settings.mesh_select_mode[2]:
                return bm.faces
        return None
    
    def execute(self,context):
        if bpy.context.mode == 'OBJECT':
            selected = bpy.context.selected_objects
            for obj in bpy.context.blend_data.objects:
                #hide object
                if self.hide:
                    if self.nonSelected:
                        if not obj.hide_get() and not obj.select_get():
                            obj.hide_set(True)
                    else:
                        if not obj.hide_get() and obj.select_get():
                            obj.hide_set(True)
                            obj.select_set(False)
                #unhide
                else:
                    #unhide and select
                    if self.select:
                        
                        if obj.hide_get():
                            obj.hide_set(False)
                            obj.select_set(True)
                        for obj in selected:
                            obj.select_set(False)
                    else:
                        if obj.hide_get():
                            obj.hide_set(False)
                            obj.select_set(False)
        elif bpy.context.mode == 'EDIT_MESH':
            for obj in bpy.context.selected_objects:
                obj.update_from_editmode()
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                selected = []
                for comp in self.getComps(bm):
                    if comp.select and not comp.hide:
                        selected.append(comp)
                for comp in self.getComps(bm):
                    #hide
                    if self.hide:
                        if self.nonSelected:
                            if not comp.select and not comp.hide:
                                comp.hide_set(True)
                        else:
                            if comp.select and not comp.hide:
                                comp.hide_set(True)
                                comp.select_set(False)
                    #unhide
                    else:
                        if self.select:
                            if comp.hide :
                                comp.hide_set(False)
                                comp.select_set(True)
                            for elem in selected:
                                elem.select_set(False)
                        else:
                            if not comp.select and comp.hide:
                                comp.hide_set(False)
                                comp.select_set(False)
                bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
                bm.to_mesh(obj.data)
                bpy.ops.object.mode_set(mode='EDIT', toggle=True)
                bm.free()
        return {'FINISHED'}

    def invoke(self,context,event):
        #unhide without selection
        if event.alt and not event.shift and not event.ctrl:
            self.hide = False
            self.nonSelected = False
            self.select = False
        #unhide and select
        elif event.shift and event.alt and not event.ctrl:
            self.select = True
            self.hide = False
            self.nonSelected = False
        #hide unselected
        elif event.ctrl and not event.shift and not event.alt:
            self.nonSelected = True
            self.hide = True
            self.select = False
        #hide selected
        elif not event.alt and not event.ctrl and not event.shift:
            self.hide = True
            self.select = False
            self.nonSelected = False
        return self.execute(context)

def register():
    bpy.utils.register_class(AHideUnhide)
    bpy.utils.register_class(AUnhideByName)
    bpy.utils.register_class(ObjectListProperty)
    bpy.types.Scene.objProp = bpy.props.CollectionProperty(type=ObjectListProperty)
    wm = bpy.context.window_manager
    #mesh keys
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=True,ctrl=False,shift=False,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=True,ctrl=False,shift=True,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.aunhide_name",'H',value='PRESS',any=False,alt=True,ctrl=True,shift=False,head=True)
    keys.append((km,kmi))

    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=False,ctrl=False,shift=False,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=True,ctrl=False,shift=False,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=False,ctrl=True,shift=False,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=False,ctrl=False,shift=True,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.ahide_unhide",'H',value='PRESS',any=False,alt=True,ctrl=False,shift=True,head=True)
    keys.append((km,kmi))
    kmi = km.keymap_items.new("object.aunhide_name",'H',value='PRESS',any=False,alt=True,ctrl=True,shift=False,head=True)
    keys.append((km,kmi))
    

def unregister():
    del bpy.types.Scene.objProp
    bpy.utils.unregister_class(AHideUnhide)
    bpy.utils.unregister_class(AUnhideByName)
    bpy.utils.unregister_class(ObjectListProperty)
    for km, kmi in keys:
        km.keymap_items.remove(kmi)