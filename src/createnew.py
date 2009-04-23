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

class CreateNewHandler():

    def __init__(self, parent, glade_file, id=None):
        self.wTree = gtk.glade.XML(parent.GLADE_DIR + glade_file)
        self.parent = parent
        self.db = self.parent.db
        self.types = self.db.return_all("types")
        self.code_syntax = parent.code_syntax
        self.fill_type_box(self.types)
        self.fill_code_box()
        self.error_box = self.wTree.get_widget("error")
        self.has_unsaved_changes = False
        self.id = id
        self.snipplet = NewSnipplet()
        self.snipplet.set_widgets(self.wTree)
        if self.id is not None:
            data = self.db.return_snipplet_data(self.id)
            self.snipplet.old_snipplet_reborn(data)
        #run so we know if we should hide or show the code box
        self.on_type_changed(None)
        
        self.wTree.signal_autoconnect(self)
   
    def on_type_changed(self, widget):
        #checks if we are using code, if so we will use a code buffer
        old_buff = self.wTree.get_widget("data").get_buffer()
        start, end = old_buff.get_bounds()
        text = old_buff.get_text(start, end)
        if self.wTree.get_widget("type").get_active() == 0:    
            self.wTree.get_widget("code_syntax").show()
            active_code = self.wTree.get_widget("code_syntax").get_active()
            buff = self.code_syntax.set_buffer_language(active_code)
        else:
            self.wTree.get_widget("code_syntax").hide()
            buff = gtk.TextBuffer()
        self.wTree.get_widget("data").set_buffer(buff)
        buff.set_text(text)
       
    def fill_type_box(self, types):
        liststore = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        for type in types:
            liststore.append([type[1], gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR +
                                                                    type[1].lower() + ".png")])
         
        combobox = self.wTree.get_widget("type")
        combobox.set_model(liststore)
        text = gtk.CellRendererText()
        icon = gtk.CellRendererPixbuf()
        combobox.pack_start(icon)
        combobox.pack_end(text)
        combobox.add_attribute(icon, "pixbuf", 1)
        combobox.add_attribute(text, "text", 0)
        combobox.set_active(0)


    def fill_code_box(self):
        #i may include pics of languages in the future but not so important
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        for lang in self.code_syntax.filetypes:
            liststore.append([lang])

        combobox = self.wTree.get_widget("code_syntax")
        combobox.set_model(liststore)
        text = gtk.CellRendererText()
        combobox.pack_start(text)
        combobox.add_attribute(text, "text", 0)
        combobox.set_active(0)
       

    
    def on_window_destroy(self, widget):
        self.wTree.get_widget("window").destroy()
        return False
  
    
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
            self.parent.update_selection_view(self.snipplet.values, self.id)
            #update db if it is a code piece to say which language was last used
            
            self.on_window_destroy(None)
        else:
            self.error_box.set_text("Missing values: " + ','.join(missing))
    

class NewSnipplet(object):
    """Used to create a New Snipplet or Edit an Old one"""
    
    def __init__(self):
        self.values = {"type" : 1, "description" : "",
                       "data" : "", "code_syntax" : "", "encryption" : False }
        
    
    def set_widgets(self, tree):
        """Pass the wTree and widgets will be autoconnected"""
        self.widgets = dict(self.values)
        for key, value in self.widgets.items():
            self.widgets[key] = tree.get_widget(key)
                    
    
    def return_missing_values(self):
        """Returns missing required info keys, or none if everything is done"""
        keys = []
        for key, value in self.values.items():
            if value is "":
                if key == "code_syntax" and self.values["type"] != 0:
                    continue
                keys.append(key)
        if keys == []:
            return None
        return keys
        
    
    def fill_snipplet(self):
        """fills the snipplet with data from widgets set_widgets(must be run first)"""
        buffer = self.widgets["data"].get_buffer()
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end)
        self.values["data"] = buffer.get_text(start, end)
        
        self.values["description"] = self.widgets["description"].get_text()
        self.values["type"] = self.widgets["type"].get_active() + 1
        self.values["encryption"] = self.widgets["encryption"].get_active()
        #if self.values["type"] == 1:
        self.values["code_syntax"] = self.widgets["code_syntax"].get_active()
        #else:
        #    self.values["code_syntax"] = ""
    
    def old_snipplet_reborn(self, data):
        buffer = self.widgets["data"].get_buffer()
        buffer.set_text(data[0])
        self.widgets["type"].set_active(data[1] - 1)
        self.widgets["description"].set_text(data[2])
        self.widgets["encryption"].set_active(data[3])
        if data[1] - 1 == 0:
            #code widget
            self.widgets["code_syntax"].set_active(data[4])
