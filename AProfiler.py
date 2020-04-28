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
#action = [('PATH','PATH','PATH'),('PROFILE','PROFILE''PROFILE'),('SWEEP','SWEEP''SWEEP')]
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
class AProfilerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    keyList = (('NONE','None','NONE'),("A", "A", "A"),("B", "B", "B"),("C", "C", "C"),
    ("D", "D", "D"),("E", "E", "E"),("F", "F", "F"),("G", "G", "G"),
    ("H", "H", "H"),("I", "I", "I"),("J", "J", "J"),("K", "K", "K"),
    ("L", "L", "L"),("M", "M", "M"),("N", "N", "N"),("O", "O", "O"),
    ("P", "P", "P"),("Q", "Q", "Q"),("R", "R", "R"),("S", "S", "S"),
    ("T", "T", "T"),("U", "U", "U"),("V", "V", "V"),("W", "W", "W"),
    ("X", "X", "X"),("Y", "Y", "Y"),("Z", "Z", "Z"))

    mMove:bpy.props.EnumProperty(name='Move',items=keyList,default="M")
    mRotate:bpy.props.EnumProperty(name='Rotate',items=keyList,default="R")
    mScale:bpy.props.EnumProperty(name='Scale',items=keyList,default="S")

    mX:bpy.props.EnumProperty(name='X',items=keyList,default="X")
    mY:bpy.props.EnumProperty(name='Y',items=keyList,default="Y")
    mZ:bpy.props.EnumProperty(name='Z',items=keyList,default="Z")

    mCap:bpy.props.EnumProperty(name='Cap',items=keyList,default="C")
    mKeep:bpy.props.EnumProperty(name='KeepSpline',items=keyList,default="V")
    m2D:bpy.props.EnumProperty(name='2DSpline',items=keyList,default="B")


    cursorColor:bpy.props.FloatVectorProperty(name="Main Color",description="Color", default=(1.0,1.0,1.0),subtype='COLOR')
    highlightColor:bpy.props.FloatVectorProperty(name="Highlight Color",description="Color", default=(0.0,1.0,0.0),subtype='COLOR')
    bTips:bpy.props.BoolProperty(name='Show KeyTips',default=True)
    bDefCap:bpy.props.BoolProperty(name='Fill Caps',default=False)
    bDefKeep:bpy.props.BoolProperty(name='Keep as Spline',default=False)
    fontSize:bpy.props.IntProperty(name='FontSize',default=15)
    tFontSize:bpy.props.IntProperty(name='FontSize',default=25)

    def draw(self,context):
        layout = self.layout
        optBox = layout.box()
        optBox.label(text='Addon Default Settings')
        modalBox = layout.box()
        modalBox.label(text="Modal Hotkeys")

        toolBox = modalBox.box()
        toolBox.label(text='Tool hotkeys in modal')
        toolRow = toolBox.row(align=True)
        toolRow.prop(self,'mMove')
        toolRow.prop(self,'mRotate')
        toolRow.prop(self,'mScale')
        addRow = toolBox.row(align=True)
        addRow.prop(self,'mCap')
        addRow.prop(self,'mKeep')
        addRow.prop(self,'m2D')
        

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
        sRow.prop(self,'fontSize')
        sRow.prop(self,'tFontSize')
        cRow = optBox.row()
        cRow.prop(self,'cursorColor')
        cRow.prop(self,'highlightColor')

#get addon preferences option by name


class AProfiler_ADV(bpy.types.Panel):
    bl_label = "AProfiler"
    bl_idname = "VIEW3D_PT_ADV"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self,context):
        layout = self.layout
        settings = context.tool_settings
        layout.template_curveprofile(settings,"custom_bevel_profile_preset")

def getProp(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

def draw_menu(self,context):
        layout = self.layout
        settings = context.tool_settings
        layout.template_curveprofile(settings,"custom_bevel_profile_preset")

class AProfiler_CreateCurve(bpy.types.Operator):
    bl_idname = "object.aprofiler_createcurve"
    bl_label = "A*Profiler Create Profile"
    bl_options = {'REGISTER','UNDO'}

    #collectionName = 'AProfiler'
    action = [('PATH','PATH','PATH'),('PROFILE','PROFILE','PROFILE'),('SWEEP','SWEEP','SWEEP'),('SWEEPADV','SWEEPADV','SWEEPADV')]
    

    curveName = ''
    profilerCollection = None
    pathSub = None
    profSub = None
    profileName = ''
    workProfile = None

    def getProfiles(self,context):
        profs = []
        count = 0
        for collection in bpy.data.collections:
            if collection.name == 'AProfiler':
                for sub in collection.objects:
                    if sub.name == 'Profiles':
                        for obj in sub.children:
                            profs.append((obj.name,obj.name,obj.name))
                            count+= 1
        return profs

    def setProfile(self,context):
        print('setting names')
        for collection in bpy.data.collections:
            if collection.name == 'AProfiler':
                for sub in collection.objects:
                    if sub.name == 'Profiles':
                        for obj in sub.children:
                            print('POINTER')
                            print(self.eProfiles[0])
                            if obj.name == self.eProfiles:
                                print('SETTING NAME')
                                print(obj.name)
                                self.profilePointer = obj.name
        return None


    eProfiles:bpy.props.EnumProperty(items=getProfiles,update=setProfile)
    eAction:bpy.props.EnumProperty(items=action)
    cName:bpy.props.StringProperty(default='Curve')
    profilePointer:bpy.props.StringProperty()


    def draw(self,context):
        layout = self.layout
        if self.eAction != 'SWEEP':
            nRow = layout.row(align=True)
            nRow.prop(self,"cName")
        if self.eAction == "SWEEP":
            nRow = layout.row(align=True)
            nRow.prop(self,"eProfiles")
        if self.eAction == "SWEEPADV":
            settings = context.tool_settings
            layout.template_curveprofile(settings,"custom_bevel_profile_preset")
            print('START ALL POINTS')
            for point in settings.custom_bevel_profile_preset.points:
                print(point.location)
            print('END CURVE POINTS')
        #print(settings.custom_bevel_profile_preset.points)

    def checkForProfiles(self):
        for sub in self.profilerCollection.objects:
            if sub.name == 'Profiles':
                self.profSub = sub
                return True
        return False

    def checkForPaths(self):
        for sub in self.profilerCollection.objects:
            if sub.name == 'Paths':
                self.pathSub = sub
                return True
        return False

    def checkForCollection(self):
        for collection in bpy.data.collections:
            if collection.name == 'AProfiler':
                self.profilerCollection = collection
                return True
        return False

    def createCollection(self):
        if not self.checkForCollection():
            self.profilerCollection = bpy.data.collections.new("AProfiler")
            bpy.context.scene.collection.children.link(self.profilerCollection)
        if not self.checkForProfiles():
            self.profSub = bpy.data.objects.new("Profiles",None)
            self.profilerCollection.objects.link(self.profSub)
        if not self.checkForPaths():
            self.pathSub = bpy.data.objects.new("Paths",None)
            self.profilerCollection.objects.link(self.pathSub)

    def checkSweep(self):
        if bpy.context.mode == 'EDIT_MESH' and self.checkIfSelection() == '0' and len(self.pathSub.children) == 0:
            return False 
        if bpy.context.mode == 'OBJECT' and len(self.pathSub.children) == 0:
            return False
        return True

    #return how many edges are selected
    def checkIfSelection(self):
        return bpy.context.scene.statistics(bpy.context.view_layer).split("|")[2].split(':')[1].split("/")[0]

    def bevelSpline(self,obj):
        print('setting bevel profile')
        print(self.profilePointer)
        prof = None
        for profile in self.profSub.children:
            if profile.name == self.profilePointer:
                prof = profile
        if obj.type == 'CURVE' and prof != None:
            obj.data.bevel_object = prof

    def createPath(self):
        objects = bpy.context.selected_objects
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            if obj.type == "MESH":
                data = obj.data
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                nonSelected = []
                for edge in bm.edges:
                    if edge.select == False:
                        nonSelected.append(edge)
                bmesh.ops.delete(bm,geom=nonSelected,context='EDGES')
                #new mesh
                if len(bm.edges)>0:
                    newMesh = bpy.data.meshes.new("ProfilerMesh")
                    bm.to_mesh(newMesh)
                    #TODO do something with names
                    #self.cName = obj.name
                    newObj = bpy.data.objects.new(self.cName, newMesh)
                    self.profilerCollection.objects.link(newObj)
                    newObj.location = obj.location
                    if self.eAction == 'PATH' or self.eAction ==  'SWEEP':
                        newObj.parent = self.pathSub
                    elif self.eAction == 'PROFILE':
                        newObj.parent = self.profSub
                    if newObj.type == "MESH":
                        newObj.select_set(True) 
                        bpy.context.view_layer.objects.active = newObj
                        bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
                        if newObj.type != 'CURVE':
                            bpy.ops.object.delete()
                            self.report({'WARNING'},'Failed to create a spline from selection')
                bm.free()
        #for obj in objects:
            #bpy.context.view_layer.objects.active = obj
            #obj.select_set(True)
        #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                return newObj
    

    #def draw(self, context):
    #self.layout.label(text="Hello World")


#bpy.context.window_manager.popup_menu(draw, title="Greeting", icon='INFO')
    def modal(self,context,event):
        kEvents = ['ESC']
        print('modal')
        #context.window_manager.popup_menu(draw_menu)
        #bpy.context.window_manager.popup_menu(draw_menu, title="Greeting", icon='INFO')
        #context.window_manager.invoke_props_popup(self, event)
        if event.type not in kEvents:
                return {'PASS_THROUGH'}
        
        if event.type == "ESC":
            print('cancelled')
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def execute(self,context):
        if self.eAction == 'PATH' or self.eAction == 'PROFILE':
            self.createPath()
        if self.eAction == 'SWEEP':
            if bpy.context.mode == 'EDIT_MESH' and self.checkIfSelection() > '0':
                    path = self.createPath()
                    self.bevelSpline(path)
            elif (bpy.context.mode == 'EDIT_MESH' and self.checkIfSelection()==0) or bpy.context.mode == 'OBJECT' :
                for obj in self.pathSub.children:
                    self.bevelSpline(obj)       
            
        return {'FINISHED'}
    def invoke(self,context,event):
        
        print(self.eAction)
        self.createCollection()
        if self.eAction == 'PATH' or self.eAction == 'PROFILE':
            return context.window_manager.invoke_props_dialog(self, width=300, height=20)
        if self.eAction == 'SWEEP':
            if self.checkSweep():
                #setting self profile to invoke get and set functions
                self.eProfiles = self.eProfiles
                return context.window_manager.invoke_props_popup(self, width=300, height=20)
            else:
                return {'CANCELLED'}
        if self.eAction == 'SWEEPADV':
            #bpy.context.window_manager.popover(draw_menu, title="Greeting", icon='INFO')
            #context.window_manager.invoke_props_popup(self,event)
            #context.window_manager.invoke_popup(self)
            context.window_manager.modal_handler_add(self) 
            return {'RUNNING_MODAL'}
            #context.window_manager.invoke_props_dialog(self, width=300, height=20)
            #return self.modal(context,event)
            #return context.window_manager.invoke_props_dialog(self, width=300, height=20)

        
#path.data.bevel_object = bevelProfile
# class AProfiler_SweepProfile(bpy.types.Operator):
#     bl_idname = "object.aprofiler_sweepprofile"
#     bl_label = "A*Profiler Sweep Profile"
#     bl_options = {'REGISTER','UNDO'}
    
#     profilerCollection = None
#     profSub = None
#     pathSub = None
#     bevelObject = None

#     def checkCollection(self):
#         for collection in bpy.data.collections:
#             if collection.name == 'AProfiler':
#                 self.profilerCollection = collection
#                 for sub in collection.objects:
#                     print(sub)
#                     if sub.name == 'Profiles':
#                         self.profSub = sub
#                     if sub.name == 'Paths':
#                         self.pathSub = sub
#                 print('collection there')
#                 return True
#         print('no collection')
#         return False
    #def setBevelObject(self):
        #for obj in self.pathSub:
            #obj.data.bevel_object = 

    #def invoke(self,context,event):




# #get collection by name
# def getCollection(name):
#     for collection in bpy.data.collections:
#         if collection.name == name:
#             return collection
#     return None

# #get object in collection by name
# def getObjectInCollection(name):
#     if checkCollections("AProfiler"):
#         for obj in getCollection("AProfiler").objects:
#             if obj.type != None and obj.name == name:
#                 return obj
#     return None

# #check if there is already a collection with specified name
# def checkCollections(value):
#     for collection in bpy.data.collections:
#         if collection != None:
#             if collection.name == value:
#                 return True
#     return False
# #check if there is already an object in collection with specified name
# def checkForObject(value):
#     for obj in getCollection("AProfiler").objects:
#         if obj.name == value:
#             return True
#     return False

# #update profile selection enum
# def updateList(self,context):
#     del listItems[:]
#     id = 0
#     for profile in getObjectInCollection("Profiles").children:
#         pId = str(id)
#         name = profile.name
#         des = profile.name
#         icon = 'OUTLINER_DATA_CURVE'
#         if (str(id),name,des,icon,id) not in listItems:
#             listItems.append((name,name,des,icon,id))
#         id+=1
#     return listItems

# #checking and creating proper structure for new objects
# def createCollectionAndParents():
#     if checkCollections("AProfiler") == False:
#         newCol = bpy.data.collections.new("AProfiler")
#         bpy.context.scene.collection.children.link(newCol)
#         profObject = bpy.data.objects.new("Profiles",None)
#         newCol.objects.link(profObject)
#         pathObject = bpy.data.objects.new("Paths",None)
#         newCol.objects.link(pathObject)
#         tempObject = bpy.data.objects.new("Temp",None)
#         newCol.objects.link(tempObject)
#     else:
#         collection = getCollection("AProfiler")
#         if checkForObject("Profiles") == False:
#             profObject = bpy.data.objects.new("Profiles",None)
#             collection.objects.link(profObject)
#         if checkForObject("Paths") == False:
#             pathObject = bpy.data.objects.new("Paths",None)
#             collection.objects.link(pathObject)
#         if checkForObject("Temp") == False:
#             tempObject = bpy.data.objects.new("Temp",None)
#             collection.objects.link(tempObject)

# #get new object from edge selection and add it to collection
# def objectFromPath(profileName,typeName):
#     objects = bpy.context.selected_objects
#     createCollectionAndParents()
#     col = getCollection("AProfiler")
#     profObj = getObjectInCollection(typeName)

#     for obj in objects:
#         if obj.type == "MESH":
#             data = obj.data
#             bm = bmesh.from_edit_mesh(data)
#             nonSelected = []
#             dupe = bm.copy()
#             for edge in dupe.edges:
#                 if edge.select == False:
#                     nonSelected.append(edge)
#             bmesh.ops.delete(dupe,geom=nonSelected,context='EDGES')
#             newMesh = bpy.data.meshes.new("QPipeMesh")
#             dupe.to_mesh(newMesh)
#             newObj = bpy.data.objects.new(profileName, newMesh)
#             col.objects.link(newObj)
#             newObj.location = obj.location
#             newObj.parent = profObj
#             bmesh.types.BMesh.free
        
# def convertToCurve(typeName):
#     profiles = getObjectInCollection(typeName)
#     for path in profiles.children:
#         if path.type == "MESH":
#             path.select_set(True) 
#             bpy.context.view_layer.objects.active = path
#             bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
#         if path.type == "CURVE":
#             path.parent = getObjectInCollection(typeName)

# #make profile from selection operator
# class AProfiler_MakeProfile(bpy.types.Operator):
#     bl_idname = "object.aprofiler_makeprofile"
#     bl_label = "A*Profiler Make Profile"
#     bl_options = {'REGISTER','UNDO'}

#     pName: bpy.props.StringProperty(name="Name :",default = "Profile")

#     def dropSelection(self):
#         bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#         for obj in bpy.context.selected_objects:
#             obj.select_set(False)
    
#     def getCreated(self):
#         for path in getObjectInCollection('Profiles').children:
#             if path.name == self.pName:
#                 return path
#         return None
    
#     def checkState(self):
#         for obj in bpy.context.selected_objects:
#             if obj.type != "MESH" and obj.type != "CURVE":
#                 self.report({'INFO'}, 'Object should be a MESH or CURVE type')
#                 return False
#             if bpy.context.mode == 'OBJECT' and obj.type == "MESH":
#                 self.report({'INFO'}, 'MESH should be in Edit Mode to select path')
#                 return False
#         return True

#     def draw(self,context):
#         layout = self.layout
#         nRow = layout.row(align=True)

#         nRow.prop(self,"pName")

#     def execute(self,context):
#         if self.checkState()==True:
#             objectFromPath(self.pName,"Profiles")
#             bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#             self.dropSelection()
#             self.getCreated().select_set(True)
#             bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
#         return {'FINISHED'}
#     def invoke(self,context,event):
#         return context.window_manager.invoke_props_dialog(self, width=300, height=20)

# #make path from selection operator
# class AProfiler_MakePath(bpy.types.Operator):
#     bl_idname = "object.aprofiler_makepath"
#     bl_label = "A*Profiler Make Path"
#     bl_options = {'REGISTER','UNDO'}

#     pName: bpy.props.StringProperty(name="Name :",default = "Path")

#     def dropSelection(self):
#         for obj in bpy.context.selected_objects:
#             obj.select_set(False)

#     def getCreated(self):
#         for path in getObjectInCollection('Paths').children:
#             if path.name == self.pName:
#                 return path
#         return None

#     def checkState(self):
#         for obj in bpy.context.selected_objects:
#             if obj.type != "MESH" and obj.type != "CURVE":
#                 self.report({'INFO'}, 'Object should be a MESH or CURVE type')
#                 return False
#             if bpy.context.mode == 'OBJECT' and obj.type == "MESH":
#                 self.report({'INFO'}, 'MESH should be in Edit Mode to select path')
#                 return False
#         return True

#     def draw(self,context):
#         layout = self.layout
#         nRow = layout.row(align=True)

#         nRow.prop(self,"pName")

#     def execute(self,context):
#         if self.checkState():
#             objectFromPath(self.pName,"Paths")
#             bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#             self.dropSelection()
#             self.getCreated().select_set(True)
#             bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
#         return {'FINISHED'}

#     def invoke(self,context,event):
#         return context.window_manager.invoke_props_dialog(self, width=300, height=20)

# #profile selection operator
# class AProfiler_SweepProfile(bpy.types.Operator):
#     bl_idname = "object.aprofiler_sweepprofile"
#     bl_label = "A*Profiler Sweep Profile"
#     bl_options = {'REGISTER', 'UNDO'}

#     def profileUpdate(self,context):
#         bpy.types.Scene.AQPipe_bevelProfile = self.sceneProfiles
#         return None

#     sceneProfiles: bpy.props.EnumProperty(name="Scene Profiles",items=updateList,update=profileUpdate)
    
#     def checkSelectionMode(self):
#         if bpy.context.mode == 'OBJECT':
#             return False
#         if bpy.context.mode == 'EDIT_MESH':
#             if bpy.context.scene.statistics(bpy.context.view_layer).split("|")[2].split(':')[1].split('/')[0] == '0':
#                 return False
#         return True

#     def draw(self,context):
#         layout = self.layout
#         enumRow = layout.row(align=True)
#         enumRow.prop(self,"sceneProfiles")
    
#     def execute(self,context):
#         if bpy.context.mode == 'EDIT_MESH':
#             if bpy.context.scene.statistics(bpy.context.view_layer).split("|")[2].split(':')[1].split('/')[0] != '0':
#                 objectFromPath('QPath','Paths')
#         bpy.ops.object.aprofiler_postedit('INVOKE_DEFAULT')
#         return {'INTERFACE'}

#     def invoke(self,context,event):
        
#         if bpy.context.mode =='OBEJCT' and self.checkSelectionMode():
#             objectFromPath('Path','Paths')
#         if not checkCollections("AProfiler"):
#             self.report({'WARNING'},'No profiles and paths data in the scene')
#             return {'CANCELED'}
#         if len(getObjectInCollection('Profiles').children) == 0:
#             self.report({'WARNING'}, 'No available profiles in the scene')
#             return {'CANCELLED'}
#         if len(getObjectInCollection('Paths').children) == 0 and not self.checkSelectionMode():
#             self.report({'WARNING'}, 'No available path in the scene')
#             return {'CANCELLED'}
#         bpy.types.Scene.AQPipe_bevelProfile = self.sceneProfiles
#         return context.window_manager.invoke_props_dialog(self, width=300, height=40)

# #additional options 
# class AProfiler_CleanUp(bpy.types.Operator):
#     bl_idname = "object.aprofiler_cleanup"
#     bl_label = "A*Profiler Clean Stuff"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self,context):
#         for object in getCollection("AProfiler").objects:
#             bpy.data.objects.remove(object,do_unlink=True,do_id_user=True,do_ui_user=True)
#         bpy.data.collections.remove(getCollection("AProfiler"))
#         return {'FINISHED'}

# class AProfiler_FlushPaths(bpy.types.Operator):
#     bl_idname = "object.aprofiler_flushpaths"
#     bl_label = "A*Profiler Flush Paths"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self,context):
#         for path in getObjectInCollection('Paths').children:
#             bpy.data.objects.remove(path,do_unlink=True,do_id_user=True,do_ui_user=True)
#         return {'FINISHED'}

# class AProfiler_FlushProfiles(bpy.types.Operator):
#     bl_idname = "object.aprofiler_flushprofiles"
#     bl_label = "A*Profiler Flush Profiles"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self,context):
#         for profile in getObjectInCollection('Profiles').children:
#             bpy.data.objects.remove(profile,do_unlink=True,do_id_user=True,do_ui_user=True)
#         return {'FINISHED'}

# class AProfiler_AdditionalOptions(bpy.types.Operator):
#     bl_idname = "object.aprofiler_addoptions"
#     bl_label = "A*Profiler Additional Options"
#     bl_options = {'REGISTER', 'UNDO'}

#     def draw(self,context):
#         layout = self.layout
#         optionBox = layout.box()
#         fPath = optionBox.row()
#         fProf = optionBox.row()
#         cleanUp = optionBox.row()
#         fPath.operator("object.aprofiler_flushpaths")
#         fProf.operator("object.aprofiler_flushprofiles")
#         cleanUp.operator("object.aprofiler_cleanup")
#     def execute(self,context):
#         return {'FINISHED'}

#     def invoke(self,context,event):
#         return context.window_manager.invoke_props_dialog(self, width=300, height=20)

# class AProfiler_PostEdit(bpy.types.Operator):
#     bl_idname = "object.aprofiler_postedit"
#     bl_label = "A*Profiler Post Edit Menu"
#     bl_options = {'REGISTER', 'UNDO'}
#     #switches
#     b2D: bpy.props.BoolProperty(default = False)
#     bKeepSpline: bpy.props.BoolProperty(default=False)
#     bCap: bpy.props.BoolProperty(default=False)
#     bScale: bpy.props.BoolProperty(name='Scale',default=False)
#     bMove:  bpy.props.BoolProperty(name='Move',default=False)
#     bRotate:bpy.props.BoolProperty(name='Rotate',default=False)
#     bXAxis: bpy.props.BoolProperty(name='X',default=False)
#     bYAxis: bpy.props.BoolProperty(name='Y',default=False)
#     bZAxis: bpy.props.BoolProperty(name='Z',default=False)
#     #base transform
#     baseScale: bpy.props.FloatVectorProperty(default=(0,0,0))
#     baseLoc: bpy.props.FloatVectorProperty(default=(0.0,0.0,0.0,0.0),subtype='TRANSLATION',size=4)
#     baseRotation: bpy.props.FloatVectorProperty(default=(0,0,0))

#     def remap(self,value, low1, high1, low2, high2):
#         return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

#     def addDraw(self,x,y,size,text,color):
#         blf.position(font_id, x, y, 0)
#         blf.size(font_id, size, 72)
#         blf.color(font_id, color[0], color[1], color[2], 1)
#         blf.draw(font_id, text)

#     def drawTooltips(self,context,event):
#         tWidth = context.area.regions[2].width
#         nWidth = bpy.context.area.regions[3].width
#         width = context.area.width
#         height = context.area.height
#         color = getProp('cursorColor')
#         size = getProp('tFontSize')
#         text = 'Sweep Profile Mode'
#         self.addDraw((width-tWidth-nWidth)/2 - len(text)*size*0.1,height-50,size,text,color)
#         if getProp('bTips'):
#             text = 'Hotkeys :'
#             shift = size * 6
#             self.addDraw(tWidth,height/2+shift,size,text,color)
#             shift -= size * 1.5
#             text = getProp('mMove') +  ' : Move'
#             self.addDraw(tWidth+size,height/2 + shift,size,text,color)
#             shift -= size * 1.5
#             text = getProp('mRotate') +  ' : Rotate'
#             self.addDraw(tWidth+size,height/2+shift,size,text,color)
#             shift -= size * 1.5
#             text = getProp('mScale') + ' : Scale'
#             self.addDraw(tWidth+size,height/2+shift,size,text,color)
#             shift -= size * 3
#             text = getProp('mX') + ' : X Axis'
#             self.addDraw(tWidth+size,height/2 + shift,size,text,color)
#             shift -= size * 1.5
#             text = getProp('mY') + ' : Y Axis'
#             self.addDraw(tWidth+size,height/2 + shift,size,text,color)
#             shift -= size * 1.5
#             text = getProp('mZ') + ' : Z Axis'
#             self.addDraw(tWidth+size,height/2 + shift,size,text,color)
#             shift -= size * 3
#             text = getProp('mCap') + ' : Cap Ends Toggle'
#             self.addDraw(tWidth+size,height/2 +shift,size,text,color)
#             shift -= size * 1.5
#             text =  getProp('mKeep') +  ' : Leave as Curve Toggle'
#             self.addDraw(tWidth+size,height/2 + shift,size,text,color)
#             shift -= size * 1.5
#             text =  getProp('m2D') +  ' : Switch to 2D Spline : Destructive !'
#             self.addDraw(tWidth+size,height/2 + shift,size,text,color)
#         if self.bMove:
#             text = 'Move   : '
#         elif self.bScale:
#             text = 'Scale  : '       
#         elif self.bRotate:
#             text = 'Rotate : '
#         else:
#             text = ""
#         size = getProp('fontSize')
#         shift = size * len(text) * 0.5
#         if self.bMove or self.bScale or self.bRotate:
#             self.addDraw(event.mouse_x,event.mouse_y-150,size,text,color)
#             if self.bXAxis:
#                 color = getProp('highlightColor')
#             else:
#                 color = getProp('cursorColor')
#             text = 'X :'
#             self.addDraw(event.mouse_x + shift,event.mouse_y-150,size,text,color)
#             shift += size * len(text) * 0.5
#             if self.bMove:
#                 text = str(round(self.baseLoc[0],2))
#             if self.bScale:
#                 text = str(round(self.getProfile().scale[0],2))
#             if self.bRotate:
#                 text = str(round(math.degrees(self.baseRotation[0]),0))
#             self.addDraw(event.mouse_x + shift,event.mouse_y-150 ,size,text,color)
#             shift += size * len(text) * 0.75
#             if self.bYAxis:
#                 color = getProp('highlightColor')
#             else:
#                 color = getProp('cursorColor')
#             text = 'Y :'
#             self.addDraw(event.mouse_x + shift,event.mouse_y-150 ,size,text,color)
#             shift += size * len(text) * 0.5
#             if self.bMove:
#                 text = str(round(self.baseLoc[1],2))
#             if self.bScale:
#                 text = str(round(self.getProfile().scale[1],2))
#             if self.bRotate:
#                 text = str(round(math.degrees(self.baseRotation[1]),0))
#             self.addDraw(event.mouse_x + shift,event.mouse_y-150 ,size,text,color)
#             shift += size * len(text) * 0.75
#             if self.bZAxis:
#                 color = getProp('highlightColor')
#             else:
#                 color = getProp('cursorColor')
#             text = 'Z :'
#             self.addDraw(event.mouse_x + shift,event.mouse_y-150 ,size,text,color)
#             shift += size * len(text) * 0.5
#             if self.bMove:
#                 text = str(round(self.baseLoc[2],2))
#             if self.bScale:
#                 text = str(round(self.getProfile().scale[2],2))
#             if self.bRotate:
#                 text = str(round(math.degrees(self.baseRotation[2]),0))
#             self.addDraw(event.mouse_x + shift,event.mouse_y-150 ,size,text,color)
#         color = getProp('cursorColor')
#         if self.bKeepSpline:
#             text = 'Result as Spline'
#         else:
#             text = 'Result as Mesh'
#         self.addDraw(event.mouse_x,event.mouse_y-150-30,size,text,color)
#         if self.bCap:
#             text = 'Cap On'
#         else:
#             text = 'Cap Off'
#         self.addDraw(event.mouse_x,event.mouse_y-150-60,size,text,color)
#         if self.b2D:
#             text = '3D Spline'
#         else:
#             text = '2D Spline'
#         self.addDraw(event.mouse_x,event.mouse_y-150-90,size,text,color)
    
#     def dropSelection(self):
#         for obj in bpy.context.selected_objects:
#             obj.select_set(False)

#     def getPath(self):
#         paths = []
#         for path in getObjectInCollection("Paths").children:
#             paths.append(path)
#         return paths
    
#     def getProfile(self):
#         for profile in getObjectInCollection("Profiles").children:
#             if profile.name == bpy.types.Scene.AQPipe_bevelProfile:
#                 return profile
#         return None
        
#     def processEvents(self,event):
#         #setting tools
#         if event.type == getProp('mKeep') and event.value == "PRESS" and self.bKeepSpline :
#             self.bKeepSpline = False
#         elif event.type == getProp('mKeep') and event.value == "PRESS" and not self.bKeepSpline :
#             self.bKeepSpline = True
#         if event.type == getProp('mScale') and event.value == "PRESS":
#             self.report({'INFO'}, 'Scale Active')
#             if self.bScale == False:
#                 self.getProfile().select_set(True) 
#                 bpy.context.view_layer.objects.active = self.getProfile()
#                 bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
#                 self.bScale = True
#                 self.bMove = False
#                 self.bRotate = False
#                 self.bXAxis = False
#                 self.bYAxis = False
#                 self.bZAxis = False
#             else:
#                 self.bScale = False
#                 self.bXAxis = False
#                 self.bYAxis = False
#                 self.bZAxis = False
#         if event.type == getProp('mMove') and event.value == "PRESS":
#             if self.bMove == False:
#                 self.report({'INFO'}, 'Move Active')
#                 #setting x-axis as default when move is active, since drag add to location is awkward with 3 axes
#                 self.getProfile().select_set(True) 
#                 bpy.context.view_layer.objects.active = self.getProfile()
#                 bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
#                 self.bXAxis = True
#                 self.bMove = True
#                 self.bScale = False
#                 self.bRotate = False
#                 self.bYAxis = False
#                 self.bZAxis = False
#             else:
#                 self.bMove = False
#                 self.bXAxis = False
#                 self.bYAxis = False
#                 self.bZAxis = False
#         if event.type == getProp('mRotate') and event.value == "PRESS":
#             self.report({'INFO'}, 'Rotate Active')
#             if self.bRotate == False:
#                 #setting x-axis as default when move is active, since drag rotate is awkward with 3 axes
#                 self.bXAxis = True
#                 self.bRotate = True
#                 self.bMove = False
#                 self.bScale = False
#                 self.bYAxis = False
#                 self.bZAxis = False
#             else:
#                 self.bRotate = False
#                 self.bXAxis = False
#                 self.bYAxis = False
#                 self.bZAxis = False
#         #setting axes
#         if event.type == getProp('mX') and event.value == "PRESS" and self.bXAxis==False:
#             self.report({'INFO'}, 'X Axis')
#             self.bXAxis = True
#             self.bYAxis = False
#             self.bZAxis = False
#         elif event.type == getProp('mX') and event.value == "PRESS" and self.bXAxis==True:
#             self.bXAxis = False
        
#         if event.type == getProp('mY') and event.value == "PRESS" and self.bYAxis==False:
#             self.report({'INFO'}, 'Y Axis')
#             self.bYAxis = True
#             self.bXAxis = False
#             self.bZAxis = False
#         elif event.type == getProp('mY') and event.value == "PRESS" and self.bYAxis==True:
#             self.bYAxis = False

#         if event.type == getProp('mZ') and event.value == "PRESS" and self.bZAxis==False:
#             self.report({'INFO'}, 'Z Axis')
#             self.bZAxis = True
#             self.bYAxis = False
#             self.bXAxis = False
#         elif event.type == getProp('mZ') and event.value == "PRESS" and self.bZAxis==True:
#             self.bZAxis = False
#         #adding transform
#         if (event.type == "WHEELUPMOUSE" or event.type == "WHEELDOWNMOUSE" or 'RIGHTMOUSE') and self.bRotate:
#             self.addRotation(event.type)
#         if (event.type == "WHEELUPMOUSE" or event.type == "WHEELDOWNMOUSE" or 'RIGHTMOUSE' ) and self.bMove:
#             self.addLocation(event.type)
#         if (event.type == "WHEELUPMOUSE" or event.type == "WHEELDOWNMOUSE" or 'RIGHTMOUSE' ) and self.bScale:
#             self.addScale(event.type)
#         if event.type == getProp('mCap') and event.value == 'PRESS' and self.bCap==False:
#             self.bCap=True
#             self.setCap()
#         elif event.type == getProp('mCap') and event.value == 'PRESS' and self.bCap==True:
#             self.bCap=False
#             self.setCap()
#         if event.type == getProp('m2D') and event.value == 'PRESS' and self.b2D==False:
#             self.b2D = True
#             self.set2D()
#         elif event.type == getProp('m2D') and event.value == 'PRESS' and self.b2D==True:
#             self.b2D = False
#             self.set2D()
            
#     def addScale(self,event):
#         if self.bScale:
#             if event == "WHEELUPMOUSE":
#                 if not self.bXAxis and not self.bYAxis and not self.bZAxis:
#                     self.getProfile().scale = getattr(self.getProfile(),'scale') + mathutils.Vector((0.1 , 0.1, 0.1 ))
#                 else:
#                     self.getProfile().scale = getattr(self.getProfile(),'scale') + mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis))) 
#             if event == "WHEELDOWNMOUSE":
#                 if not self.bXAxis and not self.bYAxis and not self.bZAxis:
#                     self.getProfile().scale = getattr(self.getProfile(),'scale') - mathutils.Vector((0.1 , 0.1, 0.1))
#                 else:
#                     self.getProfile().scale = getattr(self.getProfile(),'scale') - mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis)))
#             #scale exit with reverting scale
#             if event == 'RIGHTMOUSE':
#                 self.report({'INFO'}, 'Exit and Revert Scale')
#                 self.getProfile().scale = self.baseScale 
#             if event == 'ESC':
#                 self.report({'INFO'}, 'Exit and Revert Scale')
#                 self.getProfile().scale = self.baseScale 
#                 self.bScale = False

#     def addRotation(self,event):
#         if self.bRotate:
#             if event == "WHEELUPMOUSE":
#                 self.getProfile().rotation_euler[0] = self.getProfile().rotation_euler.x + math.radians(10)*int(self.bXAxis)
#                 self.getProfile().rotation_euler[1] = self.getProfile().rotation_euler.y + math.radians(10)*int(self.bYAxis)
#                 self.getProfile().rotation_euler[2] = self.getProfile().rotation_euler.z + math.radians(10)*int(self.bZAxis)
#                 self.baseRotation[0] += math.radians(10)*int(self.bXAxis)
#                 self.baseRotation[1] += math.radians(10)*int(self.bYAxis)
#                 self.baseRotation[2] += math.radians(10)*int(self.bZAxis)
#             if event == "WHEELDOWNMOUSE":
#                 self.getProfile().rotation_euler[0] = self.getProfile().rotation_euler.x + math.radians(-10)*int(self.bXAxis)
#                 self.getProfile().rotation_euler[1] = self.getProfile().rotation_euler.y + math.radians(-10)*int(self.bYAxis)
#                 self.getProfile().rotation_euler[2] = self.getProfile().rotation_euler.z + math.radians(-10)*int(self.bZAxis)
#                 self.baseRotation[0] += math.radians(-10)*int(self.bXAxis)
#                 self.baseRotation[1] += math.radians(-10)*int(self.bYAxis)
#                 self.baseRotation[2] += math.radians(-10)*int(self.bZAxis)
#             self.getProfile().select_set(True) 
#             bpy.context.view_layer.objects.active = self.getProfile()
#             bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
#             if event == 'RIGHTMOUSE':
#                 self.getProfile().rotation_euler[0] -= self.baseRotation[0] 
#                 self.getProfile().rotation_euler[1] -= self.baseRotation[1] 
#                 self.getProfile().rotation_euler[2] -= self.baseRotation[2]
#                 self.baseRotation = (0,0,0) 
#                 self.report({'INFO'}, 'Revert Rotation')
#             if event == 'ESC':
#                 self.getProfile().rotation_euler[0] -= self.baseRotation[0] 
#                 self.getProfile().rotation_euler[1] -= self.baseRotation[1] 
#                 self.getProfile().rotation_euler[2] -= self.baseRotation[2]
#                 self.baseRotation = (0,0,0) 
#                 self.report({'INFO'}, 'Exit and Revert Rotation')
#                 self.bRotate = False

#     def addLocation(self,event):
#         shift = mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis),0))
#         if event == "WHEELUPMOUSE" :
#             self.baseLoc += shift
#             for spline in self.getProfile().data.splines:
#                 for point in spline.points:
#                     point.co += shift
#         if event == "WHEELDOWNMOUSE":
#             self.baseLoc -= shift
#             for spline in self.getProfile().data.splines:
#                 for point in spline.points:
#                     point.co -= shift
#         if event == 'RIGHTMOUSE':
#             for spline in self.getProfile().data.splines:
#                 for point in spline.points:
#                     point.co -= self.baseLoc
#             self.baseLoc = mathutils.Vector((0.0,0.0,0.0,0.0))
#             self.report({'INFO'}, 'Revert Movement')
#         if event == 'ESC' :
#             for spline in self.getProfile().data.splines:
#                 for point in spline.points:
#                     point.co -= self.baseLoc
#             self.baseLoc = mathutils.Vector((0.0,0.0,0.0,0.0))
#             self.report({'INFO'}, 'Exit and Revert Movement')
#             self.bMove = False

#     def setCap(self):
#         if self.bCap == True:
#             for path in self.getPath():
#                 path.data.use_fill_caps = True
#             self.report({'INFO'},'Fill Caps On')
#         if self.bCap==False:
#             for path in self.getPath():
#                 path.data.use_fill_caps = False
#             self.report({'INFO'},'Fill Caps Off')
    
#     def set2D(self):
#         if self.b2D == True:
#             for path in self.getPath():
#                 path.data.dimensions = '2D'
#             self.report({'INFO'},'2D Spline')
#         if self.b2D==False:
#             for path in self.getPath():
#                 path.data.dimensions = '3D'
#             self.report({'INFO'},'3D Spline')
    
#     def convertPath(self):
#         curves = [] 
#         for path in  self.getPath():
#             if path.type == "MESH":
#                 path.select_set(True) 
#                 bpy.context.view_layer.objects.active = path
#                 bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
#         for path in self.getPath():
#             if path.type == "CURVE":
#                 curves.append(path)

#     def cancelSweep(self):
#         for path in self.getPath():
#             if path.type == 'CURVE':
#                 path.data.bevel_object = None
#                 path.select_set(True) 
#                 bpy.context.view_layer.objects.active = path
#                 bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
#         profile = self.getProfile()
#         if profile.type == 'CURVE':
#             profile.select_set(True) 
#             bpy.context.view_layer.objects.active = path
#             bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')

#     def execute(self,context):
        
#         bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
#         return {'FINISHED'}
#     def modal(self,context,event):
#         #redraw viewport       
#         context.area.tag_redraw()
#         self.processEvents(event)
#         kEvents = [getProp('mScale'),getProp('mRotate'),getProp('mMove'),getProp('mX'),getProp('mY'),getProp('mZ'),getProp('mCap'),getProp('mKeep'),'ESC','WHEELUPMOUSE','WHEELDOWNMOUSE','RIGHTMOUSE','SPACE',getProp('m2D')]
#         if event.type not in kEvents:
#             return {'PASS_THROUGH'}
#         if event.type =='ESC' and event.value=='PRESS' and not self.bRotate and not self.bMove and not self.bScale:
#             self.report({'INFO'}, 'Cancelled')
#             bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
#             self.cancelSweep()
#             return {'CANCELLED'}
#         if event.type == "SPACE":
            
#             self.report({'INFO'}, 'Finished')
#             self.dropSelection()
#             if not self.bKeepSpline:
#                 for path in self.getPath():
#                     if path.type == 'CURVE':
#                         path.select_set(True) 
#                         bpy.context.view_layer.objects.active = path
#                         bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
#                         path.parent = None
#                     #moving object to default collection
#                     for col in path.users_collection:
#                         if col.name == "AProfiler":
#                             col.objects.unlink(path)
#                     bpy.context.collection.objects.link(path)
            
#             bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
#             return {'FINISHED'}

#         return {'RUNNING_MODAL'}
#     def invoke(self,context,event):
#         TooltipText ["handler"] = bpy.types.SpaceView3D.draw_handler_add(self.drawTooltips,(context,event), 'WINDOW', 'POST_PIXEL')
#         self.bCap = getProp('bDefCap')
#         self.bKeepSpline = getProp('bDefKeep')
#         self.baseScale = self.getProfile().scale
#         bevelProfile = None
#         self.convertPath()
#         if bpy.types.Scene.AQPipe_bevelProfile != "None":
#             for profile in getObjectInCollection('Profiles').children:
#                 if profile.name == bpy.types.Scene.AQPipe_bevelProfile:
#                     if profile.type == "MESH":
#                         profile.select_set(True) 
#                         bpy.context.view_layer.objects.active = profile
#                         bpy.ops.object.convert('INVOKE_DEFAULT', target='CURVE')
#                     bevelProfile = profile
#             for path in getObjectInCollection('Paths').children:
#                 path.data.bevel_object = bevelProfile
#             context.window_manager.modal_handler_add(self) 
#         return {'RUNNING_MODAL'}

class AProfiler_Menu(bpy.types.Menu):
    bl_label = "Profiler"
    bl_idname = "VIEW3D_MT_Profiler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self,context):
        layout = self.layout
        cColumn = layout.column()
        if context.mode == 'EDIT_MESH':
            cColumn.operator('object.aprofiler_createcurve',text='Create Path').eAction = 'PATH'
            cColumn.operator('object.aprofiler_createcurve',text='Create Profile').eAction = 'PROFILE'
        cColumn.operator('object.aprofiler_createcurve',text='Sweep Profile').eAction = 'SWEEP'
        cColumn.operator('object.aprofiler_createcurve',text='Sweep Profile ADV').eAction = 'SWEEPADV'
        cColumn.separator(factor=1.0)
        # if len(getObjectInCollection('Profiles').children)>0 and len(getObjectInCollection('Paths').children)>0 and context.mode == 'OBJECT':
        #     cColumn.operator('object.aprofiler_sweepprofile')
        #     cColumn.separator(factor=1.0)
        # elif len(getObjectInCollection('Profiles').children)>0 and (len(getObjectInCollection('Paths').children)>0 or bpy.context.scene.statistics(bpy.context.view_layer).split("|")[2].split(':')[1].split('/')[0] != '0' and context.mode == 'EDIT_MESH' ):
        #     cColumn.operator('object.aprofiler_sweepprofile')
        #     cColumn.separator(factor=1.0)
        # cColumn.operator('object.aprofiler_addoptions')

def rmbMenu(self,context):
    layout = self.layout
    sColumn = layout.column()
    sColumn.menu('VIEW3D_MT_Profiler',text='A*Profiler',icon='MOD_REMESH')

def register():
    bpy.utils.register_class(AProfiler_CreateCurve)
    bpy.utils.register_class(AProfiler_Menu)
    bpy.utils.register_class(AProfiler_ADV)
    #bpy.types.Scene.AQPipe_bevelProfile = bpy.props.StringProperty(default="None")
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(rmbMenu)
    bpy.types.VIEW3D_MT_object_context_menu.append(rmbMenu)
    #bpy.utils.register_class(AProfilerPreferences)
    #bpy.utils.register_class(AProfiler_MakeProfile)
    #bpy.utils.register_class(AProfiler_MakePath)
    #bpy.utils.register_class(AProfiler_SweepProfile)
    #bpy.utils.register_class(AProfiler_AdditionalOptions)
    #bpy.utils.register_class(AProfiler_FlushProfiles)
    #bpy.utils.register_class(AProfiler_FlushPaths)
    #bpy.utils.register_class(AProfiler_CleanUp)
    #bpy.utils.register_class(AProfiler_PostEdit)
    
    
def unregister():
    #del bpy.types.Scene.AQPipe_bevelProfile
    bpy.utils.unregister_class(AProfiler_CreateCurve)
    bpy.utils.unregister_class(AProfiler_Menu)
    bpy.utils.unregister_class(AProfiler_ADV)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(rmbMenu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(rmbMenu)
    #bpy.utils.unregister_class(AProfilerPreferences)
    #bpy.utils.unregister_class(AProfiler_MakeProfile)
    #bpy.utils.unregister_class(AProfiler_MakePath)
    #bpy.utils.unregister_class(AProfiler_SweepProfile)
    #bpy.utils.unregister_class(AProfiler_AdditionalOptions)
    #bpy.utils.unregister_class(AProfiler_FlushProfiles)
    #bpy.utils.unregister_class(AProfiler_FlushPaths)
    #bpy.utils.unregister_class(AProfiler_CleanUp)
    #bpy.utils.unregister_class(AProfiler_PostEdit)
    
