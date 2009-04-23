# mainsnipplet.py
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
import time
from xml.etree import ElementTree as ET
from misc import nicetime


class MainHandler():
    
    def __init__(self, parent, glade_file):
        self.wTree = gtk.glade.XML(parent.GLADE_DIR + glade_file)
        self.wTree.signal_autoconnect(self)
        self.parent = parent
        self.db = self.parent.db
        self.clipboard = self.parent.clipboard
        self.code_syntax = self.parent.code_syntax
        self.window = self.wTree.get_widget("window")
        self.type_view = self.wTree.get_widget("types")
        self.tag_view = self.wTree.get_widget("tags")
        self.selection_view = self.wTree.get_widget("selection")
        self.data_view = self.wTree.get_widget("data")
        
        #combobox for saving filetypes
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        for item in ["xml", "text"]:
            liststore.append(["XML Files"])
            liststore.append(["All Files"])
        combobox = self.wTree.get_widget("filetypes")
        combobox.set_model(liststore)
        text = gtk.CellRendererText()
        combobox.pack_start(text)
        combobox.add_attribute(text, "text", 0)
        combobox.set_active(0)
        
        self.create_selection_area()
        self.fill_types()
        

    
    def on_window_destroy(self, widget):
        #close any encrypted files and quit
        gtk.main_quit()

  
    def on_create_snipplet_clicked(self, widget):
        self.parent.create_new_snipplet_window(widget)
        
    
    
    def create_selection_area(self):
        self.selection_columns = ["id", "", "Description", "Modified", "Encryption", "Type"]
        self.selection_liststore = gtk.ListStore(int, gtk.gdk.Pixbuf, str, str, int, str)
        self.selection_filter = self.selection_liststore.filter_new()
        self.selection_view.set_model(self.selection_filter)
        snipplets = self.db.return_snipplet_selection()
        for row in snipplets:
            #liststore: int, gtk.gdk.Pixbuf, str, int, str, bool
            #rows: id, typeimage, description, encryption, modified, visible
            row3 = nicetime(row[3])
            image = gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR + row[1].lower() + ".png")
            self.selection_liststore.append([row[0], image, row[2], row3, row[4], row[1]])
                
        #append to columns
        i = 0
        for column in self.selection_columns:
            col = gtk.TreeViewColumn(column)
            if i == 1:
                cell = gtk.CellRendererPixbuf()
            else:    
                cell = gtk.CellRendererText()
            col.pack_start(cell, False)
            
            if i == 1:
                col.set_attributes(cell, pixbuf=i)
            else:
                col.set_attributes(cell, text=i)
            
            col.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            col.set_min_width(30)
            col.set_max_width(300)
            col.set_resizable(True)
            col.set_spacing(10)
            self.selection_view.append_column(col)
            if i == 0:
                col.set_visible(False)
            i +=1
        #show the last edited snipplet by default
        self.selection_filter.set_visible_func(self.check_selection_visibility)
        self.selection_view.get_selection().select_path(0)
        self.on_selection_cursor_changed(None)
        
        
    def fill_types(self):
        types = self.db.query("""SELECT * FROM types""")
        self.types = []
        liststore = gtk.ListStore(int, gtk.gdk.Pixbuf, str)
        #by default we should show all
        liststore.append([0, gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR + "all.png"),
                         "All"])
        for type in types:
            image = gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR + type[1].lower() + ".png")
            liststore.append([type[0], image, type[1]])
            self.types.append(type[1])
        self.show_types = self.types
        self.type_view.set_model(liststore)
        columns = ["id", "pic", "type"]
        for i in range(0, len(columns)):
            col = gtk.TreeViewColumn(None)
            if columns[i] == "pic":
                cell = gtk.CellRendererPixbuf()
            else:
                cell = gtk.CellRendererText()
            col.pack_start(cell, False)
            if columns[i] == "pic":
                col.set_attributes(cell, pixbuf=i)
            else:
                col.set_attributes(cell, text=i)
            if columns[i] == "id":
                col.set_visible(False)
            self.type_view.append_column(col)
        self.type_view.get_selection().select_path(0)
            
    def on_types_cursor_changed(self, *args):
        """Show only the types that are selected"""
        model, iter = self.type_view.get_selection().get_selected()
        type = model.get_value(iter, 2)
        if type == "All":
            self.show_types = self.types
        else:
            self.show_types = [type]
        self.selection_filter.refilter()
        #we should also make sure that a valid selection is shown
        #or blank if the user has emptied all possibilites
        self.selection_view.get_selection().select_path(0)
        self.on_selection_cursor_changed(None)
    
    def check_selection_visibility(self, model, iter):  
        return model.get_value(iter, 5) in self.show_types


    def update_selection_view(self, dict, id=None):
        """called when the user creates a new snipplet"""
        row = self.db.return_most_recent_snipplet()
        row1 = gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR + row[1])
        #if we have an id, it means it was an edited so dont add again just update
        if id:
            self.selection_liststore.remove(self.edit_iter)
        row3 = nicetime(row[3])
        self.selection_liststore.prepend([row[0], row1, row[2], row3, row[4]])

    
    def on_selection_cursor_changed(self, widget):
        """Fill the data box with the snipplet selected"""
        #self.snipplet_data_liststore.clear()
        model, iter = self.selection_view.get_selection().get_selected()
        try:
            snipid = model.get_value(iter, 0)
            data = self.db.return_snipplet_data(snipid)
            #check if we have a code snipplet
            self.data_view.set_buffer(self.code_syntax.set_buffer_language(data[4]))
            self.data_view.get_buffer().set_text(data[0])
        except TypeError:
            self.data_view.get_buffer().set_text("")
        
    def on_selection_row_activated(self, widget, path=None, column=None):
        """User double clicks, show the current snipplet in an edit box"""
        model, iter = self.selection_view.get_selection().get_selected()
        snipid = model.get_value(iter, 0)
        #save iterator for later use
        self.edit_iter = iter
        self.parent.create_new_snipplet_window(widget, snipid)
  

    def on_delete_clicked(self, widget):
        popup = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                  gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                                  "Are you sure you want to delete this snipplet?")
        response = popup.run()
        if response == gtk.RESPONSE_YES:
            model, iter = self.selection_view.get_selection().get_selected()
            snipid = model.get_value(iter, 0)
            self.db.delete(snipid)
            model.remove(iter)
            self.update_status("Snipplet deleted")
        popup.destroy()

    def on_copy_clicked(self, widget):
        """If the user has some text selected we will copy this,
        else we will grab the whole snipplet"""
        buffer = self.wTree.get_widget("data").get_buffer()
        try:
            start, end = buffer.get_selection_bounds()
        except ValueError:
            start, end = buffer.get_bounds()
        self.clipboard.set_text(buffer.get_text(start, end))
        self.update_stats("Snipplet copied to clipboard")
        
    def on_export_clicked(self, widget):
        """Save snipplet dialog"""
        self.file_selection = gtk.FileChooserDialog(title="Save snipplet", parent=None, 
                                                    action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                                    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                                             gtk.STOCK_SAVE,gtk.RESPONSE_OK),
                                                    backend=None)
        self.file_selection.set_current_name(self.get_possible_filename())
        filter = gtk.FileFilter()
        filter.set_name("Snipplet (.snip)")
        filter.add_pattern("*.snip")
        self.file_selection.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        self.file_selection.add_filter(filter)
        
        response = self.file_selection.run()
        if response == gtk.RESPONSE_OK:
            #create an xml document
            model, iter = self.selection_view.get_selection().get_selected()
            snipid = model.get_value(iter, 0)
            rows = self.db.return_snipplet_data(snipid)
            root = ET.Element("snipplets")
            el_snipplet = ET.SubElement(root, "snipplet")
            type = ET.SubElement(el_snipplet, "typeid")
            type.text = str(rows[1])
            des = ET.SubElement(el_snipplet, "description")
            des.text = rows[2]
            data = ET.SubElement(el_snipplet, "data")
            data.text = rows[0]
            enc = ET.SubElement(el_snipplet, "encryption")
            enc.text = str(rows[3])
            lang = ET.SubElement(el_snipplet, "language")
            lang.text = str(rows[4])
            mod = ET.SubElement(el_snipplet, "modified")
            mod.text = str(rows[5])
            tags = ET.SubElement(el_snipplet, "tags")
            t = ['testtag1', 'testtag2']
            for tag in t:
                cur = ET.SubElement(tags, "tag")
                cur.text = tag
            print self.file_selection.get_filename()
            tree = ET.ElementTree(root)
            tree.write(self.file_selection.get_filename())
        self.file_selection.destroy()
        
    def get_possible_filename(self):
        """Default name for exported snipplet"""
        model, iter = self.selection_view.get_selection().get_selected()
        desc = model.get_value(iter, 2)
        desc = ("".join(desc.split(" ")) + ".snip").lower()
        return desc

    def file_sel_save(self, widget):
        print widget
        
    def file_sel_destroy(self, widget):
        self.file_selection.destroy()
        
        
        #filechooser = self.wTree.get_widget("filechooser")
        #filechooser.set_current_name(self.get_possible_filename())
        #filechooser.run()
        #filechooser.hide()
        #    
    def on_file_saver_event(self, widget):
        pass
        #filename = self.wTree.get_widget("
        
    
    def update_status(self, text):
        pass
        #self.wTree.get_widget("status_bar").set_text(text)
        #gobject.timeout_add(1000, self.clear_status)
        
    def clear_status(self):
        self.wTree.get_widget("status_bar").set_text("")
   

   
    def show_snipplets(self):
        """fetches and calculates all types,tags and snipplets info and creates
        snipplet objects"""
        types = self.db.return_all("types")
        tags = self.db.return_all("tags")
        
            
        
