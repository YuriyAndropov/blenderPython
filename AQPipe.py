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


#get collection 
def getCollection(name):
    for collection in bpy.data.collections:
        if collection.name == name:
            return collection
            break
   

#check if there is already a collection with specified name
def checkCollections(value):
    for collection in bpy.data.collections:
        if collection.name == value:
            return True
            break
    return False

#get new object from edge selection and add it to collection
#TODO move collection name to propperies
#TODO add object and mode check
def objectFromPath():
    objects = bpy.context.selected_objects
    cName = "QProfile"
    col = None
    if checkCollections(cName) == True:
        col = getCollection(cName)
    else:
        col = bpy.data.collections.new(cName)
        bpy.context.scene.collection.children.link(col)
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
        newObj = bpy.data.objects.new("Profile", newMesh)
        col.objects.link(newObj)
        newObj.location = object.location
        bmesh.types.BMesh.free
        
        
#TODO add object check
def convertToCurve():
    for object in getCollection("QProfile").objects:
        print(object.name)
        #bpy.context.scene.objects.active = object
        #object.select = True
        #bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        #bpy.ops.object.convert('EXECUTE_DEFAULT', target='Curve')

class AQPipe_MakeProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_makeprofile"
    bl_label = "AQPipe Make Profile"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        objectFromPath()
        convertToCurve()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AQPipe_MakeProfile)
def unregister():
    bpy.utils.unregister_class(AQPipe_MakeProfile)