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
import mathutils
import math

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
    if checkCollections("QPipe"):
        for object in getCollection("QPipe").objects:
            if object.type != None and object.name == name:
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
    if checkCollections('Profiles'):
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
#TODO move collection name to properies
#TODO add object and mode check
def objectFromPath(profileName,typeName):
    objects = bpy.context.selected_objects
    createCollectionAndParents()
    col = getCollection('QPipe')
    profObj = getObjectInCollection(typeName)

    for object in objects:
        if object.type == "MESH":
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
            print(profObj)
            print('loc')
            newObj.location = object.location
            newObj.parent = profObj
            bmesh.types.BMesh.free
            #setting origin to center of new object
            #bpy.ops.object.mode_set(mode='OBJECT')
            #bpy.ops.object.select_all( action = 'DESELECT' )
            #newObj.select_set(True)
            #bpy.context.view_layer.objects.active = newObj
            #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            


#don't want to use built-in operator for creating a curve
def createCurve():
    objects = bpy.context.selected_objects
    for object in objects:
        data = object.data
        curveData = bpy.data.curves.new('QpipeCurve', type='CURVE')
        spline = curveData.splines.new('POLY')
        for vert in data.verts:
            spline.points.add(1)
       
        
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
#FIXME not working if path was created first
class AQPipe_MakeProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_makeprofile"
    bl_label = "AQPipe Make Profile"
    bl_options = {'REGISTER'}

    pName: bpy.props.StringProperty(name="Name :",default = "Profile")

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
        #type = "Profiles"
        #objectFromPath(self.pName,"Profiles")
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
        if self.checkState():
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

    def dupProfile(self,meshProfile):
        if meshProfile.type == "MESH":
            meshProfile.select_set(True) 
            bpy.context.view_layer.objects.active = meshProfile
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            data = meshProfile.data
            bm = bmesh.from_edit_mesh(data)
            dupe = bm.copy()
            newMesh = bpy.data.meshes.new("ProfileMesh")
            dupe.to_mesh(newMesh)
            newObj = bpy.data.objects.new("SweeProfile", newMesh)
            col = getCollection('QPipe')
            col.objects.link(newObj)
            newObj.location = meshProfile.location
            newObj.parent = getObjectInCollection('Temp')
            bmesh.types.BMesh.free
            return newObj
        else:
            return None

    def draw(self,context):
        layout = self.layout
        enumRow = layout.row(align=True)

        enumRow.prop(self,"sceneProfiles")
        sceneProfiles = "0"
    
    def convertProfToCurve(self,mesh):
            if mesh.type == "MESH":
                mesh.select_set(True) 
                bpy.context.view_layer.objects.active = mesh
                bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')

    def convertPathToCurve(self):
        for path in getObjectInCollection('Paths').children:
            if path.type == "MESH":
                path.select_set(True) 
                bpy.context.view_layer.objects.active = path
                bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
        bpy.ops.object.select_all(action='DESELECT')
        for path in getObjectInCollection('Paths').children:
            path.select_set(True)
        bpy.ops.object.join()

    def execute(self,context):
        createCollectionAndParents()
        bObj = None
        for profile in getObjectInCollection('Profiles').children:
            if profile.name == self.sceneProfiles:
                bpy.types.Scene.AQPipe_bevelProfile = self.sceneProfiles
                bObj = profile
                self.convertProfToCurve(bObj)
        self.convertPathToCurve()
        curve = getObjectInCollection("Paths").children[0].data
        curve.bevel_object = bObj
        self.setBevel(bObj)
        #bpy.ops.object.aqpipe_postedit()
        return {'FINISHED'}

    def invoke(self,context,event):
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

    sceneProfiles: bpy.props.EnumProperty(name="Scene Profiles",items=updateList)

    def execute(self,context):
        return {'FINISHED'}
    def draw(self,context):
        layout = self.layout
        enumRow = layout.row(align=True)

        enumRow.prop(self,"sceneProfiles")
        
    # def draw_callback_px(self, context):
    #     #draw stuff
    def modal(self,context,event):
        print(len(self.sceneProfiles))
        #print('modal')
        if event.type == "P":
            print('keys')
            #context.window_manager.invoke_props_dialog(self, width=300, height=40)
        # if event.type == "W":
        #     #run move
        # if event.type == "E":
        #     #run rotate
        # if event.type == "R":
        #     #run scale
        # if event.type == "X":
        #     #leave as curve
        if event.type =="ESC":
            return {'CANCELLED'}
        if event.type == "SPACE":
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
    
    
    

    def invoke(self,context,event):
        #print('invoke')
        #FIXME CRASH
        #context.window_manager.invoke_props_dialog(self, width=300, height=40)
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}

def register():
    bpy.types.Scene.AQPipe_bevelProfile = bpy.props.StringProperty(default="None")
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
    bpy.utils.unregister_class(AQPipePreferences)
    bpy.utils.unregister_class(AQPipe_MakeProfile)
    bpy.utils.unregister_class(AQPipe_MakePath)
    bpy.utils.unregister_class(AQPipe_SweepProfile)
    bpy.utils.unregister_class(AQPipe_AdditionalOptions)
    bpy.utils.unregister_class(AQPipe_FlushProfiles)
    bpy.utils.unregister_class(AQPipe_FlushPaths)
    bpy.utils.unregister_class(AQPipe_CleanUp)
    bpy.utils.unregister_class(AQPipe_PostEdit)
    
