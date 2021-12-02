#!/usr/bin/env python
# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
#
#   dia_app.py ..  dia application, a gui mock
#
# for dia  see https://sosie-js.github.io/python-dia/mock/
#  version 1.3
#  This version adds gui to dia mock
#
# Copyright (C) 2021 sos-productions,  SoSIe <sosie@sos-productions.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

#Adapted From https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtkapplicationwindow.html#Example

from  logging import warnings
import sys, os
from gtk_zeroconfig import *

PROGRAM_NAME="Gui Plugin for Python-Dia"
VERSION="1.3"
LOGO= "diamock_logo.png"

LICENSE="LGPL3"
LICENSE_TEXT="""
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public License as
published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with the Gnome Library; see the file COPYING.LIB.  If not,
write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""


COPYRIGHT=LICENSE+" - using "+ui_support+ " for "+ui_lib+str(ui_lib_version_info)
AUTHORS=["Chris Daley(chebizarro)","Hans Breuer","Olivier Lutzwiller(SoSie)","Philip Kromer(dumpObj)","Zander Brown(dia)"] 
DOCUMENTORS=["Olivier Lutzwiller(SoSie)"]
COMMENTS="Dia Gui for Python "+str(python_version_info)

if "linux" in sys.platform :
    COMMENTS+="\nUse generate_run_with_dia_env.sh to set environ to:"
    COMMENTS+="\nDIA_BIN_PATH="+DIA_BIN_PATH   
    COMMENTS+="\nDIA_LIB_PATH="+DIA_LIB_PATH
    COMMENTS+="\nDIA_BASE_PATH="+DIA_BASE_PATH
    COMMENTS+="\nPYTHONPATH="+ PYTHONPATH

WEBSITE="https://sosie-js.github.io/python-dia/gui/"   
   



#====
infobar = None
window = None
messagelabel = None
_demoapp = None


def widget_destroy(widget, button):
    widget.destroy()


def activate_action(action, user_data=None):
    global window

    name = action.get_name()
    _type = type(action)
    if name == 'DarkTheme':
        value = action.get_active()
        settings = Gtk.Settings.get_default()
        settings.set_property('gtk-application-prefer-dark-theme', value)
        return

    dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.CLOSE,
                               text='You activated action: "%s" of type %s' % (name, _type))

    # FIXME: this should be done in the constructor
    dialog.set_transient_for(window)
    dialog.connect('response', widget_destroy)
    dialog.show()


def activate_radio_action(action, current, user_data=None):
    global infobar
    global messagelabel

    name = current.get_name()
    _type = type(current)
    active = current.get_active()
    value = current.get_current_value()
    if active:
        text = 'You activated radio action: "%s" of type %s.\n Current value: %d' % (name, _type, value)
        messagelabel.set_text(text)
        infobar.set_message_type(Gtk.MessageType(value))
        infobar.show()


def update_statusbar(buffer, statusbar):
    statusbar.pop(0)
    count = buffer.get_char_count()

    iter = buffer.get_iter_at_mark(buffer.get_insert())
    row = iter.get_line()
    col = iter.get_line_offset()
    msg = 'Cursor at row %d column %d - %d chars in document' % (row, col, count)

    statusbar.push(0, msg)


def mark_set_callback(buffer, new_location, mark, data):
    update_statusbar(buffer, data)





verbose = 0


DIA_STOCK_GROUP = "dia-stock-group"
DIA_STOCK_UNGROUP ="dia-stock-ungroup"
DIA_STOCK_LAYER_ADD ="dia-stock-layer-add"
DIA_STOCK_LAYER_RENAME ="dia-stock-layer-rename"
DIA_STOCK_OBJECTS_LAYER_ABOVE ="dia-stock-objects-layer-above"
DIA_STOCK_OBJECTS_LAYER_BELOW ="dia-stock-objects-layer-below"
DIA_STOCK_LAYERS ="dia-stock-layers"

def _add_stock_icon_name(factory, name, icon):

    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(dirname,'app','icons', icon+'.png')
    
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
    transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
    icon_set = Gtk.IconSet.new_from_pixbuf(transparent)

    factory.add(name, icon_set)


def register_stock_icons():
    """
    This function registers our custom toolbar icons, so they can be themed.
    It's totally optional to do this, you could just manually insert icons
    and have them not be themeable, especially if you never expect people
    to theme your app.
    """

    factory = Gtk.IconFactory()
    factory.add_default()

    _add_stock_icon_name (factory, DIA_STOCK_GROUP, "dia-group");
    _add_stock_icon_name (factory, DIA_STOCK_UNGROUP, "dia-ungroup");
    _add_stock_icon_name (factory, DIA_STOCK_LAYER_ADD, "dia-layer-add");
    _add_stock_icon_name (factory, DIA_STOCK_LAYER_RENAME, "dia-layer-rename");
    _add_stock_icon_name (factory, DIA_STOCK_OBJECTS_LAYER_ABOVE, "dia-layer-move-above");
    _add_stock_icon_name (factory, DIA_STOCK_OBJECTS_LAYER_BELOW, "dia-layer-move-below");
    _add_stock_icon_name (factory, DIA_STOCK_LAYERS, "dia-layers");

    _add_stock_icon_name (factory,"dia-gui-logo","diamock_logo")

register_stock_icons()

# Integrated UI Toolbar Constants 
"""
DIA_INTEGRATED_TOOLBAR_ZOOM_COMBO  ="dia-integrated-toolbar-zoom-combo_entry"
DIA_INTEGRATED_TOOLBAR_SNAP_GRID  = "dia-integrated-toolbar-snap-grid"
DIA_INTEGRATED_TOOLBAR_OBJECT_SNAP ="dia-integrated-toolbar-object-snap"
DIA_INTEGRATED_TOOLBAR_GUIDES_SNAP = "dia-integrated-toolbar-guides-snap"
"""


HAVE_MAC_INTEGRATION= False

def   FIRST_MODIFIER():
    if HAVE_MAC_INTEGRATION:
                FIRST_MODIFIER = "<Primary>"
    else:
                FIRST_MODIFIER = "<Control>"
    return FIRST_MODIFIER
    
def TOOL_MODIFIER():
    if HAVE_MAC_INTEGRATION:
        #/* On OSX/Quartz the unmodified tool accelerators are in conflict with the global menu */
        TOOL_MODIFIER = "<Control>"
    else:
        TOOL_MODIFIER = ""
    return TOOL_MODIFIER

def N_(sentence):
    return sentence

def CALLBACK(func_name, widget):
    if func_name in globals():
        globals()[func_name](widget)
    else:
        print(func_name)

def G_CALLBACK(func_name):
    return lambda widget: CALLBACK(func_name, widget)

menubar_action_entries= (
  ( "File", None, N_("_File"), None, None, None ),
    ( "FileNew", Gtk.STOCK_NEW, N_("_New"), "<Control>N", N_("Create a new diagram"), G_CALLBACK("file_new_callback") ),
    ( "FileOpen", Gtk.STOCK_OPEN, N_("_Open..."), "<Control>O", N_("Open a diagram file"), G_CALLBACK("file_open_callback") ),
    ( "FileQuit", Gtk.STOCK_QUIT, N_("_Quit"), "<Control>Q", N_("Quit Dia"), G_CALLBACK("file_quit_callback") ),
  ( "Help", None, N_("_Help"), None, None, None ),
    ( "HelpContents", Gtk.STOCK_HELP, N_("_Help"), "F1", N_("Dia help"), G_CALLBACK("help_manual_callback") ),
    ( "HelpAbout", Gtk.STOCK_ABOUT, N_("_About"), None, N_("Dia version, authors, license"), G_CALLBACK("help_about_callback") ),
    ( "FileSheets", None, N_("S_heets and Objects"), "F9", N_("Manage sheets and their objects"), G_CALLBACK("sheets_dialog_show_callback") ),
    ( "FilePrefs", Gtk.STOCK_PREFERENCES, N_("P_references"), None, N_("Dia preferences"), G_CALLBACK("file_preferences_callback") ),
    ( "FilePlugins", None, N_("P_lugins..."), None, N_("Manage plug-ins"), G_CALLBACK("file_plugins_callback") ),
    ( "FileTree", None, N_("Diagram _Tree"), "F8", N_("Tree representation of diagrams"), G_CALLBACK("diagram_tree_show") ),
    ( "FileSave", Gtk.STOCK_SAVE, N_("_Save"), "<Control>S", N_("Save the diagram"), G_CALLBACK("file_save_callback") ),
    ( "FileSaveas", Gtk.STOCK_SAVE_AS, N_("Save _As..."), "<Control><shift>S", N_("Save the diagram with a new name"), G_CALLBACK("file_save_as_callback") ),
    ( "FileExport", Gtk.STOCK_CONVERT, N_("_Export..."), None, N_("Export the diagram"), G_CALLBACK("file_export_callback") ),
    ( "DiagramProperties", Gtk.STOCK_PROPERTIES, N_("_Diagram Properties"), "<shift><alt>Return", N_("Modify diagram properties (grid, background)"), G_CALLBACK("view_diagram_properties_callback") ),
    ( "FilePagesetup", None, N_("Page Set_up..."), None, N_("Modify the diagram pagination"), G_CALLBACK("file_pagesetup_callback") ),
    ( "FilePrint", Gtk.STOCK_PRINT, N_("_Print..."), "<Control>P", N_("Print the diagram"), G_CALLBACK("file_print_callback") ),
    ( "FileClose", Gtk.STOCK_CLOSE, N_("_Close"), "<Control>W", N_("Close the diagram"), G_CALLBACK("file_close_callback") ),
  ( "Edit", None, N_("_Edit"), None, None, None ),
    ( "EditUndo", Gtk.STOCK_UNDO, N_("_Undo"), "<Control>Z", N_("Undo"), G_CALLBACK("edit_undo_callback") ),
    ( "EditRedo", Gtk.STOCK_REDO, N_("_Redo"), "<Control><shift>Z", N_("Redo"), G_CALLBACK("edit_redo_callback") ),
    ( "EditCopy", Gtk.STOCK_COPY, N_("_Copy"), "<Control>C", N_("Copy selection"), G_CALLBACK("edit_copy_callback") ),
    ( "EditCut", Gtk.STOCK_CUT, N_("Cu_t"), "<Control>X", N_("Cut selection"), G_CALLBACK("edit_cut_callback") ),
    ( "EditPaste", Gtk.STOCK_PASTE, N_("_Paste"), "<Control>V", N_("Paste selection"), G_CALLBACK("edit_paste_callback") ),
    ( "EditDuplicate", None, N_("_Duplicate"), "<Control>D", N_("Duplicate selection"), G_CALLBACK("edit_duplicate_callback") ),
    ( "EditDelete", Gtk.STOCK_DELETE, N_("D_elete"), "Delete", N_("Delete selection"), G_CALLBACK("edit_delete_callback") ),
    ( "EditFind", Gtk.STOCK_FIND, N_("_Find..."), "<Control>F", N_("Search for text"), G_CALLBACK("edit_find_callback") ),
    ( "EditReplace", Gtk.STOCK_FIND_AND_REPLACE, N_("_Replace..."), "<Control>H", N_("Search and replace text"), G_CALLBACK("edit_replace_callback") ),
    ( "EditCopytext", None, N_("C_opy Text"), None, N_("Copy object's text to clipboard"), G_CALLBACK("edit_copy_text_callback") ),
    ( "EditCuttext", None, N_("C_ut Text"), "<Control><shift>X", N_("Cut object's text to clipboard"), G_CALLBACK("edit_cut_text_callback") ),
    ( "EditPastetext", None, N_("P_aste Text"), "<Control><shift>V", N_("Insert text from clipboard"), G_CALLBACK("edit_paste_text_callback") ) ,
    ( "EditPasteImage", None, N_("Paste _Image"), "<Control><alt>V", N_("Insert image from clipboard"), G_CALLBACK("edit_paste_image_callback") ),
  ( "Layers", None, N_("_Layers"), None, None, None ),
    ( "LayerAdd", DIA_STOCK_LAYER_ADD, N_("_Add Layer..."), None, None, G_CALLBACK("layers_add_layer_callback") ),
    ( "LayerRename", DIA_STOCK_LAYER_RENAME, N_("_Rename Layer..."), None, None, G_CALLBACK("layers_rename_layer_callback") ),
    ( "ObjectsLayerAbove", DIA_STOCK_OBJECTS_LAYER_ABOVE, N_("_Move Selection to Layer above"), None, None, G_CALLBACK("objects_move_up_layer") ),
    ( "ObjectsLayerBelow", DIA_STOCK_OBJECTS_LAYER_BELOW, N_("Move _Selection to Layer below"), None, None, G_CALLBACK("objects_move_down_layer") ),
    ( "DiagramLayers", DIA_STOCK_LAYERS, N_("_Layers..."), "<Control>L", None, G_CALLBACK("dialogs_layers_callback") ),
  ( "View", None, N_("_View"), None, None, None ),
    ( "ViewZoomin", Gtk.STOCK_ZOOM_IN, N_("Zoom _In"), "<Control>plus", N_("Zoom in"), G_CALLBACK("view_zoom_in_callback") ),
    ( "ViewZoomout", Gtk.STOCK_ZOOM_OUT, N_("Zoom _Out"), "<Control>minus", N_("Zoom out"), G_CALLBACK("view_zoom_out_callback") ),
    ( "ViewZoom", None, N_("_Zoom"), None, None, None ),
      ( "ViewZoom16000", None, N_("1600%"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom8000", None, N_("800%"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom4000", None, N_("400%"), "<alt>4", None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom2830", None, N_("283"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom2000", None, N_("200"), "<alt>2", None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom1410", None, N_("141"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom1000", Gtk.STOCK_ZOOM_100, N_("_Normal Size"), "<alt>1", None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom850", None, N_("85"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom707", None, N_("70.7"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom500", None, N_("50"), "<alt>5", None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom354", None, N_("35.4"), None, None, G_CALLBACK("view_zoom_set_callback") ),
      ( "ViewZoom250", None, N_("25"), None, None, G_CALLBACK("view_zoom_set_callback") ),
    ( "ViewShowall", Gtk.STOCK_ZOOM_FIT, N_("Best _Fit"), "<Control>E", N_("Zoom fit"), G_CALLBACK("view_show_all_callback") ),
    ( "ViewNewview", None, N_("New _View"), None, None, G_CALLBACK("view_new_view_callback") ),
    ( "ViewCloneview", None, N_("C_lone View"), None, None, G_CALLBACK("view_clone_view_callback") ),
    ( "ViewRedraw", Gtk.STOCK_REFRESH, N_("_Refresh"), None, None, G_CALLBACK("view_redraw_callback") ),
    ( "ViewGuides", None, N_("_Guides"), None, None, None ),
      ( "ViewNewguide", None, N_("_New Guide..."), None, None, G_CALLBACK("view_new_guide_callback") ),
  ( "Objects", None, N_("_Objects"), None, None ),
    ( "ObjectsSendtoback", Gtk.STOCK_GOTO_BOTTOM, N_("Send to _Back"), "<Control><shift>B", N_("Move selection to the bottom"), G_CALLBACK("objects_place_under_callback") ),
    ( "ObjectsBringtofront", Gtk.STOCK_GOTO_TOP, N_("Bring to _Front"), "<Control><shift>F", N_("Move selection to the top"), G_CALLBACK("objects_place_over_callback") ),
    ( "ObjectsSendbackwards", Gtk.STOCK_GO_DOWN, N_("Send Ba_ckwards"), None, None, G_CALLBACK("objects_place_down_callback") ),
    ( "ObjectsBringforwards", Gtk.STOCK_GO_UP, N_("Bring F_orwards"), None, None, G_CALLBACK("objects_place_up_callback") ),
    ( "ObjectsGroup", DIA_STOCK_GROUP, N_("_Group"), "<Control>G", N_("Group selected objects"), G_CALLBACK("objects_group_callback") ),
    ( "ObjectsUngroup", DIA_STOCK_UNGROUP, N_("_Ungroup"), "<Control><shift>G", N_("Ungroup selected groups"), G_CALLBACK("objects_ungroup_callback") ),
    ( "ObjectsParent", None, N_("_Parent"), "<Control>K", None, G_CALLBACK("objects_parent_callback") ),
    ( "ObjectsUnparent", None, N_("_Unparent"), "<Control><shift>K", None, G_CALLBACK("objects_unparent_callback") ),
    ( "ObjectsUnparentchildren", None, N_("_Unparent Children"), None, None, G_CALLBACK("objects_unparent_children_callback") ),
    ( "ObjectsAlign", None, N_("_Align"), None, None, None ),
      ( "ObjectsAlignLeft", Gtk.STOCK_JUSTIFY_LEFT, N_("_Left"), "<alt><shift>L", None, G_CALLBACK("objects_align_h_callback") ),
      ( "ObjectsAlignCenter", Gtk.STOCK_JUSTIFY_CENTER, N_("_Center"), "<alt><shift>C", None, G_CALLBACK("objects_align_h_callback") ),
      ( "ObjectsAlignRight", Gtk.STOCK_JUSTIFY_RIGHT, N_("_Right"), "<alt><shift>R", None, G_CALLBACK("objects_align_h_callback") ),
      ( "ObjectsAlignTop", None, N_("_Top"), "<alt><shift>T", None, G_CALLBACK("objects_align_v_callback") ),
      ( "ObjectsAlignMiddle", None, N_("_Middle"), "<alt><shift>M", None, G_CALLBACK("objects_align_v_callback") ),
      ( "ObjectsAlignBottom", None, N_("_Bottom"), "<alt><shift>B", None, G_CALLBACK("objects_align_v_callback") ),
      ( "ObjectsAlignSpreadouthorizontally", None, N_("Spread Out _Horizontally"), "<alt><shift>H", None, G_CALLBACK("objects_align_h_callback") ),
      ( "ObjectsAlignSpreadoutvertically", None, N_("Spread Out _Vertically"), "<alt><shift>V", None, G_CALLBACK("objects_align_v_callback") ),
      ( "ObjectsAlignAdjacent", None, N_("_Adjacent"), "<alt><shift>A", None, G_CALLBACK("objects_align_h_callback") ),
      ( "ObjectsAlignStacked", None, N_("_Stacked"), "<alt><shift>S", None, G_CALLBACK("objects_align_v_callback") ),
      ( "ObjectsAlignConnected", None, N_("_Connected"), "<alt><shift>O", None, G_CALLBACK("objects_align_connected_callback") ),
      ( "ObjectsProperties", Gtk.STOCK_PROPERTIES, N_("_Properties"), "<alt>Return", None, G_CALLBACK("dialogs_properties_callback") ),
  ( "Select", None, N_("_Select"), None, None, None ),
    ( "SelectAll", None, N_("_All"), "<Control>A", None, G_CALLBACK("select_all_callback") ),
    ( "SelectNone", None, N_("_None"), "<Control><shift>A", None, G_CALLBACK("select_none_callback") ),
    ( "SelectInvert", None, N_("_Invert"), "<Control>I", None, G_CALLBACK("select_invert_callback") ),
    ( "SelectTransitive", None, N_("_Transitive"), "<Control>T", None, G_CALLBACK("select_transitive_callback") ),
    ( "SelectConnected", None, N_("_Connected"), "<Control><shift>T", None, G_CALLBACK("select_connected_callback") ),
    ( "SelectSametype", None, N_("Same _Type"), None, None, G_CALLBACK("select_same_type_callback") ),
    ( "SelectBy", None, N_("_Select By"), None, None, None ),
  ( "Layout", None, N_("L_ayout"), None, None, None ),
  ( "Dialogs", None, N_("D_ialogs"), None, None, None ),
  ( "Debug", None, N_("D_ebug"), None, None, None ),
  ( "Tools", None, N_("_Tools"), None, None, None ),
    ( "ToolsModify", None, N_("_Modify"), "N", None, None ),
    ( "ToolsMagnify", None, N_("_Magnify"), "M", None, None ),
    ( "ToolsTextedit", None, N_("_Edit Text"), "F2", None, None ),
    ( "ToolsScroll", None, N_("_Scroll"), "S", None, None ),
    ( "ToolsText", None, N_("_Text"), "T", None, None ),
    ( "ToolsBox", None, N_("_Box"), "R", None, None ),
    ( "ToolsEllipse", None, N_("_Ellipse"), "E", None, None ),
    ( "ToolsPolygon", None, N_("_Polygon"), "P", None, None ),
    ( "ToolsBeziergon", None, N_("_Beziergon"), "B", None, None ),
    ( "ToolsLine", None, N_("_Line"), "L", None, None ),
    ( "ToolsArc", None, N_("_Arc"), "A", None, None ),
    ( "ToolsZigzagline", None, N_("_Zigzagline"), "Z", None, None ),
    ( "ToolsPolyline", None, N_("_Polyline"), "Y", None ),
    ( "ToolsBezierline", None, N_("_Bezierline"), "C", None, None ),
    ( "ToolsOutline", None, N_("_Outline"), "O", None, None ),
    ( "ToolsImage", None, N_("_Image"), "I", None, None ),
    ( "ViewFullscreen", Gtk.STOCK_FULLSCREEN, N_("_Fullscreen"), "F11", None, G_CALLBACK("view_fullscreen_callback") ),
    ( "ViewAntialiased", None, N_("_Antialiased"), None, None, G_CALLBACK("view_aa_callback") ),
    ( "ViewShowgrid", None, N_("Show _Grid"), None, None, G_CALLBACK("view_visible_grid_callback") ),
    ( "ViewSnaptogrid", None, N_("_Snap to Grid"), None, None, G_CALLBACK("view_snap_to_grid_callback") ),
    ( "ViewShowguides", None, N_("_Show Guides"), None, None, G_CALLBACK("view_visible_guides_callback") ),
    ( "ViewSnaptoguides", None, N_("Snap to _Guides"), None, None, G_CALLBACK("view_snap_to_guides_callback") ),
    ( "ViewRemoveallguides", None, N_("_Remove all Guides"), None, None, G_CALLBACK("view_remove_all_guides_callback") ),
    ( "ViewSnaptoobjects", None, N_("Snap to _Objects"), None, None, G_CALLBACK("view_snap_to_objects_callback") ),
    ( "ViewShowrulers", None, N_("Show _Rulers"), None, None, G_CALLBACK("view_toggle_rulers_callback")  ),
    ( "ViewShowscrollbars", None, N_("Show Scroll_bars"), None, N_("Show or hide the toolbar"), G_CALLBACK("view_toggle_scrollbars_callback") ),
    ( "ViewShowconnectionpoints", None, N_("Show _Connection Points"), None, None, G_CALLBACK("view_show_cx_pts_callback") ),
  ( "SelectReplace", None, N_("_Replace"), None, None, G_CALLBACK("SELECT_REPLACE")  ),
  ( "SelectUnion", None, N_("_Union"), None, None, G_CALLBACK("SELECT_UNION")  ),
  ( "SelectIntersection", None, N_("I_ntersection"), None, None, G_CALLBACK("SELECT_INTERSECTION")  ),
  ( "SelectRemove", None, N_("R_emove"), None, None, G_CALLBACK("SELECT_REMOVE")  ),
  ( "SelectInverse", None, N_("In_verse"), None, None, G_CALLBACK("SELECT_INVERT")  )
)



toolmenu_action_entries =  (
    ("FileMenu", None, "_File"),                # name, stock id, label
    ("OpenMenu", None, "_Open"),                # name, stock id, label
    ("PreferencesMenu", None, "_Preferences"),  # name, stock id, label
    ("ColorMenu", None, "_Color"),              # name, stock id, label
    ("ShapeMenu", None, "_Shape"),              # name, stock id, label
    ("HelpMenu", None, "_Help"),                # name, stock id, label
    ("New", Gtk.STOCK_NEW,                      # name, stock id
     "_New", "<control>N",                      # label, accelerator
     "Create a new file",                       # tooltip
     activate_action),
    ("File1", None,                             # name, stock id
     "File1", None,                             # label, accelerator
     "Open first file",                         # tooltip
     activate_action),
    ("Save", Gtk.STOCK_SAVE,                    # name, stock id
     "_Save", "<control>S",                     # label, accelerator
     "Save current file",                       # tooltip
     activate_action),
    ("SaveAs", Gtk.STOCK_SAVE,                  # name, stock id
     "Save _As...", None,                       # label, accelerator
     "Save to a file",                          # tooltip
     activate_action),
    ("Quit", Gtk.STOCK_QUIT,                    # name, stock id
     "_Quit", "<control>Q",                     # label, accelerator
     "Quit",                                    # tooltip
     activate_action),
    ("About", None,                             # name, stock id
     "_About", "<control>A",                    # label, accelerator
     "About",                                   # tooltip
     activate_action),
    ("Logo", "demo-gtk-logo",                   # name, stock id
     None, None,                                # label, accelerator
     "GTK+",                                    # tooltip
     activate_action),
)

ui_info_toolbar="""
<ui>
  <toolbar name='ToolBar'>
    <toolitem action='Open'>
      <menu action='OpenMenu'>
        <menuitem action='File1'/>
      </menu>
    </toolitem>
    <toolitem action='Quit'/>
    <separator action='Sep1'/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>
"""


toolmenu_toggle_action_entries = (
    ("Bold", Gtk.STOCK_BOLD,                    # name, stock id
     "_Bold", "<control>B",                     # label, accelerator
     "Bold",                                    # tooltip
     activate_action,
     True),                                     # is_active
    ("DarkTheme", None,                         # name, stock id
     "_Prefer Dark Theme", None,                # label, accelerator
     "Prefer Dark Theme",                       # tooltip
     activate_action,
     False),                                    # is_active
)

(COLOR_RED,
 COLOR_GREEN,
 COLOR_BLUE) = range(3)

toolmenu_color_action_entries = (
    ("Red", None,                               # name, stock id
     "_Red", "<control>R",                      # label, accelerator
     "Blood", COLOR_RED),                       # tooltip, value
    ("Green", None,                             # name, stock id
     "_Green", "<control>G",                    # label, accelerator
     "Grass", COLOR_GREEN),                     # tooltip, value
    ("Blue", None,                              # name, stock id
     "_Blue", "<control>B",                     # label, accelerator
     "Sky", COLOR_BLUE),                        # tooltip, value
)

(SHAPE_SQUARE,
 SHAPE_RECTANGLE,
 SHAPE_OVAL) = range(3)

toolmenu_shape_action_entries = (
    ("Square", None,                            # name, stock id
     "_Square", "<control>S",                   # label, accelerator
     "Square", SHAPE_SQUARE),                   # tooltip, value
    ("Rectangle", None,                         # name, stock id
     "_Rectangle", "<control>R",                # label, accelerator
     "Rectangle", SHAPE_RECTANGLE),             # tooltip, value
    ("Oval", None,                              # name, stock id
     "_Oval", "<control>O",                     # label, accelerator
     "Egg", SHAPE_OVAL),                        # tooltip, value
)


ui_menubar="/usr/share/dia/ui/display-ui.xml"
ui_menubar_info = """
<ui>
	<menubar name="DisplayMenu">
		<menu name="File" action="File">
			<menuitem name="FileNew" action="FileNew" />
			<menuitem name="FileOpen" action="FileOpen" />
			<separator name="FileSep1" />
			<menuitem name="FileSave" action="FileSave" />
			<menuitem name="FileSaveas" action="FileSaveas" />
			<menuitem name="FileExport" action="FileExport" />
			<separator name="FileSep2 "/>
			<menuitem name="DiagramProperties" action="DiagramProperties" />
			<menuitem name="FilePagesetup" action="FilePagesetup" />
			<menuitem name="FilePrint" action="FilePrint" />
			<separator name="FileSep3" />
			<menuitem name="FileClose" action="FileClose" />
			<menuitem name="FileQuit" action="FileQuit" />
			<separator name="FileSep4" />
			<separator name="FileExtensionStart" />
		</menu>
		<menu name="Edit" action="Edit">
			<menuitem name="EditUndo" action="EditUndo" />
			<menuitem name="EditRedo" action="EditRedo" />
			<separator name="EditSep1" />
			<menuitem name="EditCopy" action="EditCopy" />
			<menuitem name="EditCut" action="EditCut" />
			<menuitem name="EditPaste" action="EditPaste" />
			<menuitem name="EditDuplicate" action="EditDuplicate" />
			<menuitem name="EditDelete" action="EditDelete" />
			<separator name="EditSep2" />
			<menuitem name="EditFind" action="EditFind" />
			<menuitem name="EditReplace" action="EditReplace" />
			<separator name="EditSep3" />
			<menuitem name="EditCopytext" action="EditCopytext" />
			<menuitem name="EditCuttext" action="EditCuttext" />
			<menuitem name="EditPastetext" action="EditPastetext" />
			<separator name="EditSep4" />
			<menuitem name="EditPasteImage" action="EditPasteImage" />
			<separator name="EditExtensionStart" />
		</menu>
		<menu name="View" action="View">
			<menuitem name="ViewZoomin" action="ViewZoomin" />
			<menuitem name="ViewZoomout" action="ViewZoomout" />
			<menu name="ViewZoom" action="ViewZoom">
				<menuitem name="ViewZoom16000" action="ViewZoom16000" />
				<menuitem name="ViewZoom8000" action="ViewZoom8000" />
				<menuitem name="ViewZoom4000" action="ViewZoom4000" />
				<menuitem name="ViewZoom2830" action="ViewZoom2830" />
				<menuitem name="ViewZoom2000" action="ViewZoom2000" />
				<menuitem name="ViewZoom1410" action="ViewZoom1410" />
				<menuitem name="ViewZoom1000" action="ViewZoom1000" />
				<menuitem name="ViewZoom850" action="ViewZoom850" />
				<menuitem name="ViewZoom707" action="ViewZoom707" />
				<menuitem name="ViewZoom500" action="ViewZoom500" />
				<menuitem name="ViewZoom354" action="ViewZoom354" />
				<menuitem name="ViewZoom250" action="ViewZoom250" />
			</menu>
			<menuitem name="ViewShowall" action="ViewShowall" />
			<separator name="ViewSep1" />
			<menuitem name="ViewFullscreen" action="ViewFullscreen" />
			<menuitem name="ViewAntialiased" action="ViewAntialiased" />
			<menuitem name="ViewShowgrid" action="ViewShowgrid" />
			<menuitem name="ViewSnaptogrid" action="ViewSnaptogrid" />
			<menuitem name="ViewSnaptoobjects" action="ViewSnaptoobjects" />
			<menuitem name="ViewShowrulers" action="ViewShowrulers" />
			<menuitem name="ViewShowconnectionpoints" action="ViewShowconnectionpoints" />
			<separator name="ViewSep2" />
			<menuitem name="ViewNewview" action="ViewNewview" />
			<menuitem name="ViewCloneview" action="ViewCloneview" />
			<menuitem name="ViewRedraw" action="ViewRedraw" />
			<separator name="ViewSep3" />
			<separator name="ViewExtensionStart" />
		</menu>
		<menu name="Layers" action="Layers">
			<menuitem name="LayerAdd" action="LayerAdd" />
			<menuitem name="LayerRename" action="LayerRename" />
			<separator name="LayersSep1" />
			<menuitem name="ObjectsLayerAbove" action="ObjectsLayerAbove" />
			<menuitem name="ObjectsLayerBelow" action="ObjectsLayerBelow" />
			<separator name="LayersSep2" />
			<menuitem name="DiagramLayers" action="DiagramLayers" />
		</menu>
		<menu name="Objects" action="Objects">
			<menuitem name="ObjectsSendtoback" action="ObjectsSendtoback" />
			<menuitem name="ObjectsBringtofront" action="ObjectsBringtofront" />
			<menuitem name="ObjectsSendbackwards" action="ObjectsSendbackwards" />
			<menuitem name="ObjectsBringforwards" action="ObjectsBringforwards" />
			<separator name="ObjectsSep1" />
			<menuitem name="ObjectsGroup" action="ObjectsGroup" />
			<menuitem name="ObjectsUngroup" action="ObjectsUngroup" />
			<separator name="ObjectsSep2" />
			<menuitem name="ObjectsParent" action="ObjectsParent" />
			<menuitem name="ObjectsUnparent" action="ObjectsUnparent" />
			<menuitem name="ObjectsUnparentchildren" action="ObjectsUnparentchildren" />
			<separator name="ObjectsSep3" />
			<menu name="ObjectsAlign" action="ObjectsAlign">
				<menuitem name="ObjectsAlignLeft" action="ObjectsAlignLeft" />
				<menuitem name="ObjectsAlignCenter" action="ObjectsAlignCenter" />
				<menuitem name="ObjectsAlignRight" action="ObjectsAlignRight" />
				<separator name="ObjectsAlignSep1" />
				<menuitem name="ObjectsAlignTop" action="ObjectsAlignTop" />
				<menuitem name="ObjectsAlignMiddle" action="ObjectsAlignMiddle" />
				<menuitem name="ObjectsAlignBottom" action="ObjectsAlignBottom" />
				<separator name="ObjectsAlignSep2" />
				<menuitem name="ObjectsAlignSpreadouthorizontally" action="ObjectsAlignSpreadouthorizontally" />
				<menuitem name="ObjectsAlignSpreadoutvertically" action="ObjectsAlignSpreadoutvertically" />
				<menuitem name="ObjectsAlignAdjacent" action="ObjectsAlignAdjacent" />
				<menuitem name="ObjectsAlignStacked" action="ObjectsAlignStacked" />
				<menuitem name="ObjectsAlignConnected" action="ObjectsAlignConnected" />
			</menu>
			<separator name="ObjectsSep4" />
			<menuitem name="ObjectsProperties" action="ObjectsProperties" />
			<separator name="ObjectsExtensionStart" />
		</menu>
		<menu name="Select" action="Select">
			<menuitem name="SelectAll" action="SelectAll" />
			<menuitem name="SelectNone" action="SelectNone" />
			<menuitem name="SelectInvert" action="SelectInvert" />
			<separator name="SelectSep1" />
			<menuitem name="SelectTransitive" action="SelectTransitive" />
			<menuitem name="SelectConnected" action="SelectConnected" />
			<menuitem name="SelectSametype" action="SelectSametype" />
			<separator name="SelectSep2" />
			<menuitem name="SelectReplace" action="SelectReplace" />
			<menuitem name="SelectUnion" action="SelectUnion" />
			<menuitem name="SelectIntersection" action="SelectIntersection" />
			<menuitem name="SelectRemove" action="SelectRemove" />
			<menuitem name="SelectInverse" action="SelectInverse" />
			<separator name="SelectSep3" />
			<menu name="SelectBy" action="SelectBy">
				<separator name="SelectByExtensionStart" />
			</menu>
			<separator name="SelectSep4" />
			<separator name="SelectExtensionStart" />
		</menu>
		<menu name="Layout" action="Layout">
			<separator name="LayoutExtensionStart" />
		</menu>
		<menu name="Tools" action="Tools">
			<menuitem name="ToolsModify" action="ToolsModify" />
			<menuitem name="ToolsTextedit" action="ToolsTextedit" />
			<menuitem name="ToolsMagnify" action="ToolsMagnify" />
			<menuitem name="ToolsScroll" action="ToolsScroll" />
			<menuitem name="ToolsText" action="ToolsText" />
			<menuitem name="ToolsBox" action="ToolsBox" />
			<menuitem name="ToolsEllipse" action="ToolsEllipse" />
			<menuitem name="ToolsPolygon" action="ToolsPolygon" />
			<menuitem name="ToolsBeziergon" action="ToolsBeziergon" />
			<separator name="ToolsSep1" />
			<menuitem name="ToolsLine" action="ToolsLine" />
			<menuitem name="ToolsArc" action="ToolsArc" />
			<menuitem name="ToolsZigzagline" action="ToolsZigzagline" />
			<menuitem name="ToolsPolyline" action="ToolsPolyline" />
			<menuitem name="ToolsBezierline" action="ToolsBezierline" />
			<menuitem name="ToolsOutline" action="ToolsOutline" />
			<separator name="ToolsSep1" />
			<menuitem name="ToolsImage" action="ToolsImage" />
			<separator name="ToolsSep2" />
			<separator name="ToolsExtensionStart" />
		</menu>
		<menu name="Dialogs" action="Dialogs">
			<separator name="DialogsExtensionStart" />
		</menu>
		<menu name="Debug" action="Debug">
			<separator name="DebugExtensionStart" />
		</menu>
		<menu name="Help" action="Help">
			<menuitem name="HelpContents" action="HelpContents" />
			<separator name="HelpExtensionStart" />
			<separator name="HelpExtensionEnd" />
			<menuitem name="HelpAbout" action="HelpAbout" />
		</menu>
	</menubar>
</ui>"""
  
ui_info_toolbar="""
<ui>
  <toolbar name="Toolbar">
	<toolitem name="FileNew" action="FileNew" />
	<toolitem name="FileOpen" action="FileOpen" />
	<toolitem name="FileSave" action="FileSave" />
	<toolitem name="FileSaveas" action="FileSaveas" />
	<toolitem name="FileExport" action="FileExport" />
	<toolitem name="FilePrint" action="FilePrint" />
	<separator/>
	<toolitem name="EditUndo" action="EditUndo" />
	<toolitem name="EditRedo" action="EditRedo" />
	<toolitem name="EditCopy" action="EditCopy" />
	<toolitem name="EditCut" action="EditCut" />
	<toolitem name="EditPaste" action="EditPaste" />
	<separator/>
	<toolitem name="ViewZoomin" action="ViewZoomin" />
	<toolitem name="ViewShowall" action="ViewShowall" />
	<toolitem name="ViewZoomout" action="ViewZoomout" />
  </toolbar>
</ui>
"""

from lxml import etree

class Gtk_UIManager_plus: 
    
    
    tree = None
    actions = None #will be generated as a template
    widgets=  None
    
    _uim=None
    
    def __init__(self):
        
        """
         menus={
            'menubar:MenuDisplay':[
                {'menu:File':('File':[
                        
                    ]}
                {'menu:Edit':('Edit':[]}
                {'menu:View':('View',[]),
                ('Layers',[]),
                ('Objects',[]),
                ('View',[]),
                ('Tools',[]),
                ('Dialogs',[]),
                ('Debug',[]),
                ('Help',[('About', Gtk.AboutDialog.show_all)])
            ]}
        """
        self._uim= Gtk.UIManager()
        self.tree=None
        self.widgets={}
        self.actions= {} #dict action_name ->  (stock_id, action_label, accel, handler)
   
    def show_tree(self, simplified=False):
        
        tree=str(self.tree).replace("'",'"')
        
        if simplified :
            tree=tree.replace('"menubar:','"')
            tree=tree.replace('"menuitem:','"')
            tree=tree.replace('"menu:','"')
            import re
            tree=re.sub(r'"(separator:[a-zA-Z0-9]+)', '***', tree)
            
       # print(tree)
        
    def _make_entry(self,type,name,value):
        return { type+":"+name :value}
    

    def add_ui_add_from_file(self,UI) :
        
        #remove xml header
        with open(UI, 'r') as fin:
            data = fin.read().splitlines(True)
            content = "".join(data[1:])
            
        self.add_ui_from_string(content)
        
        return content
        
    def add_ui_from_string(self, content) :
        
        self._uim.add_ui_from_string(content)
        
        
    def insert_action_group(self, action_group, pos=0):
        
        self._uim.insert_action_group( action_group, pos)
        
    
    def add_widget(self, widget):
        
        try :
            return self._uim.add_widget(self, widget)
        except AttributeError as e:
            warnings.warn("NonImplemented: 'UIManager' object has no attribute 'add_widget'")
    
    def get_widget(self, widget_name):
        
        return self._uim.get_widget(widget_name)
        
    def get_action_groups(self):
        
        return self._uim.get_action_groups()
        
    def get_accel_group(self):
        
        accelgroup = self._uim.get_accel_group()
        
        return accelgroup
    
    # this is the plus feature to get actions template  from menus ui.
    
    def  parse_ui_content(self,content):
        
        root = etree.XML(content)
        #print(etree.tostring(root, pretty_print=True))
        ui = root
        if ui.tag == 'ui':
            menubar=ui[0]
            if menubar.tag == 'menubar':
                #print(etree.tostring(menubar, pretty_print=True))
                menubar_name=self._get_attribute(menubar, "name")
                menus=self.parse_menus(menubar,"")        
                # { 'menubar:name':[ ...]}               
                self.tree=self._make_entry('menubar', menubar_name,menus)
            
            
         
    def _get_attribute(self, item, name):
        attributes=item.attrib
        attribute=None
        if  name in attributes:
            attribute=attributes["name"]
        return attribute

    def get_actions(self):
        actions=[]
        for action_name, action in self.actions.items():
            actions.append(tuple([action_name])+action)
            
        #import pprint
        #pprint.pprint(actions)
    
        return actions
        
    def parse_menus(self, entries, parent_name):
        sep_number=1
        menus=[]
        for entry in entries: #.getchildren():
                #optional to reach the widget by name?
                entry_name=self._get_attribute(entry, 'name')
                entry_action=self._get_attribute(entry, 'action')
  
                
                #guess action
                #for <menu|menu_item action="<name>"> :
         
                action_label=entry_name.replace(parent_name,'')
                

                if entry.tag == "menu":
                    #print("menu "+entry_action)
                    
                    # action :=  menu : name, stock id, label
                    stock_id= None
                    
                    self.actions[entry_action]=(stock_id, action_label)
                    
                    menus.append(self._make_entry('menu',entry_name,self.parse_menus(entry,parent_name+entry_name)))
                
                elif entry.tag == "menuitem":
                    #print("menuitem "+entry_action)
                    
                    #action = menuitem : name, stock_id or None,  label , accelerator or None, tooltip,handler]           
                    stock_id= None
                    accel= None
                    handler=None
                    self.actions[entry_action]=( stock_id, action_label, accel, handler)              

                    #{ 'menuitem:name':('action_name':()}
                    menus.append(self._make_entry('menuitem',entry_name,entry_action))
                    
                elif  entry.tag == "separator":
                    #print("sep "+entry_name)
                    #{ 'separator':('name':order}
                    menus.append(self._make_entry('separator',entry_name,sep_number))
                    sep_number= sep_number+1
        return menus



#UNUSED FOR NOW
class DiaMockMenubar:
     
    uimanager=None
    name=""
    menubar=None
     
    def __init__(self, menubar_name="DisplayMenu"):
        
        self.name= menubar_name
        
        self.action_group = Gtk.ActionGroup(name="my_actions")
          
    
    def attach(self, window) :      
        
        self.window=window
        
        menubar_name= self.name
        
        self.uimanager=uimanager = self.create_ui_manager(window)
        
        self.menubar = uimanager.get_widget("/"+menubar_name)
        
        
    def get_widget(self):
    
        return self.menubar
    
    def get_menu_entry(self,menu_name):
        
        menubar_name= self.name
        
        return self.uimanager.get_widget("/"+menubar_name+"/"+menu_name) #.get_submenu()

    def add_menus_actions(self):

            action_group = self.action_group
            actions=self.uimanager.get_actions()
            action_group.add_actions(actions)
            
            self.uimanager.insert_action_group( action_group)

    def create_ui_manager(self, window):
        
        uimanager= Gtk_UIManager_plus()

        # Throws exception if something went wrong
        content=uimanager.add_ui_add_from_file(UI)
        
        # parse to build actions
        uimanager.parse_ui_content(content)
        
        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
            
        window.add_accel_group(accelgroup)
        
        return uimanager

    def on_menu_file_new_generic(self, widget):
        print("A File|New menu item was selected.")

    def file_quit_callback(self, widget):
        Gtk.main_quit()

    def on_menu_others(self, widget):
        print("Menu item " + widget.get_name() + " was selected")

    def on_menu_choices_changed(self, widget, current):
        print(current.get_name() + " was selected.")

    def on_menu_choices_toggled(self, widget):
        if widget.get_active():
            print(widget.get_name() + " activated")
        else:
            print(widget.get_name() + " deactivated")

    def on_button_press_event(self, widget, event):
        # Check if right mouse button was preseed
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.popup.popup(None, None, None, None, event.button, event.time)
            return True  # event has been handled


    def add_menuitem(self,menu_name="Help",action="toto", stock_id="gtk-about", func=None):
                
        agr = Gtk.AccelGroup()        
                
        #`GtkImageMenuItem' doesn't support property `stock_id'
        menuitem = Gtk.ImageMenuItem(label=action) #"gtk-about",agr)
        
       
        
        #--- From File
        #image = Gtk.Image()
        #image.set_from_file("diamock_logo.png") 
        #menuitem.set_image(image)
        #image=Gtk.Image.new_from_file("diamock_logo.png")
        
        #-- From Stock
        #menuitem.set_image(image.new_from_stock("gtk-about",4))
        # NOTE print(image.get_icon_name()) indicates the good size 4 which seems not be pixel based
        
        if not stock_id is None :
            image=Gtk.Image.new_from_icon_name(stock_id, Gtk.IconSize.LARGE_TOOLBAR)
            menuitem.set_image(image)
        
        
      
        # DEPRECATED menuitem.set_always_show_image(True)
        
        key, mod = Gtk.accelerator_parse("<Control>H")
        #menuitem.add_accelerator("activate", agr, key, 
        #mod, Gtk.ACCEL_VISIBLE)
        
        #menuitem.connect("activate", func)
        self.get_menu_entry(menu_name).append(menuitem)
    



def _add_stock_icon_name(factory, name, icon):

    """
    This function registers our custom toolbar icons, so they can be themed.
    It's totally optional to do this, you could just manually insert icons
    and have them not be themeable, especially if you never expect people
    to theme your app.
    """
    '''
    item = Gtk.StockItem()
    item.stock_id = 'demo-gtk-logo'
    item.label = '_GTK!'
    item.modifier = 0
    item.keyval = 0file_quit_callback
    item.translation_domain = None

    Gtk.stock_add(item, 1)
    '''
    
    global _demoapp

    factory = Gtk.IconFactory()
    factory.add_default()

    dirname = os.path.abspath(os.path.dirname(__file__))

    if _demoapp is None:
        filename = os.path.join(dirname, 'app','icons', icon+'.png')
    else:
        filename = _demoapp.find_file(dirname, icon+'.png')
    
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
    transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
    icon_set = Gtk.IconSet.new_from_pixbuf(transparent)

    factory.add(name, icon_set)

def register_stock_icons():
    """
    This function registers our custom toolbar icons, so they can be themed.
    It's totally optional to do this, you could just manually insert icons
    and have them not be themeable, especially if you never expect people
    to theme your app.
    """

    factory = Gtk.IconFactory()
    factory.add_default()

    _add_stock_icon_name (factory, DIA_STOCK_GROUP, "dia-group");
    _add_stock_icon_name (factory, DIA_STOCK_UNGROUP, "dia-ungroup");
    _add_stock_icon_name (factory, DIA_STOCK_LAYER_ADD, "dia-layer-add");
    _add_stock_icon_name (factory, DIA_STOCK_LAYER_RENAME, "dia-layer-rename");
    _add_stock_icon_name (factory, DIA_STOCK_OBJECTS_LAYER_ABOVE, "dia-layer-move-above");
    _add_stock_icon_name (factory, DIA_STOCK_OBJECTS_LAYER_BELOW, "dia-layer-move-below");
    _add_stock_icon_name (factory, DIA_STOCK_LAYERS, "dia-layers");




def set_menuitem_stock_id(menuitem, stock_id):
    
    #--- From File
    #image = Gtk.Image()
    #image.set_from_file("diamock_logo.png") 
    #menuitem.set_image(image)
    #image=Gtk.Image.new_from_file("diamock_logo.png")
    
    #-- From Stock
    #menuitem.set_image(image.new_from_stock("gtk-about",4))
    # NOTE print(image.get_icon_name()) indicates the good size 4 which seems not be pixel based
    
    if not stock_id is None :
        image=Gtk.Image.new_from_icon_name(stock_id, Gtk.IconSize.LARGE_TOOLBAR)
        menuitem.set_image(image)
        
    # DEPRECATED menuitem.set_always_show_image(True)
        
def set_menuitem_accelerator(menuitem, accelerator, accel_group):
    
    if not accelerator is None:
        
        #accel_group = uimanager.get_accel_group()
        #accel_group = Gtk.AccelGroup()
        #window.add_accel_group(accel_group)  
        
        key, mod = Gtk.accelerator_parse(accelerator)
        #https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtkaccellabel.html
        menuitem.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE) 
        menuitem.set_accel_group (accel_group)
       
        
def set_menuitem_callback(menuitem, callback, args=()):

    if callback != None:
            menuitem.connect("activate", callback, *args)

def set_menuitem_label(menuitem, label):
    
    menuitem.set_label(label)

def create_menuitem(window, stock_id="gtk-about",label="Help",  accelerator=None, tooltip=None, accel_group= None):

    if stock_id != None:
        #`GtkImageMenuItem' doesn't support property `stock_id'
        menuitem = Gtk.ImageMenuItem(label=label) #"gtk-about",agr)
    else:
        menuitem  = Gtk.MenuItem(label=label) #, True)   
    
    set_menuitem_stock_id(menuitem, stock_id)
    
    set_menuitem_accelerator(menuitem, accelerator, accel_group)
    
    return menuitem    
                                         
                                         
def add_menuitem_to_menu(window, uimanager,menubar_name, menu_name, stock_id, label,  accelerator, tooltip, accel_group):

    menu_widget = uimanager.get_widget("/"+menubar_name+"/"+menu_name).get_submenu()
        
    menuitem =create_menuitem(window, stock_id,label,  accelerator, tooltip, accel_group)
   
    menu_widget.append(menuitem)
    
    return menuitem
    
def update_menuitem(menuitem, stock_id, label,  accelerator, tooltip, callback, action_group, accel_group):
   
    set_menuitem_stock_id(menuitem, stock_id)
    set_menuitem_callback(menuitem, callback)
    set_menuitem_label(menuitem, label)
    #menuitem.set_tooltip(menuitem_tooltip)  DOES NOT EXIST
   
   
   # NOTE: set menuitem_accelerator requires extra cleanup in action_group
   # even if None was provided for accelerator and callback
    name=menuitem_name=menuitem.get_name()
    action_old=action_group.get_action(name)
    action_group.remove_action(action_old)

    action_new = Gtk.Action(
        name=name,
        label=label,
        tooltip=tooltip,
    )
    
    #action_new.connect("activate", callback)
    
    #action_group.add_action_with_accel(action_new)
    action_group.add_action_with_accel(action_new, accelerator)
        
    #..before setting a new one !
    set_menuitem_accelerator(menuitem, accelerator, accel_group)
    
def add_or_update_menuitem_to_menu(window, uimanager,menubar_name, menu_name, menuitem_name, stock_id, menuitem_label,  accelerator, tooltip, callback, action_group, accel_group):
    try:
        menuitem=uimanager.get_widget("/"+menubar_name+"/"+menu_name+'/'+menuitem_name)
        if menuitem is None:
            raise(Exception("Non Existent menuitem, will create it"))
        
        #print("FOUND",menuitem)
        update_menuitem(menuitem, stock_id, menuitem_label,  accelerator, tooltip, callback, action_group, accel_group)
   
    except Exception as e:
        #if not "Non Existent menu" in str(e): 
        #   print("NOTFOUND",e)
        #else:
        #   print("NEW",e)
        menuitem=add_menuitem_to_menu(window, uimanager, menubar_name, menu_name, stock_id, menuitem_label, accelerator, tooltip, accel_group)
        set_menuitem_callback(menuitem,callback)       
       # uimanager.add_widget(menuitem)
                

class ToolMenuAction(Gtk.Action):
    __gtype_name__ = "GtkToolMenuAction"

    def do_create_tool_item(self):
        return Gtk.MenuToolButton()

def on_button_press_event(widget, event):
        # Check if right mouse button was preseed
        print(event.type )
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.popup.popup(None, None, None, None, event.button, event.time)
            return True  # event has been handled


class Gtk_StatusBar_plus(Gtk.Statusbar):   
                
    def set_message(self,message):
        self._sb.remove(self.cid, self.mid)
        self.mid=self._sb.push(self.cid,message)
        
    def __init__(self,id=None):
        
        try: #3.x
            super().__init__()
        except: #2.7
            super(Gtk.Statusbar, self).__init__()
            
        if id is None :    
            sb = self
        else:
            sb = builder.get_object(id)
                
        self._sb= sb         
        self.cid= cid =sb.get_context_id("info")
        self.mid=self.push(cid,"Ready..")
        self.pt=None
        setattr(sb,"manager",self)
       
    def install_mouse_coords_watcher(self,polling):
        self.pt=pt=RepeatTimer(polling,self.show_mouse_coords)
        pt.start()
        
    def uninstall(self):
        self.pt.stop()
        self.pt.join()



#https://www.programcreek.com/python/?code=innstereo%2Finnstereo%2Finnstereo-master%2Finnstereo%2Fdialog_windows.py#
#from .i18n import i18n, translate_gui

class diamock_gui:

    def register_action(self, action, description, menupath, func, stock_id=None, accelerator = None):
        """ register_action(string: action, string: description, string: menupath, Callback: func) -> None.  
        Register a callback function which appears in the menu. Depending on the menu path used during registrationthe callback gets called with the current DiaDiagramData object """
        
        #add menuitem        
        window = self.window
        uimanager = self.uimanager
        menubar_action_group = self.menubar_action_group 
        accel_group=uimanager.get_accel_group()
        
        menupath=menupath.split("/")
        menubar_name= menupath[1] #"DisplayMenu"
        menu_name = menupath[2] #"Help"
        menuitem_label = action
        menuitem_name= menupath[3] #menu_name+menuitem_label.replace('_','')
        #stock_id=None #"gtk-about"  or Gtk.STOCK_NEW
        #accelerator = None # or "<Control>A" 
        tooltip =  description #"Create a new file"
        callback= func

        menuitem=add_or_update_menuitem_to_menu(window, uimanager, menubar_name, menu_name, menuitem_name, stock_id, menuitem_label,  accelerator, tooltip, callback, menubar_action_group, accel_group)
       

        #read back
        """
        for action in action_group.list_actions():
            print(str(action.get_name())+':'+str(action.get_label()))
        """
            

    def __init__(self,demoapp=None):
    
        global infobar
        global window
        global messagelabel
        global _demoapp

        _demoapp = demoapp

        register_stock_icons()

        self.window = window = Gtk.Window()
        window.set_title(PROGRAM_NAME)
        
        #window.set_icon_name("dia-gui-logo")
        dirname = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(dirname,"app",LOGO)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 64, 64)    
        transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
        window.set_icon(transparent)
        
        
        
        #window.connect_after('button-press-event', on_button_press_event)
        window.connect_after('destroy', file_quit_callback)
        table = Gtk.Table(n_rows=1,
                          n_columns=5,
                          homogeneous=False)
        window.add(table)


        # Tool menu

        toolmenu_action_group = Gtk.ActionGroup(name='AppToolMenuActions')
        
        toolmenu_open_action = ToolMenuAction(name='Open',
                                     stock_id=Gtk.STOCK_OPEN,
                                     label='_Open',
                                     tooltip='Open a file')

        toolmenu_action_group.add_action(toolmenu_open_action)
        
        
        toolmenu_action_group.add_actions(toolmenu_action_entries)
        
        
        toolmenu_action_group.add_toggle_actions(toolmenu_toggle_action_entries)
        toolmenu_action_group.add_radio_actions(toolmenu_color_action_entries,
                                       COLOR_RED,
                                       activate_radio_action)
        toolmenu_action_group.add_radio_actions(toolmenu_shape_action_entries,
                                       SHAPE_SQUARE,
                                       activate_radio_action)
        
        #merge = Gtk.UIManager()
        self.uimanager = merge = Gtk_UIManager_plus()
        
        self.menubar_action_group = menubar_action_group = Gtk.ActionGroup(name='AppMenubarActions')
       
        merge.insert_action_group(menubar_action_group, 0)
        accel_group=merge.get_accel_group()
        window.add_accel_group(accel_group)

        #==========  MENUBAR ============             
                     
        # Throws exception if something went wrong
        #content=merge.add_ui_add_from_file(ui_menubar)
        merge.add_ui_from_string(ui_menubar_info)
        content=ui_menubar_info
        
        # parse to build actions
        merge.parse_ui_content(content)
        
        # optional
        #merge.show_tree()
        
        # add_menus_actions
        #actions=merge.get_actions()
        actions=menubar_action_entries
        
        menubar_action_group.add_actions(actions)
        
        #self.add_menus_actions(uimanager, action_group)
        merge.insert_action_group( menubar_action_group)
        
        menubar_name="DisplayMenu"
        menubar = merge.get_widget("/"+menubar_name)
        menubar.show()
     
        
        table.attach(menubar, 0, 1, 0, 1,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0, 0)
                     
                     
        #==========  TOOLBAR ============             
        merge.insert_action_group(toolmenu_action_group, 0)
         
        merge.add_ui_from_string(ui_info_toolbar)
        bar = merge.get_widget('/Toolbar')
        bar.show()
        table.attach(bar, 0, 1, 1, 2,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0, 0)

        infobar = Gtk.InfoBar()
        infobar.set_no_show_all(True)
        messagelabel = Gtk.Label()
        messagelabel.show()
        infobar.get_content_area().pack_start(messagelabel, True, True, 0)
        infobar.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        infobar.connect('response', lambda a, b: Gtk.Widget.hide(a))

        table.attach(infobar, 0, 1, 2, 3,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0, 0)

        #==========  BODY ============ 

        self.builder = builder = Gtk.Builder()
                
        #builder.set_translation_domain(i18n().get_ts_domain())
        """
        script_dir = os.path.dirname(__file__)
        rel_path ='diamock3.glade'
        abs_path = os.path.join(script_dir, rel_path)
        builder.add_objects_from_file(abs_path,
            ("aboutdialog", ""))
        """
        #Note Glade3.22 has a bug to insert Gtk StatusBar as the
        # entry is missing in /usr/share/glade/catalogs/gtk+.xml
        #https://stackoverflow.com/questions/50155212/adding-gtkstatusbar-in-glade3
        dirname = os.path.abspath(os.path.dirname(__file__))
        builder.add_from_file(os.path.join(dirname,'app','ui','diamock3.glade')) #from glade 3.22.1 , gtk3.0 compatible
        
        body = builder.get_object("body")


        #==========  SCROLLED ============             
                      
        sw = Gtk.ScrolledWindow(hadjustment=None,
                                vadjustment=None)
        sw.set_shadow_type(Gtk.ShadowType.IN)
        table.attach(sw, 0, 1, 3, 4,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0)

        #contents = Gtk.TextView()
        #contents.grab_focus()
        contents = body
        body.reparent(sw)
        
        sw.add(contents)
        

        #==========  STATUSBAR ============             
                     
        # Create statusbar
        
        #statusbar = Gtk.Statusbar()
        statusbar = Gtk_StatusBar_plus()
        statusbar.set_message('Ready...')
        table.attach(statusbar, 0, 1, 4, 5,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0, 0)

            
        # show text widget info in the statusbar
        """
        buffer = contents.get_buffer()
        buffer.connect('changed', update_statusbar, statusbar)
        buffer.connect('mark_set', mark_set_callback, statusbar)

        update_statusbar(buffer, statusbar)
        """

        window.set_default_size(880, 800)




    def show(self):
        self.window.show_all()
        Gtk.main()
            
    def close(self):
        Gtk.main_quit()

gui=None

def FileQuit(*args):
    gui.close()

import inspect
def onDiaLaunched():
    stack=inspect.stack()
    return ("python-startup.py" in stack[-1][1])

from dumpObj import dumpObj #here is the golden carot


###### DEFINE YOUR CALLBACK ACTIONS HERE ########
            

def help_about_callback(widget, user_data=None):
    global window

    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(dirname,"app",LOGO)
    #pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 164, 164)    
    transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)

    if gtk_support=="pyGObject":
    
        ## Using pyObject way 
    
        about = Gtk.AboutDialog(parent=window,
                                program_name=PROGRAM_NAME, 
                                version=VERSION, 
                                copyright= COPYRIGHT,
                                license= LICENSE_TEXT,
                                website=WEBSITE, 
                                website_label=WEBSITE,
                                comments=COMMENTS, 
                                authors=AUTHORS,
                                documenters=DOCUMENTORS,
                                logo=transparent,
                                #logo_icon_name='pyDiaMock',
                                title='About '+PROGRAM_NAME)
    else:
        
        ## Using text console way 
        
        print("==="+PROGRAM_NAME+VERSION+"===")
        print("Authors:"+",".join(AUTHORS))
        print(COMMENTS)
        print("Copyright:"+COPYRIGHT)
        print("Website:"+WEBSITE)
        print("Error",e)
        print("=================================")

    about.connect('response', widget_destroy)
    about.show()



# callback for fullscreen
def view_fullscreen_callback(self, action, parameter):
    # check if the state is the same as Gdk.WindowState.FULLSCREEN, which
    # is a bit flag
    is_fullscreen = self.get_window().get_state(
    ) & Gdk.WindowState.FULLSCREEN != 0
    if is_fullscreen:
        self.unfullscreen()
        self.leave_fullscreen_button.hide()
        self.fullscreen_button.show()
    else:
        self.fullscreen()
        self.fullscreen_button.hide()
        self.leave_fullscreen_button.show()

def file_quit_callback(widget):
        Gtk.main_quit()

def  help_manual_callback(widget):
        #enjoy the doc
        dumpObj(dia)
        

 
def main(demoapp=None):
    
    ###### SET YOUR DIA SCRIPT HERE ########
    
    dia.register_action ("Help", "Help", 
                         "/DisplayMenu/Help/HelpContents", 
                         help_manual_callback)
    """
    # already done : 
    dia.register_action ("About DiaMock", "About", 
                         "/DisplayMenu/Help/HelpAbout", 
                        help_about_callback)
    """

    #############

if __name__ == '__main__' or not onDiaLaunched():
    
    #dia is the mocked version of lib pydia library.
    # it is now python2-3 compatible
    #available here: https://github.com/sosie-js/python-dia-mock-plugin
    #see the installation steps on  https://sosie-js.github.io/python-dia/mock/
    
    import dia 
    gui=diamock_gui()
    
    #overrides with the good implementation this time
    setattr(dia,"register_action",gui.register_action)
    
    main()
    gui.show()
    
else:
    
    import dia
    main()
    
    
