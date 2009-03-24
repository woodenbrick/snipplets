# snipplets.py
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

import os
import gtk
import pygtk
pygtk.require("2.0")
import gtk.glade

from mainsnipplet import MainSnippletHandler
from createnewsnipplet import CreateNewSnippletHandler
import dbsnipplet
import syntaxhighlight

class RunSnipplets(object):

    def __init__(self):
        self.GLADE_DIR = "ui/glade/"
        self.HOME_DIR = os.path.join(os.environ['HOME'], ".snipplets" + os.sep)
        try:
            os.mkdir(self.HOME_DIR)
        except:
            pass
        
        self.db = dbsnipplet.DbSnipplet(self.HOME_DIR + "snippletsDB")
        #define codecompletion object here for use by all children
        self.code_syntax = syntaxhighlight.HighLighter(self.db)
        
        self.create_main_window()        

    
    def create_main_window(self):
        self.main_handler = MainSnippletHandler(self, "snipplets.glade")

   
    def update_selection_view(self, data, id):
        self.main_handler.update_selection_view(data, id)
        

    def create_new_snipplet_window(self, id=None):
        self.create_handler = CreateNewSnippletHandler(self, "create_new_snipplet.glade", id=id)

    


if __name__ == '__main__':
    RunSnipplets()
    gtk.main()
