"""
Copyright (C) 2015 Patrick Moore
patrick.moore.bu@gmail.com


Created by Patrick Moore

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
"""

bl_info = {
    "name": "Cut Mesh",
    "description": "Tools for cutting and trimming mesh objects",
    "author": "Patrick Moore",
    "version": (0, 0, 1),
    "blender": (2, 81, 0),
    "location": "View 3D > Tool Shelf",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",  # TODO update for b280 branch
    "tracker_url": "",  # TODO update for 280 branch
    "category": "3D View",
}

# Blender imports
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import (
    StringProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)

# TODO Preferences
# TODO Menu

# Tools
from .op_polytrim.polytrim import CutMesh_Polytrim


# addon preferences
class CutMeshPreferences(AddonPreferences):
    bl_idname = __name__

    # Segmentation Editor Behavior
    spline_preview_tess: IntProperty(
        name="Spline Teseslation", default=20, min=3, max=100
    )
    sketch_fit_epsilon: FloatProperty(
        name="Sketch Epsilon", default=0.25, min=0.001, max=10
    )
    patch_boundary_fit_epsilon: FloatProperty(
        name="Boundary Epsilon", default=0.35, min=0.001, max=10
    )
    spline_tessellation_epsilon: FloatProperty(
        name="Spline Epsilon", default=0.1, min=0.001, max=10
    )

    destructive: EnumProperty(
        name="Geometry Mode",
        items=[
            ("DESTRUCTIVE", "DESTRUCTIVE", "DESTRUCTIVE"),
            ("NON_DESTRUCTIVE", "NON_DESTRUCTIVE", "NON_DESTRUCTIVE"),
        ],
        default="DESTRUCTIVE",
    )
    # 2D Interaction Behavior
    non_man_snap_pxl_rad: IntProperty(
        name="Snap Radius Pixel", default=20, min=5, max=150
    )
    sel_pxl_rad: IntProperty(name="Select Radius Pixel", default=10, min=3, max=100)
    loop_close_pxl_rad = IntProperty(
        name="Select Radius Pixel", default=10, min=3, max=100
    )

    # Menu Colors
    menu_bg_color: FloatVectorProperty(
        name="Mennu Backgrounng Color",
        description="FLoating Menu color",
        min=0,
        max=1,
        default=(0.3, 0.3, 0.3),
        subtype="COLOR",
    )
    menu_border_color: FloatVectorProperty(
        name="Menu Border Color",
        description="FLoating menu border colro",
        min=0,
        max=1,
        default=(0.1, 0.1, 0.1),
        subtype="COLOR",
    )
    deact_button_color: FloatVectorProperty(
        name="Button Color",
        description="Deactivated button color",
        min=0,
        max=1,
        default=(0.5, 0.5, 0.5),
        subtype="COLOR",
    )
    act_button_color: FloatVectorProperty(
        name="Active Button Color",
        description="Activated button color",
        min=0,
        max=1,
        default=(0.2, 0.2, 1),
        subtype="COLOR",
    )

    # Geometry Colors
    act_point_color: FloatVectorProperty(
        name="Active Point Color",
        description="Selected/Active point color",
        min=0,
        max=1,
        default=(0.2, 0.7, 0.2),
        subtype="COLOR",
    )
    act_patch_color: FloatVectorProperty(
        name="Active Patch Color",
        description="Selected/Active patch color",
        min=0,
        max=1,
        default=(0.2, 0.7, 0.2),
        subtype="COLOR",
    )
    spline_default_color: FloatVectorProperty(
        name="Spline Color",
        description="Spline color",
        min=0,
        max=1,
        default=(0.2, 0.2, 0.7),
        subtype="COLOR",
    )
    hint_color: FloatVectorProperty(
        name="Hint Color",
        description="Hint Geometry color",
        min=0,
        max=1,
        default=(0.5, 1, 0.5),
        subtype="COLOR",
    )
    bad_segment_color: FloatVectorProperty(
        name="Active Button Color",
        description="Activated button color",
        min=0,
        max=1,
        default=(1, 0.6, 0.2),
        subtype="COLOR",
    )
    bad_segment_hint_color: FloatVectorProperty(
        name="Bad Segment Hint",
        description="Bad segment hint color",
        min=0,
        max=1,
        default=(1, 0, 0),
        subtype="COLOR",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Cut Mesh Preferences")
        # layout.prop(self, "mat_lib")

        ## Visualization
        row = layout.row(align=True)
        row.label(text="Visualization Settings")

        row = layout.row(align=True)
        row.prop(self, "menu_bg_color")
        row.prop(self, "menu_border_color")
        row.prop(self, "deact_button_color")
        row.prop(self, "act_button_color")

        ## Operator Defaults
        # box = layout.box().column(align=False)
        row = layout.row()
        row.label(text="Operator Defaults")


# ...This properties do not exist yet so i comment code lines..............................................

# ##### Fit and Thickness ####
# row = layout.row()
# row.label(text="Thickness, Fit and Retention")
# row = layout.row()
# row.prop(self, "def_shell_thickness")
# row.prop(self, "def_passive_radius")
# row.prop(self, "def_blockout_radius")


def register():
    bpy.utils.register_class(CutMeshPreferences)  # TODO
    # bpy.utils.register_class(CutMesh_panel)  #TODO
    # bpy.utils.register_class(CutMesh_menu)  #TODO
    bpy.utils.register_class(CutMesh_Polytrim)


def unregister():
    bpy.utils.unregister_class(CutMeshPreferences)  # TODO
    # bpy.utils.register_class(CutMesh_panel)  #TODO
    # bpy.utils.register_class(CutMesh_menu)  #TODO
    bpy.utils.unregister_class(CutMesh_Polytrim)


# class polytrimPanel(bpy.types.Panel):
#     bl_label = "Cut Mesh Tools"
#     bl_idname = "cut_mesh_panel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "CutMesh"
#     bl_context = ""

#     def draw(self, context):

#         layout = self.layout
#         layout.label(text="Mesh Cut")

#         row = layout.row()
#         row.operator("cut_mesh.polytrim")


############################################################################################
# Registration :
############################################################################################

addon_modules = []

classes = [CutMesh_Polytrim, CutMeshPreferences]


# Registration :
def register():
    for module in addon_modules:
        module.register()

    for cl in classes:
        bpy.utils.register_class(cl)


def unregister():

    for cl in classes:
        bpy.utils.unregister_class(cl)

    for module in reversed(addon_modules):
        module.unregister()


if __name__ == "__main__":
    register()
