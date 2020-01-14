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

<<<<<<< HEAD

bl_info = {
    "name": "A* QoL Tools ",
    "description": "A* Quality of Life Tools",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Generic",
    "wiki_url": '',
    "category": "Genric"
=======
bl_info = {
    "name": "A* Quality Of Life Tools",
    "description": "A* Quality Of Life Tools",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Mesh",
    "wiki_url": "",
    "category": "Mesh"
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
}

import bpy
import bmesh
<<<<<<< HEAD

=======
import mathutils
addon_keymaps = []
bufferMeshName = 'DUPE'
#bufferMesh = None
class AddonPreferences(bpy.types.AddonPreferences): 
    bl_idname = __name__

    keyList = (("A", "A", "A"),("B", "B", "B"),("C", "C", "C"),
    ("D", "D", "D"),("E", "E", "E"),("F", "F", "F"),("G", "G", "G"),
    ("H", "H", "H"),("I", "I", "I"),("J", "J", "J"),("K", "K", "K"),
    ("L", "L", "L"),("M", "M", "M"),("N", "N", "N"),("O", "O", "O"),
    ("P", "P", "P"),("Q", "Q", "Q"),("R", "R", "R"),("S", "S", "S"),
    ("T", "T", "T"),("U", "U", "U"),("V", "V", "V"),("W", "W", "W"),
    ("X", "X", "X"),("Y", "Y", "Y"),("Z", "Z", "Z"))

    def updateKeysMesh(self,context):
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
            addon_keymaps.clear()
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("object.bevel_inset",getProp("bevelKey")[0],value="PRESS",any=False,alt=getProp("bevelAlt"),ctrl=getProp("bevelCtrl"),shift=getProp("bevelShift"),head=True)
        
        addon_keymaps.append((km, kmi))
        return None

    bevelToggle:bpy.props.BoolProperty(name="Toggle",description="Enable\Disable",default=True)
    bevelKey:bpy.props.EnumProperty(items=keyList,default="B",update=updateKeysMesh)
    bevelAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False,update=updateKeysMesh)
    bevelCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=False,update=updateKeysMesh)
    bevelShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False,update=updateKeysMesh)

    copyPasteDupeSelect:bpy.props.BoolProperty(name='',default="True")
    #copyPasteMeshName:bpy.props.StringProperty(name='',default='DUPE')
    
    def draw(self, context):
        layout = self.layout
        
        bevelBox = layout.box()
        bevelBox.label(text='Bevel/Inset')

        bevelToggleRow = bevelBox.row()
        
        bevelRow = bevelBox.row()
        if not getProp('bevelToggle'):
            bevelRow.enabled = False
        bevelToggleRow.prop(self,'bevelToggle')
        bevelRow.prop(self,'bevelKey',text='Key')
        bevelRow.prop(self,'bevelAlt',text='Alt')
        bevelRow.prop(self,'bevelCtrl',text='Ctrl')
        bevelRow.prop(self,'bevelShift',text='Shift')

def getProp(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

class BevelInset(bpy.types.Operator):
    bl_idname = "object.bevel_inset"
    bl_label = "Bevel Inset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        if bpy.context.mode == 'EDIT_MESH':
            #vert
            if bpy.context.scene.tool_settings.mesh_select_mode[0]:
                bpy.ops.mesh.bevel('INVOKE_DEFAULT',vertex_only=True)
            #edge
            if bpy.context.scene.tool_settings.mesh_select_mode[1]:
                bpy.ops.mesh.bevel('INVOKE_DEFAULT')
            #face
            if bpy.context.scene.tool_settings.mesh_select_mode[2]:
                bpy.ops.mesh.inset('INVOKE_DEFAULT')
        return {'FINISHED'}
    def invoke(self,context,event):
        return self.execute(context)

def getBufferMesh():
    for mesh in bpy.data.meshes:
        if mesh.name == bufferMeshName:
            return mesh
    return None

class CopyPasteDupe(bpy.types.Operator):
    bl_idname = "object.cp_dupe"
    bl_label = "Copy Paste Dupe"
    bl_options = {'REGISTER', 'UNDO'}

    meshName = 'DUPE'
    bCreated = False
    dupeMesh = None
    bufferMesh = None

    def execute(self,context):
        bmr = bmesh.new()
        for obj in bpy.context.selected_objects:
            bm = bmesh.new()
            depsgraph = context.evaluated_depsgraph_get()
            bm.from_object(obj,depsgraph,deform=True)
            delete = []
            for vert in bm.verts:
                if not vert.select:
                    delete.append(vert)
            bmesh.ops.delete(bm,geom=delete,context='VERTS')
            mesh = bpy.data.meshes.new('copy')
            bm.to_mesh(mesh)
            bmr.from_mesh(mesh)
            bpy.data.meshes.remove(mesh,do_unlink=True)
            bm.free()
        bmr.to_mesh(self.bufferMesh)
        bmr.free()
        bm.free()
        print(self.bufferMesh)
        return {'FINISHED'}

    def invoke(self,context,event):
        self.bufferMesh = getBufferMesh()
        if self.bufferMesh == None :
            self.bufferMesh =  bpy.data.meshes.new(bufferMeshName)
        return self.execute(context)

class CopyPasteDPlace(bpy.types.Operator):
    bl_idname = "object.cp_dplace"
    bl_label = "Copy Paste Dupe Place"
    bl_options = {'REGISTER', 'UNDO'}
    
    bufferMesh = None

    def execute(self,context):
        aObj = bpy.context.active_object
        bm  = bmesh.new()
        depsgraph = context.evaluated_depsgraph_get()
        bm.from_mesh(self.bufferMesh)
        offset = mathutils.Vector(aObj.location)
        toPaste = bpy.data.objects.new('Paste',self.bufferMesh)
        bpy.context.collection.objects.link(toPaste)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bm.to_mesh(toPaste.data)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bm.free()
        return {'FINISHED'}
    def invoke(self,context,event):
        self.bufferMesh = getBufferMesh()
        if self.bufferMesh != None:
            return self.execute(context)
        self.report({'INFO'}, 'No copied data in the buffer')
        return {'CANCELLED'}



def register():
    bpy.utils.register_class(AddonPreferences)
    bpy.utils.register_class(BevelInset)
    bpy.utils.register_class(CopyPasteDupe)
    bpy.utils.register_class(CopyPasteDPlace)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("object.bevel_inset",getProp("bevelKey")[0],value="PRESS",any=False,alt=getProp("bevelAlt"),ctrl=getProp("bevelCtrl"),shift=getProp("bevelShift"),head=True)
    kmi = km.keymap_items.new("object.cp_dupe",'C',value="PRESS",any=False,ctrl=True,head=True)
    kmi = km.keymap_items.new("object.cp_dplace",'V',value="PRESS",any=False,ctrl=True,head=True)
    
    addon_keymaps.append((km, kmi))
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(AddonPreferences)
    bpy.utils.unregister_class(BevelInset)
    bpy.utils.unregister_class(CopyPasteDupe)
    bpy.utils.unregister_class(CopyPasteDPlace)
>>>>>>> babe84b22df7556f667ccb50b9819efd3781d14d
