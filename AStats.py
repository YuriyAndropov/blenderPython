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
    "name": "A* Statistics",
    "description": "Show Stats in Viewport",
    "author": "A*",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "https://youtu.be/06zMRZzpbZc",
    "category": "3D View"
}

import bpy
import blf
import bmesh
StatsText = {
    "font_id": 0,
    "handler": None,
}
font_id = 0
objectName = ""
totalComponents = [0,0,0]
totalSelected = [0,0,0]
names = ["Verts : ", "Edges : ", "Faces : ","Tris :"]
globalnames = ["Objects :","Faces :","Edges :","Verts :"]
globalValues = [0,0,0,0]


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    #TODO Add UV Channel Name check,snapping state
    #Location properties
    iLocX:bpy.props.IntProperty(name="X",description="Icon X position", default=410,min=0,max=1000)
    iLocY:bpy.props.IntProperty(name="Y",description="Icon Y position", default=986,min=0,max=1000)
    sLocX:bpy.props.IntProperty(name="X",description="Relative X position", default=90,min=0,max=1000)
    sLocY:bpy.props.IntProperty(name="Y",description="Relative Y position", default=900,min=0,max=1000)
    gLocX:bpy.props.IntProperty(name="X",description="Relative X position", default=910,min=0,max=1000)
    gLocY:bpy.props.IntProperty(name="Y",description="Relative Y position", default=70,min=0,max=1000)
    shOffsetX:bpy.props.IntProperty(name="X",description="X shadow offset ", default=1,min=-1000,max=1000)
    shOffsetY:bpy.props.IntProperty(name="Y",description="X shadow offset ", default=-1,min=-1000,max=1000)
    #sFontSize Properties
    sFontSize:bpy.props.IntProperty(name="Size",description="Font size", default=18)
    gFontSize:bpy.props.IntProperty(name="Size",description="Font size", default=16)
    mFontSize:bpy.props.IntProperty(name="Size",description="Font size", default=16)
    #Color Properties
    gStatColor:bpy.props.FloatVectorProperty(name="Color",description="Color", default=(1.0,1.0,1.0),subtype='COLOR')
    sStatColor:bpy.props.FloatVectorProperty(name="Color",description="Color", default=(1.0,1.0,1.0),subtype='COLOR')
    highlightColor:bpy.props.FloatVectorProperty(name="Color",description="Highlight color", default=(0.0,1.0,0.0),subtype='COLOR')
    shadowColor:bpy.props.FloatVectorProperty(name="Color",description="Color", default=(0.0,0.0,0.0),subtype='COLOR')
    matColor:bpy.props.FloatVectorProperty(name="Color",description="Color", default=(0.5,0.5,0.5),subtype='COLOR')
    #Switches
    bDispIcon: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispGlobal: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispShadow: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispSelected: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispActive: bpy.props.BoolProperty(name="Selection Mode Only Display",description="Switch for showing stats based on selection type(ie only verts)", default=False)
    bShowMats: bpy.props.BoolProperty(name="On/Off",description="Switch for showing names of selected materials", default=True)
    bNameGrouping: bpy.props.BoolProperty(name="Name Grouping",description="Switch for name grouping", default=True)
    bFontScaling: bpy.props.BoolProperty(name="Font Sclaing",description="Switch for font scaling", default=True)
    bCalcTris: bpy.props.BoolProperty(name="Calculate Tris",description="Switch for calculating triangles", default=True)
    bDrawFaces: bpy.props.BoolProperty(name="Draw Faces",description="Switch for drawing faces", default=True)
    bDrawEdges: bpy.props.BoolProperty(name="Draw Edges",description="Switch for drawing edges", default=True)
    bDrawVerts: bpy.props.BoolProperty(name="Draw Verts",description="Switch for drawing verts", default=True)
    #Additional Properties
    groupNames: bpy.props.IntProperty(name="Group names after",description="When the number of of selected object is bigger than the value it will be replaced by Number of Objects", default=2)

    def draw(self, context):
        layout = self.layout
        #Icon Box
        iconBox = layout.box()
        iconBox.label(text="3DView Icon Options")
        iRow = iconBox.row(align=True)
        iRow.prop(self,"bDispIcon")
        iRow.prop(self,"iLocX")
        iRow.prop(self,"iLocY")
        #GlobalStats Box
        globalStatBox = layout.box()
        globalStatBox.label(text="Global Stats Options")
        GRow = globalStatBox.row(align=True)
        GRow.prop(self, "bDispGlobal")
        GRow.prop(self, "gFontSize")
        GRow.prop(self, "gLocX")
        GRow.prop(self, "gLocY")
        GRow.prop(self, "gStatColor")
        globalStatBox.label(text="Statistics for all visible objects")
        #SelectedStats Box
        SelectedStatBox = layout.box()
        SelectedStatBox.label(text="Selected Objects Stats Options")
        SRow = SelectedStatBox.row(align=True)
        BRow = SelectedStatBox.row(align=True)
        ORow = SelectedStatBox.row(align=True)
        SRow.prop(self, "bDispSelected")
        SRow.prop(self, "sFontSize")
        SRow.prop(self, "sLocX")
        SRow.prop(self, "sLocY")
        SRow.prop(self, "sStatColor")
        SRow.prop(self,"highlightColor" )
        BRow.prop(self,'bCalcTris')
        BRow.prop(self,'bDrawFaces')
        BRow.prop(self,'bDrawEdges')
        BRow.prop(self,'bDrawVerts')
        ORow.prop(self,'bDispActive')
        SelectedStatBox.label(text="Statistics for all selected objects")
        #Box for additional properties
        AddProp = layout.box()
        AddProp.label(text="Additional Options")
        ARow = AddProp.row(align=True)
        ShadowRow = AddProp.row(align=True)
        MatRow = AddProp.row(align=True)
        MatRow.label(text="Material Options")
        ARow.prop(self,"bFontScaling" )
        ARow.prop(self, "bNameGrouping")
        ARow.prop(self, "groupNames")
        ShadowRow.label(text="Shadow Options")
        ShadowRow.prop(self, "bDispShadow")
        ShadowRow.prop(self, "shOffsetX")
        ShadowRow.prop(self, "shOffsetY")
        ShadowRow.prop(self, "shadowColor")
        MatRow.prop(self,"bShowMats")
        MatRow.prop(self,"mFontSize")
        MatRow.prop(self,"matColor")
#TODO Finish popup menu

class AStats_GizmoMenu(bpy.types.Operator):
    bl_idname = "view3d.astats_gizmomenu"
    bl_label = "AStats 3DView Menu"
    bl_options = {'REGISTER', 'UNDO'}

    def updateDispGlobal(self,context):
        setValue('bDispGlobal',self.bDispGlobalMenu)
        return None
    
    def updateDispSelected(self,context):
        setValue('bDispSelected',self.bDispSelectedMenu)
        return None
    
    def updateDispFaces(self,context):
        setValue('bDrawFaces',self.bDrawFacesMenu)
        return None

    def updateDispEdges(self,context):
        setValue('bDrawEdges',self.bDrawEdgesMenu)
        return None
    
    def updateDispVerts(self,context):
        setValue('bDrawVerts',self.bDrawVertsMenu)
        return None

    def updateDispMats(self,context):
        setValue('bShowMats',self.bShowMatsMenu)
        return None

    def updateDispActive(self,context):
        setValue('bDispActive',self.bDispActiveMenu)
        return None


    bDispGlobalMenu: bpy.props.BoolProperty(name="Display Global Stats",default = True,update=updateDispGlobal)
    bDispSelectedMenu: bpy.props.BoolProperty(name="Display Selected Stats",default = True,update=updateDispSelected)
    bDrawFacesMenu: bpy.props.BoolProperty(name="Draw Faces",description="Switch for drawing faces", default=True,update=updateDispFaces)
    bDrawEdgesMenu: bpy.props.BoolProperty(name="Draw Edges",description="Switch for drawing edges", default=True,update=updateDispEdges)
    bDrawVertsMenu: bpy.props.BoolProperty(name="Draw Verts",description="Switch for drawing verts", default=True,update=updateDispVerts)
    bShowMatsMenu: bpy.props.BoolProperty(name="Draw Materials",description="Switch for showing names of selected materials", default=True,update=updateDispMats)
    bDispActiveMenu: bpy.props.BoolProperty(name="Draw Selected Mode",description="Switch for showing stats based on selection type(ie only verts)", default=False,update=updateDispActive)
    def draw(self,context):
        layout = self.layout
        
        gSwitches = layout.box()
        gRow = gSwitches.column(align=True)
        gRow.prop(self,"bDispGlobalMenu")
        sSwitches = layout.box()
        sRow = sSwitches.column(align=True)
              
        sRow.prop(self,"bDispSelectedMenu")
        if self.bDispSelectedMenu:
            compSwitches = layout.box()
            sCol = compSwitches.column()
            sCol.prop(self,"bDrawFacesMenu")
            sCol.prop(self,"bDrawEdgesMenu")
            sCol.prop(self,"bDrawVertsMenu")
            sCol.prop(self,"bShowMatsMenu")
            sCol.prop(self,"bDispActiveMenu")

        

    def execute(self,context):
        return {'FINISHED'}

    def invoke(self, context, event):
        self.bDispGlobalMenu = getValue('bDispGlobal')
        self.bDispSelectedMenu = getValue('bDispSelected')
        return context.window_manager.invoke_popup(self,width=200)

#TODO change to menu
class AStatsButton(bpy.types.GizmoGroup):
    bl_idname = "view3d.astats_button"
    bl_label = "AStats 3D View Button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}
    

    def draw_prepare(self,context):
        width = bpy.context.area.width
        height = bpy.context.area.height
        for gizmo in self.gizmos:
            gizmo.matrix_basis[0][3] = remap(getValue('iLocX'),0,1000,0,width)
            gizmo.matrix_basis[1][3] = remap(getValue('iLocY'),0,1000,0,height)

    def setup(self, context):
        gizmoGroup = self.gizmos.new("GIZMO_GT_button_2d")
        gizmoGroup.icon = 'INFO'
        gizmoGroup.draw_options = {'BACKDROP'}
        gizmoGroup.alpha = 0.0
        gizmoGroup.color = 1,0,0
        gizmoGroup.color_highlight = 1, 0, 0
        gizmoGroup.alpha_highlight = 0.2
        gizmoGroup.scale_basis = (80 * 0.35) / 2 
        gizmoGroup.target_set_operator("view3d.astats_gizmomenu")
        gizmoGroup.use_grab_cursor = True
        gizmoGroup.matrix_basis[0][3] = 1024
        gizmoGroup.matrix_basis[1][3] = 800

def getValue(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

def setValue(name,value):
    return setattr(bpy.context.preferences.addons[__name__].preferences,name,value)

def remap(value, low1, high1, low2, high2):
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

def relativeScale(size):
    if (getValue("bFontScaling")) == True:
        x = remap(size, 0, 1000, 0 , bpy.context.area.width)
        y = remap(size, 0, 1000, 0, bpy.context.area.height )
        return int((x+y)/2)
    else:return size

def add_draw(posX,posY,size,color,text):
    blf.position(font_id, posX,posY, 0)
    blf.size(font_id, size, 72)
    blf.color(font_id, color[0], color[1], color[2], 1)
    blf.draw(font_id, text)

def setDrawParams(fontName,xName,yName,shiftX,shiftY,colorName,text,width,height):
     size = relativeScale(getValue(fontName))
     posX = remap(getValue(xName),0,1000,0,width)+shiftX
     posY = remap(getValue(yName),0,1000,0,height)+shiftY
     add_draw(posX,posY,size,getValue(colorName),text)

def getTriCount():
    tris = 0
    bm = bmesh.new()
   
    for object in bpy.context.selected_objects:
        mesh = object.data
        bm.from_mesh(mesh)
        notSelected = []
        dupe = bm.copy()
        for poly in dupe.faces:
            if not poly.select:
                notSelected.append(poly)
        
        bmesh.ops.delete(dupe,geom=notSelected,context='FACES')
        tris+= len(dupe.calc_loop_triangles())
    bmesh.types.BMesh.free
    return tris

def getDataFromSelectedObjects():
    sum = [0,0,0]
    for object in bpy.context.selected_objects:
        if object.type == "MESH":
            data = object.data
            if getValue('bCalcTris'):
                bm = bmesh.new()
                bm.from_mesh(object.data)
                sum[2]+=len(bm.calc_loop_triangles())
                bmesh.types.BMesh.free
            else:
                sum[2]+=len(data.polygons)
            sum[1]+=len(data.edges)
            sum[0]+=len(data.vertices)
    return sum

def getSelectionStats():
    faces = 0
    edges = 0
    verts = 0
    for object in bpy.context.selected_objects:
        if object.type == "MESH" and bpy.context.mode == "EDIT_MESH":
            data = object.data
            object.update_from_editmode()
            if bpy.context.scene.tool_settings.mesh_select_mode[0] == True:
                verts += data.total_vert_sel
            if bpy.context.scene.tool_settings.mesh_select_mode[1] == True:
                edges += data.total_edge_sel
            if bpy.context.scene.tool_settings.mesh_select_mode[2] == True:
                if getValue('bCalcTris'):
                    faces += getTriCount()
                else:
                    faces += data.total_face_sel
    return [verts,edges,faces]

def getGlobalStats():
    stats = [0,0,0,0]
    if len(bpy.context.visible_objects) == 0:
            stats = [0,0,0,0]
    else:
        for object in bpy.context.visible_objects:
            stats[0]+=1
            if object.type == "MESH":
                stats[1]+=len(object.data.polygons)
                stats[2]+=len(object.data.edges)
                stats[3]+=len(object.data.vertices)
    return stats

def getMaterialsFromSelection():
    mats = []
    text = ''
    for object in bpy.context.selected_objects:
        if object.type == "MESH":
            object.update_from_editmode()
            data = object.data
            if bpy.context.mode == "EDIT_MESH":
                for polygon in data.polygons:
                    material = data.materials[polygon.material_index]
                    if polygon.select:
                        if material!=None:
                            if material.name not in mats:
                                mats.append(material.name)
            else:
                for material in data.materials:
                    if material!=None:
                        mats.append(material.name)
    if len(mats) > getValue("groupNames") and getValue('bNameGrouping')==True:
        text = str(len(mats)) + " Materials"
    else:
        for index in range(0,len(mats)):
            if index == 0 :
                text += str(mats[index])
            elif index == (len(mats)):
                text+=',' + str(mats[index])
            else:
                text += ',' + str(mats[index])
    return text

def displayShadow():
    blf.enable(font_id , blf.SHADOW )
    blf.shadow(font_id, 3, getValue('shadowColor')[0], getValue('shadowColor')[1], getValue('shadowColor')[2], 0.8)
    blf.shadow_offset(font_id, getValue('shOffsetX'), getValue('shOffsetY'))

def getObjectNames():
    text = ""
    if len(bpy.context.selected_objects) > getValue("groupNames") and getValue('bNameGrouping')==True:
        text = str(len(bpy.context.selected_objects)) + " Objects"
    else :
        for object in range(len(bpy.context.selected_objects)):
            if object > 0:text += "," + bpy.context.selected_objects[object].name
            else: text += bpy.context.selected_objects[object].name
    return text

def draw_callback_px(self, context):
    nWidth = 0
    tWidth = 0
    #TODO T and N now 2 and 3. Need to do more inteligent way to track toolbars
    #disabled until I find a way to get the width of T and N toolbars
    #nWidth = bpy.context.area.regions[2].width
    #tWidth = bpy.context.area.regions[1].width
    width = bpy.context.area.width
    height = bpy.context.area.height
    if getValue('bDispShadow') == True:
        displayShadow()
    objectName = getObjectNames()
    totalComponents = getDataFromSelectedObjects()
    #Draw global stats for visible objects
    if getValue('bDispGlobal') == True:
        globalValues = getGlobalStats()
        for value in range(4):
            size = relativeScale(getValue('gFontSize'))
            text = globalnames[value]+str(globalValues[value])
            setDrawParams('gFontSize','gLocX','gLocY',0,-size*value,'gStatColor',text,width,height)
    #Draw stats for selected objects
    if getValue('bDispSelected') == True:
        setDrawParams('sFontSize','sLocX','sLocY',0,0,'sStatColor',str(objectName),width,height)
        totalSelected = getSelectionStats()
        shiftX=0
        shiftY=0
        #verts
        if (getValue('bDispActive') and bpy.context.scene.tool_settings.mesh_select_mode[0]) or (not getValue('bDispActive') and getValue('bDrawVerts')):
            shiftY = relativeScale(getValue('sFontSize'))*1.5 
            setDrawParams('sFontSize','sLocX','sLocY',0,-shiftY,'sStatColor',names[0],width,height)
            shiftX = len(names[0])*(relativeScale(getValue('sFontSize'))/2)
            if bpy.context.mode == "EDIT_MESH":
                if bpy.context.scene.tool_settings.mesh_select_mode[0]:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'highlightColor',str(totalSelected[0]),width,height)
                    shiftX += len(str(totalSelected[0]))*(relativeScale(getValue('sFontSize'))/1.5)
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor','/',width,height)
                else :
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalSelected[0])+'/',width,height)
                    shiftX += len(str(totalSelected[0]))*(relativeScale(getValue('sFontSize'))/1.5)
            shiftX += relativeScale(getValue('sFontSize'))/1.5
            setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalComponents[0]),width,height)
        #edges
        if (getValue('bDispActive') and bpy.context.scene.tool_settings.mesh_select_mode[1]) or (not getValue('bDispActive') and getValue('bDrawEdges')):
            shiftY += relativeScale(getValue('sFontSize'))*1.2
            setDrawParams('sFontSize','sLocX','sLocY',0,-shiftY,'sStatColor',names[1],width,height)
            shiftX = len(names[1])*(relativeScale(getValue('sFontSize'))/2)
            if bpy.context.mode == "EDIT_MESH":
                if bpy.context.scene.tool_settings.mesh_select_mode[1]:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'highlightColor',str(totalSelected[1]),width,height)
                    shiftX += len(str(totalSelected[1]))*(relativeScale(getValue('sFontSize'))/1.5)
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor','/',width,height)
                else:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalSelected[1])+'/',width,height)
                    shiftX += len(str(totalSelected[1]))*(relativeScale(getValue('sFontSize'))/1.5)
            shiftX += relativeScale(getValue('sFontSize'))/1.5
            setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalComponents[1]),width,height)
        #faces
        if (getValue('bDispActive') and bpy.context.scene.tool_settings.mesh_select_mode[2]) or (not getValue('bDispActive') and getValue('bDrawFaces')):
            shiftY += relativeScale(getValue('sFontSize'))*1.2
            #switch for tris/faces names
            if getValue('bCalcTris'):
                text = names[3]
            else:
                text = names[2]
            setDrawParams('sFontSize','sLocX','sLocY',0,-shiftY,'sStatColor',text,width,height)
            shiftX = len(names[0])*(relativeScale(getValue('sFontSize'))/2)
            if bpy.context.mode == "EDIT_MESH":
                if bpy.context.scene.tool_settings.mesh_select_mode[2]:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'highlightColor',str(totalSelected[2]),width,height)
                    shiftX += len(str(totalSelected[2]))*(relativeScale(getValue('sFontSize'))/1.5)
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor','/',width,height)
                else:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalSelected[2])+'/',width,height)
                    shiftX += len(str(totalSelected[2]))*(relativeScale(getValue('sFontSize'))/1.5)
            shiftX += relativeScale(getValue('sFontSize'))/1.5
            setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalComponents[2]),width,height)
        #mats
        if (getValue('bShowMats')):
            
            shiftY += relativeScale(getValue('sFontSize'))*1.2
            setDrawParams('mFontSize','sLocX','sLocY',0,-shiftY,'matColor',getMaterialsFromSelection(),width,height)

def register():
    bpy.utils.register_class(AddonPreferences)
    #bpy.utils.register_class(AStatsButton)
    #bpy.utils.register_class(AStats_GizmoMenu)
    StatsText["handler"] = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (None, None), 'WINDOW', 'POST_PIXEL')

def unregister():
    bpy.utils.unregister_class(AddonPreferences)
    #bpy.utils.unregister_class(AStatsButton)
    #bpy.utils.unregister_class(AStats_GizmoMenu)
    bpy.types.SpaceView3D.draw_handler_remove(StatsText["handler"],'WINDOW')