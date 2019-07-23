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
        bpy.ops.object.aqpipe_postedit('INVOKE_DEFAULT')
        return {'INTERFACE'}

    def invoke(self,context,event):
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

def draw_callback_px(self,context):
        width = bpy.context.area.width
        height = bpy.context.area.height

        blf.position(font_id, width/2,height/2, 0)
        blf.size(font_id, 52, 72)
        blf.color(font_id, 1, 1, 1, 1)
        blf.draw(font_id, 'test')

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
#TODO add abort with profile transform reverting to original values
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
    #TODO optimize

    def remap(self,value, low1, high1, low2, high2):
        return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

    def addDraw(self,x,y,size,text,color):
        blf.position(font_id, x, y, 0)
        blf.size(font_id, size, 72)
        blf.color(font_id, color[0], color[1], color[2], 1)
        blf.draw(font_id, text)

    def drawTooltips(self,context,event):
        tWidth = context.area.regions[2].width
        width = context.area.width
        height = context.area.height
        color = (1,0.4,0.2)
        size = 25
        text = 'Sweep Profile Mode'
        self.addDraw(width/2-tWidth - len(text)/2*21,height-50,size,text,color)
        text = 'Hotkeys :'
        self.addDraw(tWidth,height/2+63*2,size,text,color)
        size = 21
        text = 'M : Move'
        self.addDraw(tWidth+size,height/2+42*1.5,size,text,color)
        text = 'R : Rotate'
        self.addDraw(tWidth+size,height/2+21*1.5,size,text,color)
        text = 'S : Scale'
        self.addDraw(tWidth+size,height/2,size,text,color)
        
        text = 'X : X Axis'
        self.addDraw(tWidth+size,height/2 - 21 *1.5-20,size,text,color)
        text = 'Y : Y Axis'
        self.addDraw(tWidth+size,height/2 -42 *1.5 -20,size,text,color)
        text = 'Z : Z Axis'
        self.addDraw(tWidth+size,height/2 -63 *1.5 -20,size,text,color)
        text = 'C : Cap Ends Toggle'
        self.addDraw(tWidth+size,height/2 -84 *1.5 -20,size,text,color)
        text = 'Q : Leave as Curve Toggle'
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

    def setTool(self,event):
        if event.type == "S" and event.value == "PRESS":
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
        if event.type == "M" and event.value == "PRESS":
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
        if event.type == "R" and event.value == "PRESS":
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
        if event.type == 'C' and event.value == 'PRESS':
            if not self.bCap:
                self.report({'INFO'},'Fill Caps')
                self.bCap=True
            else:
                self.bCap=False
    # set axes on key press
    def setAxis(self,event):
        if self.bScale or self.bMove or self.bRotate:
            if event.type == "X" and event.value == "PRESS" and self.bXAxis==False:
                self.report({'INFO'}, 'X Axis')
                self.bXAxis = True
                self.bYAxis = False
                self.bZAxis = False
            elif event.type == "X" and event.value == "PRESS" and self.bXAxis==True:
                self.bXAxis = False

            if event.type == "Y" and event.value == "PRESS" and self.bYAxis==False:
                self.report({'INFO'}, 'Y Axis')
                self.bYAxis = True
                self.bXAxis = False
                self.bZAxis = False
            elif event.type == "Y" and event.value == "PRESS" and self.bYAxis==True:
                self.bYAxis = False

            if event.type == "Z" and event.value == "PRESS" and self.bZAxis==False:
                self.report({'INFO'}, 'Z Axis')
                self.bZAxis = True
                self.bYAxis = False
                self.bXAxis = False
            elif event.type == "Z" and event.value == "PRESS" and self.bZAxis==True:
                self.bZAxis = False
    #TODO change baseScale
    def addScale(self,event):
        if self.bScale:
            if event.type == "WHEELUPMOUSE":
                if not self.bXAxis and not self.bYAxis and not self.bZAxis:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') + mathutils.Vector((0.1 , 0.1, 0.1 ))
                else:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') + mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis))) 
            if event.type == "WHEELDOWNMOUSE":
                if not self.bXAxis and not self.bYAxis and not self.bZAxis:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') - mathutils.Vector((0.1 , 0.1, 0.1))
                else:
                    self.getProfile().scale = getattr(self.getProfile(),'scale') - mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis)))
            #scale exit with reverting scale
            if event.type == 'RIGHTMOUSE' and self.bScale :
                self.getProfile().scale = self.baseScale -1

    def addRotation(self,event):
        if self.bRotate:
            if event.type == "WHEELUPMOUSE":
                self.getProfile().rotation_euler[0] = self.getProfile().rotation_euler.x + math.radians(10)*int(self.bXAxis)
                self.getProfile().rotation_euler[1] = self.getProfile().rotation_euler.y + math.radians(10)*int(self.bYAxis)
                self.getProfile().rotation_euler[2] = self.getProfile().rotation_euler.z + math.radians(10)*int(self.bZAxis)
                self.baseRotation[0] += math.radians(10)*int(self.bXAxis)
                self.baseRotation[1] += math.radians(10)*int(self.bYAxis)
                self.baseRotation[2] += math.radians(10)*int(self.bZAxis)
            if event.type == "WHEELDOWNMOUSE":
                self.getProfile().rotation_euler[0] = self.getProfile().rotation_euler.x + math.radians(-10)*int(self.bXAxis)
                self.getProfile().rotation_euler[1] = self.getProfile().rotation_euler.y + math.radians(-10)*int(self.bYAxis)
                self.getProfile().rotation_euler[2] = self.getProfile().rotation_euler.z + math.radians(-10)*int(self.bZAxis)
                self.baseRotation[0] += math.radians(-10)*int(self.bXAxis)
                self.baseRotation[1] += math.radians(-10)*int(self.bYAxis)
                self.baseRotation[2] += math.radians(-10)*int(self.bZAxis)
            self.getProfile().select_set(True) 
            bpy.context.view_layer.objects.active = self.getProfile()
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            if event.type == 'RIGHTMOUSE' and self.bRotate :
                self.getProfile().rotation_euler[0] -= self.baseRotation[0] 
                self.getProfile().rotation_euler[1] -= self.baseRotation[1] 
                self.getProfile().rotation_euler[2] -= self.baseRotation[2]
                self.baseRotation = (0,0,0) 

    def addLocation(self,event):
        if self.bMove:
            shift = mathutils.Vector((0.1 * int(self.bXAxis), 0.1 * int(self.bYAxis), 0.1 * int(self.bZAxis),0))
            if event.type == "WHEELUPMOUSE" :
                self.baseLoc += shift
                for spline in self.getProfile().data.splines:
                    for point in spline.points:
                        point.co += shift
            if event.type == "WHEELDOWNMOUSE":
                self.baseLoc -= shift
                for spline in self.getProfile().data.splines:
                    for point in spline.points:
                        point.co -= shift
            if event.type == 'RIGHTMOUSE' and self.bMove :
                for spline in self.getProfile().data.splines:
                    for point in spline.points:
                        point.co -= self.baseLoc
                self.baseLoc = mathutils.Vector((0.0,0.0,0.0,0.0))

    def setAdditionalOptions(self):
        if self.bCap:
            for path in self.getPath():
                path.data.use_fill_caps = True
        if not self.bCap:
            for path in self.getPath():
                path.daya.use_fill_caps = False
    
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

    def execute(self,context):
        bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
        return {'FINISHED'}
    def modal(self,context,event):
        
        #TODO add all modal events to dict, so I don't have to write exeption for every case
        #TODO add keys to addon properties
        qEvents = {'S','M','ESC','SPACE','WHEELUPMOUSE','WHEELDOWNMOUSE'}
        #redraw viewport       
        context.area.tag_redraw()
        self.setTool(event)
        self.addScale(event)
        self.addRotation(event)
        self.addLocation(event)
        self.setAxis(event)
        self.setAdditionalOptions()
        if event.type =='ESC' and event.value=='PRESS':
            self.report({'INFO'}, 'Cancelled')
            bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
            return {'CANCELLED'}
        if event.type == "SPACE":
            self.report({'INFO'}, 'Finished')
            bpy.types.SpaceView3D.draw_handler_remove(TooltipText ["handler"],'WINDOW')
            return {'FINISHED'}
        #ignoring left and middle mouse for navigation
        if (event.type == 'LEFTMOUSE' and event.value == "PRESS") :
            return {'PASS_THROUGH'}
        if event.type == 'MIDDLEMOUSE' and event.value == "PRESS":
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}
    def invoke(self,context,event):
        TooltipText ["handler"] = bpy.types.SpaceView3D.draw_handler_add(self.drawTooltips,(context,event), 'WINDOW', 'POST_PIXEL')
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
                print(path.data.bevel_object)
            context.window_manager.modal_handler_add(self) 
        return {'RUNNING_MODAL'}

def rmbMenu(self,context):
    layout = self.layout

    layout.operator('object.aqpipe_postedit',text='Sweep')

def register():
    bpy.types.Scene.AQPipe_bevelProfile = bpy.props.StringProperty(default="None")
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(rmbMenu)
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
    
