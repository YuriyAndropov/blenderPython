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
    #link object to the scene(to Master Collection)
    bpy.context.collection.objects.link(newObj)
    
