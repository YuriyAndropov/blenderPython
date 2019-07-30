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
    "name": "A* Profiler",
    "description": "Fast Profile Along Path ",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Mesh",
    "wiki_url": "",
    "category": "Mesh"
}

import bpy
import bmesh
import mathutils
import math
import blf

#profile selection enum list
listItems = []
addon_keymaps = []
font_id = 0
TooltipText = {
    "font_id": 0,
    "handler": None,
}
class AQPipePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    keyList = (('NONE','None','NONE'),("A", "A", "A"),("B", "B", "B"),("C", "C", "C"),
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
        if getProp('profKey')[0] != 'NONE':
            kmi = km.keymap_items.new("object.amaas_menu",getProp("profKey")[0],value="PRESS",any=False,alt=getProp("profAlt"),ctrl=getProp("profCtrl"),shift=getProp("profShift"),head=True)
            km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
            addon_keymaps.append((km, kmi))
        if getProp('pathKey')[0] != 'NONE':
            kmi = km.keymap_items.new("object.amaas_menu",getProp("pathKey")[0],value="PRESS",any=False,alt=getProp("pathAlt"),ctrl=getProp("pathCtrl"),shift=getProp("pathShift"),head=True)
            km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
            addon_keymaps.append((km, kmi))
        if getProp('sweepKey')[0] != 'NONE':
            kmi = km.keymap_items.new("object.amaas_menu",getProp("sweepKey")[0],value="PRESS",any=False,alt=getProp("sweepAlt"),ctrl=getProp("sweepCtrl"),shift=getProp("sweepShift"),head=True)
            km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
            addon_keymaps.append((km, kmi))
        if getProp('aOptKey')[0] != 'NONE':
            kmi = km.keymap_items.new("object.amaas_menu",getProp("aOptKey")[0],value="PRESS",any=False,alt=getProp("aOptAlt"),ctrl=getProp("aOptCtrl"),shift=getProp("aOptShift"),head=True)
            km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
            addon_keymaps.append((km, kmi))
        #kmi = km.keymap_items.new("object.amaas_menu",getProp("key")[0],value="PRESS",any=False,alt=getProp("alt"),ctrl=getProp("ctrl"),shift=getProp("shift"),head=True)
        #km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
        #addon_keymaps.append((km, kmi))
        return None

    profKey:bpy.props.EnumProperty(name="Make Profile",items=keyList,default="NONE",update=updateKeys)
    profAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False,update=updateKeys)
    profCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=False,update=updateKeys)
    profShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False,update=updateKeys)

    pathKey:bpy.props.EnumProperty(name="Make Path",items=keyList,default="NONE",update=updateKeys)
    pathAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False,update=updateKeys)
    pathCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=False,update=updateKeys)
    pathShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False,update=updateKeys)

    sweepKey:bpy.props.EnumProperty(name='Sweep Profile',items=keyList,default="NONE",update=updateKeys)
    sweepAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False,update=updateKeys)
    sweepCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=False,update=updateKeys)
    sweepShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False,update=updateKeys)

    aOptKey:bpy.props.EnumProperty(name='Additional Options',items=keyList,default="NONE",update=updateKeys)
    aOptAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False,update=updateKeys)
    aOptCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=False,update=updateKeys)
    aOptShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False,update=updateKeys)

    mMove:bpy.props.EnumProperty(name='Move',items=keyList,default="M")
    mRotate:bpy.props.EnumProperty(name='Rotate',items=keyList,default="R")
    mScale:bpy.props.EnumProperty(name='Scale',items=keyList,default="S")

    mX:bpy.props.EnumProperty(name='X',items=keyList,default="X")
    mY:bpy.props.EnumProperty(name='Y',items=keyList,default="Y")
    mZ:bpy.props.EnumProperty(name='Z',items=keyList,default="Z")

    mCap:bpy.props.EnumProperty(name='Cap',items=keyList,default="C")
    mKeep:bpy.props.EnumProperty(name='KeepSpline',items=keyList,default="Q")


    cursorColor:bpy.props.FloatVectorProperty(name="Main Color",description="Color", default=(1.0,1.0,1.0),subtype='COLOR')
    highlightColor:bpy.props.FloatVectorProperty(name="Highlight Color",description="Color", default=(0.0,1.0,0.0),subtype='COLOR')
    bTips:bpy.props.BoolProperty(name='Show KeyTips',default=True)
    bDefCap:bpy.props.BoolProperty(name='Fill Caps',default=True)
    bDefKeep:bpy.props.BoolProperty(name='Keep as Spline',default=False)

    def draw(self,context):
        layout = self.layout
        optBox = layout.box()
        optBox.label(text='Addon Default Settings')
        modalBox = layout.box()
        modalBox.label(text="Modal Hotkeys")
        mainBox = layout.box()
        mainBox.label(text='Optional Hotkeys. They are not set. Addon was designed with menus in mind')
        profBox = mainBox.box()
        profBox.label(text="Make Profile Hotkey")
        profRow = profBox.row(align=True)
        profRow.prop(self,"profKey")
        profRow.prop(self,"profAlt")
        profRow.prop(self,"profCtrl")
        profRow.prop(self,"profShift")

        pathBox = mainBox.box()
        pathBox.label(text="Make Path Hotkey")
        pathRow = pathBox.row(align=True)
        pathRow.prop(self,"pathKey")
        pathRow.prop(self,"pathAlt")
        pathRow.prop(self,"pathCtrl")
        pathRow.prop(self,"pathShift")

        sweepBox = mainBox.box()
        sweepBox.label(text="Sweep Profile Hotkey")
        sweepRow = sweepBox.row(align=True)
        sweepRow.prop(self,"sweepKey")
        sweepRow.prop(self,"sweepAlt")
        sweepRow.prop(self,"sweepCtrl")
        sweepRow.prop(self,"sweepShift")

        toolBox = modalBox.box()
        toolBox.label(text='Tool hotkeys in modal')
        toolRow = toolBox.row(align=True)
        toolRow.prop(self,'mMove')
        toolRow.prop(self,'mRotate')
        toolRow.prop(self,'mScale')
        addRow = toolBox.row(align=True)
        addRow.prop(self,'mCap')
        addRow.prop(self,'mKeep')
        

        axisBox = modalBox.box()
        axisBox.label(text='Axis hotkeys in modal')
        axisRow = axisBox.row(align=True)
        axisRow.prop(self,'mX')
        axisRow.prop(self,'mY')
        axisRow.prop(self,'mZ')

        sRow = optBox.row()
        sRow.prop(self,'bTips')
        sRow.prop(self,'bDefCap')
        sRow.prop(self,'bDefKeep')
        cRow = optBox.row()
        cRow.prop(self,'cursorColor')
        cRow.prop(self,'highlightColor')

#get addon preferences option by name
def getProp(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

#get collection by name
def getCollection(name):
    for collection in bpy.data.collections:
        if collection.name == name:
            return collection
    return None

#get object in collection by name
def getObjectInCollection(name):
    if checkCollections("QPipe"):
        for obj in getCollection("QPipe").objects:
            if obj.type != None and obj.name == name:
                return obj
    return None

#check if there is already a collection with specified name
def checkCollections(value):
    for collection in bpy.data.collections:
        if collection != None:
            if collection.name == value:
                return True
    return False
#check if there is already an object in collection with specified name
def checkForObject(value):
    for obj in getCollection("QPipe").objects:
        if obj.name == value:
            return True
    return False

#update profile selection enum
def updateList(self,context):
    del listItems[:]
    id = 0
    for profile in getObjectInCollection("Profiles").children:
        pId = str(id)
        name = profile.name
        des = profile.name
        icon = 'OUTLINER_DATA_CURVE'
        if (str(id),name,des,icon,id) not in listItems:
            listItems.append((name,name,des,icon,id))
        id+=1
    return listItems

#checking and creating proper structure for new objects
def createCollectionAndParents():
    if checkCollections("QPipe") == False:
        newCol = bpy.data.collections.new("QPipe")
        bpy.context.scene.collection.children.link(newCol)
        profObject = bpy.data.objects.new("Profiles",None)
        newCol.objects.link(profObject)
        pathObject = bpy.data.objects.new("Paths",None)
        newCol.objects.link(pathObject)
        tempObject = bpy.data.objects.new("Temp",None)
        newCol.objects.link(tempObject)
    else:
        collection = getCollection("QPipe")
        if checkForObject("Profiles") == False:
            profObject = bpy.data.objects.new("Profiles",None)
            collection.objects.link(profObject)
        if checkForObject("Paths") == False:
            pathObject = bpy.data.objects.new("Paths",None)
            collection.objects.link(pathObject)
        if checkForObject("Temp") == False:
            tempObject = bpy.data.objects.new("Temp",None)
            collection.objects.link(tempObject)

#get new object from edge selection and add it to collection
def objectFromPath(profileName,typeName):
    objects = bpy.context.selected_objects
    createCollectionAndParents()
    col = getCollection('QPipe')
    profObj = getObjectInCollection(typeName)

    for obj in objects:
        if obj.type == "MESH":
            data = obj.data
            bm = bmesh.from_edit_mesh(data)
            nonSelected = []
            dupe = bm.copy()
            for edge in dupe.edges:
                if edge.select == False:
                    nonSelected.append(edge)
            bmesh.ops.delete(dupe,geom=nonSelected,context='EDGES')
            newMesh = bpy.data.meshes.new("QPipeMesh")
            dupe.to_mesh(newMesh)
            newObj = bpy.data.objects.new(profileName, newMesh)
            col.objects.link(newObj)
            newObj.location = obj.location
            newObj.parent = profObj
            bmesh.types.BMesh.free
        
def convertToCurve(typeName):
    profiles = getObjectInCollection(typeName)
    for path in profiles.children:
        if path.type == "MESH":
            path.select_set(True) 
            bpy.context.view_layer.objects.active = path
            bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
        if path.type == "CURVE":
            path.parent = getObjectInCollection(typeName)

#make profile from selection operator
class AQPipe_MakeProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_makeprofile"
    bl_label = "AQPipe Make Profile"
    bl_options = {'REGISTER'}

    pName: bpy.props.StringProperty(name="Name :",default = "Profile")

    def dropSelection(self):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
    
    def getCreated(self):
        for path in getObjectInCollection('Profiles').children:
            if path.name == self.pName:
                return path
        return None
    
    def checkState(self):
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH" and obj.type != "CURVE":
                self.report({'INFO'}, 'Object should be a MESH or CURVE type')
                return False
            if bpy.context.mode == 'OBJECT' and obj.type == "MESH":
                self.report({'INFO'}, 'MESH should be in Edit Mode to select path')
                return False
        return True

    def draw(self,context):
        layout = self.layout
        nRow = layout.row(align=True)

        nRow.prop(self,"pName")

    def execute(self,context):
        if self.checkState()==True:
            objectFromPath(self.pName,"Profiles")
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            self.dropSelection()
            self.getCreated().select_set(True)
        return {'FINISHED'}
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=20)

#make path from selection operator
class AQPipe_MakePath(bpy.types.Operator):
    bl_idname = "object.aqpipe_makepath"
    bl_label = "AQPipe Make Path"
    bl_options = {'REGISTER'}

    pName: bpy.props.StringProperty(name="Name :",default = "Path")

    def dropSelection(self):
        for obj in bpy.context.selected_objects:
            obj.select_set(False)

    def getCreated(self):
        for path in getObjectInCollection('Paths').children:
            if path.name == self.pName:
                return path
        return None

    def checkState(self):
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH" and obj.type != "CURVE":
                self.report({'INFO'}, 'Object should be a MESH or CURVE type')
                return False
            if bpy.context.mode == 'OBJECT' and obj.type == "MESH":
                self.report({'INFO'}, 'MESH should be in Edit Mode to select path')
                return False
        return True

    def draw(self,context):
        layout = self.layout
        nRow = layout.row(align=True)

        nRow.prop(self,"pName")

    def execute(self,context):
        if self.checkState():
            objectFromPath(self.pName,"Paths")
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            self.dropSelection()
            self.getCreated().select_set(True)
        return {'FINISHED'}

    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=20)

#profile selection operator
class AQPipe_SweepProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_sweepprofile"
    bl_label = "AQPipe Sweep Profile"
    bl_options = {'REGISTER', 'UNDO'}

    def profileUpdate(self,context):
        bpy.types.Scene.AQPipe_bevelProfile = self.sceneProfiles
        return None

    sceneProfiles: bpy.props.EnumProperty(name="Scene Profiles",items=updateList,update=profileUpdate)
    
    def checkSelectionMode(self):
        if bpy.context.mode == 'OBJECT':
            return False
        if bpy.context.mode == 'EDIT_MESH':
            if bpy.context.scene.statistics(bpy.context.view_layer).split("|")[2].split(':')[1].split('/')[0] == '0':
                return False
        return True

    def draw(self,context):
        layout = self.layout
        enumRow = layout.row(align=True)
        enumRow.prop(self,"sceneProfiles")
    
    def execute(self,context):
        if bpy.context.mode == 'EDIT_MESH':
            if bpy.context.scene.statistics(bpy.context.view_layer).split("|")[2].split(':')[1].split('/')[0] != '0':
                objectFromPath('QPath','Paths')
        bpy.ops.object.aqpipe_postedit('INVOKE_DEFAULT')
        return {'INTERFACE'}

    def invoke(self,context,event):
        
        if bpy.context.mode =='OBEJCT' and self.checkSelectionMode():
            objectFromPath('Path','Paths')
        if not checkCollections('QPipe'):
            self.report({'WARNING'},'No profiles and paths data in the scene')
            return {'CANCELED'}
        if len(getObjectInCollection('Profiles').children) == 0:
            self.report({'WARNING'}, 'No available profiles in the scene')
            return {'CANCELLED'}
        if len(getObjectInCollection('Paths').children) == 0 and not self.checkSelectionMode():
            self.report({'WARNING'}, 'No available path in the scene')
            return {'CANCELLED'}
        bpy.types.Scene.AQPipe_bevelProfile = self.sceneProfiles
        return context.window_manager.invoke_props_dialog(self, width=300, height=40)

#additional options 
class AQPipe_CleanUp(bpy.types.Operator):
    bl_idname = "object.aqpipe_cleanup"
    bl_label = "AQPipe Clean Stuff"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        for object in getCollection("QPipe").objects:
            bpy.data.objects.remove(object,do_unlink=True,do_id_user=True,do_ui_user=True)
        bpy.data.collections.remove(getCollection('QPipe'))
        return {'FINISHED'}

class AQPipe_FlushPaths(bpy.types.Operator):
    bl_idname = "object.aqpipe_flushpaths"
    bl_label = "AQPipe Flush Paths"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        for path in getObjectInCollection('Paths').children:
            bpy.data.objects.remove(path,do_unlink=True,do_id_user=True,do_ui_user=True)
        return {'FINISHED'}

class AQPipe_FlushProfiles(bpy.types.Operator):
    bl_idname = "object.aqpipe_flushprofiles"
    bl_label = "AQPipe Flush Profiles"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        for profile in getObjectInCollection('Profiles').children:
            bpy.data.objects.remove(profile,do_unlink=True,do_id_user=True,do_ui_user=True)
        return {'FINISHED'}

class AQPipe_AdditionalOptions(bpy.types.Operator):
    bl_idname = "object.aqpipe_addoptions"
    bl_label = "AQPipe Additional Options"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self,context):
        layout = self.layout
        optionBox = layout.box()
        fPath = optionBox.row()
        fProf = optionBox.row()
        cleanUp = optionBox.row()
        fPath.operator("object.aqpipe_flushpaths")
        fProf.operator("object.aqpipe_flushprofiles")
        cleanUp.operator("object.aqpipe_cleanup")
    def execute(self,context):
        return {'FINISHED'}

    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=20)

class AQPipe_PostEdit(bpy.types.Operator):
    bl_idname = "object.aqpipe_postedit"
    bl_label = "AQPipe Post Edit Menu"
    bl_options = {'REGISTER', 'UNDO'}
    #switches
    bKeepSpline: bpy.props.BoolProperty(default=False)
    bCap: bpy.props.BoolProperty(default=False)
    bScale: bpy.props.BoolProperty(name='Scale',default=False)
    bMove:  bpy.props.BoolProperty(name='Move',default=False)
    bRotate:bpy.props.BoolProperty(name='Rotate',default=False)
    bXAxis: bpy.props.BoolProperty(name='X',default=False)
    bYAxis: bpy.props.BoolProperty(name='Y',default=False)
    bZAxis: bpy.props.BoolProperty(name='Z',default=False)
    #base transform
    baseScale: bpy.props.FloatVectorProperty(default=(0,0,0))
    baseLoc: bpy.props.FloatVectorProperty(default=(0.0,0.0,0.0,0.0),subtype='TRANSLATION',size=4)
    baseRotation: bpy.props.FloatVectorProperty(default=(0,0,0))

    def remap(self,value, low1, high1, low2, high2):
        return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

    def addDraw(self,x,y,size,text,color):
        blf.position(font_id, x, y, 0)
        blf.size(font_id, size, 72)
        blf.color(font_id, color[0], color[1], color[2], 1)
        blf.draw(font_id, text)

    def drawTooltips(self,context,event):
        tWidth = context.area.regions[2].width
        nWidth = bpy.context.area.regions[3].width
        width = context.area.width
        height = context.area.height
        color = getProp('cursorColor')
        size = 25
        text = 'Sweep Profile Mode'
        self.addDraw((width-tWidth-nWidth)/2 - len(text)/2,height-50,size,text,color)
        if getProp('bTips'):
            text = 'Hotkeys :'
            self.addDraw(tWidth,height/2+63*2,size,text,color)
            size = 21
            text = getProp('mMove') +  ' : Move'
            self.addDraw(tWidth+size,height/2+42*1.5,size,text,color)
            text = getProp('mRotate') +  ' : Rotate'
            self.addDraw(tWidth+size,height/2+21*1.5,size,text,color)
            text = getProp('mScale') + ' : Scale'
            self.addDraw(tWidth+size,height/2,size,text,color)
        
            text = getProp('mX') + ' : X Axis'
            self.addDraw(tWidth+size,height/2 - 21 *1.5-20,size,text,color)
            text = getProp('mY') + ' : Y Axis'
            self.addDraw(tWidth+size,height/2 -42 *1.5 -20,size,text,color)
            text = getProp('mZ') + ' : Z Axis'
            self.addDraw(tWidth+size,height/2 -63 *1.5 -20,size,text,color)
            text = getProp('mCap') + ' : Cap Ends Toggle'
            self.addDraw(tWidth+size,height/2 -84 *1.5 -20,size,text,color)
            text =  getProp('mKeep') +  ' : Leave as Curve Toggle'
            self.addDraw(tWidth+size,height/2 -105 *1.5 -20,size,text,color)

        if self.bMove:
            text = 'Move : ' + 'X : ' + str(round(self.baseLoc[0],2)) + ',' + 'Y : ' + str(round(self.baseLoc[1],2)) + ',' + 'Z : ' + str(round(self.baseLoc[2],2))
        elif self.bScale:
            text = "Scale : " + 'X : ' + str(round(self.getProfile().scale[0],2)) + ',' + 'Y : '+ str(round(self.getProfile().scale[1],2)) + ',' + 'Z' + str(round(self.getProfile().scale[2],2))     
        elif self.bRotate:
            text = 'Rotate : ' + 'X : ' + str(round(math.degrees(self.baseRotation[0]),0)) + ',' + 'Y : ' + str(round(math.degrees(self.baseRotation[1]),0)) + ',' + 'Z : ' + str(round(math.degrees(self.baseRotation[2]),0))
        else:
            text = "No Operator"
        size = 15
        self.addDraw(event.mouse_x,event.mouse_y-150,size,text,color)
        if self.bKeepSpline:
            text = 'Result as Spline'
        else:
            text = 'Result as Mesh'

        self.addDraw(event.mouse_x,event.mouse_y-150-30,size,text,color)
        if self.bCap:
            text = 'Cap On'
        else:
            text = 'Cap Off'
        self.addDraw(event.mouse_x,event.mouse_y-150-60,size,text,color)
    
    def dropSelection(self):
        for obj in bpy.context.selected_objects:
            obj.select_set(False)

    def getPath(self):
        paths = []
        for path in getObjectInCollection("Paths").children:
            paths.append(path)
        return paths
    
    def getProfile(self):
        for profile in getObjectInCollection("Profiles").children:
            if profile.name == bpy.types.Scene.AQPipe_bevelProfile:
                return profile
        return None
        
    def processEvents(self,event):
        #setting tools
        if event.type == getProp('mKeep') and event.value == "PRESS" and self.bKeepSpline :
            self.bKeepSpline = False
        elif event.type == getProp('mKeep') and event.value == "PRESS" and not self.bKeepSpline :
            self.bKeepSpline = True
        if event.type == getProp('mScale') and event.value == "PRESS":
            self.report({'INFO'}, 'Scale Active')
            if self.bScale == False:
                self.getProfile().select_set(True) 
                bpy.context.view_layer.objects.active = self.getProfile()
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                self.bScale = True
                self.bMove = False
                self.bRotate = False
                self.bXAxis = False
                self.bYAxis = False
                self.bZAxis = False
            else:
                self.bScale = False
                self.bXAxis = False
                self.bYAxis = False
                self.bZAxis = False
        if event.type == getProp('mMove') and event.value == "PRESS":
            if self.bMove == False:
                self.report({'INFO'}, 'Move Active')
                #setting x-axis as default when move is active, since drag add to location is awkward with 3 axes
                self.getProfile().select_set(True) 
                bpy.context.view_layer.objects.active = self.getProfile()
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                self.bXAxis = True
                self.bMove = True
                self.bScale = False
                self.bRotate = False
                self.bYAxis = False
                self.bZAxis = False
            else:
                self.bMove = False
                self.bXAxis = False
                self.bYAxis = False
                self.bZAxis = False
        if event.type == getProp('mRotate') and event.value == "PRESS":
            self.report({'INFO'}, 'Rotate Active')
            if self.bRotate == False:
                #setting x-axis as default when move is active, since drag rotate is awkward with 3 axes
                self.bXAxis = True
                self.bRotate = True
                self.bMove = False
                self.bScale = False
                self.bYAxis = False
                self.bZAxis = False
            else:
                self.bRotate = False
                self.bXAxis = False
                self.bYAxis = False
                self.bZAxis = False
        #setting axes
        if event.type == getProp('mX') and event.value == "PRESS" and self.bXAxis==False:
            self.report({'INFO'}, 'X Axis')
            self.bXAxis = True
            self.bYAxis = False
            self.bZAxis = False
        elif event.type == getProp('mX') and event.value == "PRESS" and self.bXAxis==True:
            self.bXAxis = False
        
        if event.type == getProp('mY') and event.value == "PRESS" and self.bYAxis==False:
            self.report({'INFO'}, 'Y Axis')
            self.bYAxis = True
            self.bXAxis = False
            self.bZAxis = False
        elif event.type == getProp('mY') and event.value == "PRESS" and self.bYAxis==True:
            self.bYAxis = False

        if event.type == getProp('mZ') and event.value == "PRESS" and self.bZAxis==False:
            self.report({'INFO'}, 'Z Axis')
            self.bZAxis = True
            self.bYAxis = False
            self.bXAxis = False
        elif event.type == getProp('mZ') and event.value == "PRESS" and self.bZAxis==True:
            self.bZAxis = False
        #adding transform
        if (event.type == "WHEELUPMOUSE" or event.type == "WHEELDOWNMOUSE" or 'RIGHTMOUSE') and self.bRotate:
            self.addRotation(event.type)
        if (event.type == "WHEELUPMOUSE" or event.type == "WHEELDOWNMOUSE" or 'RIGHTMOUSE' ) and self.bMove:
            self.addLocation(event.type)
        if (event.type == "WHEELUPMOUSE" or event.type == "WHEELDOWNMOUSE" or 'RIGHTMOUSE' ) and self.bScale:
            self.addScale(event.type)
        if event.type == getProp('mCap') and event.value == 'PRESS' and self.bCap==False:
            self.bCap=True
            self.setCap()
        elif event.type == getProp('mCap') and event.value == 'PRESS' and self.bCap==True:
            self.bCap=False
            self.setCap()
            
    def addScale(self,event):
        if self.bScale:
            if event == "WHEELUPMOUSE":
                if not self.bXAxis and not self.bYAxis and not self.bZAxis:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') + mathutils.Vector((0.1 , 0.1, 0.1 ))
                else:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') + mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis))) 
            if event == "WHEELDOWNMOUSE":
                if not self.bXAxis and not self.bYAxis and not self.bZAxis:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') - mathutils.Vector((0.1 , 0.1, 0.1))
                else:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') - mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis)))
            #scale exit with reverting scale
            if event == 'RIGHTMOUSE':
                self.report({'INFO'}, 'Exit and Revert Scale')
                self.getProfile().scale = self.baseScale 
            if event == 'ESC':
                self.report({'INFO'}, 'Exit and Revert Scale')
                self.getProfile().scale = self.baseScale 
                self.bScale = False

    def addRotation(self,event):
        if self.bRotate:
            if event == "WHEELUPMOUSE":
                self.getProfile().rotation_euler[0] = self.getProfile().rotation_euler.x + math.radians(10)*int(self.bXAxis)
                self.getProfile().rotation_euler[1] = self.getProfile().rotation_euler.y + math.radians(10)*int(self.bYAxis)
                self.getProfile().rotation_euler[2] = self.getProfile().rotation_euler.z + math.radians(10)*int(self.bZAxis)
                self.baseRotation[0] += math.radians(10)*int(self.bXAxis)
                self.baseRotation[1] += math.radians(10)*int(self.bYAxis)
                self.baseRotation[2] += math.radians(10)*int(self.bZAxis)
            if event == "WHEELDOWNMOUSE":
                self.getProfile().rotation_euler[0] = self.getProfile().rotation_euler.x + math.radians(-10)*int(self.bXAxis)
                self.getProfile().rotation_euler[1] = self.getProfile().rotation_euler.y + math.radians(-10)*int(self.bYAxis)
                self.getProfile().rotation_euler[2] = self.getProfile().rotation_euler.z + math.radians(-10)*int(self.bZAxis)
                self.baseRotation[0] += math.radians(-10)*int(self.bXAxis)
                self.baseRotation[1] += math.radians(-10)*int(self.bYAxis)
                self.baseRotation[2] += math.radians(-10)*int(self.bZAxis)
            self.getProfile().select_set(True) 
            bpy.context.view_layer.objects.active = self.getProfile()
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            if event == 'RIGHTMOUSE':
                self.getProfile().rotation_euler[0] -= self.baseRotation[0] 
                self.getProfile().rotation_euler[1] -= self.baseRotation[1] 
                self.getProfile().rotation_euler[2] -= self.baseRotation[2]
                self.baseRotation = (0,0,0) 
                self.report({'INFO'}, 'Revert Rotation')
            if event == 'ESC':
                self.getProfile().rotation_euler[0] -= self.baseRotation[0] 
                self.getProfile().rotation_euler[1] -= self.baseRotation[1] 
                self.getProfile().rotation_euler[2] -= self.baseRotation[2]
                self.baseRotation = (0,0,0) 
                self.report({'INFO'}, 'Exit and Revert Rotation')
                self.bRotate = False

    def addLocation(self,event):
        shift = mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis),0))
        if event == "WHEELUPMOUSE" :
            self.baseLoc += shift
            for spline in self.getProfile().data.splines:
                for point in spline.points:
                    point.co += shift
        if event == "WHEELDOWNMOUSE":
            self.baseLoc -= shift
            for spline in self.getProfile().data.splines:
                for point in spline.points:
                    point.co -= shift
        if event == 'RIGHTMOUSE':
            for spline in self.getProfile().data.splines:
                for point in spline.points:
                    point.co -= self.baseLoc
            self.baseLoc = mathutils.Vector((0.0,0.0,0.0,0.0))
            self.report({'INFO'}, 'Revert Movement')
        if event == 'ESC' :
            for spline in self.getProfile().data.splines:
                for point in spline.points:
                    point.co -= self.baseLoc
            self.baseLoc = mathutils.Vector((0.0,0.0,0.0,0.0))
            self.report({'INFO'}, 'Exit and Revert Movement')
            self.bMove = False

    def setCap(self):
        if self.bCap == True:
            for path in self.getPath():
                path.data.use_fill_caps = True
            self.report({'INFO'},'Fill Caps On')
        if self.bCap==False:
            for path in self.getPath():
                path.data.use_fill_caps = False
            self.report({'INFO'},'Fill Caps Off')
    
    def convertPath(self):
        curves = [] 
        for path in  self.getPath():
            if path.type == "MESH":
                path.select_set(True) 
                bpy.context.view_layer.objects.active = path
                bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
        for path in self.getPath():
            if path.type == "CURVE":
                curves.append(path)

    def cancelSweep(self):
        for path in self.getPath():
            if path.type == 'CURVE':
                path.data.bevel_object = None
                path.select_set(True) 
                bpy.context.view_layer.objects.active = path
                bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
        profile = self.getProfile()
        if profile.type == 'CURVE':
            profile.select_set(True) 
            bpy.context.view_layer.objects.active = path
            bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')

    def execute(self,context):
        
        bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
        return {'FINISHED'}
    def modal(self,context,event):
        #redraw viewport       
        context.area.tag_redraw()
        self.processEvents(event)
        kEvents = [getProp('mScale'),getProp('mRotate'),getProp('mMove'),getProp('mX'),getProp('mY'),getProp('mZ'),getProp('mCap'),getProp('mKeep'),'ESC','WHEELUPMOUSE','WHEELDOWNMOUSE','RIGHTMOUSE','SPACE']
        if event.type not in kEvents:
            return {'PASS_THROUGH'}
        if event.type =='ESC' and event.value=='PRESS' and not self.bRotate and not self.bMove and not self.bScale:
            self.report({'INFO'}, 'Cancelled')
            bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
            self.cancelSweep()
            return {'CANCELLED'}
        if event.type == "SPACE":
            self.report({'INFO'}, 'Finished')
            self.dropSelection()
            if not self.bKeepSpline:
                for path in self.getPath():
                    if path.type == 'CURVE':
                        path.select_set(True) 
                        bpy.context.view_layer.objects.active = path
                        bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
            for mesh in getObjectInCollection('Paths').children:
                mesh.select_set(True)
            bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
    def invoke(self,context,event):
        TooltipText ["handler"] = bpy.types.SpaceView3D.draw_handler_add(self.drawTooltips,(context,event), 'WINDOW', 'POST_PIXEL')
        self.bCap = getProp('bDefCap')
        self.bKeepSpline = getProp('bDefKeep')
        self.baseScale = self.getProfile().scale
        bevelProfile = None
        self.convertPath()
        if bpy.types.Scene.AQPipe_bevelProfile != "None":
            for profile in getObjectInCollection('Profiles').children:
                if profile.name == bpy.types.Scene.AQPipe_bevelProfile:
                    if profile.type == "MESH":
                        profile.select_set(True) 
                        bpy.context.view_layer.objects.active = profile
                        bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
                    bevelProfile = profile
            for path in getObjectInCollection('Paths').children:
                path.data.bevel_object = bevelProfile
            context.window_manager.modal_handler_add(self) 
        return {'RUNNING_MODAL'}

class AQPipe_Menu(bpy.types.Menu):
    bl_label = "Profiler"
    bl_idname = "VIEW3D_MT_Profiler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self,context):
        layout = self.layout
        cColumn = layout.column()
        if context.mode == 'EDIT_MESH':
            cColumn.operator('object.aqpipe_makeprofile')
            cColumn.operator('object.aqpipe_makepath')
        cColumn.separator(factor=1.0)
        cColumn.operator('object.aqpipe_sweepprofile')
        cColumn.separator(factor=1.0)
        cColumn.operator('object.aqpipe_addoptions')
        

def rmbMenu(self,context):
    layout = self.layout

    layout.menu('VIEW3D_MT_Profiler',text='A*Profiler')

def register():
    bpy.utils.register_class(AQPipe_Menu)
    bpy.types.Scene.AQPipe_bevelProfile = bpy.props.StringProperty(default="None")
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(rmbMenu)
    bpy.types.VIEW3D_MT_object_context_menu.append(rmbMenu)
    bpy.utils.register_class(AQPipePreferences)
    bpy.utils.register_class(AQPipe_MakeProfile)
    bpy.utils.register_class(AQPipe_MakePath)
    bpy.utils.register_class(AQPipe_SweepProfile)
    bpy.utils.register_class(AQPipe_AdditionalOptions)
    bpy.utils.register_class(AQPipe_FlushProfiles)
    bpy.utils.register_class(AQPipe_FlushPaths)
    bpy.utils.register_class(AQPipe_CleanUp)
    bpy.utils.register_class(AQPipe_PostEdit)
    
    
def unregister():
    del bpy.types.Scene.AQPipe_bevelProfile
    bpy.utils.unregister_class(AQPipe_Menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(rmbMenu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(rmbMenu)
    bpy.utils.unregister_class(AQPipePreferences)
    bpy.utils.unregister_class(AQPipe_MakeProfile)
    bpy.utils.unregister_class(AQPipe_MakePath)
    bpy.utils.unregister_class(AQPipe_SweepProfile)
    bpy.utils.unregister_class(AQPipe_AdditionalOptions)
    bpy.utils.unregister_class(AQPipe_FlushProfiles)
    bpy.utils.unregister_class(AQPipe_FlushPaths)
    bpy.utils.unregister_class(AQPipe_CleanUp)
    bpy.utils.unregister_class(AQPipe_PostEdit)
    
