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

from mainsnipplet import MainSnippletHandlers
from createnewsnipplet import CreateNewSnippletHandlers

class WidgetsWrapper(object):
    def __init__(self, glade_file, handler_class, parent):
        """pass the handler_class to automatically bind glade handlers to their
        corresponding functions"""
        #self.widgets = gtk.glade.XML(glade_file)
        #self.widgets.signal_autoconnect(handler_class.__dict__)
        self.handler = handler_class(parent, glade_file)
        
    def get_widget(self, key):
        return 1#self.widgets.get_widget(key)
    

class Snipplet(object):
    def __init__(self):
        self.GLADE_DIR = "ui/glade/"
        self.HOME_DIR = os.path.join(os.environ['HOME'], ".snipplets")
        if not os.path.exists(self.HOME_DIR):
            os.mkdir(self.HOME_DIR)
        self.create_main_window()
    
    def create_main_window(self):
        self.main_wrapper = WidgetsWrapper(self.GLADE_DIR + "snipplets.glade",
                                          MainSnippletHandlers, self)
        self.main_window = self.main_wrapper.get_widget("window")
        
        
    def create_new_snipplet_window(self):
        self.create_wrapper = WidgetsWrapper(self.GLADE_DIR + "create_new_snipplet.glade",
                                            CreateNewSnippletHandlers, self)
        self.create_new_window = self.create_wrapper.get_widget("window")


if __name__ == '__main__':
    snipplet = Snipplet()
    gtk.main()
