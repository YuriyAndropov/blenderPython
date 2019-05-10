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

newMesh = bpy.data.meshes.new("PipeMesh")
newObj = bpy.data.objects.new("QPipe", newMesh)
newObj.location = (0,0,0)
bpy.context.collection.objects.link(newObj)

#check if there is already a collection with specified name
def checkCollections(name):
    for collection in bpy.data.collections:
        if collection.name == name:
            return True
            break

#add new collection if check is false
def addCollection(name):
    if checkCollections(name)==False:
        newCol = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(newCol)

#get curve profile from edge selection
def getProfile():
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
        newMesh = bpy.data.meshes.new("PipeMesh")
        dupe.to_mesh(newMesh)
        newObj = bpy.data.objects.new("object_name", newMesh)
        bpy.context.collection.objects.link(newObj)
        bmesh.types.BMesh.free
            
        bpy.ops.object.mode_set(mode='OBJECT')
        for object in objects:
            object.select_set(False)
        bpy.context.view_layer.objects.active = newObj
        newObj.select_set(True)
        bpy.ops.object.convert('EXEC_DEFAULT',target='CURVE')
       