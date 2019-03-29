'''
Copyright (C) 2019
yurii.andropov@live.com

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
    "name": "AStats",
    "description": "Show Stats in Viewport",
    "author": "A*",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "3D View"
}

import bpy
import blf
import bgl
StatsText = {
    "font_id": 0,
    "handler": None,
}
font_id = 0

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
        SRow.prop(self, "bDispSelected")
        SRow.prop(self, "sFontSize")
        SRow.prop(self, "sLocX")
        SRow.prop(self, "sLocY")
        SRow.prop(self, "sStatColor")
        SRow.prop(self,"highlightColor" )
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

def draw_callback_px(self, context):
    nWidth = bpy.context.area.regions[2].width
    tWidth = bpy.context.area.regions[1].width
    width = bpy.context.area.width
    height = bpy.context.area.height
    view_layer = bpy.context.view_layer
    objectName = ""
    totalComponents = [0,0,0]
    totalSelected = [0,0,0]
    names = ["Faces : ", "Edges : ", "Verts : "]
    globalnames = ["Objects :","Faces :","Edges :","Verts :"]
    globalValues = [0,0,0,0]
    materials = []
    allMaterials = []
    matNum = 0

    if getValue('bDispShadow') == True:
        blf.enable(font_id , blf.SHADOW )
        blf.shadow(font_id, 3, getValue('shadowColor')[0], getValue('shadowColor')[1], getValue('shadowColor')[2], 0.8)
        blf.shadow_offset(font_id, getValue('shOffsetX'), getValue('shOffsetY'))
    #Get object names and selected objects stats
    if len(bpy.context.selected_objects) > getValue("groupNames") and getValue('bNameGrouping')==True:
        objectName = str(len(bpy.context.selected_objects)) + " Objects"
    else :
        for n in range(len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[n]
            if len(objectName)>0:objectName += "," + object.name
            else: objectName += object.name
    selected = []
    for o in bpy.context.selected_objects:
        if o.type == "MESH":
            allMaterials = o.data.materials
            o.update_from_editmode()
            data = o.data
            totalComponents[0]+=len(data.polygons)
            totalComponents[1]+=len(data.edges)
            totalComponents[2]+=len(data.vertices)
            #cheking applied materials
            for material in data.materials:
                if material != None :
                    for poly in data.polygons:
                        if data.materials[poly.material_index] != 'NoneType':
                            if material.name == data.materials[poly.material_index].name:
                                matNum+=1
                                break
            if bpy.context.mode == "EDIT_MESH":
                totalSelected[0]+=data.total_face_sel
                totalSelected[1]+=data.total_edge_sel
                totalSelected[2]+=data.total_vert_sel
                for poly in data.polygons:
                    if poly.select :
                        selected.append(poly)
            for poly in selected:
                if len(allMaterials)!=0:
                    if material != None :
                        if materials.count(allMaterials[poly.material_index].name) == 0 :
                            materials.append(allMaterials[poly.material_index].name)
    #Draw global stats for visible objects
    if getValue('bDispGlobal') == True:
        if len(bpy.context.visible_objects) == 0:
            globalValues = [0,0,0,0]
        else:
            for g in bpy.context.visible_objects:
                globalValues[0]+=1
                if g.type == "MESH":
                    globalValues[1]+=len(g.data.polygons)
                    globalValues[2]+=len(g.data.edges)
                    globalValues[3]+=len(g.data.vertices)
        for v in range(4):
            size = relativeScale(getValue('gFontSize'))
            posX = remap(getValue('gLocX'),0,1000,tWidth,width-nWidth)
            posY = remap(getValue('gLocY'),0,1000,0,height)-size*v
            add_draw(posX,posY,size,getValue('gStatColor'),globalnames[v] + str(globalValues[v]))
    #Draw stats for selected objects
    if getValue('bDispSelected') == True:
        posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
        posY = remap(getValue('sLocY'),0,1000,0,height)
        size = relativeScale(getValue('sFontSize'))
        add_draw(posX,posY , size ,getValue('sStatColor'), str(objectName))
    #Draw only active type of selection
        if getValue('bDispActive') == True:
            if bpy.context.mode == "EDIT_MESH":
                if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                    size = relativeScale(getValue('sFontSize'))
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                    posY = remap(getValue('sLocY')-size,0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),names[2] )

                    shift = len(names[2])*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-getValue('sFontSize'),0,1000,0,height)
                    #size = relativeScale(getValue('sFontSize'))
                    add_draw(posX,posY,size,getValue('highlightColor'),str(totalSelected[2]) )

                    shift += len(str(totalSelected[2]))*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-getValue('sFontSize'),0,1000,0,height)
                    #size = relativeScale(getValue('sFontSize'))
                    add_draw(posX,posY,size,getValue('sStatColor'),"/" + str(totalComponents[2]) )

                if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
                    size = relativeScale(getValue('sFontSize'))
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                    posY = remap(getValue('sLocY')-size,0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),names[1])

                    shift = len(names[1])*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-getValue('sFontSize'),0,1000,0,height)
                    add_draw( posX,posY,size,getValue('highlightColor'),str(totalSelected[1]))

                    shift += len(str(totalSelected[1]))*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-getValue('sFontSize'),0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),"/" + str(totalComponents[1]))

                if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                    size = relativeScale(getValue('sFontSize'))
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                    posY = remap(getValue('sLocY')-size,0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),names[0])

                    shift = len(names[0])*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-size,0,1000,0,height)
                    add_draw(posX,posY,size,getValue('highlightColor'),str(totalSelected[0]))

                    shift += len(str(totalSelected[0]))*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-size,0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),"/" + str(totalComponents[0]))

                    if len(materials)>0:
                        text = ""
                        if getValue('bNameGrouping')==True and len(materials)>getValue('groupNames'):
                            if len(materials) == 1:text="1 Material"
                            else:text=str(len(materials))+" Materials"
                        else:
                            for n in materials :
                                if len(text)==0:text+=n
                                else:text+=" "+n
                        size = relativeScale(getValue('mFontSize'))
                        posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                        posY = remap(getValue('sLocY')-size*2,0,1000,0,height)
                        add_draw(posX,posY,size,getValue('matColor'),text)
        #Draw toute les chooses
        else:
            if bpy.context.mode == "EDIT_MESH":
                for i in range(3):
                    size = relativeScale(getValue('sFontSize'))
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                    posY = remap(getValue('sLocY')-(size*(i+1)),0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),names[i])

                    shift = len(names[i])*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-(size*(i+1)),0,1000,0,height)
                    if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True) and i==0:
                        color = getValue('highlightColor')
                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False) and i==1:
                        color = getValue('highlightColor')
                    elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False) and i==2:
                        color = getValue('highlightColor')
                    else:
                        color = getValue('sStatColor')
                    add_draw(posX,posY,size,color,str(totalSelected[i]))
                    shift += len(str(totalSelected[i]))*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-(size*(i+1)),0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),"/" + str(totalComponents[i]))

                if len(materials)>0 and getValue('bShowMats') == True:
                    text = ""
                    if getValue('bNameGrouping')==True and len(materials)>getValue('groupNames'):
                        if len(materials)==1:text = str(len(materials))+" Material"
                        else:text+= str(len(materials))+" Materials"
                    else:
                        for m in materials:
                            if len(text)==0:text+=m
                            else:text+=" "+m
                    size = relativeScale(getValue('mFontSize'))
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                    posY =  remap(getValue('sLocY')-(size*5),0,1000,0,height)
                    add_draw(posX,posY,size,getValue('matColor'),text)
            else:
                for i in range(3):
                    size = relativeScale(getValue('sFontSize'))
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                    posY =  remap(getValue('sLocY')-(size*(i+1)),0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),names[i])

                    shift = len(names[i])*(size/1.5)
                    posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth) + shift
                    posY = remap(getValue('sLocY')-(size*(i+1)),0,1000,0,height)
                    add_draw(posX,posY,size,getValue('sStatColor'),str(totalComponents[i]))
                    if getValue('bShowMats') == True and matNum > 0:
                        size = relativeScale(getValue('mFontSize'))
                        posX = remap(getValue('sLocX'),0,1000,tWidth,width-nWidth)
                        posY = remap(getValue('sLocY')-(size*5),0,1000,0,height)
                        text = ""
                        if matNum == 1:text="Material"
                        else:text="Materials"
                        add_draw(posX,posY,size,getValue('matColor'),str(matNum) + " " + text)

def register():
    bpy.utils.register_class(AddonPreferences)
    StatsText["handler"] = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (None, None), 'WINDOW', 'POST_PIXEL')

def unregister():
    bpy.utils.unregister_class(AddonPreferences)
    bpy.types.SpaceView3D.draw_handler_remove(StatsText["handler"],'WINDOW')

if __name__ == "__main__":
    register()
