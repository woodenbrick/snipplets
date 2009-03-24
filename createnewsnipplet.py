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
from gtkcodebuffer import CodeBuffer, SyntaxLoader
pygtk.require("2.0")


class CreateNewSnippletHandler():

    def __init__(self, parent, glade_file, id=None):
        self.wTree = gtk.glade.XML(parent.GLADE_DIR + glade_file)
        self.wTree.signal_autoconnect(self)
        self.parent = parent
        self.db = self.parent.db
        self.types = self.db.return_all("types")
        self.fill_type_box(self.types)
        self.error_box = self.wTree.get_widget("error")
        self.has_unsaved_changes = False
        self.id = id
        self.snipplet = NewSnipplet()
        self.snipplet.set_widgets(self.wTree)
        if self.id is not None:
            data = self.db.return_snipplet_data(self.id)
            self.snipplet.old_snipplet_reborn(data)
   
    def on_type_changed(self, widget):
        #checks if we are using code, if so we will use a code buffer
        old_buff = self.wTree.get_widget("data").get_buffer()
        start, end = old_buff.get_bounds()
        text = old_buff.get_text(start, end)
        if self.wTree.get_widget("type").get_active() == 0:    
            #we need some way to check the language either user defined
            #or automatic check
            lang = SyntaxLoader("php")
            buff = CodeBuffer(lang=lang)
        else:
            buff = gtk.TextBuffer()
        self.wTree.get_widget("data").set_buffer(buff)
        buff.set_text(text)
        
    def fill_type_box(self, types):
        liststore = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        for type in types:
            liststore.append([type[1], gtk.gdk.pixbuf_new_from_file(type[2])])
        
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
        self.wTree.get_widget("window").destroy()
        return True
  
    
    def on_save_new_clicked(self, widget):
        self.snipplet.fill_snipplet()
        missing = self.snipplet.return_missing_values()
        if missing is None:
            self.error_box.set_text("")
            if self.id:
                self.snipplet.values['snippletid'] = self.id
                self.db.edit(self.snipplet.values)
            else:
                self.db.add_new(self.snipplet.values)
            #ask parent to update main selection area
            self.parent.update_selection_view(self.snipplet.values)
            self.on_window_destroy(None)
            
        else:
            self.error_box.set_text("Missing values: " + ','.join(missing))
    

class NewSnipplet(object):
    """Used to create a New Snipplet or Edit an Old one"""
    
    def __init__(self):
        self.values = {"type" : 1, "description" : "",
                       "data" : "", "encryption" : False }
        
    
    def set_widgets(self, tree):
        """Pass the wTree and widgets will be autoconnected"""
        w = ["type", "description", "data", "encryption"]
        self.widgets = dict(self.values)
        for key, value in self.widgets.items():
            self.widgets[key] = tree.get_widget(key)
                    
    
    def return_missing_values(self):
        """Returns missing required info keys, or none if everything is done"""
        keys = []
        for key, value in self.values.items():
            if value is "":
                keys.append(key)
        if keys == []:
            return None
        return keys
        
    
    def fill_snipplet(self):
        """fills the snipplet with data from widgets set_widgets(must be run first)"""
        for key, value in self.values.items():
            if key == "data":
                buffer = self.widgets[key].get_buffer()
                start, end = buffer.get_bounds()
                text = buffer.get_text(start, end)
                self.values[key] = buffer.get_text(start, end)
            else:
                try:
                    self.values[key] = self.widgets[key].get_text()
                except AttributeError:
                    self.values[key] = self.widgets[key].get_active()
        self.values['type'] = self.values['type'] + 1
        
    
    def old_snipplet_reborn(self, data):
        buffer = self.widgets["data"].get_buffer()
        buffer.set_text(data[0])
        self.widgets["type"].set_active(data[1] - 1)
        self.widgets["description"].set_text(data[2])
        self.widgets["encryption"].set_active(data[3])
