#just a file for bpy snippets

#defs are for quick vs navigation
def Collections():
    #access all collections in the scene
    bpy.data.collections
    #create new collection
    newCol = bpy.data.collections.new("Name")
    #link collection to scene
    bpy.context.scene.collection.children.link(newCol)
    #link object to collection
    newCol.objects.link(newObj)

def Object():
    #create new object
    newObj = bpy.data.objects.new("Name", meshData)
    #delete object
    bpy.data.objects.remove(object,do_unlink=True,do_id_user=True,do_ui_user=True)
    #link object to the scene(to Master Collection)
    bpy.context.collection.objects.link(newObj)
    #select an object
    object.select_set(True) 
    #make object active
    bpy.context.view_layer.objects.active = object
    #parent one object1 to object2
    object1.parent = object2
    #access to children
    object.children
    #object custom properties
    bpy.ops.wm.properties_add(data_path="object.data")

def Context():
    #set context mode
    #'OBJECT', 'EDIT', 'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT', 'PARTICLE_EDIT', 'POSE'
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
