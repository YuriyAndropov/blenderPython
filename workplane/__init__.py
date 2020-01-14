bl_info = {
    "name": "Workplane",
    "category": "3D View",
    "author": "Benjamin Sauder",
    "description": "Allows for quicker workflow using move/rotate/scale on a user defined workplane",
    "version": (0, 2),
    "location": "View3D > Tool Shelf",
}


if "bpy" in locals():
    import importlib
    importlib.reload(data)
    importlib.reload(draw)
    importlib.reload(operator)
    importlib.reload(ui)
    importlib.reload(update)
    importlib.reload(util)
    
else:
    from . import (
        data,
        draw,
        operator,
        ui,
        update,
        util
        )
  

import bpy

classes = [
    data.WorkplaneProperties, 
    update.WorkPlaneUpdater,
    operator.SetWorkPlane,   
    operator.WorkplaneTranslate,
    operator.WorkplaneRotate,
    operator.WorkplaneScale,
    operator.WorkplaneExtrude,  
    ui.WorkplanePanelTransform,
    ui.WorkplanePanelMeshEdit,
]

def register():

    '''
    bpy.types.Scene.workplane_matrix = bpy.props.FloatVectorProperty(
            name="workplane_matrix",
            size=16,
            subtype="MATRIX")            
                     
    bpy.types.Scene.workplane_viewmatrix = bpy.props.FloatVectorProperty(
            name="workplane_viewmatrix",
            size=16,
            subtype="MATRIX")        

    bpy.types.Scene.workplane_grid_prefs = bpy.props.BoolVectorProperty(
            name="workplane_grid_prefs",
            size=4)
                     
    bpy.types.Scene.workplane_visible = bpy.props.BoolProperty(name="workplane_visible", default=True)
    
   
    bpy.types.Scene.workplane_user_transform_orientation = bpy.props.StringProperty(name="workplane_user_transform_orientation", default="GLOBAL")
  

    bpy.types.Scene.workplane_preview_mode = bpy.props.EnumProperty(items=draw.MODE)
    '''
   

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.workplane = bpy.props.PointerProperty(type=data.WorkplaneProperties)    

    #bpy.types.Scene.workplane_props = bpy.props.PointerProperty(
    #    name="Workplane props", type=data.WorkplaneProperties)
    
    #bpy.utils.register_module(__name__)
    
    #for window in bpy.context.window_manager.windows:
    #    for area in window.screen.areas:
    #        if area.type == 'VIEW_3D':
    #            override = {'window': window, 'screen': window.screen, 'area': area, "scene": bpy.context.scene}                
    #            bpy.ops.workplane.internal_workplane_updater(override)
    #            break
    

def unregister():
    update.WorkPlaneUpdater.Running = False
    draw.disable()

    del bpy.types.Scene.workplane
     
    for c in classes:
        bpy.utils.unregister_class(c)
            

