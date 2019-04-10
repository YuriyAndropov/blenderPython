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
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "3D View"
}

import bpy
allMaterials = []
listItems = [("0","New Material","Add New Material",'NODE_MATERIAL',0)]
matName = "Material"
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
        kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],value="PRESS",any=False,alt=getProp("alt"),ctrl=getProp("ctrl"),shift=getProp("shift"),head=True)
        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
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

def getMaterials():
    del allMaterials[:]
    for o in  bpy.context.scene.objects:
        if o.type == "MESH":
            obMaterials = o.data.materials
            for m in obMaterials:
                if m not in allMaterials:
                    allMaterials.append(m)

def updateList(self,context):
    del listItems[1:]
    id = 1
    for m in allMaterials:
        if m != None:
            pId = str(id)
            name = m.name
            des = m.name
            icon = bpy.types.UILayout.icon(m)
            if (str(id),name,des,icon,id) not in listItems:
                listItems.append((name,name,des,icon,id))
        id+=1
    return listItems

def assignNew(self,context):
    mat = bpy.data.materials.new(name=bpy.types.Scene.AMaAs_matName)
    mat.diffuse_color = (bpy.types.Scene.AMaAs_matColor[0],bpy.types.Scene.AMaAs_matColor[1],bpy.types.Scene.AMaAs_matColor[2],1)
    getMaterials()
    updateList(self,context)
    for o in bpy.context.selected_objects:
        if o.type == "MESH":
            data = o.data
            data.materials.append(mat)
            if bpy.context.mode == "OBJECT":
                for poly in data.polygons:
                    poly.material_index = len(data.materials)-1
            else:
                o.active_material_index = len(data.materials)-1
                o.update_from_editmode()
                bpy.ops.object.material_slot_assign()

def assignExisted(context):
    eMat = None
    for material in allMaterials:
        if material != None:
            if material.name == bpy.types.Scene.AMaAs_matID:
                eMat = material
    for o in bpy.context.selected_objects:
        if o.type == "MESH":
            index = None
            data = o.data
        for m in range(len(data.materials)):
            if data.materials[m]!=None:
                if data.materials[m].name == bpy.types.Scene.AMaAs_matID:
                    index = m
        if index == None :
            data.materials.append(eMat)
            index = len(data.materials)-1
        if bpy.context.mode == "OBJECT":
            for poly in data.polygons:
                poly.material_index = index
        else:
            o.active_material_index = index
            o.update_from_editmode()
            bpy.ops.object.material_slot_assign()

class AMaAs_assignButton(bpy.types.Operator):
    bl_idname = "object.amaas_button"
    bl_label = "Assign Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        if bpy.types.Scene.AMaAs_matID == "0" :
            assignNew(self,context)
            getMaterials()
            updateList(self,context)
        else:
            assignExisted(context)
        return {'FINISHED'}

class AMaAs_Menu(bpy.types.Operator):
    bl_idname = "object.amaas_menu"
    bl_label = "AMaAs PopUp Menu"
    bl_options = {'REGISTER', 'UNDO'}

    def updateName(self,context):
        matName = self.mName
        bpy.types.Scene.AMaAs_matName = self.mName
        return None

    def updateColor(self,context):
        bpy.types.Scene.AMaAs_matColor = self.matColor
        return None

    def updateID(self,context):
        bpy.types.Scene.AMaAs_matID = self.sceneMaterials
        return None

    mName: bpy.props.StringProperty(name="Name :",default = "Material",update=updateName)
    matColor:bpy.props.FloatVectorProperty(name="Color",description="Color", default=(0.5,0.5,0.5),subtype='COLOR',update=updateColor)
    sceneMaterials:bpy.props.EnumProperty(name="Scene Materials",items=updateList,update=updateID)
    sceneMaterials = "0"
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
        bRow.operator("object.amaas_button")

    def execute(self,context):
        return {'FINISHED'}

    def invoke(self, context, event):
        getMaterials()
        bpy.types.Scene.AMaAs_matName = "Material"
        bpy.types.Scene.AMaAs_matColor = (0.5,0.5,0.5)
        bpy.types.Scene.AMaAs_matID = "0"
        matName = self.mName
        updateList(self,context)
        if getProp("perMenu"):
            return context.window_manager.invoke_props_dialog(self, width = getProp("mWidthMenu"))
        else:
            return context.window_manager.invoke_popup(self, width = getProp("mWidthMenu"))

def register():
    bpy.utils.register_class(AMaAs_assignButton)
    bpy.utils.register_class(AMaAs_Menu)
    bpy.utils.register_class(AMaAsPreferences)
    bpy.types.Scene.AMaAs_matName = bpy.props.StringProperty(default="Material")
    bpy.types.Scene.AMaAs_matColor = bpy.props.FloatVectorProperty(default=(0.5,0.5,0.5),subtype='COLOR')
    bpy.types.Scene.AMaAs_matID = bpy.props.StringProperty(default="0")
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
        kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],"PRESS",any=False,alt=getProp("alt"), shift=getProp("shift"), ctrl=getProp("ctrl"), head=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(AMaAsPreferences)
    bpy.utils.unregister_class(AMaAs_assignButton)
    bpy.utils.unregister_class(AMaAs_Menu)
    del bpy.types.Scene.AMaAs_matName
    del bpy.types.Scene.AMaAs_matColor
    del bpy.types.Scene.AMaAs_matID

if __name__ == "__main__":
    register()
