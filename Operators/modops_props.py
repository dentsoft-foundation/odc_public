import bpy

from bpy.props import StringProperty, FloatProperty, EnumProperty, FloatVectorProperty, BoolProperty

def text_body_update(self,context):
    props = context.scene.ODC_modops_props
    if context.object :
        ob = context.object
        if ob.type == 'FONT' :
            mode = ob.mode
            bpy.ops.object.mode_set(mode="OBJECT")
            ob.data.body = props.text_body_prop

            # Check font options and apply them if toggled :
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()

            dict_font_options = { 

                                'BOLD' : props.bold_toggle_prop,
                                'ITALIC' : props.italic_toggle_prop,
                                'UNDERLINE' : props.underline_toggle_prop,

                                }
            for key, value in dict_font_options.items() :
                if value == True :
                    bpy.ops.font.style_toggle(style=key)

            ob.name = ob.data.body
            bpy.ops.object.mode_set(mode=mode)

def text_bold_toggle(self,context):
    if context.object :
        ob = context.object
        if ob.type == 'FONT' :
            mode = ob.mode
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()
            bpy.ops.font.style_toggle(style='BOLD')
            bpy.ops.object.mode_set(mode=mode)

def text_italic_toggle(self,context):
    if context.object :
        ob = context.object
        if ob.type == 'FONT' :
            mode = ob.mode
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()
            bpy.ops.font.style_toggle(style='ITALIC')
            bpy.ops.object.mode_set(mode=mode)

def text_underline_toggle(self,context):
    if context.object :
        ob = context.object
        if ob.type == 'FONT' :
            mode = ob.mode
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()
            bpy.ops.font.style_toggle(style='UNDERLINE')
            bpy.ops.object.mode_set(mode=mode)

class ODC_modops_props(bpy.types.PropertyGroup):

    # Decimate ratio prop :
    ######################################################################################### 
    decimate_ratio : FloatProperty(description="Enter decimate ratio ", default=0.5, step=1, precision=2)

    # Cutting tools props :
    #########################################################################################
    cutting_target : StringProperty(name="", default = "No Target !", description="Target",)

    ##############################################
    cutting_tool_list = ["Curve Cutting Tool", "Square Cutting Tool"]
    items = []
    for i in range(len(cutting_tool_list)): 
        item = (str(cutting_tool_list[i]), str(cutting_tool_list[i]), str(""), int(i))
        items.append(item)

    cutting_tool : EnumProperty(items=items, description="", default="Curve Cutting Tool")

    cutting_tool_name : StringProperty(name="", default = "NONE", description="cutting tool name",)
    ##############################################
    cutting_mode_list = ["Cut inner", "Keep inner"]
    items = []
    for i in range(len(cutting_mode_list)):
        item = (str(cutting_mode_list[i]), str(cutting_mode_list[i]), str(""), int(i))
        items.append(item)

    cutting_mode : EnumProperty(items=items, description="", default="Cut inner")

    # Model Bases props :
    ######################################################################################### 
    base_height : FloatProperty(description="Enter Base Height", default= 6, step=10, precision=2, unit='LENGTH', min=0)
    offset : FloatProperty(description="Enter offset value", default=0.20, step=1, precision=2, subtype='DISTANCE', unit='LENGTH')
    base_location_prop : FloatVectorProperty(name="Base location", description="stors the Model base location", size=3)
    show_box : BoolProperty(description="show or not the popup message box ", default=True)
    # Color material props :
    #########################################################################################
    no_material_prop = StringProperty(name="No Material", default = "No Color", description="No material_slot found for active object")

    # Splint props :
    #########################################################################################
    splint_shell_fake_prop = StringProperty(name="fake splint shell", default = "", description="Get the fake splint shell")
    splint_shell_reel_prop = StringProperty(name="reel splint shell", default = "", description="Get the reel splint shell")

    bool_model_prop : StringProperty(name="bool object", default = "", description="Get the bool object")
    splint_target_prop : StringProperty(name="splint target", default = "", description="Get the splint target model")
    splint_cutter_prop : StringProperty(name="splint cutter", default = "", description="Get the splint cutter")
    splint_thikness_prop : FloatProperty(description="Enter splint thikness", default= 2, step=10, precision=2, unit='LENGTH', min=0.5)

    #Add 3D text props :
    ###########################################################################################
    text_body_prop : StringProperty(name="text body", default = 'Input Text', description="Store the text body", update=text_body_update)
    font_size_prop : FloatProperty(description="Set Font size", default= 5.0, step=10, precision=2, min=1.0)
    text_ob_name : StringProperty(name="text object name", description="Store the text object name")
    target_model_name: StringProperty(name="target object name", description="Store the target object name")
    bold_toggle_prop : BoolProperty(description="Bold text toggle ", default=False, update=text_bold_toggle)
    italic_toggle_prop : BoolProperty(description="italic text toggle ", default=False, update=text_italic_toggle)
    underline_toggle_prop : BoolProperty(description="underline text toggle ", default=False, update=text_underline_toggle)









classes = [
    ODC_modops_props,
]


def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.ODC_modops_props = bpy.props.PointerProperty(type=ODC_modops_props)
    


def unregister():
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.ODC_modops_props
    