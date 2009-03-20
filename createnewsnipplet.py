# createnewsnipplet.py
#
# Copyright 2009 Daniel Woodhouse
#
#This file is part of snipplets.
#
#snipplets is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#snipplets is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with snipplets.  If not, see http://www.gnu.org/licenses/

import gtk
import pygtk
import gobject
pygtk.require("2.0")

from mainsnipplet import GladeHandler


class CreateNewSnippletHandlers(GladeHandler):
    """All handlers for glade created objects relating to the create-new-snipplet
    should be listed here so we can bind them all at once"""
    
    def __init__(self, parent, glade_file):
        #create layout
        GladeHandler.__init__(self, parent, glade_file)
        self.db = self.parent.db
        self.types = self.db.return_types()
        self.fill_type_box(self.types)
        
        #set initial states
        self.has_unsaved_changes = False

    
    def fill_type_box(self, types):
        liststore = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        for type in types:
            liststore.append([type[0], gtk.gdk.pixbuf_new_from_file(type[1])])
        
        combobox = self.wTree.get_widget("type")
        combobox.set_model(liststore)
        text = gtk.CellRendererText()
        icon = gtk.CellRendererPixbuf()
        combobox.pack_start(icon)
        combobox.pack_end(text)
        combobox.add_attribute(icon, "pixbuf", 1)
        combobox.add_attribute(text, "text", 0)
        combobox.set_active(0)


    
    
    def on_window_destroy(self, widget):
        pass
    
    
    
    def on_save_new_clicked(self, widget):
        pass
    
    
    
    def on_discard_new_clicked(self, widget):
        pass
