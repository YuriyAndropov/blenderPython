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
    "name": "A* Selection Sets ",
    "description": "Quick Selection Sets",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": '',
    "category": "3D View"
}

import bpy

selSets = []


# def updateList(self,context):
#     del listItems[1:]
#     id = 1
#     for set in selSets:
#         if set != None:
#             name = set.name
#             des = set.name
#             icon = GROUP_VERTEX
#             if (str(id),name,des,icon,id) not in listItems:
#                 listItems.append((name,name,des,icon,id))
#         id+=1
#     return listItems

def getSets():
    for object in bpy.context.selected_objects:
        if object.vertex_groups.name not in selSets:
            selSets.append(object.vertex_groups.name)

class ASel_Set(bpy.types.Operator):
    bl_idname = "object.asel_set"
    bl_label = "ASelSet Set"
    bl_options = {'REGISTER', 'UNDO'}

    def updateSet(self,context):
        if self.bSet:
            self.bAdd = False
            self.bSub = False
        return None
    
    def updateAdd(self,context):
        if self.bAdd :
            self.bSet = False
            self.bSub = False
        return None
    def updateSub(self,context):
        if self.bSub:
            self.bAdd = False
            self.bSet = False
        return None
    
    def updateList(self,context):
        sets = [("0","New Set","Add New Set",'GROUP_VERTEX',0)]
        id = 1
        for obj in bpy.context.selected_objects:
            for group in obj.vertex_groups:
                if group.name != None:
                    name = group.name
                    icon = 'GROUP_VERTEX'
                    if (str(id),name,name,icon,id) not in sets:
                        sets.append((str(id),name,name,icon,id))
                        id+=1
        return sets

    bSet: bpy.props.BoolProperty(default=True,name='Set',update=updateSet)
    bAdd: bpy.props.BoolProperty(default=False,name='Add',update=updateAdd)
    bSub: bpy.props.BoolProperty(default=False,name='Sub',update=updateSub)
    objSets:bpy.props.EnumProperty(name="Objects Sets",items=updateList)

    def draw(self,context):
        layout = self.layout
        setBox = layout.box()
        sRow = setBox.row(align=True)
        bRow = setBox.row(align=True)

        sRow.prop(self,"objSets")
        bRow.prop(self,"bSet")
        bRow.prop(self,"bAdd")
        bRow.prop(self,"bSub")

    def invoke(self,context,event):
        self.updateList(context)
        return context.window_manager.invoke_props_dialog(self, width = 200)
    def execute(self,context):
        return {'FINISHED'}

    



def register():
    bpy.utils.register_class(ASel_Set)
def unregister():
     bpy.utils.unregister_class(ASel_Set)