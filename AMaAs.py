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
    "name": "A* Material Assignment",
    "description": "Easy Material Assignment",
    "author": "A*",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "https://youtu.be/Q9_KhzhK62A",
    "category": "3D View"
}

import bpy
allMaterials = [("0","New Material","Add New Material",'NODE_MATERIAL',0)]
addon_keymaps = []

class AMaAsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    keyList = (("A", "A", "A"),("B", "B", "B"),("C", "C", "C"),
    ("D", "D", "D"),("E", "E", "E"),("F", "F", "F"),("G", "G", "G"),
    ("H", "H", "H"),("I", "I", "I"),("J", "J", "J"),("K", "K", "K"),
    ("L", "L", "L"),("M", "M", "M"),("N", "N", "N"),("O", "O", "O"),
    ("P", "P", "P"),("Q", "Q", "Q"),("R", "R", "R"),("S", "S", "S"),
    ("T", "T", "T"),("U", "U", "U"),("V", "V", "V"),("W", "W", "W"),
    ("X", "X", "X"),("Y", "Y", "Y"),("Z", "Z", "Z"))

    def updateKeys(self,context):
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
            addon_keymaps.clear()
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name = 'Mesh', space_type = 'EMPTY')
        kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],value="PRESS",any=False,alt=getProp("alt"),ctrl=getProp("ctrl"),shift=getProp("shift"),head=True)
        km = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode', space_type = 'EMPTY')
        kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],value="PRESS",any=False,alt=getProp("alt"),ctrl=getProp("ctrl"),shift=getProp("shift"),head=True)
        addon_keymaps.append((km, kmi))
        return None

    key:bpy.props.EnumProperty(items=keyList,default="M",update=updateKeys)
    alt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False,update=updateKeys)
    ctrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=True,update=updateKeys)
    shift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False,update=updateKeys)
    perMenu:bpy.props.BoolProperty(name="Persistent Menu",description="Persistent Menu",default=False)
    mWidthMenu:bpy.props.IntProperty(name="Menu Width",description="Menu Width",default=200)

    def draw(self,context):
        layout = self.layout
        propBox = layout.box()
        kRow = propBox.row(align=True)
        pRow = propBox.row(align=True)
        kRow.prop(self,"key")
        kRow.prop(self,"alt")
        kRow.prop(self,"ctrl")
        kRow.prop(self,"shift")
        pRow.prop(self,"perMenu")
        pRow.prop(self,"mWidthMenu")

def getProp(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

class AMaAs_Assign(bpy.types.Operator):
    bl_idname = "object.amaas_assign"
    bl_label = "Assign Material"
    bl_options = {'REGISTER', 'UNDO'}

    newMaterialName = ""
    newMaterialColor = (0,0,0,0)
    ExistedMaterialName = ""

    def assignNew(self):
        mat = bpy.data.materials.new(name=self.newMaterialName)
        mat.diffuse_color = (self.newMaterialColor[0],self.newMaterialColor[1],self.newMaterialColor[2],1)
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.append(mat)
                index = len(obj.material_slots)-1
                if bpy.context.mode == 'OBJECT':
                    for poly in obj.data.polygons:
                        poly.material_index = index
                if bpy.context.mode == 'EDIT_MESH':
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    for poly in obj.data.polygons:
                        print(poly.select)
                        if poly.select:
                            poly.material_index = index
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    
    def objMaterialCheck(self,obj):
        for slot in obj.material_slots:
            if slot.name ==self.ExistedMaterialName:
                return True
        return False

    def getExistedMaterial(self):
        for mat in bpy.context.blend_data.materials:
            if mat.name == self.ExistedMaterialName:
                return mat
        return None
    
    def findExistedIndex(self,obj):
        for i in range(len(obj.material_slots)):
            if obj.material_slots[i].name == self.ExistedMaterialName:
                return i
        return -1
        
    def assignExisted(self):
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                if self.objMaterialCheck(obj):
                    index = self.findExistedIndex(obj)
                    if bpy.context.mode == 'OBJECT':
                        for poly in obj.data.polygons:
                            poly.material_index = index
                    if bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
                        for poly in obj.data.polygons:
                            if poly.select:
                                poly.material_index = index
                        bpy.ops.object.mode_set(mode='EDIT', toggle=True)
                else:
                    mat = self.getExistedMaterial()
                    obj.data.materials.append(mat)
                    index = len(obj.data.materials)-1
                    if bpy.context.mode == 'OBJECT':
                        for poly in obj.data.polygons:
                            poly.material_index = index
                    if bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
                        for poly in obj.data.polygons:
                            if poly.select:
                                poly.material_index = index
                        bpy.ops.object.mode_set(mode='EDIT', toggle=True)

    def execute(self,context):
        if self.ExistedMaterialName == 'New Material':
            self.assignNew()
        else:
            self.assignExisted()
        return {'FINISHED'}

class AMaAs_Menu(bpy.types.Operator):
    bl_idname = "object.amaas_menu"
    bl_label = "A* Material Assignment"
    bl_options = {'REGISTER', 'UNDO'}

    def updateNewName(self,context):
        
        AMaAs_Assign.newMaterialName = self.mName
        return None

    def updateColor(self,context):
        AMaAs_Assign.newMaterialColor = self.matColor
        return None
    
    def updateName(self,context):
        for elem in allMaterials:
            if elem[0] == self.sceneMaterials:
                AMaAs_Assign.ExistedMaterialName = elem[1]
        return None

    def updateList(self,context):
        del allMaterials[1:]
        id = 1
        for mat in bpy.context.blend_data.materials:
            name = mat.name
            icon = bpy.types.UILayout.icon(mat)
            allMaterials.append((str(id),name,name,bpy.types.UILayout.icon(mat),id))
            id+=1
        return allMaterials

    mName: bpy.props.StringProperty(name="Name :",default = "Material",update=updateNewName)
    matColor:bpy.props.FloatVectorProperty(name="Color",description="Color", default=(0.5,0.5,0.5),subtype='COLOR',update=updateColor)
    sceneMaterials:bpy.props.EnumProperty(name="Scene Materials",items=updateList,update=updateName)
    
    def draw(self,context):
        layout = self.layout
        newMatBox = layout.box()
        mRow = newMatBox.row(align=True)
        nRow = newMatBox.row(align=True)
        cRow = newMatBox.row(align=True)
        bRow = newMatBox.row(align=True)

        mRow.prop(self,"sceneMaterials")
        nRow.prop(self,"mName")
        cRow.prop(self,"matColor")
        bRow.operator("object.amaas_assign")

        if self.sceneMaterials != '0':
            nRow.enabled = False
            cRow.enabled = False
    
    def execute(self,context):
        return {'FINISHED'}

    def invoke(self, context, event):
        self.sceneMaterials = '0'
        AMaAs_Assign.ExistedMaterialName = 'New Material'
        AMaAs_Assign.newMaterialColor = self.matColor
        AMaAs_Assign.newMaterialName = 'Material'
        if getProp("perMenu"):
            return context.window_manager.invoke_props_dialog(self, width = getProp("mWidthMenu"))
        else:
            return context.window_manager.invoke_popup(self, width = getProp("mWidthMenu"))

def register():
    bpy.utils.register_class(AMaAs_Assign)
    bpy.utils.register_class(AMaAs_Menu)
    bpy.utils.register_class(AMaAsPreferences)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name = 'Mesh', space_type = 'EMPTY')
        kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],"PRESS",any=False,alt=getProp("alt"), shift=getProp("shift"), ctrl=getProp("ctrl"), head=True)
        addon_keymaps.append((km, kmi))
        km = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode', space_type = 'EMPTY')
        kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],"PRESS",any=False,alt=getProp("alt"), shift=getProp("shift"), ctrl=getProp("ctrl"), head=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(AMaAsPreferences)
    bpy.utils.unregister_class(AMaAs_Assign)
    bpy.utils.unregister_class(AMaAs_Menu)
    