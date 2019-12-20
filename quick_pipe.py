import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from numpy import (array, dot, arccos, clip, pi, cos, cross)
from numpy.linalg import norm
from bpy.props import IntProperty, FloatProperty
from itertools import zip_longest

bl_info = {
    "name": "Quick Pipe",
    "author": "floatvoid (Jeremy Mitchell), Pavel Geraskin, Cebbi, Alexander Belyakov",
    "version": (2, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode > Context Menu (Right mouse), Edge Menu (Ctrl + E)",
    "description": "Quickly converts an edge selection to an extruded curve.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}


class jmPipeTool(bpy.types.Operator):
    bl_idname = "object.quickpipe"
    bl_label = "Quick Pipe"
    bl_options = {'REGISTER', 'UNDO'}

    first_mouse_x: IntProperty()
    first_value: FloatProperty()
    

    def modal(self, context, event):

        context.object.show_wire = True

        if event.type in {'RIGHTMOUSE', 'ESC', 'LEFTMOUSE'}:
            context.object.show_wire = False
            return {'FINISHED'}

        if event.type == 'Q':
            context.object.show_wire = False
            return bpy.ops.object.matchpipewidth("INVOKE_DEFAULT")

        if event.type == 'MOUSEMOVE':
            delta = (self.first_mouse_x - event.mouse_x)

            if event.ctrl:
                delta *= 0.1

                if event.shift:
                    delta *= 0.1

            context.object.data.bevel_depth = abs((self.first_value + delta) * 0.002)
        elif event.type == 'WHEELUPMOUSE':
            bpy.context.object.data.bevel_resolution += 1
        elif event.type == 'WHEELDOWNMOUSE':
            if bpy.context.object.data.bevel_resolution > 0:
                bpy.context.object.data.bevel_resolution -= 1

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:

            if (context.object.type == 'MESH'):
                self.first_mouse_x = event.mouse_x

                bpy.ops.mesh.duplicate_move()
                bpy.ops.mesh.separate(type='SELECTED')
                bpy.ops.object.editmode_toggle()

                #  pipe = context.view_layer.objects[-1]
                pipe = context.selected_objects[-1]
                bpy.ops.object.select_all(action='DESELECT')
                pipe.select_set(state=True)
                context.view_layer.objects.active = pipe
                bpy.ops.object.convert(target='CURVE')

                pipe.data.fill_mode = 'FULL'
                pipe.data.splines[0].use_smooth = True
                pipe.data.bevel_resolution = 1
                pipe.data.bevel_depth = 0.1

            elif (context.object.type == 'CURVE'):
                self.report({'WARNING'}, "Need Edit Mode!")
                return {'CANCELLED'}

            self.first_value = pipe.data.bevel_depth

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


class MatchPipeWidth(bpy.types.Operator):
    """Creates a Mesh from a pipe with corrected scaling of the edge loops for a uniform width of the pipe's segments."""
    bl_idname = "object.matchpipewidth"
    bl_label = "Match Pipe Width"

    def invoke(self, context, event):
        if context.object:
            if(context.object.type == 'CURVE'):

                curve = context.object
                spline = curve.data.splines.active
                points = spline.points

                if len(points) >= 3:
                    radius_adjustments = [None]
                    normals = [None]

                    # Calculate Radius Adjustments and Perpendicular Axes for Each Point
                    for i in range(1, len(points) - 1):
                        a = points[i - 1]
                        b = points[i]
                        c = points[i + 1]

                        ba = a.co.to_3d() - b.co.to_3d()
                        bc = c.co.to_3d() - b.co.to_3d()

                        alpha = angle(ba, bc)
                        beta = pi - alpha

                        radius_adjustments.insert(i, abs(1 / cos(beta / 2)))
                        normals.insert(i, cross(ba, bc) / norm(cross(ba, bc)))

                    ring_size = 4 + 2 * curve.data.bevel_resolution

                    # Convert to Mesh
                    bpy.ops.object.select_all(action='DESELECT')
                    # curve.select = True
                    # bpy.context.scene.objects.active = curve
                    context.active_object.select_set(state=True)

                    bpy.ops.object.shade_smooth()
                    bpy.ops.object.convert(target='MESH')

                    mesh = curve.data

                    # Get Bmesh
                    bpy.ops.object.mode_set(mode='EDIT')

                    if mesh.is_editmode:
                        bm = bmesh.from_edit_mesh(mesh)
                    else:
                        bm = bmesh.new()
                        bm.from_mesh(mesh)

                    # Group Edge Loops (Assumes that vertices are created ring after ring)
                    rings = list(grouper(bm.verts, ring_size))

                    for i in range(1, len(rings) - 1):
                        # Select Vertices
                        for vertex in rings[i]:
                            vertex.select = True

                        # Create Rotation Matrices
                        rotation_axis = cross(normals[i], (0, 0, 1))
                        rotation_angle = angle(normals[i], (0, 0, 1))
                        rotation_matrix = Matrix.Rotation(rotation_angle, 4, rotation_axis)
                        backrotation_matrix = Matrix.Rotation(-rotation_angle, 4, rotation_axis)

                        # Rotate, Scale, Rotate Back
                        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rotation_matrix, verts=rings[i])
                        bpy.ops.transform.resize(value=(radius_adjustments[i], radius_adjustments[i], 0), constraint_axis=(True, True, False))
                        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=backrotation_matrix, verts=rings[i])

                        # Deselect Vertices
                        for vertex in rings[i]:
                            vertex.select = False

                    bpy.ops.object.mode_set(mode='OBJECT')

                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "No curve selected, could not finish")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def angle(v1, v2):
    angle = arccos(dot(v1, v2) / (norm(v1) * norm(v2)))
    if (angle <= 2 * pi):
        return angle
    else:
        return 2 * pi - angle


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


# class VIEW3D_PT_tools_jmPipeTool(bpy.types.Panel):

#     bl_label = "Quick Pipe"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Tools'
#     bl_context = "mesh_edit"
#     bl_options = {'DEFAULT_CLOSED'}

#     def draw(self, context):
#         layout = self.layout

#         row = layout.row()
#         row.operator("object.quickpipe")


def menu_func(self, context):
    self.layout.operator_context = "INVOKE_DEFAULT"
    self.layout.operator(jmPipeTool.bl_idname, text="Quick Pipe")

classes = (
    jmPipeTool,
    MatchPipeWidth,
    # VIEW3D_PT_tools_jmPipeTool
)


# Register
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #  update_panel(None, bpy.context)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)  # Mesh Context Menu
    # bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)  # Vertices Menu(CTRL+V)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(menu_func)  # Edge Menu(CTRL+E)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    # bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(menu_func)

if __name__ == "__main__":
    register()