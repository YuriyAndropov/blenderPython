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
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "https://youtu.be/06zMRZzpbZc",
    "category": "3D View"
}

import bpy
import blf
StatsText = {
    "font_id": 0,
    "handler": None,
}
font_id = 0
objectName = ""
totalComponents = [0,0,0]
totalSelected = [0,0,0]
matNum = 0
names = ["Verts : ", "Edges : ", "Faces : "]
globalnames = ["Objects :","Faces :","Edges :","Verts :"]
globalValues = [0,0,0,0]
materials = []
allMaterials = []

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    #Location properties
    sLocX:bpy.props.IntProperty(name="X",description="Relative X position", default=10,min=0,max=1000)
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
    bDispGlobal: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispShadow: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispSelected: bpy.props.BoolProperty(name="On/Off",description="On/Off switch", default=True)
    bDispActive: bpy.props.BoolProperty(name="Selection Based Stats",description="Switch for showing stats based on selection type(ie only verts)", default=False)
    bShowMats: bpy.props.BoolProperty(name="On/Off",description="Switch for showing names of selected materials", default=True)
    bNameGrouping: bpy.props.BoolProperty(name="Name Grouping",description="Switch for name grouping", default=True)
    bFontScaling: bpy.props.BoolProperty(name="Font Sclaing",description="Switch for font scaling", default=True)
    bDrawFaces: bpy.props.BoolProperty(name="Draw Faces",description="Switch for drawing faces", default=True)
    bDrawEdges: bpy.props.BoolProperty(name="Draw Edges",description="Switch for drawing edges", default=True)
    bDrawVerts: bpy.props.BoolProperty(name="Draw Verts",description="Switch for drawing verts", default=True)
    #Additional Properties
    groupNames: bpy.props.IntProperty(name="Group names after",description="When the number of of selected object is bigger than the value it will be replaced by Number of Objects", default=2)

    def draw(self, context):
        layout = self.layout
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
        SRow.prop(self, "bDispSelected")
        SRow.prop(self, "sFontSize")
        SRow.prop(self, "sLocX")
        SRow.prop(self, "sLocY")
        SRow.prop(self, "sStatColor")
        SRow.prop(self,"highlightColor" )
        BRow.prop(self,'bDrawFaces')
        BRow.prop(self,'bDrawEdges')
        BRow.prop(self,'bDrawVerts')
        SelectedStatBox.label(text="Statistics for all selected objects")
        #Box for additional properties
        AddProp = layout.box()
        AddProp.label(text="Additional Options")
        ARow = AddProp.row(align=True)
        ShadowRow = AddProp.row(align=True)
        MatRow = AddProp.row(align=True)
        MatRow.label(text="Material Options")
        ARow.prop(self,"bDispActive" )
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

def getValue(name):
    return getattr(bpy.context.preferences.addons[__name__].preferences,name)

def remap(value, low1, high1, low2, high2):
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1);

def relativeScale(size):
    if (getValue("bFontScaling")) == True:
        x = remap(size, 0, 1586, 0 , bpy.context.area.width)
        y = remap(size, 0, 657, 0, bpy.context.area.height )
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

def getDataFromSelectedObjects():
    sum = [0,0,0]
    for object in bpy.context.selected_objects:
        if object.type == "MESH":
            data = object.data
            sum[0]+=len(data.polygons)
            sum[1]+=len(data.edges)
            sum[2]+=len(data.vertices)
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
                faces += data.total_vert_sel
            if bpy.context.scene.tool_settings.mesh_select_mode[1] == True:
                edges += data.total_edge_sel
            if bpy.context.scene.tool_settings.mesh_select_mode[2] == True:
                verts += data.total_face_sel
    return [faces,edges,verts]

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

def getAllMaterials():
    mats = []
    for object in bpy.context.visible_objects:
        if object.type == "MESH":
            data = object.data 
            for material in data.materials:
                if material != None:
                    mats.append(material.name)
    return mats

def getMaterialsFromSelection():
    mats = []
    text = ''
    for object in bpy.context.selected_objects:
        if object.type == "MESH":
            data = object.data
            for polygon in data.polygons:
                material = data.materials[polygon.material_index]
                if material!=None and material.name not in mats:
                    mats.append(material.name)
    if len(mats) > getValue("groupNames") and getValue('bNameGrouping')==True:
        text = str(len(mats)) + " Materials"
    else:
        for index in range(len(mats)-1):
            if index == 0 :
                text += str(mats[index])
            elif index == (len(mats)-1):
                text+=", " + str(mats[index])
            else:
                text += str(mats[index])+", "
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
    #disabled until I find a way to get the width of T and N toolbars
    #nWidth = bpy.context.area.regions[2].width
    #tWidth = bpy.context.area.regions[1].width
    width = bpy.context.area.width
    height = bpy.context.area.height
    view_layer = bpy.context.view_layer
    if getValue('bDispShadow') == True:
        displayShadow()
    objectName = getObjectNames()
    totalComponents = getDataFromSelectedObjects()
    #Draw global stats for visible objects
    if getValue('bDispGlobal') == True:
        globalValues = getGlobalStats()
        allMaterials = getAllMaterials()
        for v in range(4):
            size = relativeScale(getValue('gFontSize'))
            text = globalnames[v]+str(globalValues[v])
            setDrawParams('gFontSize','gLocX','gLocY',0,-size*v,'gStatColor',text,width,height)
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
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalSelected[1]),width,height)
                    shiftX += len(str(totalSelected[1]))*(relativeScale(getValue('sFontSize'))/1.5)
            shiftX += relativeScale(getValue('sFontSize'))/1.5
            setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalComponents[1]),width,height)
        #faces
        if (getValue('bDispActive') and bpy.context.scene.tool_settings.mesh_select_mode[2]) or (not getValue('bDispActive') and getValue('bDrawFaces')):
            shiftY += relativeScale(getValue('sFontSize'))*1.2
            setDrawParams('sFontSize','sLocX','sLocY',0,-shiftY,'sStatColor',names[2],width,height)
            shiftX = len(names[0])*(relativeScale(getValue('sFontSize'))/2)
            if bpy.context.mode == "EDIT_MESH":
                if bpy.context.scene.tool_settings.mesh_select_mode[2]:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'highlightColor',str(totalSelected[2]),width,height)
                    shiftX += len(str(totalSelected[2]))*(relativeScale(getValue('sFontSize'))/1.5)
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor','/',width,height)
                else:
                    setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalSelected[2]),width,height)
                    shiftX += len(str(totalSelected[2]))*(relativeScale(getValue('sFontSize'))/1.5)
            shiftX += relativeScale(getValue('sFontSize'))/1.5
            setDrawParams('sFontSize','sLocX','sLocY',shiftX,-shiftY,'sStatColor',str(totalComponents[2]),width,height)
        #mats
        if (getValue('bShowMats')):
            print(getMaterialsFromSelection())
            shiftY += relativeScale(getValue('sFontSize'))*1.2
            setDrawParams('mFontSize','sLocX','sLocY',0,-shiftY,'matColor',getMaterialsFromSelection(),width,height)

def register():
    bpy.utils.register_class(AddonPreferences)
    StatsText["handler"] = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (None, None), 'WINDOW', 'POST_PIXEL')

def unregister():
    bpy.utils.unregister_class(AddonPreferences)
    bpy.types.SpaceView3D.draw_handler_remove(StatsText["handler"],'WINDOW')

if __name__ == "__main__":
    register()
