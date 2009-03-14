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

    

class Snipplet(object):
    def __init__(self):
        self.GLADE_DIR = "ui/glade/"
        self.HOME_DIR = os.path.join(os.environ['HOME'], ".snipplets")
        if not os.path.exists(self.HOME_DIR):
            os.mkdir(self.HOME_DIR)
        self.create_main_window()
    
    def create_main_window(self):
        self.main_handler = MainSnippletHandlers(self, self.GLADE_DIR + "snipplets.glade")

        
        
    def create_new_snipplet_window(self):
        self.create_handler = CreateNewSnippletHandlers(self, self.GLADE_DIR +
                                                        "create_new_snipplet.glade")



if __name__ == '__main__':
    snipplet = Snipplet()
    gtk.main()
