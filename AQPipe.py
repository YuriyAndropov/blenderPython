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


#get collection by name
def getCollection(name):
    for collection in bpy.data.collections:
        if collection.name == name:
            return collection
            break
    return None

#get object in collection by name
def getObjectInCollection(name):
    for object in getCollection("QPipe").objects:
        if object.name == name:
            return object
            break
    return None

#check if there is already a collection with specified name
def checkCollections(value):
    for collection in bpy.data.collections:
        if collection.name == value:
            return True
            break
    return False
#check if there is already an object in collection with specified name
def checkForObject(value):
    for object in getCollection("QPipe").objects:
        if object.name == value:
            return True
            break
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
#TODO move collection name to propperies
#TODO add object and mode check
def objectFromPath(profileName,typeName):
    objects = bpy.context.selected_objects
    
    col = None
    profObj = None
    createCollectionAndParents()
    col = getCollection('QPipe')
    profObj = getObjectInCollection(typeName)

    for object in objects:
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
        
#TODO remove from selection.        
#TODO add object check
def convertToCurve():
    paths = getObjectInCollection("Paths")
    for path in paths.children:
        
        path.select_set(True) 
        bpy.context.view_layer.objects.active = path
        bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')

#make profile from selection operator
class AQPipe_MakeProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_makeprofile"
    bl_label = "AQPipe Make Profile"
    bl_options = {'REGISTER'}

    pName: bpy.props.StringProperty(name="Name :",default = "Profile")

    def dropSelection(self):
        for object in bpy.context.selected_objects:
            object.select_set(False)

    def draw(self,context):
        layout = self.layout
        nRow = layout.row(align=True)

        nRow.prop(self,"pName")

    def execute(self,context):
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

    def draw(self,context):
        layout = self.layout
        nRow = layout.row(align=True)

        nRow.prop(self,"pName")

    def execute(self,context):
        objectFromPath(self.pName,"Paths")
        self.dropSelection()
        bpy.ops.object.aqpipe_selectprofile('INVOKE_DEFAULT')
        return {'FINISHED'}
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=20)

#TODO add check for 0 profiles
#profile selection operator
class AQPipe_SelectProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_selectprofile"
    bl_label = "AQPipe Select Bevel Profile"
    bl_options = {'REGISTER', 'UNDO'}

    def updateProfile():
        bpy.types.Scene.AQPipe_selProfile = self.sceneProfiles
        return None

    sceneProfiles: bpy.props.EnumProperty(name="Scene Profiles",items=updateList)

    def draw(self,context):
        layout = self.layout
        enumRow = layout.row(align=True)

        enumRow.prop(self,"sceneProfiles")
        sceneProfiles = "0"

    def execute(self,context):
        return {'FINISHED'}

    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=300, height=40)

#sweep profile operator
class AQPipe_SweepProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_sweepprofile"
    bl_label = "AQPipe SweepProfileAlongPath"
    bl_options = {'REGISTER', 'UNDO'}

    def checkPath(self):
        path = getObjectInCollection("Paths")
        if len(path.children)==0: 
            bpy.ops.object.aqpipe_makepath('INVOKE_DEFAULT')
    #TODO profile conversion to a spline,set bevel object
    def setBevel(self):
        for path in getObjectInCollection("Paths").children:
            data = path.data
            data.bevel_object = bpy.types.Scene.AQPipe_selProfile
     


    def execute(self,context):
        createCollectionAndParents()
        self.checkPath()
        bpy.ops.object.aqpipe_selectprofile('INVOKE_DEFAULT')
        convertToCurve()
        self.setBevel()
        return {'FINISHED'}

    

def register():
    #pointer for selected profile
    bpy.types.Scene.AQPipe_selProfile = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.utils.register_class(AQPipe_MakeProfile)
    bpy.utils.register_class(AQPipe_MakePath)
    bpy.utils.register_class(AQPipe_SelectProfile)
    bpy.utils.register_class(AQPipe_SweepProfile)
    
def unregister():
    bpy.utils.unregister_class(AQPipe_MakeProfile)
    bpy.utils.unregister_class(AQPipe_MakePath)
    bpy.utils.unregister_class(AQPipe_SelectProfile)
    bpy.utils.unregister_class(AQPipe_SweepProfile)
    del bpy.types.Scene.AQPipe_selProfile