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
pygtk.require("2.0")

from mainsnipplet import GladeHandler


class CreateNewSnippletHandlers(GladeHandler):
    """All handlers for glade created objects relating to the create-new-snipplet
    should be listed here so we can bind them all at once"""
    def __init__(self, parent, glade_file):
        GladeHandler.__init__(self, parent, glade_file)
        self.db = self.parent.db_snipplets
        self.types = self.db.return_types()
        

    
    def on_window_destroy(self, widget):
        pass
    
    
    
    def on_save_new_clicked(self, widget):
        pass
    
    
    
    def on_discard_new_clicked(self, widget):
        pass
