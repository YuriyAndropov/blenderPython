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

def getPath():
    #check the meshes and remove selection from main mesh
    for object in bpy.context.selected_objects:
        if object == bpy.context.active_object:
            data = object.data
            bm = bmesh.from_edit_mesh(data)
            for edge in bm.edges:
                edge.select_set(False)
            bmesh.update_edit_mesh(data,False)
        #if bpy.context.scene.tool_settings.mesh_select_mode[1]==True:
                    #create a new mesh
                    #newMesh = bpy.data.meshes.new('emptyMesh')
                    #newobjObj = bpy.data.objects.new("object_name", emptyMesh)
                    #link to collection
                    #bm to mesh
                    #mesh->bpy.ops.object.convert(target='MESH', keep_original=False)
