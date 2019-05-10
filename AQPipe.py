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
    return None  

#check if there is already a collection with specified name
def checkCollections(name):
    for collection in bpy.data.collections:
        if collection.name == name:
            return True
            break
    return False

#get new object from edge selection
def objectFromPath():
    objects = bpy.context.selected_objects
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
        bpy.context.collection.objects.link(newObj)
        newObj.location = object.location
        bmesh.types.BMesh.free
        name = "QProfile"
        if checkCollections(name) == True:
            getCollection(name).objects.link(newObj)
        else:
             newCol = bpy.data.collections.new(name)
             newCol.objects.link(newObj)
   

class AQPipe_MakeProfile(bpy.types.Operator):
    bl_idname = "object.aqpipe_makeprofile"
    bl_label = "AQPipe Make Profile"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        objectFromPath()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AQPipe_MakeProfile)
def unregister():
    bpy.utils.unregister_class(AQPipe_MakeProfile)