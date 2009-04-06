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
pygtk.require("2.0")


class MainHandler():
    
    def __init__(self, parent, glade_file):
        self.wTree = gtk.glade.XML(parent.GLADE_DIR + glade_file)
        self.wTree.signal_autoconnect(self)
        self.parent = parent
        self.db = self.parent.db
        self.code_syntax = self.parent.code_syntax
        self.window = self.wTree.get_widget("window")
        self.type_view = self.wTree.get_widget("types")
        self.tag_view = self.wTree.get_widget("tags")
        self.selection_view = self.wTree.get_widget("selection")
        self.data_view = self.wTree.get_widget("data")
        
        #self.types = sniptypes.Types(self.db.return_all("types"))
        #self.tags = sniptypes.Tags(self.db.return_all("tags"))
        self.create_selection_area()
        #self.create_view_area()
        

    
    def on_window_destroy(self, widget):
        #close any encrypted files and quit
        gtk.main_quit()

  
    def on_create_snipplet_clicked(self, widget):
        self.parent.create_new_snipplet_window(widget)
        
    
    
    def create_selection_area(self):
        self.selection_columns = ["id", "", "Description", "Modified", "Encryption"]
        self.selection_liststore = gtk.ListStore(int, gtk.gdk.Pixbuf, str, str, int)
        self.selection_view.set_model(self.selection_liststore)
        
        snipplets = self.db.return_snipplet_selection()
        for row in snipplets:
            #liststore: int, gtk.gdk.Pixbuf, str, int, str
            #rows: id, typeimage, description, encryption, modified
            row1 = gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR + row[1])
            self.selection_liststore.append([row[0], row1, row[2], row[3], row[4]])
        
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
        
    #def create_view_area(self):
    #    self.snipplet_data_liststore = gtk.ListStore(str)
    #    self.data_view.set_model(self.snipplet_data_liststore)
    #    column = gtk.TreeViewColumn()
    #    cell = gtk.CellRendererText()
    #    column.pack_start(cell, False)
    #    column.set_attributes(cell, text=0)
    #    self.data_view.append_column(column)
    
    def update_selection_view(self, dict, id=None):
        """called when the user creates a new snipplet"""
        row = self.db.return_most_recent_snipplet()
        row1 = gtk.gdk.pixbuf_new_from_file(self.parent.IMAGES_DIR + row[1])
        #if we have an id, it means it was an edited so dont add again just update
        if id:
            self.selection_liststore.remove(self.edit_iter)
        self.selection_liststore.prepend([row[0], row1, row[2], row[3], row[4]])

    
    def on_selection_cursor_changed(self, widget):
        """Fill the data box with the snipplet selected"""
        #self.snipplet_data_liststore.clear()
        model, iter = self.selection_view.get_selection().get_selected()
        snipid = model.get_value(iter, 0)
        data = self.db.return_snipplet_data(snipid)
        #check if we have a code snipplet
        if data[1] == 1:
            self.data_view.set_buffer(self.code_syntax.set_buffer_language(data[4]))
        self.data_view.get_buffer().set_text(data[0])
        
    def on_selection_row_activated(self, widget, path, column):
        """User double clicks, show the current snipplet in an edit box"""
        model, iter = self.selection_view.get_selection().get_selected()
        snipid = model.get_value(iter, 0)
        #save iterator for later use
        self.edit_iter = iter
        self.parent.create_new_snipplet_window(widget, snipid)
            
    
        
    def show_snipplets(self):
        """fetches and calculates all types,tags and snipplets info and creates
        snipplet objects"""
        types = self.db.return_all("types")
        tags = self.db.return_all("tags")
        
            
        
