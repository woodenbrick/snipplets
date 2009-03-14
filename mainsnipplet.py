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




class GladeHandler(object):
    """Super class for all handler classes"""
    def __init__(self, parent, glade_file):
        self.wTree = gtk.glade.XML(glade_file)
        self.wTree.signal_autoconnect(self)
        self.parent = parent





class MainSnippletHandlers(GladeHandler):
    """All handlers for glade created objects should be listed here
    so we can bind them all at once"""
    def __init__(self, parent, glade_file):
        GladeHandler.__init__(self, parent, glade_file)

    
    def on_window_destroy(self, widget):
        #close any encrypted files and quit
        gtk.main_quit()

  
    def on_create_snipplet_clicked(self, widget):
        self.parent.create_new_snipplet_window()
        
        