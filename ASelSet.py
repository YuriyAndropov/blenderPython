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
    "category": "Mesh"
}

import bpy

class ASel_Set(bpy.types.Operator):
    bl_idname = "object.asel_set"
    bl_label = "A* Add To Selection Set"
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
                    names = []
                    name = group.name
                    icon = 'GROUP_VERTEX'
                    for item in sets:
                        names.append(item[2])
                    if name not in names:
                        sets.append((str(id),name,name,icon,id))
                        id+=1
        return sets

    def updateEnum(self,context):
        self.name = self.objSets
        return None

    bSet: bpy.props.BoolProperty(default=True,name='Set',update=updateSet)
    bAdd: bpy.props.BoolProperty(default=False,name='Add',update=updateAdd)
    bSub: bpy.props.BoolProperty(default=False,name='Sub',update=updateSub)
    objSets:bpy.props.EnumProperty(name="Objects Sets",items=updateList)
    newSet: bpy.props.StringProperty(default='NewSet')

    def draw(self,context):
        layout = self.layout
        setBox = layout.box()
        sRow = setBox.row(align=True)
        nRow = setBox.row(align=True)
        bRow = setBox.row(align=True)

        sRow.prop(self,"objSets")
        nRow.prop(self,'newSet')
        bRow.prop(self,"bSet")
        bRow.prop(self,"bAdd")
        bRow.prop(self,"bSub")

    def invoke(self,context,event):
        if bpy.context.mode != "EDIT_MESH":
            self.report({'WARNING'},'Invalid mode')
            return{'CANCELLED'}
        elif bpy.context.scene.statistics(bpy.context.view_layer).split("|")[1].split(':')[1].split("/")[0]=='0':
            self.report({'WARNING'},'Nothing is selected')
            return{'CANCELLED'}
        self.updateList(context)
        return context.window_manager.invoke_props_dialog(self, width = 200)
    def execute(self,context):
        #get enum items
        sets = self.updateList(context)
        #get group name
        if self.objSets == '0':
            name = self.newSet
        else:
            for item in sets:
                if item[0]==self.objSets:
                    name = item[1]
        for obj in bpy.context.selected_objects:
            obj.update_from_editmode()
            #get selected vert ID
            verts = []
            allVerts = []
            data = obj.data
            vGroup = None
            for vert in data.vertices:
                allVerts.append(vert.index)
                if vert.select:
                    verts.append(vert.index)
            for group in obj.vertex_groups:
                if group.name == name:
                    vGroup = group
                    break
            if vGroup == None:
                vGroup = obj.vertex_groups.new(name=self.newSet)
            #adding to group is possible only in object mode
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            if self.bSet:
                vGroup.remove(allVerts)
                vGroup.add(verts,1,'REPLACE')
            elif self.bAdd:
                vGroup.add(verts,1,'ADD')
            elif self.bSub:
                vGroup.remove(verts)
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        return {'FINISHED'}

class ASel_Get(bpy.types.Operator):
    bl_idname = "object.asel_get"
    bl_label = "A* Recall Selection Set"
    bl_options = {'REGISTER', 'UNDO'}

    def updateGet(self,context):
        if self.bGet:
            self.bAdd = False
            self.bSub = False
        return None
    
    def updateAdd(self,context):
        if self.bAdd :
            self.bGet = False
            self.bSub = False
        return None

    def updateSub(self,context):
        if self.bSub:
            self.bAdd = False
            self.bGet = False
        return None
    
    def updateList(self,context):
        sets = []
        id = 1
        for obj in bpy.context.selected_objects:
            for group in obj.vertex_groups:
                if group.name != None:
                    names = []
                    name = group.name
                    icon = 'GROUP_VERTEX'
                    for item in sets:
                        names.append(item[2])
                    if name not in names:
                        sets.append((str(id),name,name,icon,id))
                        id+=1
        return sets

    bGet: bpy.props.BoolProperty(default=True,name='Get',update=updateGet)
    bAdd: bpy.props.BoolProperty(default=False,name='Add',update=updateAdd)
    bSub: bpy.props.BoolProperty(default=False,name='Sub',update=updateSub)
    objSets:bpy.props.EnumProperty(name="Objects Sets",items=updateList)

    def draw(self,context):
        layout = self.layout
        setBox = layout.box()
        sRow = setBox.row(align=True)
        nRow = setBox.row(align=True)
        bRow = setBox.row(align=True)

        sRow.prop(self,"objSets")
        bRow.prop(self,"bGet")
        bRow.prop(self,"bAdd")
        bRow.prop(self,"bSub")

    def invoke(self,context,event):
        if bpy.context.mode != "EDIT_MESH":
            self.report({'WARNING'},'Invalid mode')
            return{'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width = 200)
    
    def execute(self,context):
        sets = self.updateList(context)
        for item in sets:
            if item[0]==self.objSets:
                name = item[2]
        if self.bGet:
            bpy.ops.mesh.select_all(action='DESELECT')
        for obj in bpy.context.selected_objects:
            data = obj.data
            vGroup = None
            for v_group in obj.vertex_groups:
                if v_group.name == name:
                    vGroup = v_group
            if vGroup != None:
                bpy.context.view_layer.objects.active = obj
                obj.vertex_groups.active_index = vGroup.index
                if self.bGet:
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.object.vertex_group_select()
                if self.bAdd:
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.object.vertex_group_select()
                if self.bSub:
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.object.vertex_group_deselect()
        return {'FINISHED'}

def contMenu(self,context):
    layout = self.layout
    layout.separator()
    sColumn = layout.column()
    layout.separator()
    layout.operator_context = 'INVOKE_DEFAULT'
    sColumn.operator('object.asel_set',text='Add To Selection Set')
    sColumn.operator('object.asel_get',text='Recall Selection Set')


def register():
    bpy.utils.register_class(ASel_Set)
    bpy.utils.register_class(ASel_Get)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(contMenu)
    
def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(contMenu)
    bpy.utils.unregister_class(ASel_Set)
    bpy.utils.unregister_class(ASel_Get)
    
    