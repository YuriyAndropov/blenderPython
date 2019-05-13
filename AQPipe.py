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
    "name": "A* Quick Pipe",
    "description": "Fast Profile Along Path Generation",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "3D View"
}

import bpy
import bmesh

#profile selection enum list
listItems = []
addon_keymaps = []

class AQPipePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    keyList = (("A", "A", "A"),("B", "B", "B"),("C", "C", "C"),
    ("D", "D", "D"),("E", "E", "E"),("F", "F", "F"),("G", "G", "G"),
    ("H", "H", "H"),("I", "I", "I"),("J", "J", "J"),("K", "K", "K"),
    ("L", "L", "L"),("M", "M", "M"),("N", "N", "N"),("O", "O", "O"),
    ("P", "P", "P"),("Q", "Q", "Q"),("R", "R", "R"),("S", "S", "S"),
    ("T", "T", "T"),("U", "U", "U"),("V", "V", "V"),("W", "W", "W"),
    ("X", "X", "X"),("Y", "Y", "Y"),("Z", "Z", "Z"))

    

    profKey:bpy.props.EnumProperty(items=keyList,default="M")
    profAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False)
    profCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=True)
    profShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False)

    pathKey:bpy.props.EnumProperty(items=keyList,default="M")
    pathAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False)
    pathCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=True)
    pathShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False)

    sweepKey:bpy.props.EnumProperty(items=keyList,default="M")
    sweepAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False)
    sweepCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=True)
    sweepShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False)

    aOptKey:bpy.props.EnumProperty(items=keyList,default="M")
    aOptAlt:bpy.props.BoolProperty(name="Alt",description="Alt modifier",default=False)
    aOptCtrl:bpy.props.BoolProperty(name="Ctrl",description="Ctrl modifier",default=True)
    aOptShift:bpy.props.BoolProperty(name="Shift",description="Shift modifier",default=False)

    def draw(self,context):
        layout = self.layout
        propBox = layout.box()
        profRow = propBox.row(align=True)
        pathRow = propBox.row(align=True)
        sweepRow = propBox.row(align=True)
        aOptRow = propBox.row(align=True)

        profRow.prop(self,"profKey")
        profRow.prop(self,"profAlt")
        profRow.prop(self,"profCtrl")
        profRow.prop(self,"profShift")

        pathRow.prop(self,"pathKey")
        pathRow.prop(self,"pathAlt")
        pathRow.prop(self,"pathCtrl")
        pathRow.prop(self,"pathShift")

        sweepRow.prop(self,"sweepKey")
        sweepRow.prop(self,"sweepAlt")
        sweepRow.prop(self,"sweepCtrl")
        sweepRow.prop(self,"sweepShift")

        aOptRow.prop(self,"aOptKey")
        aOptRow.prop(self,"aOptAlt")
        aOptRow.prop(self,"aOptCtrl")
        aOptRow.prop(self,"aOptShift")

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
    for object in getCollection("QPipe").objects:
        if object.name == name:
            return object
    return None

#check if there is already a collection with specified name
def checkCollections(value):
    for collection in bpy.data.collections:
        if collection.name == value:
            return True
    return False
#check if there is already an object in collection with specified name
def checkForObject(value):
    for object in getCollection("QPipe").objects:
        if object.name == value:
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

#TODO add check for None type collection
#checking and creating proper structure for new objects
def createCollectionAndParents():
    newCol = None
    if checkCollections("QPipe") == False:
        newCol = bpy.data.collections.new("QPipe")
        bpy.context.scene.collection.children.link(newCol)
        profObject = bpy.data.objects.new("Profiles",None)
        newCol.objects.link(profObject)
        pathObject = bpy.data.objects.new("Paths",None)
        newCol.objects.link(pathObject)
    else:
        if checkForObject("Profiles") == False:
            profObject = bpy.data.objects.new("Profiles",None)
            newCol.objects.link(profObject)
        if checkForObject("Paths") == False:
            pathObject = bpy.data.objects.new("Paths",None)
            newCol.objects.link(pathObject)

#get new object from edge selection and add it to collection
#TODO move collection name to properies
#TODO add object and mode check
def objectFromPath(profileName,typeName):
   
    objects = bpy.context.selected_objects
    col = None
    profObj = None
    createCollectionAndParents()
    col = getCollection('QPipe')
    profObj = getObjectInCollection(typeName)
    

    for object in objects:
        if object.type == "MESH" and bpy.context.mode == 'EDIT':
            data = object.data
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
            newObj.location = object.location
            newObj.parent = profObj
            bmesh.types.BMesh.free
   
        
def convertToCurve():
    paths = getObjectInCollection("Paths")
    for path in paths.children:
        if path.type == "MESH":
            path.select_set(True) 
            bpy.context.view_layer.objects.active = path
            bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
        if path.type == "CURVE":
            object.parent = getObjectInCollection("Profiles")
            


#make profile from selection operator
class AQPipe_MakeProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_makeprofile"
    bl_label = "AQPipe Make Profile"
    bl_options = {'REGISTER'}

    pName: bpy.props.StringProperty(name="Name :",default = "Profile")
    actionType: bpy.props.StringProperty(name="ActionType",default = "")

    def dropSelection(self):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        for object in bpy.context.selected_objects:
            object.select_set(False)
    
    def checkState(self):
        for object in bpy.context.selected_objects:
            if object.type != "MESH" and object.type != "CURVE":
                self.report({'INFO'}, 'Object should be a MESH or CURVE type')
                return False
            if bpy.context.mode == 'OBJECT' and object.type == "MESH":
                self.report({'INFO'}, 'MESH should be in Edit Mode to select path')
                return False
        return True

    def draw(self,context):
        layout = self.layout
        nRow = layout.row(align=True)

        nRow.prop(self,"pName")

    def execute(self,context):
        print (self.actionType)
        if self.checkState()==True:
            objectFromPath(self.pName,"Profiles")
            self.dropSelection()
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
        for object in bpy.context.selected_objects:
            object.select_set(False)

    def checkState(self):
        for object in bpy.context.selected_objects:
            if object.type != "MESH" and object.type != "CURVE":
                self.report({'INFO'}, 'Object should be a MESH or CURVE type')
                return False
            if bpy.context.mode == 'OBJECT' and object.type == "MESH":
                self.report({'INFO'}, 'MESH should be in Edit Mode to select path')
                return False
        return True

    def draw(self,context):
        layout = self.layout
        nRow = layout.row(align=True)

        nRow.prop(self,"pName")

    def execute(self,context):
        objectFromPath(self.pName,"Paths")
        self.dropSelection()
        return {'FINISHED'}

    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=20)

#TODO add check for 0 profiles
#profile selection operator
class AQPipe_SweepProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_sweepprofile"
    bl_label = "AQPipe Sweep Profile"
    bl_options = {'REGISTER', 'UNDO'}


    sceneProfiles: bpy.props.EnumProperty(name="Scene Profiles",items=updateList)
  
    def setBevel(self,bevelObject):
        for path in getObjectInCollection("Paths").children:
            curve = path.data
            curve.bevel_object = bevelObject

    def draw(self,context):
        layout = self.layout
        enumRow = layout.row(align=True)

        enumRow.prop(self,"sceneProfiles")
        sceneProfiles = "0"

    def execute(self,context):
        createCollectionAndParents()
        bObj = None
        for profile in getObjectInCollection('Profiles').children:
            if profile.name == self.sceneProfiles:
                bObj = profile
        self.setBevel(bObj)
        return {'FINISHED'}

    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=40)

#TODO add flush paths and profiles, remove QPipe data
#additional options 
class AQPipe_AdditionalOptions(bpy.types.Operator):
    bl_idname = "object.aqpipe_addoptions"
    bl_label = "AQPipe Additional Options"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self,context):
        return {'FINISHED'}
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=20)

    

def register():
    bpy.utils.register_class(AQPipePreferences)
    bpy.utils.register_class(AQPipe_MakeProfile)
    bpy.utils.register_class(AQPipe_MakePath)
    bpy.utils.register_class(AQPipe_SweepProfile)
    bpy.utils.register_class(AQPipe_AdditionalOptions)
    
    
def unregister():
    
    bpy.utils.unregister_class(AQPipePreferences)
    bpy.utils.unregister_class(AQPipe_MakeProfile)
    bpy.utils.unregister_class(AQPipe_MakePath)
    bpy.utils.unregister_class(AQPipe_SweepProfile)
    bpy.utils.unregister_class(AQPipe_AdditionalOptions)
