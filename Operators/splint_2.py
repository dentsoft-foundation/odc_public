import bpy

splint_cutter_color = [0.0, 0.6, 0.8, 1.0]
#Popup message box function :

def ShowMessageBox(message="", title="INFO", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)



##################################################################################################
#Splint functions :
#######################################################################################
#Add splint cutter curve function :

def add_splint_cutter():

    # Prepare scene settings :
    bpy.ops.transform.select_orientation(orientation="GLOBAL")
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_elements = {"FACE"}
    bpy.context.scene.tool_settings.transform_pivot_point = "INDIVIDUAL_ORIGINS"
    
    # Get Model :
    splint_target_name = bpy.context.scene.ODC_modops_props.splint_target_prop
    Model = bpy.data.objects[splint_target_name]

    #Ensure remove old splint cutter :
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.hide_view_clear()
    bpy.ops.object.select_all(action="DESELECT")

    for obj in bpy.data.objects :
        if "splint_cutter" in obj.name :
            obj.select_set(True)
            bpy.ops.object.delete(use_global=False, confirm=False)

    #hide everything but Model :
    bpy.ops.object.select_all(action="DESELECT")
    Model.select_set(True)
    bpy.context.view_layer.objects.active = Model
    bpy.ops.object.hide_view_set(unselected=True)

    # ....Add Curve ....... :
    bpy.ops.curve.primitive_bezier_curve_add(
        radius=1, enter_editmode=False, align="CURSOR"
    )  

    # Set splint_cutter name :
    splint_cutter = bpy.context.view_layer.objects.active
    splint_cutter.name = "splint_cutter"
    curve = splint_cutter.data
    curve.name = "splint_cutter_curve"
    bpy.context.scene.ODC_modops_props.splint_cutter_prop = splint_cutter.name

    # Prepare curve and Set curve settings :
    bpy.ops.object.mode_set(mode="EDIT")

    bpy.ops.curve.select_all(action="DESELECT")
    curve.splines[0].bezier_points[0].select_control_point = True
    bpy.ops.curve.dissolve_verts()
    bpy.ops.curve.select_all(action="SELECT")
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

    bpy.context.object.data.dimensions = "3D"
    bpy.context.object.data.twist_smooth = 3
    bpy.ops.curve.handle_type_set(type="AUTOMATIC")
    bpy.context.object.data.bevel_depth = 0.3
    bpy.context.object.data.extrude = 0
    bpy.context.scene.tool_settings.curve_paint_settings.error_threshold = 1
    bpy.context.scene.tool_settings.curve_paint_settings.corner_angle = 0.785398
    #bpy.context.scene.tool_settings.curve_paint_settings.corner_angle = 1.5708
    bpy.context.scene.tool_settings.curve_paint_settings.depth_mode = "SURFACE"
    bpy.context.scene.tool_settings.curve_paint_settings.surface_offset = 0
    bpy.context.scene.tool_settings.curve_paint_settings.use_offset_absolute = True

    # Add color material :
    if "ODC_splint_cutter_mat" in bpy.data.materials :
        mat = bpy.data.materials["ODC_splint_cutter_mat"]
    else :
        mat = bpy.data.materials.new("ODC_splint_cutter_mat")
        mat.diffuse_color = splint_cutter_color
        mat.roughness = 0.2

    curve.materials.append(mat)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.wm.tool_set_by_id(name="builtin.cursor")
    bpy.context.space_data.overlay.show_outline_selected = False

    #add shrinkwrap modifier :
    bpy.ops.object.modifier_add(type='SHRINKWRAP')
    bpy.context.object.modifiers["Shrinkwrap"].target = Model
    bpy.context.object.modifiers["Shrinkwrap"].offset = 0.1
    bpy.context.object.modifiers["Shrinkwrap"].wrap_mode = 'ABOVE_SURFACE'
    bpy.context.object.modifiers["Shrinkwrap"].use_apply_on_spline = True

#######################################################################################
#Delete last splint_cutter curve point function :

def delete_last_splint_cutter_point():

    splint_cutter_name = bpy.context.scene.ODC_modops_props.splint_cutter_prop 
    splint_cutter = bpy.data.objects[splint_cutter_name]
    curve = splint_cutter.data
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.dissolve_verts()
    curve.splines[0].bezier_points[0].select_control_point = True
    bpy.ops.object.mode_set(mode="OBJECT")

#######################################################################################
#Extrude to cursor function :
def splint_cutter_curve_point_to_cursor():

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.extrude(mode="INIT")
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
    bpy.ops.object.mode_set(mode="OBJECT")

def splint_cutter_finish() :

    splint_cutter_name = bpy.context.scene.ODC_modops_props.splint_cutter_prop 
    splint_cutter = bpy.data.objects[splint_cutter_name]
    
    splint_cutter.select_set(True)
    bpy.context.view_layer.objects.active = splint_cutter

    #change curve setting :
    bpy.context.object.data.offset = 0
    bpy.context.object.data.extrude = 0
    bpy.context.object.data.bevel_depth = 0

    #close curve :
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.cyclic_toggle()
    
    #apply modifier :
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")

    #change curve setting :
    bpy.context.object.data.bevel_depth = 0.3
    bpy.context.object.data.extrude = 2.5
    bpy.context.object.data.offset = 0.3

    bpy.ops.wm.tool_set_by_id(name="builtin.select")
    bpy.context.space_data.overlay.show_outline_selected = True

def cancel_splint_cutter() :

    bpy.ops.object.mode_set(mode="OBJECT")

    splint_cutter_name = bpy.context.scene.ODC_modops_props.splint_cutter_prop 
    splint_cutter = bpy.data.objects[splint_cutter_name]

    splint_target_name = bpy.context.scene.ODC_modops_props.splint_target_prop
    Model = bpy.data.objects[splint_target_name]

    bpy.ops.object.select_all(action="DESELECT")
    splint_cutter.select_set(True)
    bpy.context.view_layer.objects.active = splint_cutter
    bpy.ops.object.delete(use_global=False, confirm=False)

    bpy.ops.object.select_all(action="DESELECT")
    Model.select_set(True)
    bpy.context.view_layer.objects.active = Model

    bpy.ops.wm.tool_set_by_id(name="builtin.select")
    bpy.context.space_data.overlay.show_outline_selected = True

#######################################################################################
#Make splint_shell Function :

def make_splint_shell() :

        Model_name = bpy.context.scene.ODC_modops_props.splint_target_prop
        Model = bpy.data.objects[Model_name]

        splint_cutter_name = bpy.context.scene.ODC_modops_props.splint_cutter_prop 
        splint_cutter = bpy.data.objects[splint_cutter_name]

        #ensure Model and splint_cutter are visibles objects:
        Model.hide_set(False)
        splint_cutter.hide_set(False)

        # Get Model :
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        Model.select_set(True)
        bpy.context.view_layer.objects.active = Model

        #Duplicate Model :
        bpy.ops.object.duplicate_move()
        splint_shell = bpy.context.view_layer.objects.active
        splint_shell.name = "splint_shell"
        
        #Make it low_res :
        bpy.context.object.data.use_remesh_smooth_normals = True
        bpy.context.object.data.remesh_voxel_size = 0.3
        bpy.ops.object.voxel_remesh()

        # Get splint_cutter :
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        splint_cutter.select_set(True)
        bpy.context.view_layer.objects.active = splint_cutter
        for _ in splint_cutter.material_slots :
            bpy.ops.object.material_slot_remove()

        #change curve setting :
        splint_thikness = bpy.context.scene.ODC_modops_props.splint_thikness_prop
        bpy.context.object.data.offset = splint_thikness + 1
        bpy.context.object.data.extrude = splint_thikness 
        bpy.context.object.data.bevel_depth = splint_thikness + 1

        # convert curve to mesh :

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.convert(target="MESH")
        bpy.ops.object.shade_flat()

        # Remesh splint_cutter : 
        bpy.context.object.data.remesh_voxel_size = 0.3
        bpy.context.object.data.use_remesh_smooth_normals = True
        bpy.ops.object.voxel_remesh()

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        
        #Get splint_shell :
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        splint_shell.select_set(True)
        bpy.context.view_layer.objects.active = splint_shell
        
        # deselect all vertices :
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        
        #Boolean union :
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].show_viewport = False
        bpy.context.object.modifiers["Boolean"].operation = 'UNION'
        bpy.context.object.modifiers["Boolean"].object = splint_cutter
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

        # Separate by loose parts :
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.separate(type="LOOSE")
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.hide_view_set(unselected=True)
        
        bpy.ops.object.select_all(action="DESELECT")
        
        message = " Please select splint shell part and click Enter !"
        ShowMessageBox(message=message, icon="COLORSET_02_VEC")
        #bpy.ops.object.hide_view_set(unselected=True)
        

def metaball_splint() :

    # Prepare scene settings :
    bpy.context.tool_settings.mesh_select_mode = (True, False, False)
    bpy.context.scene.tool_settings.use_snap = False
    bpy.context.scene.tool_settings.use_proportional_edit_objects = False
    bpy.ops.object.mode_set(mode="OBJECT")

    # Add Metaballs :

    shell = bpy.context.view_layer.objects.active

    loc, rot, scale = shell.matrix_world.decompose()

    verts = shell.data.vertices
    vcords = [ rot  @ v.co + loc for v in verts]
    mball_elements_cords = [ vco - vcords[0] for vco in vcords[1:]]

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")

    thikness = bpy.context.scene.ODC_modops_props.splint_thikness_prop
    radius = thikness * 5/8

    bpy.ops.object.metaball_add(type='BALL', radius=radius, enter_editmode=False, location= vcords[0])

    Mball_object = bpy.context.view_layer.objects.active
    Mball_object.name = "Mball_object"
    mball = Mball_object.data
    mball.resolution = 0.6
    bpy.context.object.data.update_method = 'FAST'

    for i in range(len(mball_elements_cords)) :
        element = mball.elements.new()
        element.co = mball_elements_cords[i]
        element.radius = radius*2

    bpy.ops.object.convert(target='MESH')

    # Remesh splint : 
    bpy.context.object.data.remesh_voxel_size = 0.3
    bpy.context.object.data.use_remesh_smooth_normals = True
    bpy.ops.object.voxel_remesh()

    Mball_object = bpy.context.view_layer.objects.active
    Mball_object.name = "splint"
    mball_mesh = Mball_object.data
    mball_mesh.name = "splint_mesh"

#make splint2 finish splint function :
def splint_cut_finish() :

    Model_name = bpy.context.scene.ODC_modops_props.splint_target_prop
    Model = bpy.data.objects[Model_name]

    splint_cutter_name = bpy.context.scene.ODC_modops_props.splint_cutter_prop 
    splint_cutter = bpy.data.objects[splint_cutter_name]

    bool_model_prop = bpy.context.scene.ODC_modops_props.bool_model_prop

    splint = bpy.context.view_layer.objects.active#Get splint

    #delete splint shell :
    bpy.ops.object.hide_view_clear()
    for obj in bpy.data.objects :
        if "shell" in obj.name :
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.delete(use_global=False, confirm=False)

    # active_obj = splint       
    splint.select_set(True)
    bpy.context.view_layer.objects.active = splint
    bpy.ops.object.shade_flat()

    #cut splint border using splint_cutter:
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].show_viewport = False
    bpy.context.object.modifiers["Boolean"].object = splint_cutter
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    if bool_model_prop:
        bool_model = bpy.data.objects[bool_model_prop]
        bool_model.hide_set(False)

    else :
        bool_model = Model
        
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].show_viewport = False
    bpy.context.object.modifiers["Boolean"].object = bool_model
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    # Remesh splint : 
    bpy.context.object.data.remesh_voxel_size = 0.2
    bpy.context.object.data.use_remesh_smooth_normals = True
    bpy.ops.object.voxel_remesh()

    #hide everything but Model+splint :
    bpy.ops.object.select_all(action="DESELECT")
    splint.select_set(True)
    Model.select_set(True)
    bpy.context.view_layer.objects.active = splint
    bpy.ops.object.hide_view_set(unselected=True)
    
    splint_color = bpy.data.materials.new("ODC_splint_material")
    splint_color.diffuse_color = [0.0, 0.6, 0.8, 1.0]
    splint.data.materials.append(splint_color)

    #bpy.ops.object.shade_smooth()

    bpy.ops.object.select_all(action="DESELECT")


####################################################################################### 
#Make splint_cutter operator :
    
class ODC2_OT_splint_cutter(bpy.types.Operator):
    """make splint_cutter tool"""

    bl_idname = "odc2.splint_cutter"
    bl_label = "Trace splint"
    bl_options = {"REGISTER", "UNDO"}

    def modal(self, context, event):

        if event.type == ("LEFTMOUSE"):#add point and extrude to cursor

            if event.value == ("PRESS"):

                return {"PASS_THROUGH"}
            
            if event.value == ("RELEASE"):
                
                splint_cutter_curve_point_to_cursor()

        elif event.type == ("DEL"):#delete last curve point

            if event.value == ("PRESS"):

                delete_last_splint_cutter_point()

        elif event.type == "RET":#finish curve

            if event.value == ("PRESS"):
                
                splint_cutter_finish()
                
                return {"FINISHED"}
        
        elif event.type == ("ESC"):#cancel modal operator and delete curve

            if event.value == ("PRESS"):

                cancel_splint_cutter()
                return {"CANCELLED"}

        else :

            # allow navigation
            return {"PASS_THROUGH"}

        return {"RUNNING_MODAL"}

    def invoke(self, context, event):

        if bpy.context.selected_objects == []:

            message = " Please select Model !"
            ShowMessageBox(message=message, icon="COLORSET_02_VEC")

            return {"CANCELLED"}

        else:

            if context.space_data.type == "VIEW_3D":

                # Assign Model name to cutting_target property :
                Model = bpy.context.view_layer.objects.active
                context.scene.ODC_modops_props.splint_target_prop = Model.name
                
                bpy.ops.object.mode_set(mode="OBJECT")
                bpy.ops.object.hide_view_clear()
                bpy.ops.object.select_all(action="DESELECT")

                for obj in bpy.data.objects :
                    if "splint_cutter" in obj.name :
                        obj.select_set(True)
                        bpy.ops.object.delete(use_global=False, confirm=False)

                bpy.ops.object.select_all(action="DESELECT")
                Model.select_set(True)
                bpy.context.view_layer.objects.active = Model

                # Hide everything but model :
                bpy.ops.object.hide_view_set(unselected=True)

                add_splint_cutter()

                context.window_manager.modal_handler_add(self)

                message = " Make outline curve and click <ENTER> !"
                ShowMessageBox(message=message, icon="COLORSET_02_VEC")

                
                return {"RUNNING_MODAL"}

            else:

                self.report({"WARNING"}, "Active space must be a View3d")

                return {"CANCELLED"}

####################################################################################### 

class ODC2_OT_make_splint2(bpy.types.Operator):
    " make splint"

    bl_idname = "odc2.make_splint2"
    bl_label = "Splint"

    def modal(self, context, event):

        props = context.scene.ODC_modops_props

        if event.type == "RET":
            if event.value == ("PRESS"):

                splint_shell_reel = context.view_layer.objects.active
                bpy.context.scene.ODC_modops_props.splint_shell_reel_prop = splint_shell_reel.name

                metaball_splint()#make metaball splint
                splint_cut_finish()#cut splint finish splint
                
                return {"FINISHED"}

        elif event.type == ("ESC"):

            Model_name = props.splint_target_prop
            Model = bpy.data.objects[Model_name]

            splint_cutter_name = props.splint_cutter_prop 
            splint_cutter = bpy.data.objects[splint_cutter_name]

            bpy.ops.object.select_all(action="SELECT")
            splint_cutter.select_set(False)
            Model.select_set(False)
            bpy.ops.object.delete(use_global=False, confirm=False)
            Model.select_set(True)
            context.view_layer.objects.active = Model

            return {"CANCELLED"}

        else :

            # allow navigation
            return {"PASS_THROUGH"}

        return {"RUNNING_MODAL"}

    def invoke(self, context, event):

        if context.space_data.type == "VIEW_3D":

            make_splint_shell()
            bpy.ops.wm.tool_set_by_id(name="builtin.select")

            context.window_manager.modal_handler_add(self)

            return {"RUNNING_MODAL"}

        else:

            self.report({"WARNING"}, "Active space must be a View3d")

            return {"CANCELLED"}

#Register classes :
classes = [
    ODC2_OT_splint_cutter,
    ODC2_OT_make_splint2,
]


def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    