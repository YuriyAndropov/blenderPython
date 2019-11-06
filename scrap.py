if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
            context.area.tag_redraw()
            self.coords = [event.mouse_region_x,event.mouse_region_y]
            uv = bpy.context.region.view2d.region_to_view(self.coords[0],self.coords[1])
            for obj in bpy.context.selected_objects:
                bm = bmesh.from_edit_mesh(obj.data)
                uv_layer = bm.loops.layers.uv.verify()
                #uv vert raycast
                if bpy.context.scene.tool_settings.uv_select_mode == 'VERTEX':
                    bm.verts.ensure_lookup_table()
                    distances = {}
                    for vert in bm.verts:
                        for loop in vert.link_loops:
                            loop_uv = loop[uv_layer]
                            l1 = numpy.array(uv)
                            l2 = numpy.array(loop_uv.uv)
                            distances[numpy.linalg.norm(l1 - l2)] = loop
                    if min(distances)<=0.1:
                        distances.get(min(distances))[uv_layer].select = True